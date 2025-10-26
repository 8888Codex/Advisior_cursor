"""
Reddit Research Engine - Strategic Community Analysis
Analyzes Reddit communities to extract persona insights

NO Reddit API - use Perplexity API for Reddit research instead
"""
import os
from typing import Dict, List, Optional
import httpx
from anthropic import AsyncAnthropic

class RedditResearchEngine:
    """
    Researches target audience on Reddit using Perplexity API.
    
    Strategy:
    1. Use Perplexity to find relevant Reddit communities
    2. Use Perplexity to analyze discussions in those communities
    3. Extract pain points, goals, values, and behavioral patterns
    4. Synthesize findings into structured persona data
    """
    
    def __init__(self):
        self._perplexity_api_key = None
        self._anthropic_client = None
    
    def _ensure_initialized(self):
        """Lazy initialization"""
        if self._perplexity_api_key is None:
            self._perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
            if not self._perplexity_api_key:
                raise ValueError("PERPLEXITY_API_KEY required for Reddit research")
        
        if self._anthropic_client is None:
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_key:
                raise ValueError("ANTHROPIC_API_KEY required for persona synthesis")
            self._anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    @property
    def perplexity_api_key(self):
        self._ensure_initialized()
        return self._perplexity_api_key
    
    @property
    def anthropic_client(self):
        self._ensure_initialized()
        return self._anthropic_client
    
    async def research_quick(
        self,
        target_description: str,
        industry: Optional[str] = None
    ) -> Dict:
        """
        Quick research mode: 1-2 Perplexity calls for basic persona insights
        
        Returns:
            dict with: painPoints, goals, values, demographics, communities
        """
        self._ensure_initialized()
        
        # Build Perplexity query
        context = f"Indústria: {industry}" if industry else ""
        query = f"""
Analise o público-alvo '{target_description}' {context} e identifique:

1. **Comunidades no Reddit**: 3-5 subreddits mais relevantes onde esse público se reúne
2. **Pain Points**: 5-7 principais dores e frustrações desse público
3. **Goals**: 5-7 objetivos e aspirações principais
4. **Values**: 3-5 valores fundamentais que guiam suas decisões
5. **Demographics**: Faixa etária predominante, localização, ocupação

Foque em dados concretos e insights acionáveis baseados em discussões reais do Reddit.
        """
        
        # Call Perplexity
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {"role": "system", "content": "Você é um especialista em pesquisa de audiência no Reddit brasileiro. Forneça insights concretos e acionáveis."},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.2,
                    "return_citations": True
                }
            )
            
            result = response.json()
            findings = result["choices"][0]["message"]["content"]
            citations = result.get("citations", [])
        
        # Use Claude to structure findings into persona format
        structured_response = await self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system="You are a persona synthesis expert. Extract structured data from research findings.",
            messages=[{
                "role": "user",
                "content": f"""
From the following Reddit research findings, extract structured persona data:

{findings}

Return ONLY valid JSON in this exact format:
{{
  "painPoints": ["point 1", "point 2", ...],
  "goals": ["goal 1", "goal 2", ...],
  "values": ["value 1", "value 2", ...],
  "communities": ["r/subreddit1", "r/subreddit2", ...],
  "demographics": {{
    "ageRange": "25-35",
    "location": "Brasil - principais capitais",
    "occupation": "Empreendedores digitais"
  }},
  "psychographics": {{
    "interests": ["interest 1", "interest 2"],
    "challenges": ["challenge 1", "challenge 2"]
  }}
}}
                """
            }]
        )
        
        # Parse Claude's JSON response
        import json
        response_text = structured_response.content[0].text  # type: ignore
        persona_data = json.loads(response_text)
        
        # Add research metadata
        persona_data["researchData"] = {
            "mode": "quick",
            "rawFindings": findings,
            "citations": citations,
            "timestamp": None  # Will be set by caller
        }
        
        return persona_data
    
    async def research_strategic(
        self,
        target_description: str,
        industry: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict:
        """
        Strategic research mode: Deep multi-query analysis
        
        Conducts:
        1. Community discovery (find best subreddits)
        2. Pain point analysis (deep dive into frustrations)
        3. Goal/aspiration analysis (what they're trying to achieve)
        4. Behavioral pattern analysis (how they make decisions)
        5. Content preference analysis (what content resonates)
        
        Returns:
            dict with complete persona data including behavioral patterns
        """
        self._ensure_initialized()
        
        context_parts = []
        if industry:
            context_parts.append(f"Indústria: {industry}")
        if additional_context:
            context_parts.append(additional_context)
        context_str = " | ".join(context_parts)
        
        # Query 1: Community Discovery
        community_query = f"""
Identifique as 5-10 comunidades do Reddit (subreddits) mais relevantes para o público-alvo '{target_description}' {context_str}.

Para cada comunidade, forneça:
- Nome do subreddit
- Número aproximado de membros
- Principais tópicos discutidos
- Por que esse subreddit é relevante para esse público

Foque em comunidades brasileiras (r/brasil, r/investimentos, etc) quando possível.
        """
        
        # Query 2: Pain Points & Frustrations
        pain_query = f"""
Analise discussões no Reddit sobre '{target_description}' {context_str} e identifique:

1. **Principais Frustrações**: 7-10 dores recorrentes mencionadas
2. **Problemas Não Resolvidos**: Gaps que o mercado ainda não atende
3. **Objeções Comuns**: Resistências e preocupações frequentes

Cite exemplos concretos de posts/comentários quando possível.
        """
        
        # Query 3: Goals & Aspirations
        goal_query = f"""
Baseado em discussões do Reddit sobre '{target_description}' {context_str}, identifique:

1. **Objetivos Imediatos**: O que buscam agora (próximos 3-6 meses)
2. **Aspirações de Longo Prazo**: Onde querem estar em 1-3 anos
3. **Motivações Principais**: Por que estão buscando esses objetivos
4. **Métricas de Sucesso**: Como medem progresso

Forneça insights acionáveis para marketing.
        """
        
        # Query 4: Behavioral Patterns
        behavior_query = f"""
Analise padrões comportamentais do público '{target_description}' {context_str} no Reddit:

1. **Processo de Decisão**: Como pesquisam e decidem compras/investimentos
2. **Fontes de Confiança**: Quem/o que influencia suas decisões
3. **Gatilhos de Ação**: O que os leva a tomar ação
4. **Objeções Comuns**: O que os impede de agir
5. **Timing**: Quando estão mais propensos a agir

Foque em insights para criação de conteúdo e campanhas.
        """
        
        # Query 5: Content Preferences
        content_query = f"""
Analise preferências de conteúdo do público '{target_description}' {context_str} no Reddit:

1. **Formatos Preferidos**: Quais tipos de conteúdo geram mais engajamento (vídeos, textos longos, infográficos, etc)
2. **Tom e Linguagem**: Formal vs informal, técnico vs acessível
3. **Temas de Interesse**: Tópicos que geram discussão
4. **Calls-to-Action**: O que os motiva a comentar/compartilhar

Forneça diretrizes práticas para criação de conteúdo.
        """
        
        # Execute all queries in parallel
        import asyncio
        
        async def query_perplexity(query: str) -> tuple[str, list]:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.perplexity_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-sonar-large-128k-online",
                        "messages": [
                            {"role": "system", "content": "Você é um especialista em pesquisa de audiência. Forneça insights concretos baseados em dados reais do Reddit."},
                            {"role": "user", "content": query}
                        ],
                        "temperature": 0.2,
                        "return_citations": True
                    }
                )
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                citations = result.get("citations", [])
                return content, citations
        
        # Run all queries concurrently
        results = await asyncio.gather(
            query_perplexity(community_query),
            query_perplexity(pain_query),
            query_perplexity(goal_query),
            query_perplexity(behavior_query),
            query_perplexity(content_query)
        )
        
        communities_findings, communities_citations = results[0]
        pain_findings, pain_citations = results[1]
        goal_findings, goal_citations = results[2]
        behavior_findings, behavior_citations = results[3]
        content_findings, content_citations = results[4]
        
        # Combine all findings
        all_findings = f"""
## Comunidades Relevantes
{communities_findings}

## Pain Points & Frustrações
{pain_findings}

## Objetivos & Aspirações
{goal_findings}

## Padrões Comportamentais
{behavior_findings}

## Preferências de Conteúdo
{content_findings}
        """
        
        all_citations = (
            communities_citations + pain_citations + goal_citations +
            behavior_citations + content_citations
        )
        
        # Use Claude to synthesize into structured persona
        synthesis_response = await self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            system="You are a persona synthesis expert. Create comprehensive, actionable persona profiles from research data.",
            messages=[{
                "role": "user",
                "content": f"""
From the following comprehensive Reddit research findings, create a detailed persona profile:

{all_findings}

Return ONLY valid JSON in this exact format:
{{
  "painPoints": ["detailed pain point 1", "detailed pain point 2", ...],
  "goals": ["specific goal 1", "specific goal 2", ...],
  "values": ["core value 1", "core value 2", ...],
  "communities": ["r/subreddit1", "r/subreddit2", ...],
  "demographics": {{
    "ageRange": "25-35",
    "location": "Brasil - principais capitais",
    "occupation": "Empreendedores digitais",
    "educationLevel": "Superior completo",
    "incomeRange": "R$ 3.000 - R$ 10.000/mês"
  }},
  "psychographics": {{
    "interests": ["interest 1", "interest 2", ...],
    "challenges": ["challenge 1", "challenge 2", ...],
    "motivations": ["motivation 1", "motivation 2", ...],
    "frustrations": ["frustration 1", "frustration 2", ...]
  }},
  "behavioralPatterns": {{
    "decisionProcess": "how they research and decide",
    "trustSources": ["source 1", "source 2", ...],
    "actionTriggers": ["trigger 1", "trigger 2", ...],
    "objections": ["objection 1", "objection 2", ...],
    "buyingTiming": "when they're most likely to buy"
  }},
  "contentPreferences": {{
    "preferredFormats": ["format 1", "format 2", ...],
    "toneStyle": "formal/informal/technical/accessible",
    "engagementThemes": ["theme 1", "theme 2", ...],
    "effectiveCTAs": ["CTA type 1", "CTA type 2", ...]
  }}
}}
                """
            }]
        )
        
        # Parse Claude's JSON response
        import json
        response_text = synthesis_response.content[0].text  # type: ignore
        persona_data = json.loads(response_text)
        
        # Add research metadata
        persona_data["researchData"] = {
            "mode": "strategic",
            "rawFindings": all_findings,
            "citations": all_citations,
            "timestamp": None  # Will be set by caller
        }
        
        return persona_data

# Global instance
reddit_research = RedditResearchEngine()
