from fastapi import APIRouter, HTTPException, Request
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from python_backend.models import (
    CouncilConversation, CouncilConversationCreate, CouncilMessage, MessageSend, MessageReaction
)
from python_backend.storage import storage
from python_backend.crew_agent import LegendAgentFactory

router = APIRouter(
    tags=["Council Chat"],
)

limiter = Limiter(key_func=get_remote_address)

@router.post("/api/council/conversations", response_model=CouncilConversation, status_code=201)
@limiter.limit("10/hour")
async def create_council_conversation(request: Request, data: CouncilConversationCreate):
    """
    Cria nova conversa com conselho de especialistas.
    
    Requisitos:
    - personaId: Obrigatório (deve existir)
    - expertIds: Lista com pelo menos 2 especialistas
    - problem: Descrição do problema (mínimo 10 caracteres)
    """
    user_id = "default_user"
    
    try:
        # Validar persona
        persona = await storage.get_persona(data.personaId)
        if not persona:
            raise HTTPException(
                status_code=404,
                detail=f"Persona com ID {data.personaId} não encontrada. Crie uma persona primeiro."
            )
        
        # Validar especialistas
        if not data.expertIds or len(data.expertIds) < 1:
            raise HTTPException(
                status_code=400,
                detail="Selecione pelo menos 1 especialista para a conversa."
            )
        
        experts = []
        for expert_id in data.expertIds:
            expert = await storage.get_expert(expert_id)
            if not expert:
                raise HTTPException(
                    status_code=404,
                    detail=f"Especialista {expert_id} não encontrado."
                )
            experts.append(expert)
        
        # Validar problema
        if not data.problem or len(data.problem.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Descrição do problema deve ter pelo menos 10 caracteres."
            )
        
        # Criar conversa
        conversation = await storage.create_council_conversation(
            user_id=user_id,
            persona_id=data.personaId,
            problem=data.problem,
            expert_ids=data.expertIds,
            analysis_id=data.analysisId  # Já é Optional[str] no modelo
        )
        
        # Criar mensagem inicial do sistema
        await storage.create_council_message(
            conversation_id=conversation.id,
            role="system",
            content=f"Conselho iniciado com {len(experts)} especialista(s). Problema: {data.problem}"
        )
        
        print(f"[Council Chat] Conversa criada: {conversation.id} com {len(experts)} especialistas")
        return conversation
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Council Chat] Erro ao criar conversa: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar conversa: {str(e)}"
        )

@router.get("/api/council/conversations", response_model=List[CouncilConversation])
async def get_council_conversations():
    """Lista todas as conversas do conselho do usuário"""
    user_id = "default_user"
    return await storage.get_council_conversations(user_id)

@router.get("/api/council/conversations/{conversation_id}", response_model=CouncilConversation)
async def get_council_conversation(conversation_id: str):
    """Obtém uma conversa específica do conselho"""
    conversation = await storage.get_council_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return conversation

@router.get("/api/council/conversations/{conversation_id}/messages", response_model=List[CouncilMessage])
async def get_council_messages(conversation_id: str):
    """Obtém todas as mensagens de uma conversa do conselho"""
    # Verificar se conversa existe
    conversation = await storage.get_council_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    messages = await storage.get_council_messages(conversation_id)
    return messages

async def _process_council_message_background(conversation_id: str, message_content: str):
    """Processa mensagem do conselho em background"""
    import asyncio
    
    try:
        # Buscar conversa
        conversation = await storage.get_council_conversation(conversation_id)
        if not conversation:
            print(f"[Council Chat Background] Conversa {conversation_id} não encontrada")
            return
        
        # Buscar persona
        persona = await storage.get_persona(conversation.personaId)
        if not persona:
            print(f"[Council Chat Background] Persona não encontrada")
            return
        
        # Buscar especialistas
        experts = []
        for expert_id in conversation.expertIds:
            expert = await storage.get_expert(expert_id)
            if not expert:
                print(f"[Council Chat Background] Aviso: Especialista {expert_id} não encontrado, pulando...")
                continue
            experts.append(expert)
        
        if not experts:
            print(f"[Council Chat Background] Nenhum especialista válido encontrado")
            return
        
        # Buscar histórico da conversa (já inclui a mensagem do usuário que foi salva antes)
        history = await storage.get_council_messages(conversation_id)
        
        print(f"[Council Chat Background] Obtendo respostas de {len(experts)} especialistas...")
        
        # Buscar análise inicial se disponível
        analysis_context = ""
        if conversation.analysisId:
            print(f"[Council Chat Background] 🔍 Buscando análise: {conversation.analysisId}")
            try:
                analysis = await storage.get_council_analysis(conversation.analysisId)
                if analysis:
                    print(f"[Council Chat Background] ✅ Análise encontrada! Consenso: {len(analysis.consensus)} chars, Contribuições: {len(analysis.contributions)}")
                    analysis_context = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONTEXTO DA ANÁLISE INICIAL DO CONSELHO                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

