import os
import json
import asyncio
import re
from typing import Dict, List, Optional, Any, Union
from datetime import datetime as dt
from uuid import uuid4

from fastapi import HTTPException
from dotenv import load_dotenv, find_dotenv
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

from python_backend.models import Expert, CouncilAnalysis, ExpertContribution, Persona, ActionPlan, Phase, Action
from python_backend.storage import storage

# Carregar .env quando o módulo é importado
_env_file = find_dotenv(usecwd=True)
if _env_file:
    load_dotenv(_env_file, override=True)

class CouncilOrchestrator:
    """
    Orchestrates the council of marketing experts to analyze problems
    """
    
    def __init__(self):
        """Initialize the council orchestrator with API clients"""
        # Garantir que .env está carregado
        _env_file = find_dotenv(usecwd=True)
        if _env_file:
            load_dotenv(_env_file, override=True)
        
        anthropic_key = os.getenv("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            print("[CouncilOrchestrator] ⚠️  ANTHROPIC_API_KEY não encontrada. Council analysis será desabilitado.")
            print("[CouncilOrchestrator] Para habilitar, adicione ANTHROPIC_API_KEY=sk-ant-... no arquivo .env")
            self.anthropic_client = None
        else:
            self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)
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
        profile: Optional[dict] = None,
        persona: Optional[Persona] = None,
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
        
        if not self.anthropic_client:
            raise HTTPException(
                status_code=503,
                detail="Serviço de análise de conselho indisponível. Configure ANTHROPIC_API_KEY no arquivo .env"
            )
        
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
                persona=persona,
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
            research_findings=research_findings,
            persona=persona
        )
        
        # Step 4: Generate action plan based on consensus and persona
        action_plan = None
        try:
            await asyncio.sleep(self.call_delay)
            action_plan = await self._generate_action_plan(
                problem=problem,
                consensus=consensus,
                contributions=contributions,
                persona=persona,
                profile=profile
            )
        except Exception as e:
            print(f"[CouncilOrchestrator] Erro ao gerar plano de ação: {e}")
            import traceback
            traceback.print_exc()
            # Continue without action plan - não é crítico
        
        # Build final analysis
        analysis = CouncilAnalysis(
            id=analysis_id,
            userId=user_id,
            problem=problem,
            personaId=persona.id if persona else None,
            profileId=profile.id if profile else None,
            marketResearch=research_findings,
            contributions=contributions,
            consensus=consensus,
            actionPlan=action_plan,
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
    ) -> ExpertContribution:
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
        
        return ExpertContribution(
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
        profile: Optional[dict],
        persona: Optional[Persona] = None,
        user_id: Optional[str] = None
    ) -> ExpertContribution:
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
            ExpertContribution with expert's unique perspective
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
                
                # Add persona context if available (CRÍTICO para personalização)
                if persona:
                    persona_context = f"""**CLIENTE IDEAL - PERSONA:**
- Nome: {persona.name}
- Demográficos: {json.dumps(persona.demographics, ensure_ascii=False, indent=2) if isinstance(persona.demographics, dict) else persona.demographics}
- Objetivos: {', '.join(persona.goals[:5]) if persona.goals else 'Não especificados'}
- Pain Points (Dores): {', '.join(persona.painPoints[:5]) if persona.painPoints else 'Não especificados'}
- Valores: {', '.join(persona.values[:5]) if persona.values else 'Não especificados'}
- Preferências de Conteúdo: {json.dumps(persona.contentPreferences, ensure_ascii=False, indent=2) if isinstance(persona.contentPreferences, dict) else persona.contentPreferences}
- Comportamentos: {json.dumps(persona.behavioralPatterns, ensure_ascii=False, indent=2) if isinstance(persona.behavioralPatterns, dict) else persona.behavioralPatterns}

**INSTRUÇÃO CRÍTICA:** Todas as suas recomendações DEVE ser específicas para este perfil de cliente ideal. 
Ajuste linguagem, canais, estratégias e táticas para ressoar com esta persona específica.
Considere os pain points e objetivos desta persona em cada recomendação.

"""
                    context_parts.append(persona_context)
                
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
Como {expert.name}, forneça sua análise especializada para este problema. Estruture sua resposta EXATAMENTE da seguinte forma:

