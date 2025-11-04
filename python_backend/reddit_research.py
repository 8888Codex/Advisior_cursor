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
from dotenv import load_dotenv, find_dotenv
from anthropic import AsyncAnthropic

# Carregar .env quando o módulo é importado
_env_file = find_dotenv(usecwd=True)
if _env_file:
    load_dotenv(_env_file, override=True)

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
        # Garantir que .env está carregado
        _env_file = find_dotenv(usecwd=True)
        if _env_file:
            load_dotenv(_env_file, override=True)
        
        if self._perplexity_api_key is None:
            self._perplexity_api_key = os.getenv("PERPLEXITY_API_KEY") or os.environ.get("PERPLEXITY_API_KEY")
            if not self._perplexity_api_key:
                raise ValueError("PERPLEXITY_API_KEY environment variable not set")
        
        if self._anthropic_client is None:
            anthropic_key = os.getenv("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
            if not anthropic_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable not set. "
                    "Verifique se o arquivo .env existe e contém ANTHROPIC_API_KEY=sk-ant-... "
                    "ou configure como variável de ambiente do sistema."
                )
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
        
        # If we've tried all models and none worked, check if it's a resource_exhausted error
        if last_error:
            print(f"[RedditResearch] All fallback models failed. Last error: {str(last_error)}")
            
            # If it's an HTTPStatusError, pass it through so it can be handled properly
            if isinstance(last_error, httpx.HTTPStatusError):
                if "resource_exhausted" in last_error.response.text.lower():
                    print("[RedditResearch] Resource exhausted error detected")
                raise last_error
                
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
            # Call Claude API with retry logic for network issues
            retry_count = 0
            max_retries = 3
            backoff_factor = 1.5
            
            while retry_count <= max_retries:
                try:
                    message = await self._anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=4000,
                        temperature=0.2,
                        system="Você é um assistente especializado em estruturar dados de pesquisa em formatos JSON.",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    break  # Success, exit retry loop
                except Exception as retry_error:
                    retry_count += 1
                    if retry_count > max_retries:
                        print(f"[RedditResearch] Max retries ({max_retries}) reached. Giving up.")
                        raise  # Re-raise the last exception
                    
                    wait_time = backoff_factor ** retry_count
                    print(f"[RedditResearch] Retry {retry_count}/{max_retries} after error: {str(retry_error)}. Waiting {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
            
            
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
Você é um especialista em criação de personas de marketing de alta precisão.

INPUT DO USUÁRIO (pode ser vago):
- Descrição: "{target_description}"
- Indústria: {context if context else "não especificada"}

DADOS DE PESQUISA:
{perplexity_content}

ANÁLISE CRÍTICA DO INPUT:
1. O input é vago ou genérico? Se sim, USE OS DADOS DE PESQUISA para INFERIR detalhes específicos
2. Faltam cargos específicos? DEDUZA baseado no contexto (budget, team size, indústria)
3. Sem setor definido? IDENTIFIQUE o setor mais provável baseado nas características

TAREFA:
Crie uma persona ULTRA-ESPECÍFICA seguindo os frameworks modernos de 2025:

PRINCÍPIOS OBRIGATÓRIOS:
1. NUNCA seja genérico - sempre específico
2. INFIRA detalhes que o usuário não mencionou mas são lógicos
3. QUANTIFIQUE tudo que for possível (tempo, dinheiro, frequência)
4. Use DADOS REAIS da pesquisa, não suposições genéricas
5. Comece com job statement claro e acionável
6. Estruture usando framework BAG completo (Behaviors, Aspirations, Goals)
7. Inclua elementos quantitativos DETALHADOS para todos os pontos de dor
8. Mapeie jornada moderna com todos os pontos de contato

EXPANSÃO INTELIGENTE:
Se input diz "profissionais B2B" → Identifique CARGOS específicos (CMO, Diretor, Head)
Se menciona "10k/mês em ads" → Infira faturamento, tamanho empresa, maturidade
Se não menciona setor → Use padrões da pesquisa para identificar setor provável

Formate os dados no seguinte formato JSON:
{{
  "job_statement": "string",
  "functional_jobs": ["string"],
  "emotional_jobs": ["string"],
  "social_jobs": ["string"],
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
  "researchData": {{
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
            if "researchData" not in structured_data:
                structured_data["researchData"] = {}
            
            structured_data["researchData"]["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            structured_data["researchData"]["target_description"] = target_description
            if industry:
                structured_data["researchData"]["industry"] = industry
            
            # Cache the result
            self._set_cache_result(cache_key, structured_data)
            
            print(f"[RedditResearch] Pesquisa rápida concluída com sucesso para '{target_description}'")
            return structured_data
            
        except Exception as e:
            print(f"[RedditResearch] Error in quick research: {str(e)}")
            
            # Fornecer dados de fallback para evitar erro 500
            print(f"[RedditResearch] Gerando dados de fallback para '{target_description}'")
            
            fallback_data = {
                "job_statement": f"Ajudar {target_description} a ter sucesso em seus objetivos profissionais",
                "functional_jobs": ["Economizar tempo", "Aumentar produtividade"],
                "emotional_jobs": ["Reduzir estresse", "Aumentar confiança"],
                "social_jobs": ["Ser reconhecido por pares", "Demonstrar competência"],
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
                    "income": "Classe média a alta",
                    "occupation": "Profissional freelancer"
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
        Strategic research mode: DEEP comprehensive research with multiple API calls
        
        Args:
            target_description: Description of the target audience
            industry: Optional industry context
            additional_context: Additional context to refine the research
        
        Returns:
            Dict with comprehensive persona data with REAL insights
        """
        try:
            # Check cache first
            cache_key = self._get_cache_key("research_strategic", target_description=target_description, industry=industry, additional_context=additional_context)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                return cached_result
            
            print(f"[RedditResearch] 🔍 MODO ESTRATÉGICO - Pesquisa profunda para '{target_description}'")
            self._ensure_initialized()
            
            context = f"na indústria de {industry}" if industry else ""
            additional = f". {additional_context}" if additional_context else ""
            
            # ============================================================================
            # FASE 1: DESCOBERTA DE COMUNIDADES E FONTES (Primeira chamada Perplexity)
            # ============================================================================
            discovery_query = f"""Pesquise profundamente sobre {target_description} {context}{additional}.

TAREFA 1 - DESCOBERTA:
Identifique COMUNIDADES REAIS onde este público está ativo:
- Subreddits específicos (ex: r/marketing, r/startups, r/entrepreneur)
- Fóruns e grupos online
- Comunidades profissionais
- Canais e influenciadores que seguem

RETORNE:
1. Lista de 5-10 comunidades específicas com URLs
2. Principais tópicos discutidos
3. Principais preocupações e dores mencionadas
4. Linguagem e termos que usam"""

            print(f"[RedditResearch] 📊 Fase 1: Descobrindo comunidades...")
            discovery_response = await self._call_perplexity_api(discovery_query)
            discovery_text = self._extract_content_from_response(discovery_response)
            
            # ============================================================================
            # FASE 2: ANÁLISE PROFUNDA DE PAIN POINTS (Segunda chamada Perplexity)
            # ============================================================================
            pain_points_query = f"""Baseado no público {target_description} {context}{additional}, faça uma análise QUANTIFICADA e ESPECÍFICA.

TAREFA 2 - PAIN POINTS QUANTIFICADOS:
Identifique problemas REAIS com NÚMEROS:
- Custos específicos (ex: CAC de R$X, tempo de Y horas/semana)
- Impactos mensuráveis (ex: perda de X% de leads, Y% de churn)
- Frequência dos problemas (diário, semanal, mensal)
- ROI e métricas que acompanham

RETORNE:
1. Top 5 pain points com custos estimados
2. Impacto financeiro de cada problema
3. Frequência de ocorrência
4. Métricas que mais monitoram"""

            print(f"[RedditResearch] 💰 Fase 2: Analisando pain points quantificados...")
            pain_response = await self._call_perplexity_api(pain_points_query)
            pain_text = self._extract_content_from_response(pain_response)
            
            # ============================================================================
            # FASE 3: COMPORTAMENTOS E DECISÕES (Terceira chamada Perplexity)
            # ============================================================================
            behavior_query = f"""Pesquise o comportamento de compra e decisão de {target_description} {context}{additional}.

TAREFA 3 - COMPORTAMENTOS REAIS:
Identifique padrões de decisão e ação:
- Como pesquisam soluções (canais, ferramentas, processos)
- Critérios de decisão (preço, features, suporte, etc)
- Influenciadores e fontes de confiança
- Objeções típicas e medos
- Ciclo de decisão (tempo médio, etapas)

RETORNE:
1. Processo de pesquisa detalhado
2. Critérios de decisão priorizados
3. Principais objeções
4. Tempo médio de decisão"""

            print(f"[RedditResearch] 🎯 Fase 3: Mapeando comportamentos e decisões...")
            behavior_response = await self._call_perplexity_api(behavior_query)
            behavior_text = self._extract_content_from_response(behavior_response)
            
            # ============================================================================
            # FASE 4: SÍNTESE COM CLAUDE (Quarta chamada - Claude)
            # ============================================================================
            print(f"[RedditResearch] 🤖 Fase 4: Sintetizando com Claude...")
            
            synthesis_prompt = f"""Você é um especialista em personas B2B e análise de público-alvo com 15+ anos de experiência.

Recebi 3 pesquisas profundas sobre: {target_description} {context}{additional}

DESCOBERTA DE COMUNIDADES:
{discovery_text}

PAIN POINTS QUANTIFICADOS:
{pain_text}

COMPORTAMENTOS E DECISÕES:
{behavior_text}

TAREFA FINAL:
Crie uma persona ULTRA-ESPECÍFICA e ESTRATÉGICA no formato JSON:

{{
  "job_statement": "Job to be done principal (específico e acionável)",
  "functional_jobs": ["5-7 jobs funcionais ESPECÍFICOS"],
  "emotional_jobs": ["4-5 jobs emocionais REAIS"],
  "social_jobs": ["3-4 jobs sociais ESPECÍFICOS"],
  "behaviors": {{
    "online": ["5-7 comportamentos online ESPECÍFICOS com ferramentas/plataformas"],
    "purchasing": ["4-5 comportamentos de compra DETALHADOS"],
    "content_consumption": ["4-5 preferências de conteúdo ESPECÍFICAS"]
  }},
  "aspirations": ["4-5 aspirações ESPECÍFICAS E AMBICIOSAS"],
  "goals": ["5-7 objetivos MENSURÁVEIS com números"],
  "pain_points_quantified": [
    {{
      "description": "Pain point ESPECÍFICO",
      "impact": "Impacto MENSURÁVEL",
      "cost": "Custo ESTIMADO em R$ ou tempo",
      "frequency": "Frequência ESPECÍFICA (diária/semanal/mensal)"
    }}
  ],
  "decision_criteria": {{
    "must_have": ["3-5 critérios ESSENCIAIS"],
    "nice_to_have": ["2-3 critérios DESEJÁVEIS"],
    "deal_breakers": ["2-3 ELIMINATÓRIOS"]
  }},
  "demographics": {{
    "age": "Faixa etária ESPECÍFICA",
    "location": "Localizações ESPECÍFICAS",
    "occupation": "Cargos ESPECÍFICOS",
    "education": "Nível ESPECÍFICO",
    "income": "Faixa salarial ESPECÍFICA em R$"
  }},
  "values": ["4-5 valores ESPECÍFICOS"],
  "touchpoints": [
    {{
      "channel": "Canal ESPECÍFICO",
      "stage": "awareness/consideration/decision",
      "importance": 1-10,
      "preferred_content": ["tipos de conteúdo ESPECÍFICOS"]
    }}
  ],
  "content_preferences": {{
    "formats": ["formatos ESPECÍFICOS"],
    "topics": ["tópicos ESPECÍFICOS"],
    "channels": ["canais ESPECÍFICOS"],
    "influencers": ["influenciadores ESPECÍFICOS se mencionados"]
  }},
  "communities": ["5-10 comunidades ESPECÍFICAS com URLs se possível"]
}}

REGRAS OBRIGATÓRIAS:
1. SEMPRE incluir NÚMEROS e QUANTIFICAÇÕES
2. SEMPRE ser ESPECÍFICO (não genérico)
3. SEMPRE basear nas pesquisas fornecidas
4. SEMPRE incluir custos estimados nos pain points
5. SEMPRE detalhar critérios de decisão

RETORNE APENAS O JSON, SEM MARKDOWN OU EXPLICAÇÕES."""

            claude_response = await self._anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.3,  # Mais determinístico para dados estruturados
                messages=[{"role": "user", "content": synthesis_prompt}]
            )
            
            result_text = claude_response.content[0].text.strip()
            
            # Remover markdown se presente
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            elif result_text.startswith("```"):
                result_text = result_text.replace("```", "").strip()
            
            # Parse JSON
            result = json.loads(result_text)
            
            # Adicionar metadata da pesquisa
            result["research_data"] = {
                "sources": self._extract_sources_from_response(discovery_response),
                "confidence_level": "high",  # Pesquisa profunda = alta confiança
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "target_description": target_description,
                "industry": industry,
                "additional_context": additional_context,
                "research_depth": "strategic",
                "perplexity_calls": 3,
                "claude_synthesis": True
            }
            
            # Cache the result
            self._set_cache_result(cache_key, result)
            
            print(f"[RedditResearch] ✅ Pesquisa estratégica concluída com ALTA qualidade!")
            
            return result
                
        except Exception as e:
            print(f"[RedditResearch] ❌ Error in strategic research: {str(e)}")
            
            # Provide fallback data
            fallback_data = {
                "job_statement": f"Ajudar {target_description} a ter sucesso em seus objetivos profissionais",
                "functional_jobs": ["Economizar tempo", "Aumentar produtividade"],
                "emotional_jobs": ["Reduzir estresse", "Aumentar confiança"],
                "social_jobs": ["Ser reconhecido por pares", "Demonstrar competência"],
                "behaviors": {
                    "online": ["Pesquisa por soluções online", "Consome conteúdo educativo"],
                    "purchasing": ["Compara opções", "Busca recomendações"],
                    "content_consumption": ["Prefere conteúdo prático", "Consome em múltiplos formatos"]
                },
                "aspirations": [
                    f"Ser reconhecido como expert em {industry or 'seu campo'}",
                    "Alcançar equilíbrio entre vida pessoal e profissional"
                ],
                "goals": ["Aumentar visibilidade online", "Melhorar conversões", "Desenvolver habilidades técnicas"],
                "demographics": {
                    "age": "30-45 anos",
                    "location": "Centros urbanos",
                    "education": "Ensino superior completo",
                    "income": "Classe média a alta",
                    "occupation": "Profissional"
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
                    "is_fallback": True,
                    "error": str(e)
                }
            }
            
            if industry:
                fallback_data["research_data"]["industry"] = industry
            if additional_context:
                fallback_data["research_data"]["additional_context"] = additional_context
                
            # Cache o resultado de fallback também
            self._set_cache_result(cache_key, fallback_data)
            
            return fallback_data

# Singleton instance
reddit_research = RedditResearchEngine()