**PROBLEMA ORIGINAL:**
{analysis.problem}

**CONSENSO ESTRATÉGICO GERADO PELO CONSELHO:**
{analysis.consensus}

"""
                    if analysis.contributions:
                        analysis_context += "**CONTRIBUIÇÕES INICIAIS DOS ESPECIALISTAS:**\n"
                        for contrib in analysis.contributions:
                            analysis_context += f"\n--- {contrib.expertName} ---\n"
                            
                            if contrib.keyInsights:
                                analysis_context += f"\n### INSIGHTS DE {contrib.expertName.upper()}:\n"
                                for idx, insight in enumerate(contrib.keyInsights, 1):
                                    analysis_context += f"  {idx}. {insight}\n"
                                analysis_context += "\n"
                            
                            if contrib.recommendations:
                                analysis_context += f"### RECOMENDAÇÕES DE {contrib.expertName.upper()}:\n"
                                for idx, rec in enumerate(contrib.recommendations, 1):
                                    analysis_context += f"  {idx}. {rec}\n"
                                analysis_context += "\n"
                        analysis_context += "\n"
                    if analysis.actionPlan:
                        analysis_context += "**PLANO DE AÇÃO CRIADO:**\n"
                        analysis_context += f"Total de {len(analysis.actionPlan.phases)} fases | Duração: {analysis.actionPlan.totalDuration}\n\n"
                    
                    # Adicionar contexto COMPLETO da persona (CRÍTICO)
                    analysis_context += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           PERSONA DO CLIENTE IDEAL                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

**NOME DA PERSONA:** {persona.name}

**JOB STATEMENT (Trabalho Principal):**
{persona.job_statement if hasattr(persona, 'job_statement') else 'N/A'}

**PRINCIPAIS JOBS TO BE DONE:**
Funcionais: {', '.join(persona.functional_jobs[:5]) if hasattr(persona, 'functional_jobs') and persona.functional_jobs else 'N/A'}
Emocionais: {', '.join(persona.emotional_jobs[:3]) if hasattr(persona, 'emotional_jobs') and persona.emotional_jobs else 'N/A'}
Sociais: {', '.join(persona.social_jobs[:2]) if hasattr(persona, 'social_jobs') and persona.social_jobs else 'N/A'}

**PAIN POINTS PRINCIPAIS:**
"""
                    if hasattr(persona, 'pain_points_quantified') and persona.pain_points_quantified:
                        for idx, pain in enumerate(persona.pain_points_quantified[:3], 1):
                            analysis_context += f"{idx}. {pain['description'] if isinstance(pain, dict) else pain.description} - Impacto: {pain['impact'] if isinstance(pain, dict) else pain.impact}\n"
                    
                    analysis_context += f"""
**DEMOGRAPHICS:**
{persona.demographics if hasattr(persona, 'demographics') else 'N/A'}

**GOALS:**
{', '.join(persona.goals[:5]) if hasattr(persona, 'goals') and persona.goals else 'N/A'}

**VALORES CORE:**
{', '.join(persona.values[:5]) if hasattr(persona, 'values') and persona.values else 'N/A'}

"""
                else:
                    print(f"[Council Chat Background] ❌ Análise não encontrada no banco para ID: {conversation.analysisId}")
            except Exception as e:
                print(f"[Council Chat Background] ❌ Erro ao buscar análise inicial: {e}")
                import traceback
                traceback.print_exc()
                analysis_context = ""
        else:
            print(f"[Council Chat Background] ⚠️ Conversa sem analysisId - contexto limitado")
        
        # Para cada especialista, gerar resposta
        for expert in experts:
            try:
                conversation_history = ""
                if history:
                    conversation_history = "\n\n**HISTÓRICO DA CONVERSA (últimas mensagens):**\n"
                    for msg in history[-15:]:
                        if msg.role == "user":
                            conversation_history += f"\n👤 Usuário: {msg.content}\n"
                        elif msg.role == "expert":
                            conversation_history += f"\n👨‍💼 {msg.expertName}: {msg.content[:200]}...\n"
                
                persona_context = f"""
[CONTEXTO DO CLIENTE IDEAL - PERSONA]:
Nome: {persona.name}
Objetivos: {', '.join(persona.goals[:5]) if persona.goals else 'Não especificados'}
Pain Points: {', '.join(persona.painPoints[:5]) if persona.painPoints else 'Não especificados'}
Valores: {', '.join(persona.values[:5]) if persona.values else 'Não especificados'}

IMPORTANTE: Suas recomendações devem ser específicas para este perfil de cliente ideal.
"""
                
                messages_for_claude = []
                for msg in history:
                    if msg.role == "user":
                        messages_for_claude.append({"role": "user", "content": msg.content})
                    elif msg.role == "expert":
                        expert_msg_content = f"[{msg.expertName}]: {msg.content}"
                        messages_for_claude.append({"role": "assistant", "content": expert_msg_content})
                
                messages_for_claude.append({"role": "user", "content": message_content})
                
                enriched_system_prompt = expert.systemPrompt
                
                # Adicionar instrução CRÍTICA no topo
                enriched_system_prompt += """

╔══════════════════════════════════════════════════════════════════════════════╗
║  ⚠️  CONTEXTO COMPLETO DISPONÍVEL - NÃO PEÇA INFORMAÇÕES BÁSICAS NOVAMENTE  ║
╚══════════════════════════════════════════════════════════════════════════════╝

**VOCÊ TEM TODO O CONTEXTO NECESSÁRIO ABAIXO. NÃO PEÇA INFORMAÇÕES BÁSICAS NOVAMENTE.**

O usuário JÁ passou por uma análise inicial COMPLETA com o conselho de especialistas.
Abaixo está TODO o contexto dessa análise, incluindo:
- ✅ O problema original completo
- ✅ O consenso estratégico do conselho
- ✅ TODOS os insights e recomendações de cada especialista (não apenas resumo)
- ✅ O plano de ação estruturado com fases
- ✅ A persona COMPLETA do público-alvo (demographics, jobs, pain points, goals, valores)
- ✅ O histórico completo desta conversa

**USE ESTE CONTEXTO** para responder de forma CONTEXTUALIZADA e EXTREMAMENTE VALIOSA.

❌ NÃO pergunte "qual é seu negócio?"
❌ NÃO pergunte "quem é seu público?"
❌ NÃO pergunte "qual seu objetivo?"
❌ NÃO pergunte informações que JÁ ESTÃO no contexto abaixo

✅ RESPONDA com base no contexto completo
✅ AGREGUE VALOR com insights específicos
✅ SEJA DIRETO e acionável

"""
                
                # FORÇAR formato executável (não texto livre)
                execution_template = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FORMATO OBRIGATÓRIO DE RESPOSTA                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

