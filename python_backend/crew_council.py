import os
import json
import asyncio
import re
from typing import Dict, List, Optional, Any, Union
from datetime import datetime as dt
from uuid import uuid4

from fastapi import HTTPException
from python_backend.prompts.template_master import (
    DEFAULT_PT_BR,
    DEFAULT_FRAMEWORK_NAMING,
    DEFAULT_SIGNATURE_PATTERN,
    DEFAULT_REFUSAL_PROTOCOL,
    DEFAULT_CONVERSATIONAL_GUIDELINES,
    _build_conversational_guidelines,
    _get_conversational_fewshots,
)
from anthropic import AsyncAnthropic
import httpx

from python_backend.models import Expert, BusinessProfile, CouncilAnalysis, AgentContribution
from python_backend.storage import storage


class CouncilOrchestrator:
    """
    Orchestrates the council of marketing experts to analyze problems
    """
    
    def __init__(self):
        """Initialize the council orchestrator with API clients"""
        self.anthropic_client = AsyncAnthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        # Limit concurrent API calls to avoid rate limiting (reduced to 1 for rate limit safety)
        self.semaphore = asyncio.Semaphore(1)
        # Add delay between calls to stay within rate limits
        self.call_delay = 2.0  # seconds between calls
        # Memória leve de preferências por sessão (user_id -> dict)
        # Não persiste, apenas durante a execução do processo
        self._session_preferences: Dict[str, Dict[str, Any]] = {}
    
    async def analyze_problem(
        self,
        user_id: str,
        problem: str,
        experts: List[Expert],
        research_findings: Optional[str] = None,
        profile: Optional[BusinessProfile] = None,
        citations: Optional[List[Dict[str, str]]] = None
    ) -> CouncilAnalysis:
        """
        Analyze a marketing problem with the council of experts
        
        Args:
            user_id: The user requesting the analysis
            problem: The marketing problem or question to analyze
            experts: List of experts to include in the council
            research_findings: Optional market research data
            profile: Optional business profile for context
            citations: Optional list of citations to include
            
        Returns:
            CouncilAnalysis with expert contributions and consensus
        """
        if not experts or len(experts) < 1:
            raise HTTPException(status_code=400, detail="At least one expert is required")
        
        if not problem or len(problem.strip()) < 10:
            raise HTTPException(status_code=400, detail="Problem description is too short")
        
        # Load persistent user preferences and merge with session preferences
        persistent_prefs = await self._load_user_preferences(user_id)
        if persistent_prefs:
            # Merge com preferências da sessão (sessão tem prioridade se conflitar)
            if user_id not in self._session_preferences:
                self._session_preferences[user_id] = {}
            self._session_preferences[user_id] = {**persistent_prefs, **self._session_preferences[user_id]}
        
        # Extrair preferências implícitas da mensagem e atualizar
        detected_prefs = self._extract_preferences_from_message(problem)
        if detected_prefs:
            self._update_user_preferences(user_id, detected_prefs)
            
        # Create unique ID for this analysis
        analysis_id = str(uuid4())
        
        # Step 1: Get individual expert analyses in parallel
        tasks = []
        for expert in experts:
            task = self._get_expert_analysis(
                expert=expert,
                problem=problem,
                research_findings=research_findings,
                profile=profile,
                user_id=user_id
            )
            tasks.append(task)
            
        # Wait for all expert analyses to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Step 2: Filter out any failed analyses
        valid_contributions = []
        for i, contrib in enumerate(results):
            if isinstance(contrib, Exception):
                print(f"⚠️ Expert {experts[i].name} analysis failed: {str(contrib)}")
            else:
                valid_contributions.append(contrib)
        
        if not valid_contributions:
            raise Exception("All expert analyses failed - unable to generate council analysis")
        
        contributions = valid_contributions
        
        # Step 3: Synthesize consensus from all contributions
        # Add delay before synthesis to avoid rate limits
        await asyncio.sleep(self.call_delay)
        consensus = await self._synthesize_consensus(
            problem=problem,
            contributions=contributions,
            research_findings=research_findings
        )
        
        # Build final analysis
        analysis = CouncilAnalysis(
            id=analysis_id,
            userId=user_id,
            problem=problem,
            profileId=profile.id if profile else None,
            marketResearch=research_findings,
            contributions=contributions,
            consensus=consensus,
            citations=citations or []
        )
        
        return analysis
    
    def _build_error_contribution(
        self,
        expert: Expert,
        error_type: str,
        error_detail: str,
        attempted_action: str = "obter análise",
        fallback_action: str = "tente novamente em alguns minutos"
    ) -> AgentContribution:
        """
        Constrói uma contribuição padronizada de erro/recuperação seguindo o padrão:
        "Não consegui X por Y; tentei Z; proponho W"
        
        Args:
            expert: O expert que falhou
            error_type: Tipo do erro (timeout, api_error, parse_error, etc)
            error_detail: Detalhe específico do erro
            attempted_action: O que foi tentado fazer
            fallback_action: Ação alternativa proposta
        """
        error_messages = {
            "timeout": f"Não consegui {attempted_action} de {expert.name} porque a requisição excedeu o tempo limite (60s).",
            "api_error": f"Não consegui {attempted_action} de {expert.name} devido a um erro na API: {error_detail}.",
            "parse_error": f"Não consegui processar a resposta de {expert.name} corretamente: {error_detail}.",
            "network_error": f"Não consegui {attempted_action} de {expert.name} devido a problema de rede: {error_detail}.",
            "rate_limit": f"Não consegui {attempted_action} de {expert.name} porque atingimos o limite de requisições.",
            "unknown": f"Não consegui {attempted_action} de {expert.name} devido a um erro inesperado: {error_detail}.",
        }
        
        base_message = error_messages.get(error_type, error_messages["unknown"])
        
        # Adicionar tentativas realizadas
        attempted = "Tentei novamente com retry automático (3 tentativas com backoff exponencial)."
        if error_type == "timeout":
            attempted = "Tentei aguardar até 60 segundos pela resposta."
        elif error_type == "rate_limit":
            attempted = "Tentei aguardar o período de rate limit antes de retentar."
        
        # Proposta de ação alternativa
        proposal = f"Proponho: {fallback_action}. Se o problema persistir, você pode tentar com menos experts ou aguardar alguns minutos."
        
        full_message = f"{base_message} {attempted} {proposal}"
        
        return AgentContribution(
            expertId=expert.id,
            expertName=expert.name,
            analysis=full_message,
            keyInsights=[f"Análise não disponível: {error_type}"],
            recommendations=[fallback_action]
        )

    async def _get_expert_analysis(
        self,
        expert: Expert,
        problem: str,
        research_findings: Optional[str],
        profile: Optional[BusinessProfile],
        user_id: Optional[str] = None
    ) -> AgentContribution:
        """
        Get analysis from a single expert using their cognitive clone.
        Uses semaphore to limit concurrent API calls and prevent rate limiting.
        
        Args:
            expert: Expert to analyze
            problem: Problem/question to analyze
            research_findings: Optional market research
            profile: Optional business profile
            user_id: Optional user ID for session preferences
        
        Returns:
            AgentContribution with expert's unique perspective
        """
        async with self.semaphore:
            # Add delay before each API call to avoid rate limits
            await asyncio.sleep(self.call_delay)
            
            # Extrair preferências implícitas da mensagem se user_id disponível
            if user_id:
                detected_prefs = self._extract_preferences_from_message(problem)
                if detected_prefs:
                    self._update_user_preferences(user_id, detected_prefs)
            
            try:
                # Build context-rich prompt
                context_parts = []
                
                # Add business context if available
                if profile:
                    context_parts.append(
                        f"**Business Context:**\n"
                        f"- Company: {profile.companyName} ({profile.companySize} employees)\n"
                        f"- Industry: {profile.industry}\n"
                        f"- Target Audience: {profile.targetAudience}\n"
                        f"- Products: {profile.mainProducts}\n"
                        f"- Channels: {', '.join(profile.channels)}\n"
                        f"- Budget: {profile.budgetRange}\n"
                        f"- Primary Goal: {profile.primaryGoal}\n"
                        f"- Main Challenge: {profile.mainChallenge}\n"
                        f"- Timeline: {profile.timeline}\n"
                    )
                
                # Add market research if available
                if research_findings:
                    context_parts.append(
                        f"**Market Research & Intelligence:**\n{research_findings}\n"
                    )
                
                # Build final user message
                context = "\n\n".join(context_parts) if context_parts else ""
                
                user_message = f"""{context}

**Problema/Questão:**
{problem}

**Sua Tarefa:**
Como {expert.name}, forneça sua análise especializada para este problema. Estruture sua resposta da seguinte forma:

1.  **Análise Principal (Core Analysis)**: Sua perspectiva única sobre o problema (2-3 parágrafos).
2.  **Principais Insights (Key Insights)**: 3-5 insights críticos em formato de lista (bullet points).
3.  **Recomendações Acionáveis (Actionable Recommendations)**: 3-5 recomendações táticas e específicas em formato de lista (bullet points).

Utilize seus frameworks, metodologias e filosofias de assinatura. Seja autêntico aos seus padrões cognitivos e estilo de comunicação. Responda sempre em português do Brasil (pt-BR)."""
                
                # Call Claude with expert's system prompt (with timeout)
                retry_count = 0
                max_retries = 3
                backoff_factor = 1.5
                response = None
                
                try:
                    # Augment system prompt with safety/structure if missing
                    system_prompt = self._augment_system_prompt(expert.systemPrompt, expert.name, user_id=user_id)

                    while retry_count <= max_retries:
                        try:
                            response = await asyncio.wait_for(
                                self.anthropic_client.messages.create(
                                    model="claude-3-haiku-20240307",
                                    max_tokens=3000,
                                    system=system_prompt,
                                    messages=[{
                                        "role": "user",
                                        "content": user_message
                                    }]
                                ),
                                timeout=60.0  # 60 second timeout per expert
                            )
                            break  # Success, exit retry loop
                        except Exception as retry_error:
                            retry_count += 1
                            if retry_count > max_retries:
                                print(f"[CouncilOrchestrator] Max retries ({max_retries}) reached for {expert.name}. Giving up.")
                                raise  # Re-raise the last exception
                            
                            wait_time = backoff_factor ** retry_count
                            print(f"[CouncilOrchestrator] Retry {retry_count}/{max_retries} for {expert.name} after error: {str(retry_error)}. Waiting {wait_time:.1f}s")
                            await asyncio.sleep(wait_time)
                    
                    # Extract text response (handle TextBlock type)
                    response_text = ""
                    for block in response.content:
                        if block.type == "text":
                            response_text = block.text  # type: ignore
                            break
                    
                    # Parse structured response with robust parser
                    insights = self._extract_bullet_points(response_text, "Principais Insights")
                    recommendations = self._extract_bullet_points(response_text, "Recomendações Acionáveis")
                    
                    return AgentContribution(
                        expertId=expert.id,
                        expertName=expert.name,
                        analysis=response_text,
                        keyInsights=insights,
                        recommendations=recommendations
                    )
                except asyncio.TimeoutError:
                    print(f"[CouncilOrchestrator] {expert.name} analysis timed out after 60 seconds")
                    return self._build_error_contribution(
                        expert=expert,
                        error_type="timeout",
                        error_detail="60 segundos",
                        attempted_action="obter análise",
                        fallback_action="tente novamente em alguns minutos ou reduza o número de experts"
                    )
                except Exception as e:
                    error_str = str(e)
                    # Identificar tipo de erro baseado na mensagem
                    error_type = "unknown"
                    if "timeout" in error_str.lower():
                        error_type = "timeout"
                    elif "rate" in error_str.lower() or "limit" in error_str.lower():
                        error_type = "rate_limit"
                    elif "network" in error_str.lower() or "connection" in error_str.lower():
                        error_type = "network_error"
                    elif "api" in error_str.lower() or "anthropic" in error_str.lower():
                        error_type = "api_error"
                    
                    print(f"[CouncilOrchestrator] {expert.name} analysis failed: {error_str}")
                    return self._build_error_contribution(
                        expert=expert,
                        error_type=error_type,
                        error_detail=error_str[:200],  # Limitar tamanho
                        attempted_action="obter análise",
                        fallback_action="tente novamente em alguns minutos"
                    )
            except Exception as e:
                print(f"[CouncilOrchestrator] Unexpected error in _get_expert_analysis: {str(e)}")
                raise

    def _extract_bullet_points(self, text: str, section_title: str) -> List[str]:
        """
        Extracts bullet points from a specific section of the AI's response.
        This new version is more robust against formatting variations.
        """
        try:
            # Define the known sections in order to find boundaries
            section_titles_map = {
                "Análise Principal": "Core Analysis",
                "Principais Insights": "Key Insights",
                "Recomendações Acionáveis": "Actionable Recommendations",
            }
            section_titles = list(section_titles_map.keys())
            
            # Create a regex pattern that matches either the Portuguese or English title
            title_pt = section_title
            title_en = section_titles_map.get(title_pt, title_pt) # Fallback to pt title if not found
            # Escape titles for regex and create a pattern to match either
            pattern_str = f"({re.escape(title_pt)}|{re.escape(title_en)})"

            # Find the starting position of the target section
            start_regex = re.compile(rf'(\d+\.\s*)?(\*\*)?{pattern_str}(\*\*)?:?', re.IGNORECASE)
            start_match = start_regex.search(text)
            
            if not start_match:
                # This is a fallback message if the section title itself isn't in the response.
                return [f"A seção '{section_title}' não foi encontrada na resposta do especialista."]

            start_index = start_match.end()

            # Determine the end boundary by finding the start of the NEXT section
            end_index = len(text)
            
            current_title_index = -1
            for i, title in enumerate(section_titles):
                if title.lower() in section_title.lower():
                    current_title_index = i
                    break

            if current_title_index != -1 and current_title_index < len(section_titles) - 1:
                next_section_title_pt = section_titles[current_title_index + 1]
                next_section_title_en = section_titles_map.get(next_section_title_pt, next_section_title_pt)
                next_pattern_str = f"({re.escape(next_section_title_pt)}|{re.escape(next_section_title_en)})"
                
                end_regex = re.compile(rf'(\d+\.\s*)?(\*\*)?{next_pattern_str}(\*\*)?:?', re.IGNORECASE)
                end_match = end_regex.search(text, start_index)
                if end_match:
                    end_index = end_match.start()
            
            # Extract the content of the relevant section
            section_text = text[start_index:end_index].strip()

            # Extract bullet points from the section text using a more reliable multiline pattern
            bullets = re.findall(r"^\s*(?:[-•*]|\d+\.)\s+(.*)", section_text, re.MULTILINE)
            
            cleaned_bullets = [b.strip().replace('**', '') for b in bullets if b.strip()]

            # If no bullets were found, fallback to splitting by lines, which is less precise but better than nothing.
            if not cleaned_bullets:
                lines = section_text.split('\n')
                # Filter out empty lines and potential sub-headings
                cleaned_bullets = [line.strip() for line in lines if line.strip() and not line.strip().endswith(':')]

            if not cleaned_bullets:
                # This message now accurately reflects that we found the section but it had no extractable points.
                return ["Não foi possível extrair os pontos principais desta seção."]
                
            return cleaned_bullets
        except Exception as e:
            print(f"Erro ao extrair pontos da seção '{section_title}': {str(e)}")
            return ["Ocorreu um erro interno ao processar a resposta do especialista."]

    async def _synthesize_consensus(
        self,
        problem: str,
        contributions: List[AgentContribution],
        research_findings: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesize a consensus view from all expert contributions
        """
        try:
            # Build context for synthesis
            expert_insights = []
            expert_recommendations = []
            
            for contrib in contributions:
                # Add each expert's insights
                expert_insights.append(f"**{contrib.expertName}**:")
                for insight in contrib.keyInsights:
                    expert_insights.append(f"- {insight}")
                expert_insights.append("")  # blank line
                
                # Add each expert's recommendations
                expert_recommendations.append(f"**{contrib.expertName}**:")
                for rec in contrib.recommendations:
                    expert_recommendations.append(f"- {rec}")
                expert_recommendations.append("")  # blank line
            
            # Build synthesis prompt
            system_prompt = """Você é um estrategista de marketing habilidoso que sintetiza insights de múltiplos especialistas.
Sua função é identificar padrões, encontrar consensos e destacar perspectivas únicas entre as contribuições dos especialistas.
Apresente uma visão equilibrada e abrangente que represente a inteligência coletiva do conselho de marketing.
Seja objetivo, claro e acionável em sua síntese. Responda SEMPRE em português do Brasil (pt-BR)."""

            user_message = f"""**Problema de Marketing/Questão:**
{problem}

**Insights dos Especialistas:**
{chr(10).join(expert_insights)}

**Recomendações dos Especialistas:**
{chr(10).join(expert_recommendations)}

**Sua Tarefa:**
Sintetize essas perspectivas de especialistas em uma visão de consenso coesa e bem estruturada. O resultado deve ser um relatório de texto completo.

O relatório deve incluir:
1.  **Síntese Geral:** Um resumo conciso da perspectiva geral (2-3 parágrafos).
2.  **Insights-Chave do Consenso:** 5 principais insights que representam áreas de concordância.
3.  **Recomendações Prioritárias:** 5 recomendações acionáveis e priorizadas.
4.  **Perspectivas Divergentes:** 1-2 áreas onde os especialistas ofereceram abordagens diferentes (se houver).
5.  **Próximos Passos (15 min):** Ação imediata que pode ser executada nos próximos 15 minutos.
6.  **Risco Principal:** 1 risco principal a observar durante a implementação.
7.  **Pergunta de Avanço:** Encerre com 1 pergunta socrática ou operacional que ajude o usuário a avançar no problema.

**Instruções Importantes:**
- Escreva toda a resposta em português do Brasil (pt-BR).
- Use formatação Markdown (negrito, listas) para clareza.
- Seja prático, específico e acionável.
- O resultado deve ser um relatório de texto contínuo, não um objeto JSON.
- A pergunta final deve ser natural e ajudar o usuário a pensar no próximo passo ou aprofundar o entendimento."""

            # Call Claude for synthesis
            try:
                response = await asyncio.wait_for(
                    self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=4000,
                        system=system_prompt,
                        messages=[{
                            "role": "user",
                            "content": user_message
                        }]
                    ),
                    timeout=60.0
                )
                
                # Extract text response
                response_text = ""
                for block in response.content:
                    if block.type == "text":
                        response_text = block.text  # type: ignore
                        break
                
                # A SOLUÇÃO: Retornar o texto completo da síntese como a string de consenso.
                # O modelo Pydantic espera uma string, não um dicionário.
                return response_text

            except asyncio.TimeoutError:
                print("[CouncilOrchestrator] Consensus synthesis timed out")
                return """**Não consegui sintetizar o consenso** porque a requisição excedeu o tempo limite (60s).

**Tentei:** Aguardar até 60 segundos pela resposta de síntese.

**Proponho:** Tente novamente em alguns minutos ou reduza o número de experts consultados. Se o problema persistir, você pode analisar as contribuições individuais dos experts que foram obtidas com sucesso."""
            except Exception as e:
                error_str = str(e)
                error_type = "síntese do conselho"
                if "timeout" in error_str.lower():
                    error_type = "síntese do conselho devido a timeout"
                elif "rate" in error_str.lower() or "limit" in error_str.lower():
                    error_type = "síntese do conselho devido a limite de requisições"
                
                print(f"[CouncilOrchestrator] Consensus synthesis failed: {error_str}")
                return f"""**Não consegui realizar a {error_type}** devido a um erro: {error_str[:200]}.

**Tentei:** Processar as contribuições dos experts e gerar síntese coesa.

**Proponho:** Tente novamente em alguns minutos. Se o problema persistir, você pode analisar as contribuições individuais dos experts que foram obtidas com sucesso."""
        except Exception as e:
            print(f"[CouncilOrchestrator] Unexpected error in _synthesize_consensus: {str(e)}")
            return f"""**Erro inesperado ao sintetizar o conselho:** {str(e)}.

**Tentei:** Processar todas as contribuições e gerar síntese.

**Proponho:** Tente novamente. Se o problema persistir, entre em contato com o suporte."""

    def _get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Retorna preferências do usuário para a sessão atual.
        Tenta carregar do storage persistente primeiro, depois cai para sessão em memória.
        
        Preferências guardadas:
        - style_preference: "objetivo" | "detalhado"
        - focus_preference: "ROI-first" | "brand-first"
        - tone_preference: "prático" | "estratégico"
        - communication_preference: "bullets" | "blocos"
        - conversation_style: "coach" | "consultor" | "direto"
        """
        # Retorna preferências da sessão em memória (fallback rápido)
        return self._session_preferences.get(user_id, {})
    
    async def _load_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Carrega preferências persistentes do storage.
        Retorna dicionário vazio se não houver preferências salvas.
        """
        try:
            preferences = await storage.get_user_preferences(user_id)
            if preferences:
                # Converter UserPreferences para dict
                prefs_dict = {
                    "style_preference": preferences.style_preference,
                    "focus_preference": preferences.focus_preference,
                    "tone_preference": preferences.tone_preference,
                    "communication_preference": preferences.communication_preference,
                    "conversation_style": preferences.conversation_style,
                }
                # Remover None values
                return {k: v for k, v in prefs_dict.items() if v is not None}
        except Exception as e:
            print(f"[CouncilOrchestrator] Warning: Could not load user preferences: {e}")
        return {}
    
    def _update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        """
        Atualiza preferências do usuário na sessão atual.
        Não persiste - apenas durante a execução do processo.
        """
        if user_id not in self._session_preferences:
            self._session_preferences[user_id] = {}
        self._session_preferences[user_id].update(preferences)
    
    def _extract_preferences_from_message(self, message: str) -> Dict[str, Any]:
        """
        Tenta extrair preferências implícitas da mensagem do usuário.
        Retorna dicionário de preferências detectadas.
        """
        preferences = {}
        message_lower = message.lower()
        
        # Detectar preferência de estilo
        if any(word in message_lower for word in ["direto", "objetivo", "resumo", "resumido"]):
            preferences["style_preference"] = "objetivo"
        elif any(word in message_lower for word in ["detalhado", "completo", "explicação completa"]):
            preferences["style_preference"] = "detalhado"
        
        # Detectar preferência de foco
        if any(word in message_lower for word in ["roi", "conversão", "vendas", "resultado", "métricas"]):
            preferences["focus_preference"] = "ROI-first"
        elif any(word in message_lower for word in ["marca", "brand", "reputação", "posicionamento"]):
            preferences["focus_preference"] = "brand-first"
        
        # Detectar preferência de tom
        if any(word in message_lower for word in ["prático", "ação", "implementar", "como fazer"]):
            preferences["tone_preference"] = "prático"
        elif any(word in message_lower for word in ["estratégico", "visão", "planejamento", "longo prazo"]):
            preferences["tone_preference"] = "estratégico"
        
        return preferences

    def _augment_system_prompt(self, system_prompt: str, expert_name: str, user_id: Optional[str] = None) -> str:
        """
        Garante PT-BR e adiciona protocolos operacionais ao prompt de sistema do especialista,
        sem sobrescrever o conteúdo original.
        Inclui Conversational Guidelines se CONVERSATION_MODE estiver ativado.
        Usa preferências da sessão do usuário se disponíveis.
        """
        blocks: List[str] = []
        base = system_prompt or ""
        blocks.append(base)

        normalized = base.lower()
        if "portugu" not in normalized:
            blocks.append("\n\n" + DEFAULT_PT_BR)
        if "framework naming protocol" not in normalized:
            blocks.append("\n\n" + DEFAULT_FRAMEWORK_NAMING)
        if "signature response pattern" not in normalized:
            blocks.append("\n\n" + DEFAULT_SIGNATURE_PATTERN)
        if "protocolo de recusa" not in normalized and "refusal" not in normalized:
            blocks.append("\n\n" + DEFAULT_REFUSAL_PROTOCOL)

        # Conversational Guidelines (toggleável por env)
        conversation_mode = os.getenv("CONVERSATION_MODE", "on").lower() == "on"
        conversation_style = os.getenv("CONVERSATION_STYLE", "consultor").lower()
        
        if conversation_mode and "conversational guidelines" not in normalized and "diretrizes conversacionais" not in normalized:
            # Validar estilo válido
            valid_styles = ["coach", "consultor", "direto"]
            if conversation_style not in valid_styles:
                conversation_style = "consultor"
            
            # Ajustar estilo baseado em preferências do usuário se disponível
            if user_id:
                user_prefs = self._get_user_preferences(user_id)
                if user_prefs.get("tone_preference") == "prático":
                    conversation_style = "direto"
                elif user_prefs.get("tone_preference") == "estratégico":
                    conversation_style = "coach"
            
            guidelines = _build_conversational_guidelines(conversation_style)
            blocks.append("\n\n" + guidelines)
            
            # Adicionar few-shots conversacionais se disponíveis
            fewshots = _get_conversational_fewshots(expert_name, max_examples=2)
            if fewshots:
                blocks.append("\n\n" + fewshots)
            
            # Adicionar preferências detectadas do usuário como contexto
            if user_id:
                user_prefs = self._get_user_preferences(user_id)
                if user_prefs:
                    pref_lines = []
                    if "style_preference" in user_prefs:
                        pref_lines.append(f"- Estilo preferido: {user_prefs['style_preference']}")
                    if "focus_preference" in user_prefs:
                        pref_lines.append(f"- Foco preferido: {user_prefs['focus_preference']}")
                    if "tone_preference" in user_prefs:
                        pref_lines.append(f"- Tom preferido: {user_prefs['tone_preference']}")
                    
                    if pref_lines:
                        blocks.append("\n\n## Preferências Detectadas do Usuário")
                        blocks.append("\n".join(pref_lines))
                        blocks.append("\nAdapte sua resposta considerando essas preferências quando possível.")

        # Hint de tom conciso e acionável
        blocks.append(
            "\n\n## Diretiva de Tom\nSeja conciso, estruturado e acionável. Mantenha o estilo cognitivo de "
            f"{expert_name} sem linguagem abusiva."
        )

        return "".join(blocks)

# Create a singleton instance
council_orchestrator = CouncilOrchestrator()