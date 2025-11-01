from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Literal, Dict, Any
from datetime import datetime
from enum import Enum
import re

# =============================================================================
# USER MODELS
# =============================================================================

class User(BaseModel):
    """User account model"""
    id: str
    email: EmailStr
    password: str  # This will be hashed
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    """User creation model"""
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserPreferences(BaseModel):
    """User preferences for conversation style and content"""
    user_id: str
    style_preference: Optional[Literal["objetivo", "detalhado"]] = None
    focus_preference: Optional[Literal["ROI-first", "brand-first"]] = None
    tone_preference: Optional[Literal["prático", "estratégico"]] = None
    communication_preference: Optional[Literal["bullets", "blocos"]] = None
    conversation_style: Optional[Literal["coach", "consultor", "direto"]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserPreferencesUpdate(BaseModel):
    """Update user preferences"""
    style_preference: Optional[Literal["objetivo", "detalhado"]] = None
    focus_preference: Optional[Literal["ROI-first", "brand-first"]] = None
    tone_preference: Optional[Literal["prático", "estratégico"]] = None
    communication_preference: Optional[Literal["bullets", "blocos"]] = None
    conversation_style: Optional[Literal["coach", "consultor", "direto"]] = None

# =============================================================================
# EXPERT MODELS
# =============================================================================

class ExpertType(str, Enum):
    HIGH_FIDELITY = "high_fidelity"
    CUSTOM = "custom"

class CategoryType(str, Enum):
    """Expert specialization categories"""
    MARKETING = "marketing"          # Traditional marketing strategy (Kotler, Ogilvy, Hopkins, Burnett, Wells, Wanamaker)
    POSITIONING = "positioning"       # Strategic positioning (Al Ries & Trout)
    CREATIVE = "creative"             # Creative advertising (Bill Bernbach)
    DIRECT_RESPONSE = "direct_response"  # Direct response marketing (Dan Kennedy)
    CONTENT = "content"               # Content marketing (Seth Godin, Ann Handley)
    SEO = "seo"                       # SEO & digital marketing (Neil Patel)
    SOCIAL = "social"                 # Social media marketing (Gary Vaynerchuk)
    GROWTH = "growth"                 # Growth hacking & systems (Sean Ellis, Brian Balfour, Andrew Chen)
    VIRAL = "viral"                   # Viral marketing (Jonah Berger)
    PRODUCT = "product"               # Product psychology & habits (Nir Eyal)

class Expert(BaseModel):
    id: str
    name: str
    title: str
    expertise: List[str]
    bio: str
    systemPrompt: str
    avatar: Optional[str] = None
    expertType: ExpertType = ExpertType.HIGH_FIDELITY
    category: CategoryType = CategoryType.MARKETING  # Default to marketing
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class ExpertCreate(BaseModel):
    name: str
    title: str
    expertise: List[str]
    bio: str
    systemPrompt: str
    avatar: Optional[str] = None
    expertType: ExpertType = ExpertType.CUSTOM
    category: CategoryType = CategoryType.MARKETING
    
    @validator('name', 'title', 'bio')
    def sanitize_html(cls, v):
        """Remove HTML tags from text fields to prevent XSS"""
        if v:
            # Remove HTML tags
            v = re.sub(r'<[^>]*>', '', v)
        return v
    
    @validator('name')
    def validate_name_length(cls, v):
        """Validate name length"""
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v

# =============================================================================
# TASK MODELS (Background Tasks)
# =============================================================================

class TaskStatus(str, Enum):
    """Status of a background task"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskType(str, Enum):
    """Type of background task"""
    COUNCIL_ANALYSIS = "council_analysis"
    COUNCIL_CHAT_MESSAGE = "council_chat_message"
    EXPERT_CHAT_MESSAGE = "expert_chat_message"

class BackgroundTask(BaseModel):
    """Represents a background task"""
    id: str
    userId: str
    taskType: TaskType
    status: TaskStatus
    progress: int = Field(default=0, ge=0, le=100)  # 0-100
    result: Optional[Dict[str, Any]] = None  # Task result (varies by type)
    error: Optional[str] = None  # Error message if failed
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)
    completedAt: Optional[datetime] = None

class TaskCreate(BaseModel):
    """Request to create a new background task"""
    taskType: TaskType
    metadata: Optional[Dict[str, Any]] = None

class TaskUpdate(BaseModel):
    """Update task status/progress"""
    status: Optional[TaskStatus] = None
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# =============================================================================
# CONVERSATION MODELS
# =============================================================================

class Conversation(BaseModel):
    """Conversation model"""
    id: str
    userId: str
    expertId: str
    title: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(BaseModel):
    """Request to create a new conversation"""
    expertId: str
    title: Optional[str] = None

class Message(BaseModel):
    """Message model"""
    id: str
    conversationId: str
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MessageSend(BaseModel):
    """Request to send a message"""
    content: str

class MessageResponse(BaseModel):
    """Response after sending a message"""
    message: Message

# =============================================================================
# PERSONA MODELS
# =============================================================================

class Persona(BaseModel):
    """Persona model - represents ideal client profile"""
    id: str
    userId: str
    name: str
    researchMode: Literal["quick", "strategic"]
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    painPoints: List[str] = []
    goals: List[str] = []
    values: List[str] = []
    contentPreferences: Optional[Dict[str, Any]] = None
    behavioralPatterns: Optional[Dict[str, Any]] = None
    communities: List[str] = []
    researchData: Optional[Dict[str, Any]] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class PersonaCreate(BaseModel):
    """Request to create a new persona"""
    name: str
    researchMode: Literal["quick", "strategic"]
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    painPoints: List[str] = []
    goals: List[str] = []
    values: List[str] = []
    contentPreferences: Optional[Dict[str, Any]] = None
    behavioralPatterns: Optional[Dict[str, Any]] = None
    communities: List[str] = []
    researchData: Optional[Dict[str, Any]] = None

class PersonaModern(BaseModel):
    """Modern persona model with all fields"""
    id: str
    userId: str
    name: str
    researchMode: Literal["quick", "strategic"]
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    painPoints: List[str] = []
    goals: List[str] = []
    values: List[str] = []
    contentPreferences: Optional[Dict[str, Any]] = None
    behavioralPatterns: Optional[Dict[str, Any]] = None
    communities: List[str] = []
    researchData: Optional[Dict[str, Any]] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

# =============================================================================
# COUNCIL MODELS
# =============================================================================

class ExpertContribution(BaseModel):
    """Contribution from a single expert"""
    expertId: str
    expertName: str
    analysis: str
    keyInsights: List[str]
    recommendations: List[str]

class Action(BaseModel):
    """Action item in action plan"""
    id: str
    title: str
    description: str
    responsible: str
    priority: Literal["alta", "média", "baixa"]
    estimatedTime: str
    tools: List[str] = []
    steps: List[str] = []

class Phase(BaseModel):
    """Phase in action plan"""
    phaseNumber: int
    name: str
    duration: str
    objectives: List[str]
    actions: List[Action]
    dependencies: List[str] = []
    deliverables: List[str] = []

class ActionPlan(BaseModel):
    """Complete action plan"""
    phases: List[Phase]
    totalDuration: str
    estimatedBudget: Optional[str] = None
    successMetrics: List[str] = []

class CouncilAnalysis(BaseModel):
    """Council analysis result"""
    id: str
    problem: str
    personaId: Optional[str] = None
    contributions: List[ExpertContribution]
    consensus: str
    actionPlan: Optional[ActionPlan] = None
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class CouncilAnalysisCreate(BaseModel):
    """Request to create a council analysis"""
    problem: str
    personaId: str  # OBRIGATÓRIA
    expertIds: List[str]

class CouncilConversation(BaseModel):
    """Conversation with council of experts"""
    id: str
    userId: str
    personaId: str
    problem: str
    expertIds: List[str]
    analysisId: Optional[str] = None  # ID da análise inicial que gerou esta conversa
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class CouncilConversationCreate(BaseModel):
    """Request to create a new council conversation"""
    problem: str
    personaId: str
    expertIds: List[str]
    analysisId: Optional[str] = None  # ID da análise inicial (opcional)

class MessageSend(BaseModel):
    """Request to send a message to the council"""
    content: str

class MessageReaction(BaseModel):
    """Reaction from one expert to another's message"""
    expertId: str
    expertName: str
    type: Literal["agree", "disagree", "add", "question"]
    content: Optional[str] = None  # Additional comment

class CouncilMessage(BaseModel):
    """Message in a council conversation"""
    id: str
    conversationId: str
    expertId: Optional[str] = None  # None = user message
    expertName: Optional[str] = None
    content: str
    role: Literal["user", "expert", "system"]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reactions: List[MessageReaction] = []

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
    """Request to automatically clone an expert based on input"""
    input: str  # User's input to analyze
    targetExpertId: Optional[str] = None  # Optional: target expert to clone from

class AutoCloneResponse(BaseModel):
    """Response from auto clone request"""
    expertId: str

# Category Info for frontend display
class CategoryInfo(BaseModel):
    """Category information for displaying expert categories"""
    id: str
    name: str
    description: str
    icon: str
    color: str
    expertCount: int