**⚠️  VOCÊ DEVE RESPONDER NESTE FORMATO EXATO (NÃO FORMATO LIVRE):**

## 🎯 DIAGNÓSTICO RÁPIDO
[1-2 linhas identificando o problema core, não parágrafo longo]

## ⚡ 3 AÇÕES IMEDIATAS (15 MIN CADA)

**AÇÃO 1:** [Título específico - ex: "Escrever headline usando fórmula 4U"]
- **Fazer agora:** [Passo-a-passo ultra específico em 3-5 bullet points]
- **Resultado:** [O que você terá ao completar]
- **Tempo:** ~15 min

**AÇÃO 2:** [Título específico]
- **Fazer agora:** [Passo-a-passo]
- **Resultado:** [Output esperado]
- **Tempo:** ~15 min

**AÇÃO 3:** [Título específico]
- **Fazer agora:** [Passo-a-passo]
- **Resultado:** [Output esperado]
- **Tempo:** ~15 min

## 📋 TEMPLATE PRONTO PARA USAR

[Gere 1 artefato REAL que o usuário pode copiar e usar:
- Email de vendas pronto
- Post de LinkedIn completo
- Script de VSL
- Checklist de implementação
- Sequência de automação
- etc.]

## 📊 COMO MEDIR SUCESSO
[1 métrica específica e como medir - ex: "Taxa de abertura >25% no email"]

