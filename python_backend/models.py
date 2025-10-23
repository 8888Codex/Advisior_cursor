from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum

class ExpertType(str, Enum):
    HIGH_FIDELITY = "high_fidelity"
    CUSTOM = "custom"

class Expert(BaseModel):
    id: str
    name: str
    title: str
    expertise: List[str]
    bio: str
    systemPrompt: str
    avatar: Optional[str] = None
    expertType: ExpertType = ExpertType.HIGH_FIDELITY
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class ExpertCreate(BaseModel):
    name: str
    title: str
    expertise: List[str]
    bio: str
    systemPrompt: str
    avatar: Optional[str] = None
    expertType: ExpertType = ExpertType.CUSTOM

class Conversation(BaseModel):
    id: str
    expertId: str
    title: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(BaseModel):
    expertId: str
    title: str

class Message(BaseModel):
    id: str
    conversationId: str
    role: Literal["user", "assistant"]
    content: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class MessageCreate(BaseModel):
    conversationId: str
    role: Literal["user", "assistant"]
    content: str

class MessageSend(BaseModel):
    content: str

class MessageResponse(BaseModel):
    userMessage: Message
    assistantMessage: Message
