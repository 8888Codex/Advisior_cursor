"""
Perplexity Research Module
Contextualizes market research using BusinessProfile data
"""
import os
import httpx
import asyncio
from typing import List, Dict, Optional, Any
from python_backend.models import BusinessProfile

class PerplexityResearch:
    """Wrapper for Perplexity API with business context and lazy initialization"""
    
    def __init__(self):
        self._api_key = None
        self._base_url = None
        self._model = None
    
    def _ensure_initialized(self):
        """Lazy initialization - validates API key only when needed"""
        if self._api_key is None:
            self._api_key = os.getenv("PERPLEXITY_API_KEY")
            if not self._api_key:
                raise ValueError(
                    "PERPLEXITY_API_KEY environment variable is required for market research. "
                    "Please configure your API key in environment variables."
                )
            
            self._base_url = "https://api.perplexity.ai/chat/completions"
            self._model = "sonar-pro"  # Advanced search with grounding for complex queries
    
    @property
    def api_key(self):
        self._ensure_initialized()
        return self._api_key
    
    @property
    def base_url(self):
        self._ensure_initialized()
        return self._base_url
    
    @property
    def model(self):
        self._ensure_initialized()
        return self._model
    
    async def research(
        self,
        problem: str,
        profile: Optional[BusinessProfile] = None
    ) -> Dict[str, Any]:
        """
        Perform contextualized market research
        
        Args:
            problem: User's business problem/question
            profile: BusinessProfile for context (optional)
        
        Returns:
            Dict with findings and sources
        """
        # Build contextualized research query
        query = self._build_research_query(problem, profile)
        
        # Call Perplexity API with retry logic
        retry_count = 0
        max_retries = 3
        backoff_factor = 1.5
        last_error = None
        
        # Try multiple models if needed
        models_to_try = [self.model, "sonar-reasoning", "sonar", "sonar-pro"]
        
        for model in models_to_try:
            retry_count = 0
            while retry_count <= max_retries:
                try:
                    print(f"[PerplexityResearch] Trying model {model}, attempt {retry_count+1}/{max_retries+1}")
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        response = await client.post(
                            self.base_url,
                            headers={
                                "Authorization": f"Bearer {self.api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": model,
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": (
                                            "Você é um analista de pesquisa de mercado. SEMPRE responda em português brasileiro. "
                                            "Forneça insights factuais e baseados em dados com estatísticas específicas, tendências e exemplos. "
                                            "Foque em dados recentes (2024-2025). "
                                            "Inclua análise competitiva e benchmarks do setor quando relevante."
                                        )
                                    },
                                    {
                                        "role": "user",
                                        "content": query
                                    }
                                ],
                                "temperature": 0.2,
                                "search_recency_filter": "month",
                                "return_related_questions": False
                            }
                        )
                        response.raise_for_status()
                        data = response.json()
                        print(f"[PerplexityResearch] Successfully used model {model}")
                        # Success! Break out of both loops
                        break
                except httpx.HTTPStatusError as e:
                    print(f"[PerplexityResearch] HTTP error with model {model}: {e.response.status_code} - {e.response.text}")
                    # If it's a resource_exhausted error, we should propagate it immediately
                    if "resource_exhausted" in e.response.text.lower():
                        print("[PerplexityResearch] Resource exhausted error detected, raising immediately")
                        raise
                    last_error = e
                    retry_count += 1
                    if retry_count <= max_retries:
                        wait_time = backoff_factor ** retry_count
                        print(f"[PerplexityResearch] Waiting {wait_time:.1f}s before retry")
                        await asyncio.sleep(wait_time)
                    continue
                except Exception as e:
                    print(f"[PerplexityResearch] Unexpected error with model {model}: {str(e)}")
                    last_error = e
                    retry_count += 1
                    if retry_count <= max_retries:
                        wait_time = backoff_factor ** retry_count
                        print(f"[PerplexityResearch] Waiting {wait_time:.1f}s before retry")
                        await asyncio.sleep(wait_time)
                    continue
            
            # If we got data successfully, break out of the model loop
            if 'data' in locals():
                break
        
        # If we've tried all models and retries and still failed
        if 'data' not in locals():
            if last_error:
                # If it's an HTTPStatusError, pass it through
                if isinstance(last_error, httpx.HTTPStatusError):
                    raise last_error
                raise ValueError(f"All Perplexity API attempts failed: {str(last_error)}")
            raise ValueError("Failed to get data from Perplexity API after all attempts")
        
        # Extract findings and citations
        findings = data["choices"][0]["message"]["content"]
        # Sources can be in 'citations' or 'search_results'
        sources = []
        if "citations" in data:
            sources = data["citations"]
        elif "search_results" in data:
            sources = [result.get("url", "") for result in data["search_results"]]
        
        return {
            "query": query,
            "findings": findings,
            "sources": sources,
            "model": data["model"]
        }
    
    def _build_research_query(
        self,
        problem: str,
        profile: Optional[BusinessProfile]
    ) -> str:
        """Build contextualized research query using business profile"""
        
        if not profile:
            # Generic research without context
            return f"Pesquisa de mercado e tendências para: {problem}"
        
        # Build rich context from profile (Pydantic uses camelCase attributes)
        context_parts = []
        
        # Industry and company size context
        context_parts.append(
            f"Setor: {profile.industry} "
            f"(porte da empresa: {profile.companySize})"
        )
        
        # Target audience context
        context_parts.append(f"Público-alvo: {profile.targetAudience}")
        
        # Channels context
        if profile.channels:
            channels_str = ", ".join(profile.channels)
            context_parts.append(f"Canais de venda: {channels_str}")
        
        # Primary goal context
        goal_map = {
            "growth": "focado em crescimento e aquisição de clientes",
            "positioning": "trabalhando em posicionamento e diferenciação de marca",
            "retention": "melhorando retenção e fidelização de clientes",
            "launch": "lançando novos produtos/serviços",
            "awareness": "construindo reconhecimento de marca"
        }
        goal_desc = goal_map.get(profile.primaryGoal, profile.primaryGoal)
        context_parts.append(f"Objetivo principal: {goal_desc}")
        
        # Build final query
        context = ". ".join(context_parts)
        
        query = (
            f"Contexto: {context}. "
            f"Problema/Pergunta: {problem}. "
            f"\n\nForneça pesquisa de mercado incluindo: "
            f"1) Tendências atuais da indústria e estatísticas para {profile.industry}, "
            f"2) Cenário competitivo e benchmarks, "
            f"3) Melhores práticas para empresas de porte similar ({profile.companySize}), "
            f"4) Dados específicos relevantes ao problema mencionado acima. "
            f"Foque em insights acionáveis com dados recentes (2024-2025)."
        )
        
        return query

# Global instance
perplexity_research = PerplexityResearch()
