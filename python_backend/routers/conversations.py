from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from python_backend.models import Conversation, ConversationCreate, Message, MessageCreate, MessageSend, MessageResponse
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

@router.post("/api/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
@limiter.limit("10/minute")
async def send_message(request: Request, conversation_id: str, data: MessageSend):
    conversation = await storage.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    expert = await storage.get_expert(conversation.expertId)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert for this conversation not found")
        
    history = await storage.get_messages(conversation_id)
    
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

    agent = LegendAgentFactory.create_agent(expert.name, enriched_system_prompt)
    ai_response = await agent.chat([h.model_dump() for h in history], data.content)
    
    user_message = await storage.create_message(MessageCreate(
        conversationId=conversation_id, role="user", content=data.content
    ))
    assistant_message = await storage.create_message(MessageCreate(
        conversationId=conversation_id, role="assistant", content=ai_response
    ))
    
    return MessageResponse(userMessage=user_message, assistantMessage=assistant_message)