## Análise Principal

[Sua perspectiva única sobre o problema em 2-3 parágrafos. Seja específico e use seus frameworks característicos.]

## Principais Insights

- [Insight 1: Deve ser específico, acionável e relacionado ao problema]
- [Insight 2: Aplique sua metodologia única]
- [Insight 3: Conecte ao contexto do negócio]
- [Insight 4: Seja prático e direto]
- [Insight 5: Use sua terminologia característica]

## Recomendações Acionáveis

- [Recomendação 1: Específica, mensurável e com prazo claro]
- [Recomendação 2: Baseada em seus frameworks proprietários]
- [Recomendação 3: Priorizada por impacto]
- [Recomendação 4: Conectada aos objetivos do negócio]
- [Recomendação 5: Acionável imediatamente]

**INSTRUÇÕES CRÍTICAS:**
- Use EXATAMENTE os títulos acima: "## Análise Principal", "## Principais Insights", "## Recomendações Acionáveis"
- Cada seção de insights e recomendações DEVE ter pelo menos 3 itens e preferencialmente 5
- Use bullet points com "-" (hífen) para listas
- Seja autêntico ao seu estilo cognitivo e use seus frameworks característicos
- Responda SEMPRE em português do Brasil (pt-BR)
- Seja específico, não genérico"""
                
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
                    
                    return ExpertContribution(
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
        Improved version with better pattern matching.
        """
        try:
            # Normalize text - remove extra whitespace
            text = re.sub(r'\n{3,}', '\n\n', text)
            
            # Define the known sections in order
            section_titles_map = {
                "Análise Principal": ["Análise Principal", "Core Analysis", "## Análise Principal"],
                "Principais Insights": ["Principais Insights", "Key Insights", "## Principais Insights"],
                "Recomendações Acionáveis": ["Recomendações Acionáveis", "Actionable Recommendations", "## Recomendações Acionáveis"],
            }
            section_titles = list(section_titles_map.keys())
            
            # Get all possible title variations for the target section
            target_variations = section_titles_map.get(section_title, [section_title])
            target_variations.extend([f"## {st}" for st in target_variations])
            target_variations.extend([f"**{st}**" for st in target_variations])
            target_variations.extend([f"### {st}" for st in target_variations])
            
            # Find the starting position - try multiple patterns
            start_index = None
            for variation in target_variations:
                # Try markdown header pattern (## or ###)
                pattern1 = re.compile(rf'##+\s*{re.escape(variation.replace("## ", "").replace("### ", ""))}\s*:?\s*\n', re.IGNORECASE)
                match = pattern1.search(text)
                if match:
                    start_index = match.end()
                    break
                
                # Try numbered or bold pattern
                pattern2 = re.compile(rf'(?:^\d+\.\s*)?(\*\*)?{re.escape(variation.replace("## ", "").replace("### ", "").replace("**", ""))}(\*\*)?:?\s*\n', re.IGNORECASE | re.MULTILINE)
                match = pattern2.search(text)
                if match:
                    start_index = match.end()
                    break
            
            if start_index is None:
                print(f"[CouncilOrchestrator] Seção '{section_title}' não encontrada. Tentando busca mais ampla...")
                # Fallback: busca mais ampla
                for variation in target_variations:
                    clean_variation = variation.replace("## ", "").replace("### ", "").replace("**", "")
                    if clean_variation.lower() in text.lower():
                        # Find position after this title
                        idx = text.lower().find(clean_variation.lower())
                        if idx != -1:
                            start_index = idx + len(clean_variation)
                            # Move past any colon, newline, etc.
                            while start_index < len(text) and text[start_index] in [':', '\n', ' ', '*']:
                                start_index += 1
                            break
                
                if start_index is None:
                    return [f"Seção '{section_title}' não foi encontrada na resposta do especialista."]

            # Determine the end boundary by finding the start of the NEXT section
            end_index = len(text)
            
            current_title_index = -1
            for i, title in enumerate(section_titles):
                if title == section_title:
                    current_title_index = i
                    break

            if current_title_index != -1 and current_title_index < len(section_titles) - 1:
                next_section_title = section_titles[current_title_index + 1]
                next_variations = section_titles_map.get(next_section_title, [next_section_title])
                next_variations.extend([f"## {st}" for st in next_variations])
                next_variations.extend([f"### {st}" for st in next_variations])
                
                for variation in next_variations:
                    pattern = re.compile(rf'##+\s*{re.escape(variation.replace("## ", "").replace("### ", ""))}\s*:?\s*\n', re.IGNORECASE)
                    match = pattern.search(text, start_index)
                    if match:
                        end_index = match.start()
                        break
            
            # Extract the content of the relevant section
            section_text = text[start_index:end_index].strip()

            # Extract bullet points - try multiple patterns
            bullets = []
            
            # Pattern 1: Standard bullet points (-, •, *)
            pattern1 = re.compile(r'^\s*[-•*]\s+(.+)$', re.MULTILINE)
            bullets.extend(pattern1.findall(section_text))
            
            # Pattern 2: Numbered list (1., 2., etc.)
            pattern2 = re.compile(r'^\s*\d+\.\s+(.+)$', re.MULTILINE)
            bullets.extend(pattern2.findall(section_text))
            
            # Pattern 3: Lines starting with whitespace (indented)
            lines = section_text.split('\n')
            for line in lines:
                stripped = line.strip()
                # Skip empty, headers, or very short lines
                if stripped and len(stripped) > 10 and not stripped.startswith('#'):
                    # If it looks like a bullet point but wasn't captured
                    if stripped.startswith('-') or stripped.startswith('•') or stripped.startswith('*'):
                        # Extract content after bullet
                        content = re.sub(r'^[-•*]\s*', '', stripped)
                        if content and content not in bullets:
                            bullets.append(content)
                    elif re.match(r'^\d+\.', stripped):
                        # Extract content after number
                        content = re.sub(r'^\d+\.\s*', '', stripped)
                        if content and content not in bullets:
                            bullets.append(content)
            
            # Clean bullets
            cleaned_bullets = []
            seen = set()
            for b in bullets:
                # Remove markdown formatting
                clean = re.sub(r'\*\*|__', '', b.strip())
                # Remove leading/trailing punctuation issues
                clean = re.sub(r'^[-•*\s]+', '', clean)
                clean = clean.strip()
                
                # Skip if too short, empty, or duplicate
                if clean and len(clean) > 5 and clean.lower() not in seen:
                    cleaned_bullets.append(clean)
                    seen.add(clean.lower())

            # Fallback: if no bullets found, try splitting by double newlines or numbered items
            if not cleaned_bullets:
                # Try to find paragraphs or numbered sections
                paragraphs = [p.strip() for p in section_text.split('\n\n') if p.strip() and len(p.strip()) > 20]
                if paragraphs:
                    cleaned_bullets = paragraphs[:5]  # Limit to 5
                else:
                    # Last resort: split by single newlines
                    lines = [l.strip() for l in section_text.split('\n') if l.strip() and len(l.strip()) > 15 and not l.strip().startswith('#')]
                    if lines:
                        cleaned_bullets = lines[:5]

            if not cleaned_bullets:
                return [f"Não foi possível extrair os pontos principais da seção '{section_title}'. A seção pode estar vazia ou em formato inesperado."]
                
            return cleaned_bullets
        except Exception as e:
            print(f"[CouncilOrchestrator] Erro ao extrair pontos da seção '{section_title}': {str(e)}")
            import traceback
            traceback.print_exc()
            return [f"Erro ao processar a resposta do especialista: {str(e)[:100]}"]

    async def _synthesize_consensus(
        self,
        problem: str,
        contributions: List[ExpertContribution],
        research_findings: Optional[str] = None,
        persona: Optional[Persona] = None
    ) -> str:
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

            # Build persona context if available
            persona_context = ""
            if persona:
                persona_context = f"""
**CLIENTE IDEAL - PERSONA (Contexto Crítico):**
- Nome: {persona.name}
- Objetivos: {', '.join(persona.goals[:5]) if persona.goals else 'Não especificados'}
- Pain Points: {', '.join(persona.painPoints[:5]) if persona.painPoints else 'Não especificados'}
- Valores: {', '.join(persona.values[:5]) if persona.values else 'Não especificados'}

**IMPORTANTE:** O consenso deve considerar especificamente este perfil de cliente ideal. 
Recomendações devem ser práticas e acionáveis para ressoar com esta persona.

"""
            
            user_message = f"""{persona_context}**Problema de Marketing/Questão:**
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

    async def _generate_action_plan(
        self,
        problem: str,
        consensus: str,
        contributions: List[ExpertContribution],
        persona: Optional[Persona] = None,
        profile: Optional[dict] = None
    ) -> Optional[ActionPlan]:
        """
        Gera plano de ação completo e estruturado baseado no consenso.
        Usa Claude para criar plano executável com fases, ações e métricas.
        """
        try:
            # Build persona context
            persona_context = ""
            if persona:
                persona_context = f"""
