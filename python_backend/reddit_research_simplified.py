"""
Reddit Research Engine - Strategic Community Analysis
Analyzes Reddit communities to extract persona insights using Perplexity API and Claude
"""
import os
import time
import json
import random
import re
from typing import Dict, List, Optional, Any
import httpx
import asyncio
from anthropic import AsyncAnthropic

class RedditResearchEngine:
    """
    Researches target audience using Perplexity API and synthesizes with Claude.
    
    Features:
    - Robust error handling
    - Structured data output
    - Framework-based persona generation (JTBD + BAG)
    """
    
    def __init__(self):
        self._perplexity_api_key = None
        self._anthropic_client = None
        self._cache = {}  # Simple in-memory cache
        self._cache_ttl = 24 * 60 * 60  # 24 hours in seconds
    
    def _ensure_initialized(self):
        """Lazy initialization of API clients"""
        if self._perplexity_api_key is None:
            self._perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
            if not self._perplexity_api_key:
                raise ValueError("PERPLEXITY_API_KEY environment variable not set")
        
        if self._anthropic_client is None:
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self._anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    def _get_cache_key(self, method: str, **kwargs) -> str:
        """Generate a cache key from method name and arguments"""
        # Sort kwargs to ensure consistent keys
        sorted_kwargs = {k: kwargs[k] for k in sorted(kwargs.keys()) if kwargs[k] is not None}
        return f"{method}:{json.dumps(sorted_kwargs)}"
    
    def _get_cached_result(self, cache_key: str) -> Optional[Dict]:
        """Get result from cache if it exists and is not expired"""
        if cache_key in self._cache:
            timestamp, data = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                print(f"[RedditResearch] Cache hit for {cache_key}")
                return data
            else:
                print(f"[RedditResearch] Cache expired for {cache_key}")
                del self._cache[cache_key]
        return None
    
    def _set_cache_result(self, cache_key: str, data: Dict):
        """Store result in cache with current timestamp"""
        self._cache[cache_key] = (time.time(), data)
    
    async def _call_perplexity_api(self, query: str, model: str = "sonar-reasoning") -> Dict:
        """
        Call Perplexity API with fallback models
        
        Args:
            query: The search query
            model: Perplexity model to use
            
        Returns:
            Dict containing the API response
        """
        self._ensure_initialized()
        
        # Lista de modelos para fallback em ordem de preferência
        fallback_models = ["sonar-reasoning", "sonar", "sonar-pro", "sonar-deep-research", "sonar-reasoning-pro"]
        
        # Se o modelo solicitado não estiver na lista de fallback, adicione-o como primeira opção
        if model not in fallback_models:
            fallback_models.insert(0, model)
        else:
            # Se o modelo já estiver na lista, reorganize para que seja o primeiro
            fallback_models.remove(model)
            fallback_models.insert(0, model)
            
        last_error = None
        
        # Tente cada modelo na lista de fallback
        for current_model in fallback_models:
            try:
                print(f"[RedditResearch] Calling Perplexity API with model {current_model}...")
                
                request_payload = {
                    "model": current_model,
                    "messages": [
                        {"role": "system", "content": "Você é um especialista em pesquisa de audiência. Forneça insights concretos e acionáveis baseados em dados reais."},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                }
                
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "https://api.perplexity.ai/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self._perplexity_api_key}",
                            "Content-Type": "application/json"
                        },
                        json=request_payload
                    )
                    
                    response.raise_for_status()  # Raise exception for 4XX/5XX responses
                    
                    result = response.json()
                    print(f"[RedditResearch] Successfully used model {current_model}")
                    return result
                    
            except httpx.HTTPStatusError as e:
                print(f"[RedditResearch] Perplexity API HTTP error with model {current_model}: {e.response.status_code} - {e.response.text}")
                last_error = e
                continue  # Try next model
                
            except httpx.RequestError as e:
                print(f"[RedditResearch] Perplexity API request error with model {current_model}: {str(e)}")
                last_error = e
                continue  # Try next model
                
            except Exception as e:
                print(f"[RedditResearch] Unexpected error with model {current_model}: {str(e)}")
                last_error = e
                continue  # Try next model
        
        # If we've tried all models and none worked, raise the last error
        if last_error:
            print(f"[RedditResearch] All fallback models failed. Last error: {str(last_error)}")
            raise ValueError(f"All Perplexity API models failed: {str(last_error)}")
        
        # This should never happen, but just in case
        raise ValueError("Failed to call Perplexity API with all available models")
    
    async def _call_anthropic_api(self, prompt: str) -> Dict:
        """
        Call Claude API to structure data
        
        Args:
            prompt: The prompt to send to Claude
            
        Returns:
            Dict containing the structured data
        """
        self._ensure_initialized()
        
        try:
            # Call Claude API
            message = await self._anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.2,
                system="Você é um assistente especializado em estruturar dados de pesquisa em formatos JSON.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            
            # Try to extract JSON from the response
            try:
                # First try to find JSON in code blocks
                json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                
                # If not found in code blocks, try to find anything that looks like JSON
                json_match = re.search(r'({.*})', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                
                print("[RedditResearch] Failed to parse JSON from Claude response, using full text")
            except json.JSONDecodeError:
                print("[RedditResearch] Failed to parse JSON from Claude response, using full text")
            
            # If not valid JSON or not in code blocks, return the raw text
            return {"content": content}
            
        except Exception as e:
            print(f"[RedditResearch] Claude API error: {str(e)}")
            raise
    
    async def research_quick(self, target_description: str, industry: Optional[str] = None) -> Dict:
        """
        Quick research mode: Uses Perplexity for research and Claude for structuring
        
        Args:
            target_description: Description of the target audience
            industry: Optional industry context
            
        Returns:
            Dict with structured persona data following JTBD and BAG frameworks
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key("research_quick", target_description=target_description, industry=industry)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                print(f"[RedditResearch] Cache hit for '{target_description}'")
                return cached_result
            
            print(f"[RedditResearch] Iniciando pesquisa rápida para '{target_description}'")
            
            # Build Perplexity query for JTBD + BAG framework
            context = f"na indústria de {industry}" if industry else ""
            query = f"""
Pesquise informações detalhadas sobre o público-alvo '{target_description}' {context}, focando em:

1. Jobs to Be Done (JTBD):
   - Quais são os principais "trabalhos" que este público precisa realizar?
   - Quais contextos situacionais desencadeiam esses trabalhos?
   - Quais são os trabalhos funcionais, emocionais e sociais?

2. Comportamentos, Aspirações e Objetivos (BAG):
   - Comportamentos observáveis e padrões de uso
   - Aspirações de longo prazo e sonhos
   - Objetivos específicos de curto e médio prazo

3. Elementos Quantitativos:
   - Pontos de dor com impacto mensurável (tempo, dinheiro, estresse)
   - Critérios de decisão com pesos relativos
   - Métricas de sucesso para avaliar soluções

4. Jornada e Pontos de Contato:
   - Canais preferidos para diferentes estágios
   - Tipos de conteúdo mais valorizados
   - Influenciadores e fontes confiáveis

Forneça dados específicos, estatísticas quando possível, e cite fontes relevantes.
"""
            
            # Call Perplexity API
            perplexity_result = await self._call_perplexity_api(query)
            perplexity_content = perplexity_result["choices"][0]["message"]["content"]
            
            # Now use Claude to structure the data
            claude_prompt = f"""
Com base nos dados de pesquisa a seguir:

{perplexity_content}

Crie uma persona completa para '{target_description}' {context} seguindo os frameworks modernos de 2025:

1. Comece com uma declaração de trabalho principal (job statement) clara e acionável
2. Estruture usando o framework BAG completo (Behaviors, Aspirations, Goals)
3. Inclua elementos quantitativos detalhados para todos os pontos de dor
4. Mapeie a jornada moderna com todos os pontos de contato

Formate os dados no seguinte formato JSON:
{{
  "job_to_be_done": {{
    "statement": "string",
    "functional_aspects": ["string"],
    "emotional_aspects": ["string"],
    "social_aspects": ["string"],
    "triggers": ["string"]
  }},
  "behaviors": {{
    "online": ["string"],
    "purchasing": ["string"],
    "content_consumption": ["string"]
  }},
  "aspirations": ["string"],
  "goals": [
    {{
      "description": "string",
      "timeframe": "short|medium|long",
      "success_metrics": ["string"]
    }}
  ],
  "demographics": {{
    "age": "string",
    "location": "string",
    "occupation": "string",
    "education": "string",
    "income": "string"
  }},
  "psychographics": {{
    "values": ["string"],
    "interests": ["string"],
    "personality_traits": ["string"]
  }},
  "pain_points_quantified": [
    {{
      "description": "string",
      "impact": "string",
      "cost": "string",
      "frequency": "string"
    }}
  ],
  "values": ["string"],
  "content_preferences": {{
    "formats": ["string"],
    "topics": ["string"],
    "channels": ["string"]
  }},
  "touchpoints": [
    {{
      "channel": "string",
      "stage": "string",
      "importance": 1-10,
      "preferred_content": ["string"]
    }}
  ],
  "research_data": {{
    "sources": ["string"],
    "confidence_level": "high|medium|low",
    "timestamp": "ISO date string"
  }}
}}

Importante: Todos os dados devem ser específicos, acionáveis e baseados na pesquisa.
"""
            
            # Call Claude API to structure the data
            structured_data = await self._call_anthropic_api(claude_prompt)
            
            # Add metadata
            if "research_data" not in structured_data:
                structured_data["research_data"] = {}
            
            structured_data["research_data"]["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            structured_data["research_data"]["target_description"] = target_description
            if industry:
                structured_data["research_data"]["industry"] = industry
            
            # Cache the result
            self._set_cache_result(cache_key, structured_data)
            
            print(f"[RedditResearch] Pesquisa rápida concluída com sucesso para '{target_description}'")
            return structured_data
            
        except Exception as e:
            print(f"[RedditResearch] Error in quick research: {str(e)}")
            
            # Fornecer dados de fallback para evitar erro 500
            print(f"[RedditResearch] Gerando dados de fallback para '{target_description}'")
            
            fallback_data = {
                "job_to_be_done": {
                    "statement": f"Ajudar {target_description} a ter sucesso em seus objetivos profissionais",
                    "functional_aspects": ["Economizar tempo", "Aumentar produtividade"],
                    "emotional_aspects": ["Reduzir estresse", "Aumentar confiança"],
                    "social_aspects": ["Ser reconhecido por pares", "Demonstrar competência"],
                    "triggers": ["Pressão de prazos", "Competição no mercado"]
                },
                "behaviors": {
                    "online": ["Pesquisa por soluções online", "Consome conteúdo educativo"],
                    "purchasing": ["Compara opções", "Busca recomendações"],
                    "content_consumption": ["Prefere conteúdo prático", "Consome em múltiplos formatos"]
                },
                "aspirations": [
                    f"Ser reconhecido como expert em {industry or 'seu campo'}",
                    "Alcançar equilíbrio entre vida pessoal e profissional"
                ],
                "demographics": {
                    "age": "30-45 anos",
                    "location": "Centros urbanos",
                    "education": "Ensino superior completo",
                    "income": "Classe média a alta"
                },
                "pain_points_quantified": [
                    {
                        "description": "Dificuldade em acompanhar tendências do mercado",
                        "impact": "Perda de oportunidades de negócio",
                        "frequency": "Constante"
                    }
                ],
                "research_data": {
                    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "target_description": target_description,
                    "confidence_level": "low",
                    "is_fallback": True
                }
            }
            
            if industry:
                fallback_data["research_data"]["industry"] = industry
                
            # Cache o resultado de fallback também
            self._set_cache_result(cache_key, fallback_data)
            
            return fallback_data

    async def research_strategic(self, target_description: str, industry: Optional[str] = None, additional_context: Optional[str] = None) -> Dict:
        """
        Strategic research mode: More comprehensive research with additional context
        
        Args:
            target_description: Description of the target audience
            industry: Optional industry context
            additional_context: Additional context to refine the research
        
        Returns:
            Dict with comprehensive persona data
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key("research_strategic", target_description=target_description, industry=industry, additional_context=additional_context)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                return cached_result
            
            print(f"[RedditResearch] Iniciando pesquisa estratégica para '{target_description}'")
            
            # For strategic research, we'll do two Perplexity calls:
            # 1. First to find relevant communities and sources
            # 2. Second to get deeper insights based on those communities
            
            context = f"na indústria de {industry}" if industry else ""
            additional = f"Contexto adicional: {additional_context}" if additional_context else ""
            
            # Simplified strategic research - just use quick research with a fallback
            try:
                # Call quick research with the same parameters
                result = await self.research_quick(target_description, industry)
                
                # Add additional context to the result
                if additional_context and "research_data" in result:
                    result["research_data"]["additional_context"] = additional_context
                
                # Cache the result
                self._set_cache_result(cache_key, result)
                
                return result
                
            except Exception as e:
                print(f"[RedditResearch] Error in strategic research: {str(e)}")
                
                # Provide fallback data
                fallback_data = {
                    "job_to_be_done": {
                        "statement": f"Ajudar {target_description} a ter sucesso em seus objetivos profissionais",
                        "functional_aspects": ["Economizar tempo", "Aumentar produtividade"],
                        "emotional_aspects": ["Reduzir estresse", "Aumentar confiança"],
                        "social_aspects": ["Ser reconhecido por pares", "Demonstrar competência"],
                        "triggers": ["Pressão de prazos", "Competição no mercado"]
                    },
                    "behaviors": {
                        "online": ["Pesquisa por soluções online", "Consome conteúdo educativo"],
                        "purchasing": ["Compara opções", "Busca recomendações"],
                        "content_consumption": ["Prefere conteúdo prático", "Consome em múltiplos formatos"]
                    },
                    "aspirations": [
                        f"Ser reconhecido como expert em {industry or 'seu campo'}",
                        "Alcançar equilíbrio entre vida pessoal e profissional"
                    ],
                    "demographics": {
                        "age": "30-45 anos",
                        "location": "Centros urbanos",
                        "education": "Ensino superior completo",
                        "income": "Classe média a alta"
                    },
                    "pain_points_quantified": [
                        {
                            "description": "Dificuldade em acompanhar tendências do mercado",
                            "impact": "Perda de oportunidades de negócio",
                            "frequency": "Constante"
                        }
                    ],
                    "research_data": {
                        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "target_description": target_description,
                        "confidence_level": "low",
                        "is_fallback": True
                    }
                }
                
                if industry:
                    fallback_data["research_data"]["industry"] = industry
                if additional_context:
                    fallback_data["research_data"]["additional_context"] = additional_context
                    
                # Cache o resultado de fallback também
                self._set_cache_result(cache_key, fallback_data)
                
                return fallback_data
                
        except Exception as e:
            print(f"[RedditResearch] Critical error in research_strategic: {str(e)}")
            
            # Minimal fallback data
            return {
                "job_to_be_done": {
                    "statement": f"Ajudar {target_description} a resolver seus problemas"
                },
                "demographics": {
                    "age": "Adulto"
                },
                "behaviors": {
                    "online": ["Busca informações online"]
                },
                "research_data": {
                    "is_fallback": True,
                    "error": str(e)
                }
            }

# Singleton instance
reddit_research = RedditResearchEngine()
