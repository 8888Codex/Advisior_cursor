"""
Modern Persona Models - JTBD and BAG Frameworks
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

# =============================================================================
# PERSONA MODERN MODELS - JTBD + BAG FRAMEWORKS
# =============================================================================

class JobStatement(BaseModel):
    """Job statement model for JTBD framework"""
    statement: str
    priority: int
    triggers: List[str] = []

class Goal(BaseModel):
    """Goal model for BAG framework"""
    description: str
    timeframe: str  # short, medium, long
    success_metrics: List[str] = []
    obstacles: List[str] = []

class QuantifiedPain(BaseModel):
    """Quantified pain point with measurable impact"""
    description: str
    impact: str  # ex: "10 horas semanais"
    cost: Optional[str] = None  # ex: "R$30K anualmente"
    frequency: str  # ex: "diariamente"

class Touchpoint(BaseModel):
    """Customer journey touchpoint"""
    channel: str
    stage: str
    importance: int  # 1-10
    preferred_content: List[str] = []

class Community(BaseModel):
    """Online community where the persona is active"""
    name: str
    description: str
    relevance: str  # high, medium, low

class ContentPreferences(BaseModel):
    """Content preferences for the persona"""
    formats: List[str] = []
    topics: List[str] = []
    channels: List[str] = []
    influencers: List[str] = []

class ResearchData(BaseModel):
    """Metadata about the research"""
    sources: List[str] = []
    confidence_level: str = "medium"  # high, medium, low
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    generated_at: Optional[str] = None
    target_description: Optional[str] = None
    industry: Optional[str] = None
    additional_context: Optional[str] = None

class Demographics(BaseModel):
    """Demographic information"""
    age: str
    location: str
    occupation: str
    education: Optional[str] = None
    income: Optional[str] = None

class PersonaModern(BaseModel):
    """
    Modern persona model following JTBD and BAG frameworks
    
    Combines:
    - Jobs to Be Done (JTBD)
    - Behaviors, Aspirations, Goals (BAG)
    - Quantified pain points
    - Modern customer journey
    """
    # Basic identification
    id: str
    userId: str
    name: str
    researchMode: str = "strategic"  # quick, strategic
    
    # Framework Híbrido: Personas + JTBD
    job_statement: str
    situational_contexts: List[str] = []
    functional_jobs: List[str] = []
    emotional_jobs: List[str] = []
    social_jobs: List[str] = []
    
    # Framework BAG
    behaviors: Dict[str, List[str]] = {}
    aspirations: List[str] = []
    goals: List[str] = []
    
    # Elementos quantitativos
    pain_points_quantified: List[QuantifiedPain] = []
    decision_criteria: Dict[str, float] = {}  # critério: peso
    
    # Demographics and values
    demographics: Demographics
    values: List[str] = []
    
    # Jornada moderna
    touchpoints: List[Touchpoint] = []
    content_preferences: ContentPreferences = ContentPreferences()
    communities: List[Community] = []
    
    # Research metadata
    research_data: ResearchData = ResearchData()
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PersonaModernCreate(BaseModel):
    """Request payload for modern persona creation"""
    mode: str = "strategic"  # quick, strategic
    targetDescription: str
    industry: Optional[str] = None
    additionalContext: Optional[str] = None
    framework: str = "hybrid"  # hybrid, jtbd, bag