**CLIENTE IDEAL (PERSONA):**
- Nome: {persona.name}
- Objetivos: {', '.join(persona.goals[:5]) if persona.goals else 'Não especificados'}
- Pain Points: {', '.join(persona.painPoints[:5]) if persona.painPoints else 'Não especificados'}
- Valores: {', '.join(persona.values[:5]) if persona.values else 'Não especificados'}
- Comportamentos: {json.dumps(persona.behavioralPatterns, ensure_ascii=False, indent=2) if isinstance(persona.behavioralPatterns, dict) else 'Não especificados'}
"""
            
            # Build profile context
            profile_context = ""
            if profile:
                profile_context = f"""
**CONTEXTO DO NEGÓCIO:**
- Empresa: {profile.companyName}
- Indústria: {profile.industry}
- Objetivo Principal: {profile.primaryGoal}
- Desafio Principal: {profile.mainChallenge}
- Timeline: {profile.timeline}
- Budget: {profile.budgetRange}
"""
            
            # Build contributions summary
            contributions_summary = "\n".join([
                f"- **{c.expertName}**: {', '.join(c.recommendations[:3])}"
                for c in contributions[:5]
            ])
            
            prompt = f"""
Você é um consultor estratégico especializado em criar planos de ação executáveis e estruturados.

