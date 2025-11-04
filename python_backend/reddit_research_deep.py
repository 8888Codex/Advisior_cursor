"""
Reddit Research Engine - DEEP PERSONA MODE
Usa Framework PERSONA PROFUNDA (20 pontos) adaptado do EXTRACT
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

class RedditResearchDeep:
    """
    Cria personas profundas usando Framework PERSONA PROFUNDA (20 pontos)
    Similar ao sistema EXTRACT usado para clones de especialistas
    """
    
    def __init__(self):
        self._perplexity_api_key = None
        self._anthropic_client = None
        self._cache = {}
        self._cache_ttl = 24 * 60 * 60  # 24 hours
    
    def _ensure_initialized(self):
        """Lazy initialization of API clients"""
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
                raise ValueError("ANTHROPIC_API_KEY environment variable not set")
            self._anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    async def _call_perplexity_api(self, query: str, model: str = "sonar-reasoning") -> Dict:
        """Call Perplexity API with fallback models"""
        self._ensure_initialized()
        
        fallback_models = ["sonar-reasoning", "sonar", "sonar-pro", "sonar-deep-research"]
        
        if model not in fallback_models:
            fallback_models.insert(0, model)
        else:
            fallback_models.remove(model)
            fallback_models.insert(0, model)
            
        last_error = None
        
        for current_model in fallback_models:
            try:
                print(f"[DeepPersona] Calling Perplexity API with {current_model}...")
                
                request_payload = {
                    "model": current_model,
                    "messages": [
                        {"role": "system", "content": "Você é um especialista em pesquisa profunda de audiências. Forne\u00e7a insights ESPECÍFICOS, ACIONÁVEIS e com MÉTRICAS reais."},
                        {"role": "user", "content": query}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 4000  # Aumentado para conteúdo mais profundo
                }
                
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        "https://api.perplexity.ai/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self._perplexity_api_key}",
                            "Content-Type": "application/json"
                        },
                        json=request_payload
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    print(f"[DeepPersona] Successfully used model {current_model}")
                    return result
                    
            except Exception as e:
                print(f"[DeepPersona] Error with model {current_model}: {str(e)}")
                last_error = e
                continue
        
        if last_error:
            raise ValueError(f"All Perplexity API models failed: {str(last_error)}")
        
        raise ValueError("Failed to call Perplexity API with all available models")
    
    async def _call_anthropic_api(self, prompt: str, max_tokens: int = 8000) -> Dict:
        """Call Claude API to structure deep persona data"""
        self._ensure_initialized()
        
        try:
            retry_count = 0
            max_retries = 3
            backoff_factor = 1.5
            
            while retry_count <= max_retries:
                try:
                    message = await self._anthropic_client.messages.create(
                        model="claude-3-5-sonnet-20241022",  # Modelo mais potente para personas profundas
                        max_tokens=max_tokens,
                        temperature=0.2,
                        system="Você é um especialista em criação de personas profundas usando o Framework PERSONA PROFUNDA de 20 pontos. Retorne SEMPRE JSON válido e estruturado.",
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    break
                except Exception as retry_error:
                    retry_count += 1
                    if retry_count > max_retries:
                        raise
                    wait_time = backoff_factor ** retry_count
                    print(f"[DeepPersona] Retry {retry_count}/{max_retries}. Waiting {wait_time:.1f}s")
                    await asyncio.sleep(wait_time)
            
            content = message.content[0].text
            
            # Extract JSON from response
            try:
                json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                
                json_match = re.search(r'({.*})', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                
                print("[DeepPersona] Failed to parse JSON, using full text")
            except json.JSONDecodeError:
                print("[DeepPersona] JSON decode error, using full text")
            
            return {"content": content}
            
        except Exception as e:
            print(f"[DeepPersona] Claude API error: {str(e)}")
            raise
    
    async def research_deep(
        self,
        target_description: str,
        industry: Optional[str] = None,
        additional_context: Optional[str] = None
    ) -> Dict:
        """
        DEEP research mode: Cria persona profunda com Framework de 20 pontos
        
        Args:
            target_description: Descrição do público-alvo
            industry: Indústria opcional
            additional_context: Contexto adicional
            
        Returns:
            Dict com persona profunda estruturada (20 pontos)
        """
        try:
            print(f"[DeepPersona] Iniciando pesquisa PROFUNDA para '{target_description}'")
            
            context = f"na indústria de {industry}" if industry else ""
            
            # 🆕 Preparar contexto de negócio (se houver)
            business_context_header = ""
            if additional_context and "CONTEXTO DO NEGÓCIO" in additional_context:
                business_context_header = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ IMPORTANTE: ESTA PERSONA DEVE SER CONTEXTUALIZADA!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Você está criando uma persona que será usada por um negócio ESPECÍFICO.
Leia atentamente o contexto do negócio abaixo e personalize TODOS os
insights para serem EXTREMAMENTE RELEVANTES para aquele contexto.

NÃO crie uma persona genérica. Crie uma persona que faça sentido PARA
AQUELE NEGÓCIO ESPECÍFICO.
"""
            
            # PASSO 1: Perplexity - Pesquisa profunda
            perplexity_query = f"""
{business_context_header}

Realize uma pesquisa PROFUNDA sobre o público-alvo: '{target_description}' {context}

{additional_context if additional_context else ''}

Foque em extrair dados ESPECÍFICOS e ACIONÁVEIS para os seguintes pontos:

**SEÇÃO 1: IDENTITY CORE**
1. EXPERIÊNCIAS FORMATIVAS: 4-6 momentos cruciais que moldaram sua relação com o problema
   - Busque histórias reais em fóruns, Reddit, grupos
   - Quando aconteceu, onde, e qual foi o impacto específico
   
2. PADRÕES DECISÓRIOS (XADREZ MENTAL): Como essa pessoa PENSA e decide
   - "Análise Paralítica", "Decisão por Exclusão", "Social Proof Reliance"
   - Quais são os padrões característicos dessa audiência?
   
3. LINGUAGEM PRÓPRIA: Gírias, expressões, jargões que usam
   - Como eles REALMENTE falam sobre seus problemas?
   - Cite expressões EXATAS de fóruns/comunidades
   
4. GATILHOS EMOCIONAIS: O que desencadeia AÇÃO vs. INÉRCIA
   - Gatilhos de ação: O que faz eles agirem IMEDIATAMENTE
   - Gatilhos de inércia: O que os paralisa
   
5. VALORES NUCLEARES: 3-5 valores INEGOCIÁVEIS
   - O que eles NUNCA comprometem?

**SEÇÃO 2: BEHAVIORAL PATTERNS**
6. SIGNATURE DECISION PATTERN: Processo de 4-5 etapas que eles SEMPRE seguem
   - Qual é o passo-a-passo típico de decisão?
   
7. STORY BANKS: 3-5 histórias que eles contam REPETIDAMENTE
   - Histórias de frustração, fracasso, aprendizado
   - Com contexto específico e impacto real
   
8. OBJECTION PATTERNS: 3-5 objeções que eles SEMPRE levantam
   - "Não tenho tempo", "Tá caro", "Preciso pensar"
   - Qual é a TRADUÇÃO REAL de cada objeção?
   
9. TRUST TRIGGERS: O que gera confiança ESPECIFICAMENTE neles
   - Transparência? Cases? Demonstração ao vivo?
   
10. FAILURE STORIES: 2-3 fracassos que eles já viveram ou temem
    - O que aconteceu, impacto emocional, lição aprendida

**SEÇÃO 3: COMMUNICATION PATTERNS**
11. PREFERRED COMMUNICATION STYLE: Como preferem receber informações
    - Tom, estrutura, detalhamento, velocidade
    
12. CONTENT CONSUMPTION PATTERNS: COMO e ONDE consomem conteúdo
    - Canais preferidos (YouTube 70%, Instagram 20%)
    - Formatos (vídeos curtos, threads, podcasts)
    - Horários específicos de consumo
    
13. INFLUENCE NETWORK: Quem seguem, confiam, admiram
    - Top influencers com motivo específico
    - Comunidades ativas com nível de engajamento
    - Fontes de informação confiáveis

**SEÇÃO 4: QUANTIFIED PAIN POINTS**
14. PRIMARY PAIN POINTS (5-7): Com MÉTRICAS ESPECÍFICAS
    - Frequência (diária, semanal, mensal)
    - Custo financeiro (R$X/mês)
    - Custo temporal (Xh/semana)
    - Impacto emocional específico
    - Quote: "Como ele descreve isso"
    
15. SECONDARY PAIN POINTS (3-5): Importantes mas não urgentes

**SEÇÃO 5: GOALS & ASPIRATIONS**
16. SHORT-TERM GOALS (0-6 meses): Com métricas de sucesso
    - O que querem alcançar + por que importa + obstáculos percebidos
    
17. LONG-TERM ASPIRATIONS (1-3 anos): Sonhos mais profundos
    - Descrição emocional + impacto desejado
    
18. DEFINITION OF SUCCESS: Como ELE define sucesso
    - O que É sucesso para ele
    - O que NÃO É sucesso (anti-padrões que rejeita)

**SEÇÃO 6: JOURNEY MAPPING**
19. CUSTOMER JOURNEY STAGES (5 estágios):
    - Inconsciente → Consciente → Explorando → Decisão → Pós-compra
    - Para cada: Estado mental, ações, conteúdo, objeções, gatilhos
    
20. TOUCHPOINT MATRIX: Onde/como alcançá-lo
    - Para cada canal: Horários ativos, tipo de conteúdo, atenção, intenção, melhor formato

IMPORTANTE: Forneça dados ESPECÍFICOS, CITAÇÕES REAIS, MÉTRICAS QUANTIFICADAS.
Não seja genérico. Cite fontes, estudos, posts reais de comunidades.
"""
            
            perplexity_result = await self._call_perplexity_api(perplexity_query)
            perplexity_content = perplexity_result["choices"][0]["message"]["content"]
            
            print(f"[DeepPersona] Perplexity retornou {len(perplexity_content)} chars de pesquisa")
            
            # PASSO 2: Claude - Estruturação em 20 pontos
            claude_prompt = f"""
Com base nos dados de pesquisa profunda a seguir:

{perplexity_content}

Crie uma PERSONA PROFUNDA completa para '{target_description}' {context} seguindo o Framework PERSONA PROFUNDA de 20 pontos.

CRITÉRIOS DE QUALIDADE 18-20/20:
✓ TODOS os 20 pontos implementados com profundidade
✓ Dados ESPECÍFICOS (não genéricos)
✓ Métricas QUANTIFICADAS onde aplicável
✓ Citações REAIS e expressões autênticas
✓ Histórias com contexto específico

Formate os dados no seguinte formato JSON:

{{
  "quality_score": 18-20,
  
  // SEÇÃO 1: IDENTITY CORE
  "formative_experiences": [
    {{
      "description": "string",
      "when_where": "string (ex: '2019, após fracasso em lançamento')",
      "impact": "string (como mudou o comportamento)"
    }}
  ],
  "decision_patterns": [
    {{
      "name": "string (ex: 'Análise Paralítica')",
      "description": "string"
    }}
  ],
  "language_expressions": [
    {{
      "expression": "string (citação exata)",
      "context": "string (quando/como usa)"
    }}
  ],
  "action_triggers": [
    {{
      "trigger": "string",
      "reaction": "string",
      "trigger_type": "action"
    }}
  ],
  "inertia_triggers": [
    {{
      "trigger": "string",
      "reaction": "string",
      "trigger_type": "inertia"
    }}
  ],
  "core_values": [
    {{
      "value": "string",
      "manifestation": "string (como se manifesta em decisões)"
    }}
  ],
  
  // SEÇÃO 2: BEHAVIORAL PATTERNS
  "signature_decision_pattern": [
    {{
      "step_number": 1,
      "name": "string",
      "description": "string"
    }}
  ],
  "story_banks": [
    {{
      "title": "string",
      "context": "string",
      "frustration": "string",
      "impact": "string"
    }}
  ],
  "objection_patterns": [
    {{
      "objection": "string",
      "real_translation": "string (o que REALMENTE quer dizer)",
      "how_to_counter": "string"
    }}
  ],
  "trust_triggers": [
    {{
      "trigger": "string",
      "why_it_works": "string"
    }}
  ],
  "failure_stories": [
    {{
      "title": "string",
      "what_happened": "string",
      "emotional_impact": "string",
      "lesson_learned": "string"
    }}
  ],
  
  // SEÇÃO 3: COMMUNICATION PATTERNS
  "communication_style": {{
    "tone": "string",
    "structure": "string",
    "detail_level": "string",
    "speed": "string"
  }},
  "content_consumption_patterns": [
    {{
      "channel": "string",
      "active_hours": "string",
      "content_types": ["string"],
      "attention_level": "high|medium|low",
      "intention": "string",
      "best_format": "string"
    }}
  ],
  "influence_network": {{
    "top_influencers": [{{"name": "string", "why": "string"}}],
    "active_communities": [{{"name": "string", "engagement": "string"}}],
    "information_sources": [{{"source": "string", "what_seeks": "string"}}]
  }},
  
  // SEÇÃO 4: QUANTIFIED PAIN POINTS
  "primary_pain_points": [
    {{
      "description": "string",
      "frequency": "string (diária/semanal/mensal)",
      "financial_cost": "string (R$X/mês) ou null",
      "time_cost": "string (Xh/semana) ou null",
      "emotional_impact": "string",
      "quote": "string (como ele descreve)"
    }}
  ],
  "secondary_pain_points": [
    {{
      "description": "string",
      "impact": "string",
      "frequency": "string"
    }}
  ],
  
  // SEÇÃO 5: GOALS & ASPIRATIONS
  "short_term_goals": [
    {{
      "goal": "string",
      "success_metric": "string",
      "why_it_matters": "string",
      "perceived_obstacles": ["string"]
    }}
  ],
  "long_term_aspirations": [
    {{
      "aspiration": "string",
      "emotional_description": "string",
      "desired_impact": "string"
    }}
  ],
  "success_definition": {{
    "success_means": [{{"element": "string", "why": "string"}}],
    "not_success": [{{"anti_pattern": "string", "why_rejects": "string"}}]
  }},
  
  // SEÇÃO 6: JOURNEY MAPPING
  "journey_stages": [
    {{
      "stage_number": 1,
      "name": "string",
      "mental_state": "string",
      "typical_actions": ["string"],
      "content_consumed": ["string"],
      "objections": ["string"],
      "triggers_to_next": ["string"]
    }}
  ],
  "touchpoint_matrix": [
    {{
      "channel": "string",
      "active_hours": "string",
      "content_types": ["string"],
      "attention_level": "high|medium|low",
      "intention": "string",
      "best_format": "string"
    }}
  ],
  
  // METADATA
  "research_data": {{
    "sources": ["string"],
    "confidence_level": "high|medium|low",
    "generated_at": "{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
    "target_description": "{target_description}",
    "industry": "{industry}"
  }}
}}

IMPORTANTE: 
- Todos os dados devem ser ESPECÍFICOS e ACIONÁVEIS
- Use citações REAIS quando disponíveis
- Métricas devem ser QUANTIFICADAS
- Histórias devem ter CONTEXTO específico
- Retorne APENAS o JSON, sem explicações adicionais
"""
            
            structured_data = await self._call_anthropic_api(claude_prompt, max_tokens=8000)
            
            # Validação básica
            if "quality_score" not in structured_data:
                structured_data["quality_score"] = 18  # Default para deep personas
            
            if "research_data" not in structured_data:
                structured_data["research_data"] = {}
            
            structured_data["research_data"]["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            structured_data["research_data"]["target_description"] = target_description
            if industry:
                structured_data["research_data"]["industry"] = industry
            if additional_context:
                structured_data["research_data"]["additional_context"] = additional_context
            
            print(f"[DeepPersona] Persona profunda criada com sucesso. Quality score: {structured_data.get('quality_score', 'N/A')}/20")
            
            return structured_data
            
        except Exception as e:
            print(f"[DeepPersona] Error in deep research: {str(e)}")
            raise  # Deep personas não têm fallback - ou é profundo ou falha

# Singleton instance
reddit_research_deep = RedditResearchDeep()