## ⚠️ ARMADILHA A EVITAR
[1 erro comum que destruiria a implementação]

**IMPORTANTE:**
- Máximo 300 palavras TOTAL
- Zero teoria ou filosofia
- Zero parágrafos longos
- 100% executável agora
- Template deve ser copy-paste ready
"""
                
                enriched_system_prompt += "\n\n" + execution_template
                
                if analysis_context:
                    enriched_system_prompt += "\n\n" + analysis_context
                enriched_system_prompt += "\n\n" + persona_context
                if conversation_history:
                    enriched_system_prompt += "\n\n" + conversation_history
                
                enriched_system_prompt += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INSTRUÇÕES PARA A CONVERSA COLABORATIVA                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

**VOCÊ ESTÁ EM UMA MESA DE CONVERSA COM OUTROS ESPECIALISTAS:**

1. Você TEM ACESSO COMPLETO ao contexto da análise inicial acima (incluindo suas próprias contribuições)

2. Quando o usuário mencionar "plano", "plano de ação", "fases", "ações", etc., 
   VOCÊ DEVE fazer referência ao plano de ação que foi criado anteriormente.

3. Você pode debater, questionar ou complementar as opiniões dos outros especialistas.

4. Mantenha seu próprio estilo, framework e metodologia, mas seja colaborativo.

5. Se o usuário perguntar sobre algo relacionado à análise inicial ou ao plano,
   use esse contexto para responder de forma precisa e detalhada.

6. Esta é uma conversa contínua - todos os especialistas estão "na mesma mesa" 
   e compartilham o mesmo contexto completo.

7. **LEMBRE-SE:** O usuário já forneceu TODAS as informações. Não peça novamente!
"""
                
                agent = LegendAgentFactory.create_agent(expert.name, enriched_system_prompt)
                ai_response = await agent.chat(messages_for_claude, message_content)
                
                await storage.create_council_message(
                    conversation_id=conversation_id,
                    expert_id=expert.id,
                    expert_name=expert.name,
                    role="expert",
                    content=ai_response
                )
                
                print(f"[Council Chat Background] Resposta de {expert.name} gerada e salva")
                
            except Exception as e:
                print(f"[Council Chat Background] Erro ao gerar resposta de {expert.name}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"[Council Chat Background] Processamento completo para conversa {conversation_id}")
        
    except Exception as e:
        print(f"[Council Chat Background] Erro geral: {e}")
        import traceback
        traceback.print_exc()

@router.post("/api/council/conversations/{conversation_id}/messages", status_code=202)
@limiter.limit("30/minute")
async def send_message_to_council(request: Request, conversation_id: str, data: MessageSend):
    """
    Envia mensagem para o conselho e recebe respostas de todos os especialistas.
    
    RETORNA IMEDIATAMENTE (202 Accepted) e processa em background.
    O cliente deve fazer polling em /api/council/conversations/{id}/messages para
    verificar quando as respostas dos especialistas estiverem prontas.
    """
    import asyncio
    
    try:
        # Validar que a conversa existe
        conversation = await storage.get_council_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")
        
        # Salvar mensagem do usuário imediatamente
        user_message = await storage.create_council_message(
            conversation_id=conversation_id,
            role="user",
            content=data.content
        )
        
        # Processar respostas em background (não bloqueia a resposta)
        asyncio.create_task(_process_council_message_background(conversation_id, data.content))
        
        # Retornar imediatamente
        return {
            "status": "processing",
            "message": "Mensagem recebida. Processando respostas dos especialistas em background...",
            "userMessage": user_message,
            "conversationId": conversation_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Council Chat] Erro ao iniciar processamento: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )

@router.post("/api/council/conversations/{conversation_id}/messages/{message_id}/reactions", status_code=201)
@limiter.limit("20/minute")
async def add_message_reaction(
    request: Request,
    conversation_id: str,
    message_id: str,
    reaction: MessageReaction
):
    """Adiciona reação de um especialista a uma mensagem de outro"""
    # Verificar se conversa existe
    conversation = await storage.get_council_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Adicionar reação
    success = await storage.add_council_message_reaction(message_id, reaction)
    if not success:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    
    return {"success": True, "reaction": reaction}