{persona_context}
{profile_context}

**PROBLEMA:**
{problem}

**CONSENSO DOS ESPECIALISTAS:**
{consensus}

**RECOMENDAÇÕES-CHAVE DOS ESPECIALISTAS:**
{contributions_summary}

**SUA TAREFA:**
Crie um PLANO DE AÇÃO COMPLETO e ESTRUTURADO em formato JSON seguindo EXATAMENTE este schema:

{{
  "phases": [
    {{
      "phaseNumber": 1,
      "name": "Nome da Fase",
      "duration": "X semanas",
      "objectives": ["objetivo 1", "objetivo 2"],
      "actions": [
        {{
          "id": "action-1-1",
          "title": "Título da Ação",
          "description": "Descrição detalhada da ação",
          "responsible": "Responsável (ex: Equipe de Marketing, CEO, Agência)",
          "priority": "alta",
          "estimatedTime": "X horas",
          "tools": ["ferramenta1", "ferramenta2"],
          "steps": ["passo 1", "passo 2", "passo 3"]
        }}
      ],
      "dependencies": [],
      "deliverables": ["entregável 1", "entregável 2"]
    }}
  ],
  "totalDuration": "X-Y semanas",
  "estimatedBudget": "R$ X ou não especificado",
  "successMetrics": ["métrica 1 (SMART)", "métrica 2 (SMART)"]
}}

