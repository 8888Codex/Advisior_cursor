from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from python_backend.models import Conversation, ConversationCreate, Message, MessageSend, MessageResponse
from python_backend.storage import storage
from python_backend.crew_agent import LegendAgentFactory

router = APIRouter(
    tags=["Conversations"],
)

limiter = Limiter(key_func=get_remote_address)

@router.get("/api/conversations", response_model=List[Conversation])
@router.get("/api/conversations/", response_model=List[Conversation])
async def get_conversations(expertId: Optional[str] = None):
    return await storage.get_conversations(expertId)

@router.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    conversation = await storage.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/api/conversations", response_model=Conversation, status_code=201)
@router.post("/api/conversations/", response_model=Conversation, status_code=201)
async def create_conversation(data: ConversationCreate):
    expert = await storage.get_expert(data.expertId)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    conversation = await storage.create_conversation(data)
    return conversation

@router.get("/api/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: str):
    return await storage.get_messages(conversation_id)

@router.post("/api/conversations/{conversation_id}/messages", status_code=201)
@limiter.limit("10/minute")
async def send_message(request: Request, conversation_id: str, data: MessageSend):
    print(f"[CHAT] Recebida mensagem para conversa {conversation_id}: {data.content[:50]}...")
    try:
        print(f"[CHAT] Buscando conversa...")
        conversation = await storage.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        print(f"[CHAT] Buscando expert {conversation.expertId}...")
        expert = await storage.get_expert(conversation.expertId)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert for this conversation not found")
            
        print(f"[CHAT] Buscando histórico...")
        history = await storage.get_messages(conversation_id)
        print(f"[CHAT] Histórico: {len(history)} mensagens")
        
        # TODO: Refactor this to use a service
        user_id = "default_user"
        profile = await storage.get_business_profile(user_id)
        enriched_system_prompt = expert.systemPrompt
        if profile:
            profile_context = f"""\n\n---
[CONTEXTO DO NEGÓCIO DO CLIENTE]:
• Empresa: {profile.companyName}
• Indústria: {profile.industry}
• Objetivo Principal: {profile.primaryGoal}
• Desafio Principal: {profile.mainChallenge}
INSTRUÇÃO IMPORTANTE: Use essas informações para oferecer conselhos mais específicos e relevantes. NÃO mencione explicitamente que você recebeu essas informações.
---"""
            enriched_system_prompt += profile_context

        # Criar agente - ele vai verificar a API key internamente
        try:
            print(f"[CHAT] Criando agente para {expert.name}...")
            agent = LegendAgentFactory.create_agent(expert.name, enriched_system_prompt)
            print(f"[CHAT] Enviando mensagem para Claude...")
            ai_response = await agent.chat([h.model_dump() for h in history], data.content)
            print(f"[CHAT] Resposta recebida ({len(ai_response)} caracteres)")
        except ValueError as ve:
            # Erro de configuração (API key não encontrada)
            error_msg = str(ve)
            if "ANTHROPIC_API_KEY" in error_msg:
                raise HTTPException(
                    status_code=503,
                    detail="⚠️ ANTHROPIC_API_KEY não configurada. Para usar o chat com especialistas, adicione ANTHROPIC_API_KEY=sk-ant-... no arquivo .env na raiz do projeto e reinicie o servidor."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Erro de configuração: {error_msg}"
            )
        except Exception as e:
            # Outros erros da API
            error_msg = str(e)
            import traceback
            print(f"[ERROR] Erro ao chamar Claude: {error_msg}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower() or "ANTHROPIC" in str(e):
                raise HTTPException(
                    status_code=503,
                    detail="⚠️ Erro de autenticação com a API Claude. Verifique se ANTHROPIC_API_KEY está configurada corretamente no arquivo .env e reinicie o servidor."
                )
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                raise HTTPException(
                    status_code=429,
                    detail="Limite de requisições atingido. Aguarde um momento e tente novamente."
                )
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar mensagem com IA: {error_msg}"
            )
        
        print(f"[CHAT] Salvando mensagens no banco...")
        # Criar mensagens diretamente usando o pool do PostgreSQL
        from python_backend.models import Message
        import uuid
        
        # Mensagem do usuário
        user_message_id = str(uuid.uuid4())
        await storage.pool.execute(
            'INSERT INTO messages (id, "conversationId", role, content, "createdAt") VALUES ($1, $2, $3, $4, NOW())',
            user_message_id, conversation_id, "user", data.content
        )
        
        # Mensagem do assistente
        ai_message_id = str(uuid.uuid4())
        await storage.pool.execute(
            'INSERT INTO messages (id, "conversationId", role, content, "createdAt") VALUES ($1, $2, $3, $4, NOW())',
            ai_message_id, conversation_id, "assistant", ai_response
        )
        
        # Atualizar updatedAt da conversa
        await storage.pool.execute(
            'UPDATE conversations SET "updatedAt" = NOW() WHERE id = $1',
            conversation_id
        )
        
        # Buscar as mensagens criadas
        user_msg_record = await storage.pool.fetchrow('SELECT * FROM messages WHERE id = $1', user_message_id)
        ai_msg_record = await storage.pool.fetchrow('SELECT * FROM messages WHERE id = $1', ai_message_id)
        
        # Mapear campos
        def map_msg_fields(record):
            d = dict(record)
            if "conversationid" in d and "conversationId" not in d:
                d["conversationId"] = d["conversationid"]
            if "createdat" in d and "createdAt" not in d:
                d["createdAt"] = d["createdat"]
            return Message(**d)
        
        user_message = map_msg_fields(user_msg_record)
        assistant_message = map_msg_fields(ai_msg_record)
        
        print(f"[CHAT] Mensagens salvas. Retornando resposta...")
        # Frontend espera 'userMessage' e 'assistantMessage'
        return {"userMessage": user_message, "assistantMessage": assistant_message}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        print(f"[ERROR] Chat error: {error_detail}")
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        
        # Mensagens de erro mais amigáveis
        if "ANTHROPIC_API_KEY" in error_detail or "api_key" in error_detail.lower():
            raise HTTPException(
                status_code=500,
                detail="Erro de autenticação com a API de IA. Verifique se ANTHROPIC_API_KEY está configurada corretamente."
            )
        elif "timeout" in error_detail.lower():
            raise HTTPException(
                status_code=504,
                detail="A requisição demorou muito para processar. Tente novamente."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar mensagem: {error_detail}"
            )
