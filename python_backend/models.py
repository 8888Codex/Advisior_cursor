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

class BusinessProfile(BaseModel):
    id: str
    userId: str  # Will use session/auth later
    companyName: str
    industry: str
    companySize: str  # "1-10", "11-50", "51-200", "201-1000", "1000+"
    targetAudience: str
    mainProducts: str
    channels: List[str]  # ["online", "retail", "b2b", "marketplace"]
    budgetRange: str  # "< $10k/month", "$10k-$50k/month", "$50k-$100k/month", "> $100k/month"
    primaryGoal: str  # "growth", "positioning", "retention", "launch"
    mainChallenge: str
    timeline: str  # "immediate", "3-6 months", "6-12 months", "long-term"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class BusinessProfileCreate(BaseModel):
    companyName: str
    industry: str
    companySize: str
    targetAudience: str
    mainProducts: str
    channels: List[str]
    budgetRange: str
    primaryGoal: str
    mainChallenge: str
    timeline: str

class AgentContribution(BaseModel):
    """Individual expert's contribution to council analysis"""
    expertId: str
    expertName: str
    analysis: str
    keyInsights: List[str]
    recommendations: List[str]

class CouncilAnalysis(BaseModel):
    """Complete council analysis with all expert contributions"""
    id: str
    userId: str
    problem: str
    profileId: Optional[str] = None  # BusinessProfile ID if used
    marketResearch: Optional[str] = None  # Perplexity findings
    contributions: List[AgentContribution]
    consensus: str  # Synthesized final recommendation
    citations: List[str] = []  # From Perplexity
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class CouncilAnalysisCreate(BaseModel):
    """Request payload for council analysis"""
    problem: str
    expertIds: Optional[List[str]] = None  # If None, use all 8 legends

class ExpertRecommendation(BaseModel):
    """Single expert recommendation with relevance score and justification"""
    expertId: str
    expertName: str
    relevanceScore: int  # 1-5 stars
    justification: str

class RecommendExpertsRequest(BaseModel):
    """Request to get expert recommendations based on problem"""
    problem: str

class RecommendExpertsResponse(BaseModel):
    """Response with recommended experts ranked by relevance"""
    recommendations: List[ExpertRecommendation]

class AutoCloneRequest(BaseModel):
    """Request to auto-clone a cognitive expert from minimal input"""
    targetName: str
    context: Optional[str] = None  # Optional additional context