**REQUISITOS CRÍTICOS:**
1. Mínimo 3 fases, máximo 6 fases
2. Cada fase deve ter 3-8 ações específicas e acionáveis
3. Priorize ações práticas que considerem a persona do cliente ideal
4. Inclua dependências entre fases quando relevante (usar IDs como "phase-1")
5. Métricas devem ser SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
6. Considere o contexto do negócio e persona em TODAS as ações
7. Ações devem ser específicas o suficiente para serem executadas imediatamente
8. Retorne APENAS o JSON válido, sem markdown ou texto adicional antes/depois

**EXEMPLO DE PRIORIDADES:**
- "alta": Ações críticas que bloqueiam outras ou têm alto impacto
- "média": Ações importantes mas que podem ser ajustadas
- "baixa": Ações complementares ou de longo prazo

**IMPORTANTE:** Retorne APENAS JSON válido. Não use ```json ou qualquer markdown.
"""
            
            response = await asyncio.wait_for(
                self.anthropic_client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    system="Você é um consultor estratégico especializado em criar planos de ação executáveis. Retorne sempre JSON válido, sem markdown.",
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                ),
                timeout=90.0  # 90 segundos para gerar plano completo
            )
            
            # Extract text from response
            text = response.content[0].text if response.content else ""
            
            # Clean markdown if present
            text = re.sub(r'```json\s*\n?', '', text)
            text = re.sub(r'```\s*\n?', '', text)
            text = text.strip()
            
            # Try to find JSON object in text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
            
            try:
                plan_dict = json.loads(text)
                
                # Validate and convert to ActionPlan model
                phases = []
                for phase_data in plan_dict.get("phases", []):
                    actions = []
                    for action_data in phase_data.get("actions", []):
                        action = Action(
                            id=action_data.get("id", f"action-{phase_data.get('phaseNumber', 0)}-{len(actions) + 1}"),
                            title=action_data.get("title", "Ação sem título"),
                            description=action_data.get("description", ""),
                            responsible=action_data.get("responsible", "Equipe"),
                            priority=action_data.get("priority", "média"),
                            estimatedTime=action_data.get("estimatedTime", "Não especificado"),
                            tools=action_data.get("tools", []),
                            steps=action_data.get("steps", [])
                        )
                        actions.append(action)
                    
                    phase = Phase(
                        phaseNumber=phase_data.get("phaseNumber", 0),
                        name=phase_data.get("name", "Fase sem nome"),
                        duration=phase_data.get("duration", "Não especificado"),
                        objectives=phase_data.get("objectives", []),
                        actions=actions,
                        dependencies=phase_data.get("dependencies", []),
                        deliverables=phase_data.get("deliverables", [])
                    )
                    phases.append(phase)
                
                action_plan = ActionPlan(
                    phases=phases,
                    totalDuration=plan_dict.get("totalDuration", "Não especificado"),
                    estimatedBudget=plan_dict.get("estimatedBudget"),
                    successMetrics=plan_dict.get("successMetrics", [])
                )
                
                print(f"[CouncilOrchestrator] ✓ Plano de ação gerado: {len(phases)} fases, {sum(len(p.actions) for p in phases)} ações")
                return action_plan
                
            except json.JSONDecodeError as e:
                print(f"[CouncilOrchestrator] Erro ao parsear JSON do plano de ação: {e}")
                print(f"[CouncilOrchestrator] Texto recebido: {text[:500]}...")
                return None
                
        except Exception as e:
            print(f"[CouncilOrchestrator] Erro ao gerar plano de ação: {e}")
            import traceback
            traceback.print_exc()
            return None

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