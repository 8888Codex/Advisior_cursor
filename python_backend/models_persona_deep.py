"""
Models for Deep Persona - Framework PERSONA PROFUNDA (20 pontos)
Adaptação do Framework EXTRACT para personas de audiência
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

# =============================================================================
# SEÇÃO 1: IDENTITY CORE
# =============================================================================

class FormativeExperience(BaseModel):
    """Experiência formativa que moldou a relação com o problema"""
    description: str
    when_where: str  # Ex: "2019, após fracasso em lançamento"
    impact: str  # Como mudou o comportamento

class DecisionPattern(BaseModel):
    """Padrão decisório (Xadrez Mental)"""
    name: str  # Ex: "Análise Paralítica"
    description: str  # Como esse padrão funciona

class LanguageExpression(BaseModel):
    """Linguagem própria - como a pessoa fala"""
    expression: str  # Ex: "Tá muito cru ainda"
    context: str  # Quando/como usa essa expressão

class EmotionalTrigger(BaseModel):
    """Gatilho emocional"""
    trigger: str
    reaction: str
    trigger_type: str  # "action" ou "inertia"

class CoreValue(BaseModel):
    """Valor nuclear inegociável"""
    value: str
    manifestation: str  # Como se manifesta em decisões

# =============================================================================
# SEÇÃO 2: BEHAVIORAL PATTERNS
# =============================================================================

class SignatureDecisionStep(BaseModel):
    """Uma etapa do padrão de decisão característico"""
    step_number: int
    name: str
    description: str

class StoryBank(BaseModel):
    """História que a pessoa conta repetidamente"""
    title: str
    context: str
    frustration: str
    impact: str

class ObjectionPattern(BaseModel):
    """Objeção recorrente"""
    objection: str
    real_translation: str  # O que ele REALMENTE quer dizer
    how_to_counter: str  # Como contornar

class TrustTrigger(BaseModel):
    """Gerador de confiança"""
    trigger: str
    why_it_works: str

class FailureStory(BaseModel):
    """História de fracasso"""
    title: str
    what_happened: str
    emotional_impact: str
    lesson_learned: str

# =============================================================================
# SEÇÃO 3: COMMUNICATION PATTERNS
# =============================================================================

class CommunicationStyle(BaseModel):
    """Estilo de comunicação preferido"""
    tone: str  # Ex: "Direto, sem enrolação"
    structure: str  # Ex: "Passo-a-passo numerado"
    detail_level: str  # Ex: "Médio - quer entender o 'por quê'"
    speed: str  # Ex: "Resumo executivo + onde aprofundar"

class ContentConsumptionPattern(BaseModel):
    """Padrão de consumo de conteúdo"""
    channel: str
    active_hours: str
    content_types: List[str]
    attention_level: str  # "high", "medium", "low"
    intention: str
    best_format: str

class InfluenceNetwork(BaseModel):
    """Rede de influência"""
    top_influencers: List[Dict[str, str]]  # [{"name": "X", "why": "Y"}]
    active_communities: List[Dict[str, str]]  # [{"name": "X", "engagement": "Y"}]
    information_sources: List[Dict[str, str]]  # [{"source": "X", "what_seeks": "Y"}]

# =============================================================================
# SEÇÃO 4: QUANTIFIED PAIN POINTS
# =============================================================================

class PrimaryPainPoint(BaseModel):
    """Ponto de dor primário com métricas"""
    description: str
    frequency: str  # "diária", "semanal", "mensal"
    financial_cost: Optional[str] = None  # Ex: "R$3-5K/mês"
    time_cost: Optional[str] = None  # Ex: "10h/semana"
    emotional_impact: str
    quote: str  # Como ele descreve isso

class SecondaryPainPoint(BaseModel):
    """Ponto de dor secundário"""
    description: str
    impact: str
    frequency: str

# =============================================================================
# SEÇÃO 5: GOALS & ASPIRATIONS
# =============================================================================

class ShortTermGoal(BaseModel):
    """Objetivo de curto prazo (0-6 meses)"""
    goal: str
    success_metric: str
    why_it_matters: str
    perceived_obstacles: List[str]

class LongTermAspiration(BaseModel):
    """Aspiração de longo prazo (1-3 anos)"""
    aspiration: str
    emotional_description: str
    desired_impact: str

class SuccessDefinition(BaseModel):
    """Como ELE define sucesso"""
    success_means: List[Dict[str, str]]  # [{"element": "X", "why": "Y"}]
    not_success: List[Dict[str, str]]  # [{"anti_pattern": "X", "why_rejects": "Y"}]

# =============================================================================
# SEÇÃO 6: JOURNEY MAPPING
# =============================================================================

class JourneyStage(BaseModel):
    """Estágio da jornada do cliente"""
    stage_number: int
    name: str
    mental_state: str
    typical_actions: List[str]
    content_consumed: List[str]
    objections: List[str]
    triggers_to_next: List[str]

class TouchpointDetail(BaseModel):
    """Detalhe de um touchpoint"""
    channel: str
    active_hours: str
    content_types: List[str]
    attention_level: str  # "high", "medium", "low"
    intention: str
    best_format: str

# =============================================================================
# PERSONA PROFUNDA - MODELO COMPLETO
# =============================================================================

class PersonaDeep(BaseModel):
    """
    Persona Profunda seguindo Framework PERSONA PROFUNDA (20 pontos)
    Adaptação do Framework EXTRACT para audiências
    """
    # Basic identification
    id: str
    userId: str
    name: str
    researchMode: str = "deep"  # "quick", "strategic", "deep"
    target_description: str
    industry: Optional[str] = None
    
    # ==========================================================================
    # SEÇÃO 1: IDENTITY CORE (5 pontos)
    # ==========================================================================
    
    # 1. Experiências Formativas
    formative_experiences: List[FormativeExperience] = []
    
    # 2. Padrões Decisórios (Xadrez Mental)
    decision_patterns: List[DecisionPattern] = []
    
    # 3. Linguagem Própria
    language_expressions: List[LanguageExpression] = []
    
    # 4. Gatilhos Emocionais
    action_triggers: List[EmotionalTrigger] = []
    inertia_triggers: List[EmotionalTrigger] = []
    
    # 5. Valores Nucleares
    core_values: List[CoreValue] = []
    
    # ==========================================================================
    # SEÇÃO 2: BEHAVIORAL PATTERNS (5 pontos)
    # ==========================================================================
    
    # 6. Signature Decision Pattern
    signature_decision_pattern: List[SignatureDecisionStep] = []
    
    # 7. Story Banks
    story_banks: List[StoryBank] = []
    
    # 8. Objection Patterns
    objection_patterns: List[ObjectionPattern] = []
    
    # 9. Trust Triggers
    trust_triggers: List[TrustTrigger] = []
    
    # 10. Failure Stories
    failure_stories: List[FailureStory] = []
    
    # ==========================================================================
    # SEÇÃO 3: COMMUNICATION PATTERNS (3 pontos)
    # ==========================================================================
    
    # 11. Preferred Communication Style
    communication_style: Optional[CommunicationStyle] = None
    
    # 12. Content Consumption Patterns
    content_consumption_patterns: List[ContentConsumptionPattern] = []
    
    # 13. Influence Network
    influence_network: Optional[InfluenceNetwork] = None
    
    # ==========================================================================
    # SEÇÃO 4: QUANTIFIED PAIN POINTS (2 pontos)
    # ==========================================================================
    
    # 14. Primary Pain Points
    primary_pain_points: List[PrimaryPainPoint] = []
    
    # 15. Secondary Pain Points
    secondary_pain_points: List[SecondaryPainPoint] = []
    
    # ==========================================================================
    # SEÇÃO 5: GOALS & ASPIRATIONS (3 pontos)
    # ==========================================================================
    
    # 16. Short-Term Goals
    short_term_goals: List[ShortTermGoal] = []
    
    # 17. Long-Term Aspirations
    long_term_aspirations: List[LongTermAspiration] = []
    
    # 18. Definition of Success
    success_definition: Optional[SuccessDefinition] = None
    
    # ==========================================================================
    # SEÇÃO 6: JOURNEY MAPPING (2 pontos)
    # ==========================================================================
    
    # 19. Customer Journey Stages
    journey_stages: List[JourneyStage] = []
    
    # 20. Touchpoint Matrix
    touchpoint_matrix: List[TouchpointDetail] = []
    
    # ==========================================================================
    # METADATA
    # ==========================================================================
    
    # Research metadata
    research_data: Dict = {}
    quality_score: Optional[int] = None  # 1-20 (meta: 18-20)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PersonaDeepCreate(BaseModel):
    """Request payload for deep persona creation"""
    targetDescription: str
    industry: Optional[str] = None
    additionalContext: Optional[str] = None
    # mode is always "deep" for this endpoint

