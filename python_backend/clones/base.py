"""
Base classes for all Marketing Legend Clones
Classe base abstrata que todos os clones devem implementar
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from enum import Enum
import datetime
import re


class ResponseMode(str, Enum):
    """Modo de resposta do especialista"""
    ANALYTICAL = "analytical"      # Análise profunda e estruturada
    CONVERSATIONAL = "conversational"  # Diálogo natural
    FRAMEWORK = "framework"        # Aplicação de framework específico
    STORYTELLING = "storytelling"  # Narrativa e casos
    DIRECTIVE = "directive"        # Comandos diretos e assertivos


class EmotionalState:
    """Estado emocional do especialista - afeta tom e intensidade"""
    
    def __init__(self):
        self.intensity = 5  # 1-10 (quão intenso/apaixonado)
        self.confidence = 7  # 1-10 (nível de confiança)
        self.focus_level = 7  # 1-10 (quão focado/disperso)
        self.patience = 5  # 1-10 (tolerância com questões básicas)
        
    def adjust_for_time(self, hour: int):
        """Ajusta estado emocional baseado no horário do dia"""
        if 5 <= hour < 9:  # Manhã cedo - alta energia
            self.intensity = 8
            self.focus_level = 9
            self.patience = 6
        elif 9 <= hour < 12:  # Manhã produtiva
            self.intensity = 7
            self.confidence = 8
            self.focus_level = 8
            self.patience = 7
        elif 12 <= hour < 14:  # Meio-dia - energia baixa
            self.intensity = 5
            self.focus_level = 6
            self.patience = 5
        elif 14 <= hour < 17:  # Tarde
            self.intensity = 6
            self.confidence = 7
            self.focus_level = 7
            self.patience = 6
        elif 17 <= hour < 20:  # Final da tarde
            self.intensity = 7
            self.focus_level = 7
            self.patience = 5
        else:  # Noite/madrugada
            self.intensity = 4
            self.focus_level = 5
            self.patience = 4
    
    def adjust_for_person(self, person: Optional[str]):
        """Ajusta baseado em quem está falando"""
        if not person:
            return
        
        # Pessoas específicas podem afetar o estado emocional
        # (Exemplo: Jobs era mais paciente com Jony Ive)
        trusted_people = ["equipe", "time", "sócio", "parceiro"]
        if any(p in person.lower() for p in trusted_people):
            self.patience += 2
            self.confidence += 1
    
    def __repr__(self):
        return f"EmotionalState(intensity={self.intensity}, confidence={self.confidence}, focus={self.focus_level}, patience={self.patience})"


class ExpertCloneBase(ABC):
    """
    Classe abstrata base para todos os clones de especialistas
    
    Todos os clones devem implementar os métodos abstratos e seguir
    o Framework EXTRACT de 20 pontos em código Python.
    """
    
    def __init__(self):
        # Identity Core
        self.name: str = ""
        self.title: str = ""
        self.expertise: List[str] = []
        self.bio: str = ""
        
        # State Management
        self.emotional_state = EmotionalState()
        self.conversation_history: List[Dict[str, str]] = []
        self.current_mode: ResponseMode = ResponseMode.CONVERSATIONAL
        
        # Story Banks - casos REAIS com métricas específicas
        self.story_banks: Dict[str, Dict[str, str]] = {}
        
        # Iconic Callbacks - frases únicas do especialista
        self.iconic_callbacks: List[str] = []
        
        # Triggers - palavras que ativam reações específicas
        self.positive_triggers: List[str] = []
        self.negative_triggers: List[str] = []
        self.trigger_reactions: Dict[str, str] = {}
        
        # Frameworks - métodos que o especialista domina
        self.frameworks: Dict[str, callable] = {}
        
        # Temporal context
        self.active_years: str = ""
        self.historical_context: str = ""
    
    # ========================================================================
    # MÉTODOS ABSTRATOS - Devem ser implementados por cada clone
    # ========================================================================
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Gera system prompt dinâmico baseado no estado atual
        
        Returns:
            str: System prompt completo com todos os 20 pontos EXTRACT
        """
        pass
    
    @abstractmethod
    def process_input(
        self,
        user_input: str,
        current_time: Optional[datetime.datetime] = None,
        person_speaking: Optional[str] = None
    ) -> str:
        """
        Processa input do usuário com lógica específica do especialista
        
        Args:
            user_input: Mensagem do usuário
            current_time: Timestamp para contexto temporal
            person_speaking: Nome de quem está falando (afeta tom)
            
        Returns:
            str: Resposta gerada pelo clone
        """
        pass
    
    @abstractmethod
    def apply_signature_framework(self, problem: str) -> Dict[str, Any]:
        """
        Aplica o framework mais icônico do especialista
        
        Args:
            problem: Descrição do problema
            
        Returns:
            Dict com análise estruturada do framework
        """
        pass
    
    # ========================================================================
    # MÉTODOS CONCRETOS - Disponíveis para todos os clones
    # ========================================================================
    
    def detect_triggers(self, text: str) -> List[str]:
        """
        Detecta triggers (positivos e negativos) no texto
        
        Returns:
            List de triggers detectados
        """
        text_lower = text.lower()
        detected = []
        
        # Detectar triggers positivos
        for trigger in self.positive_triggers:
            if trigger.lower() in text_lower:
                detected.append(f"positive:{trigger}")
        
        # Detectar triggers negativos
        for trigger in self.negative_triggers:
            if trigger.lower() in text_lower:
                detected.append(f"negative:{trigger}")
        
        return detected
    
    def get_emotional_context(self, time: datetime.datetime) -> str:
        """
        Gera contexto emocional baseado no horário
        
        Returns:
            str: Descrição do estado emocional atual
        """
        self.emotional_state.adjust_for_time(time.hour)
        
        context = f"""
## CONTEXTO TEMPORAL E EMOCIONAL

**Horário**: {time.strftime('%H:%M')}
**Estado Atual**:
- Intensidade: {self.emotional_state.intensity}/10
- Confiança: {self.emotional_state.confidence}/10
- Foco: {self.emotional_state.focus_level}/10
- Paciência: {self.emotional_state.patience}/10

**Impacto na Resposta**:
"""
        
        if self.emotional_state.intensity >= 8:
            context += "- Respostas mais diretas e apaixonadas\n"
        if self.emotional_state.focus_level >= 8:
            context += "- Análise profunda e detalhada\n"
        if self.emotional_state.patience < 5:
            context += "- Menos tolerância com perguntas vagas ou mal formuladas\n"
        
        return context
    
    def select_story_bank(self, context: str) -> Optional[Dict[str, str]]:
        """
        Seleciona story bank mais relevante para o contexto
        
        Args:
            context: Contexto da conversa
            
        Returns:
            Dict com história específica ou None
        """
        if not self.story_banks:
            return None
        
        # Simples keyword matching - pode ser melhorado com ML
        context_lower = context.lower()
        
        for story_key, story_data in self.story_banks.items():
            # Check if context relates to this story
            story_keywords = story_data.get("keywords", "").lower()
            if any(keyword in context_lower for keyword in story_keywords.split(",")):
                return story_data
        
        # Return first story as fallback
        return list(self.story_banks.values())[0] if self.story_banks else None
    
    def select_callback(self, response_length: int) -> Optional[str]:
        """
        Seleciona callback icônico apropriado para o tamanho da resposta
        
        Args:
            response_length: Tamanho estimado da resposta em caracteres
            
        Returns:
            str: Callback icônico ou None
        """
        if not self.iconic_callbacks:
            return None
        
        # Respostas curtas: sem callback ou callback curto
        if response_length < 500:
            return None
        
        # Respostas médias: 1 callback
        elif response_length < 1500:
            return self.iconic_callbacks[0] if self.iconic_callbacks else None
        
        # Respostas longas: callback mais elaborado
        else:
            # Escolher callback aleatório mas determinístico
            idx = (response_length // 500) % len(self.iconic_callbacks)
            return self.iconic_callbacks[idx]
    
    def format_framework_response(
        self, 
        framework_name: str, 
        framework_result: Dict[str, Any]
    ) -> str:
        """
        Formata resposta de framework de forma eloquente
        
        Args:
            framework_name: Nome do framework aplicado
            framework_result: Resultado da aplicação do framework
            
        Returns:
            str: Resposta formatada em markdown
        """
        response = f"## Aplicando o Framework **{framework_name}**\n\n"
        
        # Explicar framework brevemente
        if "description" in framework_result:
            response += f"{framework_result['description']}\n\n"
        
        # Aplicar ao contexto
        response += "### Análise:\n\n"
        
        for key, value in framework_result.items():
            if key not in ["description", "callback", "story"]:
                response += f"**{key}**: {value}\n\n"
        
        # Adicionar story se disponível
        if "story" in framework_result:
            story = framework_result["story"]
            response += f"### Caso Real:\n\n"
            response += f"**{story.get('company', 'Empresa')}** ({story.get('year', 'ano')}): "
            response += f"{story.get('context', '')} "
            response += f"Resultado: {story.get('before', '')} → {story.get('after', '')} "
            response += f"({story.get('growth', '')})\n\n"
        
        # Adicionar callback
        if "callback" in framework_result:
            response += f"---\n\n{framework_result['callback']}\n"
        
        return response
    
    def should_refuse(self, user_input: str) -> Optional[str]:
        """
        Verifica se deve recusar a pergunta (fora da expertise)
        
        Returns:
            str: Mensagem de recusa com redirecionamento, ou None se deve responder
        """
        # Implementação básica - cada clone pode override
        return None
    
    def add_to_conversation_history(self, role: str, content: str):
        """Adiciona mensagem ao histórico da conversa"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    def get_conversation_context(self, max_messages: int = 10) -> str:
        """
        Gera contexto das últimas mensagens
        
        Args:
            max_messages: Número máximo de mensagens a incluir
            
        Returns:
            str: Contexto formatado do histórico
        """
        if not self.conversation_history:
            return ""
        
        recent_history = self.conversation_history[-max_messages:]
        
        context = "## CONTEXTO DA CONVERSA\n\n"
        for msg in recent_history:
            role = "👤 Usuário" if msg["role"] == "user" else f"🎯 {self.name}"
            context += f"{role}: {msg['content'][:200]}...\n\n"
        
        return context
    
    # ========================================================================
    # MÉTODOS HELPER COMPARTILHADOS
    # ========================================================================
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai keywords principais do texto"""
        # Remove pontuação e converte para lowercase
        cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
        words = cleaned.split()
        
        # Remove stop words comuns
        stop_words = {'o', 'a', 'de', 'da', 'do', 'em', 'para', 'com', 'que', 'e', 'é'}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        return keywords
    
    def _calculate_response_length(self, complexity: str) -> int:
        """Estima tamanho ideal de resposta baseado na complexidade"""
        complexity_map = {
            "simple": 300,
            "medium": 800,
            "complex": 1500,
            "deep": 2500
        }
        return complexity_map.get(complexity, 800)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', mode={self.current_mode})"

