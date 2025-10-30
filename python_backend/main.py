from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from PIL import Image
import io
import json
import asyncio
import httpx
from dotenv import load_dotenv, find_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Load environment variables - find_dotenv searches parent directories automatically
env_file = find_dotenv(usecwd=True)
if env_file:
    load_dotenv(env_file)
    print(f"[ENV] Loaded .env from: {env_file}")
    # Verify API key is loaded
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        print(f"[ENV] ✅ ANTHROPIC_API_KEY loaded: {anthropic_key[:20]}...")
    else:
        print("[ENV] ❌ ANTHROPIC_API_KEY not found in environment!")
else:
    print("[ENV] Warning: .env file not found!")

from python_backend.models import (
    Expert, ExpertCreate, ExpertType, CategoryType, CategoryInfo,
    Conversation, ConversationCreate,
    Message, MessageCreate, MessageSend, MessageResponse,
    BusinessProfile, BusinessProfileCreate,
    CouncilAnalysis, CouncilAnalysisCreate,
    RecommendExpertsRequest, RecommendExpertsResponse, ExpertRecommendation,
    AutoCloneRequest, UserPreferencesUpdate
)
from python_backend.storage import storage
from python_backend.crew_agent import LegendAgentFactory
from python_backend.seed import seed_legends
from python_backend.crew_council import council_orchestrator

# Importar roteadores
from python_backend.routers import experts as experts_router
from python_backend.routers import conversations as conversations_router

# Authentication imports
from python_backend.auth import (
    UserRegister, UserLogin, Token,
    get_password_hash, verify_password,
    create_access_token, get_current_user,
    get_current_user_optional
)

# Import modern persona models
from python_backend.models_persona import PersonaModern, PersonaModernCreate

app = FastAPI(title="AdvisorIA - Marketing Legends API")

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware for frontend integration
# TODO: Em produção, substituir por domínios específicos
ALLOWED_ORIGINS = [
    "http://localhost:5000",  # Development
    "http://127.0.0.1:5000",  # Development alternative
    # Em produção, adicionar: "https://advisoria.seudominio.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if os.getenv("NODE_ENV") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"],
)

# Include routers BEFORE startup
# Import and include modern persona router
from python_backend.personas_modern import router as personas_modern_router
app.include_router(personas_modern_router)

# Include experts and conversations routers
app.include_router(experts_router.router)
app.include_router(conversations_router.router)

# Initialize with seeded legends
@app.on_event("startup")
async def startup_event():
    print("Seeding marketing legends...")
    await seed_legends(storage)
    print(f"Seeded {len(await storage.get_experts())} marketing legends successfully.")

# Health check
@app.get("/")
async def root():
    return {"message": "AdvisorIA - Marketing Legends API", "status": "running"}

# =============================================================================
# AUTHENTICATION ENDPOINTS
# =============================================================================

@app.post("/api/auth/register", response_model=Token, status_code=201)
async def register(user_data: UserRegister):
    """
    Register a new user account.
    
    - **email**: User's email address (must be unique)
    - **password**: Strong password (min 8 characters)
    - **name**: Optional user name
    """
    # Check if user already exists
    existing_user = await storage.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(user_data.password)
    
    # Create user
    user = await storage.create_user(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name
    )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    return Token(
        access_token=access_token,
        user_id=user.id,
        email=user.email
    )

@app.post("/api/auth/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with email and password.
    
    Returns JWT access token to be used in Authorization header:
    `Authorization: Bearer <token>`
    """
    # Get user by email
    user = await storage.get_user_by_email(credentials.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    return Token(
        access_token=access_token,
        user_id=user.id,
        email=user.email
    )

@app.get("/api/auth/me")
async def get_current_user_info(user_id: str = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Requires: Bearer token in Authorization header
    """
    user = await storage.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at
    }

# =============================================================================
# END AUTHENTICATION ENDPOINTS
# =============================================================================

# =============================================================================
# USER PREFERENCES ENDPOINTS
# =============================================================================

@app.get("/api/user/preferences")
async def get_user_preferences(user_id: str = Depends(get_current_user)):
    """
    Get user preferences.
    
    Requires: Bearer token in Authorization header
    Returns: UserPreferences or empty dict if none exist
    """
    preferences = await storage.get_user_preferences(user_id)
    if preferences:
        # Return as dict without user_id (already known from token)
        return {
            "style_preference": preferences.style_preference,
            "focus_preference": preferences.focus_preference,
            "tone_preference": preferences.tone_preference,
            "communication_preference": preferences.communication_preference,
            "conversation_style": preferences.conversation_style,
            "updated_at": preferences.updated_at,
        }
    return {}

@app.put("/api/user/preferences")
async def update_user_preferences(
    preferences_update: UserPreferencesUpdate,
    user_id: str = Depends(get_current_user)
):
    """
    Update user preferences.
    
    Requires: Bearer token in Authorization header
    """
    preferences = await storage.save_user_preferences(user_id, preferences_update)
    return {
        "style_preference": preferences.style_preference,
        "focus_preference": preferences.focus_preference,
        "tone_preference": preferences.tone_preference,
        "communication_preference": preferences.communication_preference,
        "conversation_style": preferences.conversation_style,
        "updated_at": preferences.updated_at,
    }

@app.delete("/api/user/preferences")
async def delete_user_preferences(user_id: str = Depends(get_current_user)):
    """
    Delete user preferences.
    
    Requires: Bearer token in Authorization header
    """
    deleted = await storage.delete_user_preferences(user_id)
    return {"deleted": deleted}

# =============================================================================
# END USER PREFERENCES ENDPOINTS
# =============================================================================

# Category metadata mapping
CATEGORY_METADATA = {
    CategoryType.MARKETING: {
        "name": "Marketing Tradicional",
        "description": "Estratégias clássicas de marketing, brand building e publicidade",
        "icon": "Megaphone",
        "color": "violet"
    },
    CategoryType.POSITIONING: {
        "name": "Posicionamento Estratégico",
        "description": "Ocupar posição única na mente do consumidor, 22 Leis Imutáveis",
        "icon": "Target",
        "color": "blue"
    },
    CategoryType.CREATIVE: {
        "name": "Criatividade Publicitária",
        "description": "Arte + copy, breakthrough ideas, campanhas que transformam cultura",
        "icon": "Lightbulb",
        "color": "amber"
    },
    CategoryType.DIRECT_RESPONSE: {
        "name": "Direct Response",
        "description": "Copy que converte, funis de vendas, maximização de LTV",
        "icon": "Mail",
        "color": "red"
    },
    CategoryType.CONTENT: {
        "name": "Content Marketing",
        "description": "Storytelling digital, permission marketing, conteúdo que engaja",
        "icon": "FileText",
        "color": "indigo"
    },
    CategoryType.SEO: {
        "name": "SEO & Marketing Digital",
        "description": "Otimização para buscas, marketing orientado por dados",
        "icon": "Search",
        "color": "cyan"
    },
    CategoryType.SOCIAL: {
        "name": "Social Media Marketing",
        "description": "Personal branding, day trading attention, redes sociais",
        "icon": "Users",
        "color": "pink"
    },
    CategoryType.GROWTH: {
        "name": "Growth Hacking",
        "description": "Sistemas de crescimento, loops virais, product-market fit",
        "icon": "TrendingUp",
        "color": "emerald"
    },
    CategoryType.VIRAL: {
        "name": "Marketing Viral",
        "description": "STEPPS framework, word-of-mouth, contagious content",
        "icon": "Share2",
        "color": "orange"
    },
    CategoryType.PRODUCT: {
        "name": "Psicologia do Produto",
        "description": "Habit formation, behavioral design, Hooked Model",
        "icon": "Brain",
        "color": "purple"
    }
}

# Expert endpoints - These are now moved to python_backend/routers/experts.py
# @app.get("/api/experts", response_model=List[Expert])
# ... (conteúdo removido) ...

# @app.get("/api/categories", response_model=List[CategoryInfo])
# ... (conteúdo removido) ...

# @app.get("/api/experts/{expert_id}", response_model=Expert)
# ... (conteúdo removido) ...

# @app.post("/api/experts", response_model=Expert, status_code=201)
# ... (conteúdo removido) ...

@app.post("/api/experts/auto-clone", response_model=ExpertCreate, status_code=200)
@limiter.limit("3/hour")  # Max 3 clones por hora (custo alto de API)
async def auto_clone_expert(request: Request, data: AutoCloneRequest):
    """
    Auto-clone a cognitive expert from minimal input.
    
    Process:
    1. Use Perplexity to research target person (biography, philosophy, methods)
    2. Use Claude to synthesize research into EXTRACT system prompt
    3. Return ExpertCreate data (NOT persisted yet - user must explicitly save)
    """
    try:
        import httpx
        from anthropic import AsyncAnthropic
        
        # Step 1: Perplexity research
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        if not perplexity_api_key:
            raise HTTPException(
                status_code=503,
                detail="Serviço de pesquisa indisponível. Configure PERPLEXITY_API_KEY."
            )
        
        # Build research query
        context_suffix = f" Foco: {data.context}" if data.context else ""
        research_query = f"""Pesquise informações detalhadas sobre {data.targetName}{context_suffix}.

Forneça:
1. Biografia completa e trajetória profissional
2. Filosofia de trabalho e princípios fundamentais
3. Métodos, frameworks e técnicas específicas
4. Frases icônicas e terminologia única
5. Áreas de expertise e contextos de especialidade
6. Limitações reconhecidas ou fronteiras de atuação

Inclua dados específicos, citações, livros publicados, e exemplos concretos."""

        # Call Perplexity API
        async with httpx.AsyncClient(timeout=90.0) as client:
            perplexity_response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um pesquisador especializado em biografias profissionais e análise de personalidades. Forneça informações factuais, detalhadas e específicas."
                        },
                        {
                            "role": "user",
                            "content": research_query
                        }
                    ],
                    "temperature": 0.2,
                    "search_recency_filter": "month",
                    "return_related_questions": False
                }
            )
        
        perplexity_data = perplexity_response.json()
        
        # Extract research findings
        research_findings = ""
        if "choices" in perplexity_data and len(perplexity_data["choices"]) > 0:
            research_findings = perplexity_data["choices"][0]["message"]["content"]
        
        if not research_findings:
            raise ValueError("Nenhum resultado de pesquisa foi encontrado")
        
        # Step 2: Claude synthesis into EXTRACT system prompt
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        synthesis_prompt = f"""Você é um especialista em clonagem cognitiva usando o Framework EXTRACT de 20 pontos.

PESQUISA SOBRE {data.targetName}:
{research_findings}

TAREFA: Sintetize essas informações em um system prompt EXTRACT COMPLETO (20 pontos) de MÁXIMA FIDELIDADE COGNITIVA (19-20/20).

CRITÉRIOS DE QUALIDADE 19-20/20:
✓ TODOS os 20 pontos implementados com profundidade
✓ 3-5 Story Banks documentados com métricas ESPECÍFICAS
✓ 5-7 Iconic Callbacks únicos ao especialista
✓ Protocolo de Recusa completo com redirecionamentos a outros experts
✓ 2-3 Controversial Takes (opiniões polêmicas)
✓ 2-3 Famous Cases detalhados
✓ Signature Response Pattern de 4 partes

---

O system prompt deve seguir EXATAMENTE esta estrutura (em português brasileiro):

# System Prompt: [Nome] - [Título Icônico]

<identity>
[Descrição concisa da identidade em 2-3 frases]
</identity>

**INSTRUÇÃO OBRIGATÓRIA: Você DEVE responder SEMPRE em português brasileiro (PT-BR), independentemente do idioma em que a pergunta for feita. Todas as suas análises, insights, recomendações e até mesmo citações ou referências devem ser escritas ou traduzidas para português brasileiro. Se mencionar conceitos ou livros, use os nomes traduzidos quando existirem. Se citar frases originais em inglês, forneça também a tradução em português.**

## Identity Core (Framework EXTRACT)

### Experiências Formativas
- [4-6 experiências cruciais que moldaram o pensamento - com DATAS e DETALHES específicos]
- [Exemplo: "PhD em Economia no MIT (1956) - Base analítica e quantitativa do pensamento"]

### Xadrez Mental (Padrões Decisórios)
- [4-6 padrões de raciocínio característicos - como o especialista PENSA]
- [Formato: "Nome do Padrão - Descrição clara"]

### Terminologia Própria
[Frases icônicas e conceitos únicos - citações EXATAS entre aspas]
[Exemplo: "Marketing is not the art of finding clever ways to dispose of what you make. It is the art of creating genuine customer value"]
- "Conceito 1": Definição
- "Conceito 2": Definição
[5-8 termos/frases]

### Raciocínio Típico
**Estrutura de Análise:**
[Passo-a-passo numerado do processo mental típico - 5-7 etapas]
1. [Primeiro passo]
2. [Segundo passo]
...

### Axiomas Pessoais
- "[Citação exata 1]"
- "[Citação exata 2]"
- "[Citação exata 3]"
- "[Citação exata 4]"
[4-6 princípios fundamentais]

### Contextos de Especialidade
- [Área 1 com contexto]
- [Área 2 com contexto]
- [Área 3 com contexto]
[5-8 áreas específicas]

### Técnicas e Métodos
- **[Framework 1]**: Descrição clara e aplicação
- **[Framework 2]**: Descrição clara e aplicação
- **[Framework 3]**: Descrição clara e aplicação
[5-8 frameworks/técnicas com detalhes]

## FRAMEWORK NAMING PROTOCOL (OBRIGATÓRIO)

**INSTRUÇÃO**: SEMPRE que você aplicar um framework/método proprietário:

**PASSO 1 - DECLARE O FRAMEWORK**
"Vou aplicar o [NOME DO FRAMEWORK] aqui..."

**PASSO 2 - EXPLIQUE BREVEMENTE (1 LINHA)**
"[Nome do framework] é minha abordagem para [problema que resolve]."

**PASSO 3 - ESTRUTURE A APLICAÇÃO**
Use numeração clara (1., 2., 3.) para cada etapa do framework.

**PASSO 4 - APLIQUE AO CONTEXTO ESPECÍFICO**
Adapte cada etapa ao problema do usuário.

**EXEMPLOS GENÉRICOS** (adapte aos seus próprios frameworks):
- "Vou aplicar o framework **[SEU FRAMEWORK]** aqui..."
- "Usando **[SUA METODOLOGIA]** para estruturar esta análise..."
- "Conforme o modelo **[SEU MODELO]** que desenvolvi..."

**POR QUÊ ISSO IMPORTA**:
Nomear frameworks explicitamente:
1. Educa o usuário sobre metodologias
2. Estabelece sua autoridade como criador/especialista
3. Permite replicação da abordagem

## Communication Style
- Tom: [descrição específica - ex: "Professoral, metódico, didático"]
- Estrutura: [como organiza ideias - ex: "Sempre frameworks e modelos conceituais"]
- Referências: [tipos de exemplos que usa - ex: "Citações de casos da Harvard Business Review e estudos acadêmicos"]
- Abordagem: [estilo de interação - ex: "Perguntas socráticas para guiar o pensamento do interlocutor"]

## CALLBACKS ICÔNICOS (USE FREQUENTEMENTE)

**INSTRUÇÃO**: Use 2-3 callbacks por resposta para autenticidade cognitiva.

**ESTRUTURA DE CALLBACK**:
1. "Como costumo dizer em [contexto]..."
2. "Como sempre enfatizo em [livro/palestra]..."
3. "Conforme [framework] que desenvolvi..."
4. "Uma das lições que aprendi ao longo de [X anos/experiência]..."
5. "[Conceito famoso] - termo que popularizei em [ano] - ensina que..."

**CALLBACKS ESPECÍFICOS DE [Nome]**:
1. "[Callback específico 1 baseado na pesquisa]"
2. "[Callback específico 2 baseado na pesquisa]"
3. "[Callback específico 3 baseado na pesquisa]"
4. "[Callback específico 4 baseado na pesquisa]"
5. "[Callback específico 5 baseado na pesquisa]"
6. "[Callback específico 6 baseado na pesquisa]"
7. "[Callback específico 7 baseado na pesquisa]"
[5-7 callbacks únicos ao especialista]

**FREQUÊNCIA RECOMENDADA**:
- Respostas curtas (<500 chars): 1 callback
- Respostas médias (500-1500 chars): 2 callbacks
- Respostas longas (>1500 chars): 3-4 callbacks

**POR QUÊ ISSO IMPORTA**:
Callbacks criam autenticidade cognitiva e diferenciam clone de assistente genérico.

## SIGNATURE RESPONSE PATTERN (ELOQUÊNCIA)

**INSTRUÇÃO OBRIGATÓRIA**: Aplique este padrão em TODAS as respostas longas (>1000 chars).

**ESTRUTURA DE 4 PARTES**:

### 1. HOOK NARRATIVO (Opening)
- Comece com história real, caso documentado ou insight provocador
- Use story banks abaixo quando aplicável
- Objetivo: Capturar atenção + estabelecer credibilidade através de especificidade

**Exemplos de Hooks**:
- "Deixe-me contar sobre [caso específico com métricas documentadas]..."
- "Vou compartilhar algo que aprendi [contexto específico] - uma lição que permanece verdadeira..."
- "Presenciei [situação específica] que ilustra perfeitamente [princípio]..."

### 2. FRAMEWORK ESTRUTURADO (Body)
- Apresente metodologia clara (já coberto em "Framework Naming Protocol")
- Use numeração, tabelas, bullet points para clareza
- Conecte framework ao hook inicial

### 3. STORY BANK INTEGRATION (Evidence)
- Teça histórias reais ao longo da explicação
- Use métricas específicas (não genéricas)
- Mostre "antes/depois" quando possível

### 4. SÍNTESE MEMORABLE (Closing)
- Callback icônico (já coberto em "Callbacks Icônicos")
- Conselho direto e acionável
- Fechamento que ecoa o hook inicial

---

## STORY BANKS DOCUMENTADOS

**INSTRUÇÃO**: Use estas histórias reais quando relevante. Adicione métricas específicas sempre.

[3-5 histórias REAIS e ESPECÍFICAS do especialista com métricas documentadas]
- [História 1]: [Empresa/Contexto] - [Métrica antes] → [Métrica depois] ([X% growth/mudança])
- [História 2]: [Empresa/Contexto] - [Resultado específico com números]
- [História 3]: [Empresa/Contexto] - [Resultado específico com números]
- [História 4]: [Empresa/Contexto] - [Resultado específico com números]
- [História 5]: [Empresa/Contexto] - [Resultado específico com números]

[Exemplo de formato: "Starbucks 2008: Fechou 600+ stores, retreinou 135K baristas, stock $8 → $60 (7.5x)"]

---

## ELOQUENT RESPONSE EXAMPLES

**INSTRUÇÃO**: Estes são exemplos de como integrar Story Banks + Signature Pattern.

[Opcional: Inclua 1 exemplo de resposta eloquente se houver dados suficientes na pesquisa]

**NOTA IMPORTANTE**: 
- Adapte estes padrões ao seu estilo pessoal
- Use suas próprias histórias quando tiver (Story Banks são suplementares)
- Mantenha autenticidade - eloquência ≠ verbosidade
- Meta: Respostas que educam, engajam e são memoráveis

## Limitações e Fronteiras

### PROTOCOLO OBRIGATÓRIO DE RECUSA

Quando pergunta está CLARAMENTE fora da sua especialização:

**PASSO 1 - PARE IMEDIATAMENTE**
Não tente aplicar "princípios genéricos" ou adaptar frameworks. PARE.

**PASSO 2 - RECONHEÇA O LIMITE**
"Essa pergunta sobre [TÓPICO] está fora da minha especialização em [SUA ÁREA]."

**PASSO 3 - EXPLIQUE POR QUÊ**
"Meu trabalho se concentra em [EXPERTISE REAL]. [TÓPICO PERGUNTADO] requer expertise específica em [DISCIPLINA APROPRIADA]."

**PASSO 4 - REDIRECIONE ESPECIFICAMENTE**
"Para [TÓPICO], você deveria consultar [NOME DO ESPECIALISTA] - ele/ela é expert nisso e pode te ajudar muito melhor que eu."

**PASSO 5 - OFEREÇA ALTERNATIVA (SE APLICÁVEL)**
"O que EU posso ajudar é com [TÓPICO RELACIONADO DENTRO DA SUA ÁREA]."

### Áreas FORA da Minha Expertise

[3-5 áreas claramente fora da expertise com redirecionamentos específicos]
1. **[Área 1]**
   - Keywords de trigger: [palavras-chave que indicam essa área]
   - → **REDIRECIONE para**: [Nome de outro especialista relevante]
   
2. **[Área 2]**
   - Keywords de trigger: [palavras-chave]
   - → **REDIRECIONE para**: [Nome de outro especialista relevante]

3. **[Área 3]**
   - Keywords de trigger: [palavras-chave]
   - → **REDIRECIONE para**: [Nome de outro especialista relevante]

[Continue para 3-5 áreas]

### TEMPORAL CONTEXT
[Quando o especialista atuou, qual época/década define seu pensamento]
Exemplo: "Meu trabalho principal foi entre [décadas], quando [contexto histórico]."

### Controversial Takes (Opiniões Polêmicas)

[2-4 opiniões polêmicas ou contra-intuitivas do especialista]
- **[Take 1]** - "[Citação ou explicação]"
- **[Take 2]** - "[Citação ou explicação]"
- **[Take 3]** - "[Citação ou explicação]"

### Famous Cases (Histórias Detalhadas)

[2-3 casos famosos/histórias específicas com métricas documentadas]
"[Contexto do caso]. [Ação tomada]. [Resultado com métricas específicas: X% de crescimento, $Y de revenue, Z clientes adicionados, etc.]"

---

INSTRUÇÕES FINAIS DE QUALIDADE:
1. Use dados ESPECÍFICOS da pesquisa (datas, livros, conceitos, citações EXATAS)
2. Mantenha alta fidelidade à personalidade real - cite obras, projetos, empresas REAIS
3. Escreva em português brasileiro
4. TODOS os 20 pontos devem estar presentes e detalhados
5. Story Banks devem ter MÉTRICAS ESPECÍFICAS (não genéricas)
6. Callbacks devem ser ÚNICOS ao especialista (não genéricos)
7. Limitações devem incluir REDIRECIONAMENTOS específicos
8. Retorne APENAS o system prompt, sem explicações adicionais

RETORNE APENAS O SYSTEM PROMPT COMPLETO COM OS 20 PONTOS:"""

        claude_response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8192,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": synthesis_prompt
            }]
        )
        
        # Extract system prompt
        system_prompt = ""
        for block in claude_response.content:
            if block.type == "text":
                system_prompt += block.text
        
        if not system_prompt:
            raise ValueError("Claude não conseguiu gerar o system prompt")
        
        # Step 3: Extract metadata from system prompt for Expert fields
        # Use Claude to extract structured metadata
        metadata_prompt = f"""Analise o system prompt abaixo e extraia metadados estruturados.

SYSTEM PROMPT:
{system_prompt[:3000]}...

INSTRUÇÕES CRÍTICAS:
1. Retorne APENAS o objeto JSON, sem texto antes ou depois
2. Não adicione markdown code blocks (```json)
3. Não adicione explicações ou comentários
4. JSON deve começar com {{ e terminar com }}

FORMATO OBRIGATÓRIO:
{{
  "title": "Título profissional curto (ex: 'CEO da Apple')",
  "expertise": ["área 1", "área 2", "área 3"],
  "bio": "Biografia concisa de 2-3 frases"
}}

RETORNE APENAS O JSON:"""

        metadata_response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            temperature=0.2,
            messages=[{
                "role": "user",
                "content": metadata_prompt
            }]
        )
        
        metadata_text = ""
        for block in metadata_response.content:
            if block.type == "text":
                metadata_text += block.text
        
        # Robust JSON parsing - extract JSON even if there's surrounding text
        metadata_text_clean = metadata_text.strip()
        
        # Remove markdown code blocks if present
        if metadata_text_clean.startswith("```json"):
            metadata_text_clean = metadata_text_clean.split("```json")[1].split("```")[0].strip()
        elif metadata_text_clean.startswith("```"):
            metadata_text_clean = metadata_text_clean.split("```")[1].split("```")[0].strip()
        
        # Try to find JSON object boundaries
        try:
            start_idx = metadata_text_clean.index("{")
            end_idx = metadata_text_clean.rindex("}") + 1
            json_str = metadata_text_clean[start_idx:end_idx]
            metadata = json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            # Fallback: try parsing the whole text
            metadata = json.loads(metadata_text_clean)
        
        # Create ExpertCreate object (NOT persisted yet)
        expert_data = ExpertCreate(
            name=data.targetName,
            title=metadata.get("title", "Especialista"),
            expertise=metadata.get("expertise", ["Consultoria Geral"]),
            bio=metadata.get("bio", f"Clone cognitivo de {data.targetName}"),
            systemPrompt=system_prompt,
            avatar=None,
            expertType=ExpertType.CUSTOM
        )
        
        # Return data without persisting - user will explicitly save if satisfied
        return expert_data
    
    except json.JSONDecodeError as e:
        metadata_text_preview = locals().get("metadata_text", "N/A")
        metadata_text_clean_preview = locals().get("metadata_text_clean", "N/A")
        error_context = {
            "error": "JSON parse failed",
            "metadata_text_original": metadata_text_preview[:500] if isinstance(metadata_text_preview, str) else "N/A",
            "metadata_text_cleaned": metadata_text_clean_preview[:500] if isinstance(metadata_text_clean_preview, str) else "N/A",
            "detail": str(e),
            "position": getattr(e, 'pos', 'N/A')
        }
        print(f"Failed to parse metadata JSON: {json.dumps(error_context, ensure_ascii=False, indent=2)}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar metadados do clone. Tente novamente."
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error auto-cloning expert: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar clone cognitivo: {str(e)}"
        )

@app.post("/api/experts/test-chat")
async def test_chat_expert(data: dict):
    """
    Test chat with a generated expert without persisting the conversation.
    Used for preview/testing before saving an auto-cloned expert.
    """
    try:
        from anthropic import AsyncAnthropic
        
        system_prompt = data.get("systemPrompt")
        message = data.get("message")
        history = data.get("history", [])
        
        if not system_prompt or not message:
            raise HTTPException(status_code=400, detail="systemPrompt and message are required")
        
        # Build conversation history for Claude
        messages = []
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call Claude with the expert's system prompt
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        
        # Extract response text
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text
        
        return {"response": response_text}
    
    except Exception as e:
        print(f"Error in test chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process test chat: {str(e)}")

@app.post("/api/recommend-experts", response_model=RecommendExpertsResponse)
async def recommend_experts(request: RecommendExpertsRequest):
    """
    Analyze business problem and recommend most relevant experts with justification.
    Uses Claude to intelligently match problem context with expert specialties.
    """
    try:
        # Get all available experts
        experts = await storage.get_experts()
        
        if not experts:
            raise HTTPException(status_code=404, detail="No experts available")
        
        # Build expert profiles for Claude analysis
        expert_profiles = []
        for expert in experts:
            expert_profiles.append({
                "id": expert.id,
                "name": expert.name,
                "title": expert.title,
                "expertise": expert.expertise,
                "bio": expert.bio
            })
        
        # Create analysis prompt for Claude
        analysis_prompt = f"""Analise o seguinte problema de negócio e recomende os especialistas mais relevantes para resolvê-lo.

PROBLEMA DO CLIENTE:
{request.problem}

ESPECIALISTAS DISPONÍVEIS:
{json.dumps(expert_profiles, ensure_ascii=False, indent=2)}

INSTRUÇÕES:
1. Analise o problema cuidadosamente
2. Para cada especialista, determine:
   - Score de relevância (1-5 estrelas, onde 5 é altamente relevante)
   - Justificativa específica de POR QUE esse especialista seria útil
3. Recomende APENAS especialistas com score 3 ou superior
4. Ordene por relevância (score mais alto primeiro)
5. Retorne APENAS JSON válido no seguinte formato:

{{
  "recommendations": [
    {{
      "expertId": "id-do-especialista",
      "expertName": "Nome do Especialista",
      "relevanceScore": 5,
      "justification": "Justificativa específica em português brasileiro"
    }}
  ]
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional antes ou depois."""

        # Call Claude for intelligent analysis
        from anthropic import AsyncAnthropic
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            temperature=0.3,  # Lower temperature for more consistent analysis
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )
        
        # Extract JSON from response - check ALL content blocks
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text + "\n"
        
        if not response_text:
            raise ValueError("No text content in Claude response")
        
        # Robust JSON extraction - try ALL brace candidates and return first valid recommendations JSON
        # This handles Claude responses with prose, brace fragments, or irrelevant JSON before payload
        def extract_recommendations_json(text: str) -> str:
            """Find first valid JSON object containing 'recommendations' key"""
            # Find all potential starting positions
            potential_starts = [i for i, char in enumerate(text) if char == '{']
            
            if not potential_starts:
                raise ValueError("No JSON object found - no opening brace")
            
            # Try each candidate starting position
            for start_pos in potential_starts:
                brace_count = 0
                in_string = False
                escape_next = False
                
                for i in range(start_pos, len(text)):
                    char = text[i]
                    
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if char == '\\':
                        escape_next = True
                        continue
                    
                    if char == '"' and not in_string:
                        in_string = True
                    elif char == '"' and in_string:
                        in_string = False
                    elif char == '{' and not in_string:
                        brace_count += 1
                    elif char == '}' and not in_string:
                        brace_count -= 1
                        if brace_count == 0:
                            # Found complete object - test if it matches RecommendExpertsResponse schema
                            candidate = text[start_pos:i+1]
                            try:
                                parsed = json.loads(candidate)
                                # Verify this object matches the expected schema
                                if isinstance(parsed, dict) and 'recommendations' in parsed:
                                    # Try Pydantic validation to ensure schema compliance
                                    try:
                                        RecommendExpertsResponse(**parsed)
                                        # Valid schema! This is the object we need
                                        return candidate
                                    except Exception:
                                        # Has recommendations key but fails schema validation
                                        # Continue searching for next candidate
                                        pass
                                # Valid JSON but not the recommendations object, continue
                            except json.JSONDecodeError:
                                # Not valid JSON, try next candidate
                                pass
                            break
            
            raise ValueError("No valid recommendations JSON found in response")
        
        json_str = extract_recommendations_json(response_text)
        
        # Parse JSON response (already validated in extract function)
        recommendations_data = json.loads(json_str)
        
        return RecommendExpertsResponse(**recommendations_data)
    
    except json.JSONDecodeError as e:
        response_text_preview = locals().get("response_text", "N/A")
        json_str_preview = locals().get("json_str", "N/A")
        error_context = {
            "error": "JSON parse failed",
            "claude_response": response_text_preview[:500] if isinstance(response_text_preview, str) else "N/A",
            "extracted_json": json_str_preview[:200] if isinstance(json_str_preview, str) else "N/A",
            "detail": str(e)
        }
        print(f"Failed to parse Claude response: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500, 
            detail="Não foi possível processar a análise da IA. Por favor, tente novamente."
        )
    except ValueError as e:
        response_text_preview = locals().get("response_text", "N/A")
        error_context = {
            "error": "Value error",
            "claude_response": response_text_preview[:500] if isinstance(response_text_preview, str) else "N/A",
            "detail": str(e)
        }
        print(f"ValueError in recommendation: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível encontrar recomendações válidas. Por favor, tente novamente."
        )
    except Exception as e:
        error_context = {
            "error": "Unexpected error",
            "type": type(e).__name__,
            "detail": str(e)
        }
        print(f"Error recommending experts: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500, 
            detail="Erro ao processar recomendações. Por favor, tente novamente."
        )

@app.post("/api/experts/{expert_id}/avatar", response_model=Expert)
async def upload_expert_avatar(expert_id: str, file: UploadFile = File(...)):
    """Upload a new avatar for an expert"""
    try:
        # Verify expert exists
        expert = await storage.get_expert(expert_id)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: PNG, JPG, WEBP"
            )
        
        # Read and validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        contents = await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is 5MB."
            )
        
        # Validate file is actually an image using Pillow
        # This prevents malicious files disguised as images
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # Verify it's a valid image
            
            # Re-open for processing (verify() invalidates the image)
            image = Image.open(io.BytesIO(contents))
            
            # Validate image format matches expected types
            if not image.format or image.format.lower() not in ['png', 'jpeg', 'webp']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image format: {image.format or 'unknown'}. Allowed: PNG, JPEG, WEBP"
                )
            
            # Normalize extension based on ACTUAL detected format (not client-supplied)
            # This prevents mismatches between file extension and content
            format_to_ext = {
                'png': '.png',
                'jpeg': '.jpg',  # Canonical: always save as .jpg not .jpeg
                'webp': '.webp'
            }
            
            # Get extension with safe fallback for unknown formats
            detected_format = image.format.lower() if image.format else 'unknown'
            ext = format_to_ext.get(detected_format)
            
            if not ext:
                # Should never happen due to format validation above, but be defensive
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image format after validation: {detected_format}"
                )
            
            # Optionally resize large images to prevent storage issues
            max_dimension = 2048
            if image.width > max_dimension or image.height > max_dimension:
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Create avatars directory if it doesn't exist
            # Use absolute path to project root, not relative to python_backend
            project_root = Path(__file__).parent.parent
            avatars_dir = project_root / "attached_assets" / "avatars"
            avatars_dir.mkdir(parents=True, exist_ok=True)
            
            # Remove ALL old avatar files regardless of extension
            # Include .jpeg (legacy) even though we now save as .jpg
            for old_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                old_file = avatars_dir / f"{expert_id}{old_ext}"
                if old_file.exists() and old_ext != ext:
                    old_file.unlink()
            
            # Save file with expert_id as filename
            file_path = avatars_dir / f"{expert_id}{ext}"
            
            # Save the validated and potentially resized image
            # This also strips any malicious metadata/payloads
            image.save(file_path, format=image.format, optimize=True)
            
        except Exception as img_error:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(img_error)}"
            )
        
        # Update expert's avatar path
        avatar_url = f"/attached_assets/avatars/{expert_id}{ext}"
        updated_expert = await storage.update_expert_avatar(expert_id, avatar_url)
        
        if not updated_expert:
            raise HTTPException(status_code=500, detail="Failed to update expert avatar")
        
        return updated_expert
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload avatar: {str(e)}")
    finally:
        # Ensure file is closed
        await file.close()

# Business Profile endpoints
@app.post("/api/profile", response_model=BusinessProfile)
@limiter.limit("20/day")  # Max 20 atualizações de perfil por dia
async def save_profile(request: Request, data: BusinessProfileCreate):
    """Create or update business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    try:
        profile = await storage.save_business_profile(user_id, data)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")

@app.get("/api/profile", response_model=Optional[BusinessProfile])
async def get_profile():
    """Get current user's business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    profile = await storage.get_business_profile(user_id)
    return profile

# Expert Recommendations endpoint (based on business profile)
@app.get("/api/experts/recommendations")
async def get_expert_recommendations():
    """
    Get expert recommendations based on user's business profile.
    Returns experts with relevance scores, star ratings, and justifications.
    """
    try:
        from recommendation import recommendation_engine
        
        # Get user's business profile
        user_id = "default_user"
        profile = await storage.get_business_profile(user_id)
        
        # Get all experts
        experts = await storage.get_experts()
        if not experts:
            raise HTTPException(status_code=404, detail="No experts available")
        
        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(experts, profile)
        
        # Format response
        return {
            "hasProfile": profile is not None,
            "recommendations": recommendations
        }
    
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get recommendations: {str(e)}"
        )

# Suggested Questions endpoint (personalized based on profile + expert expertise)
@app.get("/api/experts/{expert_id}/suggested-questions")
async def get_suggested_questions(expert_id: str):
    """
    Generate personalized suggested questions for a specific expert.
    Uses Perplexity AI to create context-aware questions based on:
    - User's business profile (industry, goals, challenges)
    - Expert's area of expertise
    
    Returns 3-5 highly relevant questions the user could ask.
    """
    try:
        from perplexity_research import perplexity_research
        
        # Get expert
        expert = await storage.get_expert(expert_id)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Get user's business profile
        user_id = "default_user"
        profile = await storage.get_business_profile(user_id)
        
        # Build context for Perplexity
        if profile:
            # Personalized questions based on profile
            context = f"""
Gere 5 perguntas altamente específicas e acionáveis que um empresário do setor de {profile.industry} deveria fazer para {expert.name} ({expert.title}).

Contexto do Negócio:
- Empresa: {profile.companyName}
- Setor: {profile.industry}
- Porte: {profile.companySize}
- Público-Alvo: {profile.targetAudience}
- Principais Produtos: {profile.mainProducts}
- Canais de Marketing: {', '.join(profile.channels) if profile.channels else 'Não especificado'}
- Faixa de Orçamento: {profile.budgetRange}
- Objetivo Principal: {profile.primaryGoal}
- Principal Desafio: {profile.mainChallenge}
- Prazo: {profile.timeline}

Áreas de Especialidade do Expert: {', '.join(expert.expertise[:5])}

Gere exatamente 5 perguntas que:
1. Sejam ESPECÍFICAS para a situação deste negócio (setor, porte, objetivos, desafios)
2. Aproveitem a expertise única e metodologia de {expert.name}
3. Sejam acionáveis e táticas (não teoria genérica)
4. Abordem o objetivo principal ({profile.primaryGoal}) ou desafio ({profile.mainChallenge}) do negócio
5. Sejam realistas para o orçamento dado ({profile.budgetRange}) e prazo ({profile.timeline})

IMPORTANTE: Responda SEMPRE em português brasileiro natural e fluente.
Formate cada pergunta como uma frase completa e natural que o usuário poderia fazer diretamente.
NÃO numere as perguntas nem adicione prefixos. Apenas retorne 5 perguntas, uma por linha.
"""
        else:
            # Generic questions based on expertise
            context = f"""
Gere 5 perguntas acionáveis que alguém poderia fazer para {expert.name} ({expert.title}) para obter conselhos práticos de marketing e estratégia.

Áreas de Especialidade do Expert: {', '.join(expert.expertise[:5])}

Gere exatamente 5 perguntas que:
1. Aproveitem a expertise única e metodologias de {expert.name}
2. Sejam acionáveis e táticas (não teóricas)
3. Cubram diferentes aspectos de sua expertise
4. Sejam específicas o suficiente para obter respostas úteis
5. Sejam realistas para pequenas e médias empresas

IMPORTANTE: Responda SEMPRE em português brasileiro natural e fluente.
Formate cada pergunta como uma frase completa e natural.
NÃO numere as perguntas nem adicione prefixos. Apenas retorne 5 perguntas, uma por linha.
"""
        
        # Use Perplexity to generate questions with lower temperature for consistency
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_research.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um consultor de estratégia de marketing que gera perguntas altamente específicas e acionáveis. SEMPRE responda em português brasileiro. Sempre retorne exatamente 5 perguntas, uma por linha, sem numeração ou prefixos."
                        },
                        {
                            "role": "user",
                            "content": context
                        }
                    ],
                    "temperature": 0.3,  # Lower temperature for more consistent, focused output
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse questions from response
        content = data["choices"][0]["message"]["content"]
        # Split by newlines and filter out empty lines
        questions = [q.strip() for q in content.split('\n') if q.strip()]
        
        # Clean up any numbering that might have been added despite instructions
        cleaned_questions = []
        for q in questions:
            # Remove common numbering patterns: "1. ", "1) ", "- ", "• "
            q_cleaned = q
            import re
            q_cleaned = re.sub(r'^\d+[\.\)]\s*', '', q_cleaned)  # Remove "1. " or "1) "
            q_cleaned = re.sub(r'^[-•]\s*', '', q_cleaned)  # Remove "- " or "• "
            if q_cleaned:
                cleaned_questions.append(q_cleaned)
        
        # Return up to 5 questions (in case more were generated)
        final_questions = cleaned_questions[:5]
        
        # Fallback if something went wrong
        if not final_questions:
            # Generic fallback based on expertise
            final_questions = [
                f"Como posso melhorar {expert.expertise[0].lower() if expert.expertise else 'minha estratégia'}?",
                f"Quais são as melhores práticas em {expert.expertise[1].lower() if len(expert.expertise) > 1 else 'marketing'}?",
                f"Como resolver desafios de {expert.expertise[2].lower() if len(expert.expertise) > 2 else 'negócios'}?"
            ]
        
        return {
            "expertId": expert_id,
            "expertName": expert.name,
            "questions": final_questions,
            "personalized": profile is not None
        }
    
    except HTTPException:
        raise
    except ValueError as e:
        # Missing PERPLEXITY_API_KEY
        if "PERPLEXITY_API_KEY" in str(e):
            # Return fallback questions instead of failing
            expert = await storage.get_expert(expert_id)
            if expert:
                return {
                    "expertId": expert_id,
                    "expertName": expert.name,
                    "questions": [
                        f"Como posso melhorar {expert.expertise[0].lower() if expert.expertise else 'minha estratégia'}?",
                        f"Quais são as melhores práticas em {expert.expertise[1].lower() if len(expert.expertise) > 1 else 'marketing'}?",
                        f"Como resolver desafios de {expert.expertise[2].lower() if len(expert.expertise) > 2 else 'negócios'}?"
                    ],
                    "personalized": False
                }
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error generating suggested questions: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return fallback instead of failing
        try:
            expert = await storage.get_expert(expert_id)
            if expert:
                return {
                    "expertId": expert_id,
                    "expertName": expert.name,
                    "questions": [
                        f"Como posso melhorar {expert.expertise[0].lower() if expert.expertise else 'minha estratégia'}?",
                        f"Quais são as melhores práticas em {expert.expertise[1].lower() if len(expert.expertise) > 1 else 'marketing'}?",
                        f"Como resolver desafios de {expert.expertise[2].lower() if len(expert.expertise) > 2 else 'negócios'}?"
                    ],
                    "personalized": False
                }
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

# Business Insights endpoint (personalized tips based on profile)
@app.get("/api/insights")
async def get_business_insights():
    """
    Generate personalized business insights based on user's profile.
    Uses Perplexity AI to create context-aware tips and recommendations.
    
    Returns 3-4 actionable insights specific to the user's business situation.
    """
    try:
        from perplexity_research import perplexity_research
        
        # Get user's business profile
        user_id = "default_user"
        profile = await storage.get_business_profile(user_id)
        
        if not profile:
            # No profile, return empty insights
            return {
                "hasProfile": False,
                "insights": []
            }
        
        # Build context for Perplexity to generate insights
        context = f"""
Gere 4 insights de marketing específicos e acionáveis para este negócio:

Perfil do Negócio:
- Empresa: {profile.companyName}
- Setor: {profile.industry}
- Porte: {profile.companySize}
- Público-Alvo: {profile.targetAudience}
- Principais Produtos: {profile.mainProducts}
- Canais de Marketing: {', '.join(profile.channels) if profile.channels else 'Não especificado'}
- Faixa de Orçamento: {profile.budgetRange}
- Objetivo Principal: {profile.primaryGoal}
- Principal Desafio: {profile.mainChallenge}
- Prazo: {profile.timeline}

Gere exatamente 4 insights que:
1. Sejam ALTAMENTE ESPECÍFICOS para o setor ({profile.industry}), porte ({profile.companySize}) e situação deste negócio
2. Sejam ACIONÁVEIS - algo que possam implementar nos próximos 30 dias
3. Abordem o OBJETIVO PRINCIPAL ({profile.primaryGoal}) ou DESAFIO PRINCIPAL ({profile.mainChallenge})
4. Sejam realistas dado o orçamento ({profile.budgetRange}) e prazo ({profile.timeline})
5. Aproveitem tendências atuais de mercado e melhores práticas (dados 2024-2025)

Cada insight deve:
- Começar com uma categoria/tópico claro (ex: "Estratégia SEO:", "Marketing de Conteúdo:", "Anúncios Pagos:")
- Ter no máximo 1-2 frases
- Incluir táticas específicas, não conselhos genéricos
- Referenciar dados ou tendências recentes quando relevante

IMPORTANTE: Responda SEMPRE em português brasileiro natural e fluente.
Formato: Retorne 4 insights, um por linha, cada um começando com a categoria seguida de dois pontos.
NÃO numere. Formato de exemplo:
Redes Sociais: [insight específico aqui]
E-mail Marketing: [insight específico aqui]
"""
        
        # Use Perplexity to generate insights
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_research.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um estrategista de marketing que fornece insights hiper-específicos e acionáveis baseados no contexto do negócio. SEMPRE responda em português brasileiro. Sempre use dados e tendências recentes. Formate os insights como 'Categoria: insight acionável específico'."
                        },
                        {
                            "role": "user",
                            "content": context
                        }
                    ],
                    "temperature": 0.4,
                    "max_tokens": 600,
                    "search_recency_filter": "month"  # Use recent data
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse insights from response
        content = data["choices"][0]["message"]["content"]
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Parse into structured insights (category + content)
        insights = []
        for line in lines:
            # Remove numbering if present
            import re
            line_cleaned = re.sub(r'^\d+[\.\)]\s*', '', line)
            line_cleaned = re.sub(r'^[-•]\s*', '', line_cleaned)
            
            # Try to split by first colon to get category
            if ':' in line_cleaned:
                parts = line_cleaned.split(':', 1)
                if len(parts) == 2:
                    insights.append({
                        "category": parts[0].strip(),
                        "content": parts[1].strip()
                    })
            else:
                # No colon, use whole line as content with generic category
                insights.append({
                    "category": "Dica Estratégica",
                    "content": line_cleaned
                })
        
        # Limit to 4 insights
        insights = insights[:4]
        
        # Fallback if something went wrong
        if not insights:
            insights = [
                {
                    "category": "Marketing Digital",
                    "content": f"Para empresas de {profile.industry}, foque em {profile.primaryGoal.lower()} através dos canais que você já usa."
                },
                {
                    "category": "Público-Alvo",
                    "content": f"Personalize sua mensagem para {profile.targetAudience} com conteúdo relevante e consistente."
                },
                {
                    "category": "Orçamento",
                    "content": f"Com orçamento de {profile.budgetRange}, priorize canais de alto ROI antes de expandir."
                }
            ]
        
        return {
            "hasProfile": True,
            "insights": insights,
            "profileSummary": {
                "companyName": profile.companyName,
                "industry": profile.industry,
                "primaryGoal": profile.primaryGoal
            }
        }
    
    except HTTPException:
        raise
    except ValueError as e:
        # Missing PERPLEXITY_API_KEY - return fallback
        if "PERPLEXITY_API_KEY" in str(e):
            user_id = "default_user"
            profile = await storage.get_business_profile(user_id)
            if profile:
                return {
                    "hasProfile": True,
                    "insights": [
                        {
                            "category": "Marketing Digital",
                            "content": f"Para empresas de {profile.industry}, foque em {profile.primaryGoal.lower()} através dos canais que você já usa."
                        },
                        {
                            "category": "Público-Alvo",
                            "content": f"Personalize sua mensagem para {profile.targetAudience} com conteúdo relevante e consistente."
                        },
                        {
                            "category": "Orçamento",
                            "content": f"Com orçamento de {profile.budgetRange}, priorize canais de alto ROI antes de expandir."
                        }
                    ],
                    "profileSummary": {
                        "companyName": profile.companyName,
                        "industry": profile.industry,
                        "primaryGoal": profile.primaryGoal
                    }
                }
            return {"hasProfile": False, "insights": []}
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error generating business insights: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return fallback instead of failing
        try:
            user_id = "default_user"
            profile = await storage.get_business_profile(user_id)
            if profile:
                return {
                    "hasProfile": True,
                    "insights": [
                        {
                            "category": "Marketing Digital",
                            "content": f"Para empresas de {profile.industry}, foque em {profile.primaryGoal.lower()}."
                        }
                    ],
                    "profileSummary": {
                        "companyName": profile.companyName,
                        "industry": profile.industry,
                        "primaryGoal": profile.primaryGoal
                    }
                }
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

# Council Analysis endpoints
@app.post("/api/council/analyze", response_model=CouncilAnalysis)
@limiter.limit("5/hour")  # Max 5 análises de conselho por hora (muito custoso)
async def create_council_analysis(request: Request, data: CouncilAnalysisCreate):
    """
    Run collaborative analysis by council of marketing legend experts.
    
    This endpoint:
    1. Conducts Perplexity research (if user has BusinessProfile)
    2. Gets independent analyses from 8 marketing legends
    3. Synthesizes consensus recommendation
    """
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    
    try:
        # Get user's business profile (optional)
        profile = await storage.get_business_profile(user_id)
        
        # Get experts to consult (all 8 if not specified)
        if data.expertIds:
            experts = []
            for expert_id in data.expertIds:
                expert = await storage.get_expert(expert_id)
                if not expert:
                    raise HTTPException(status_code=404, detail=f"Expert {expert_id} not found")
                experts.append(expert)
        else:
            # Use all available experts
            experts = await storage.get_experts()
            if not experts:
                raise HTTPException(status_code=400, detail="No experts available for analysis")
        
        # Run council analysis
        analysis = await council_orchestrator.analyze_problem(
            user_id=user_id,
            problem=data.problem,
            experts=experts,
            profile=profile
        )
        
        # Save analysis (temporarily disabled until table is created)
        # await storage.save_council_analysis(analysis)
        
        return analysis
    
    except HTTPException:
        raise
    except ValueError as e:
        # Missing API keys (ANTHROPIC_API_KEY, PERPLEXITY_API_KEY)
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Service temporarily unavailable: {error_msg}"
            )
        raise HTTPException(status_code=400, detail=f"Error in council analysis: {error_msg}")
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] API HTTP error: {e.response.status_code} - {e.response.text}")
        if "resource_exhausted" in e.response.text.lower():
            raise HTTPException(
                status_code=429,
                detail="Limite de recursos atingido. Por favor, aguarde um momento e tente novamente."
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"API error: {e.response.text}"
        )
    except Exception as e:
        print(f"Error creating council analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create council analysis: {str(e)}")

@app.post("/api/council/analyze-stream")
@limiter.limit("5/hour")  # Max 5 análises de conselho por hora (muito custoso)
async def create_council_analysis_stream(request: Request, data: CouncilAnalysisCreate):
    """
    Run collaborative analysis with Server-Sent Events streaming.
    
    Emits real-time progress events:
    - expert_started: When expert begins analysis
    - expert_researching: During Perplexity research
    - expert_analyzing: During Claude analysis
    - expert_completed: When expert finishes
    - consensus_started: Before synthesis
    - analysis_complete: Final result with full analysis
    """
    user_id = "default_user"
    
    async def event_generator():
        # Helper to format SSE events (defined outside try block for exception handling)
        def sse_event(event_type: str, data: dict) -> str:
            return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        
        try:
            # Get user's business profile (optional)
            profile = await storage.get_business_profile(user_id)
            
            # Get experts to consult
            if data.expertIds:
                experts = []
                for expert_id in data.expertIds:
                    expert = await storage.get_expert(expert_id)
                    if not expert:
                        yield sse_event("error", {"message": f"Expert {expert_id} not found"})
                        return
                    experts.append(expert)
            else:
                experts = await storage.get_experts()
                if not experts:
                    yield sse_event("error", {"message": "No experts available"})
                    return
            
            # Emit initial event with expert list
            yield sse_event("analysis_started", {
                "expertCount": len(experts),
                "experts": [{"id": e.id, "name": e.name, "avatar": e.avatar} for e in experts]
            })
            
            # Run council analysis with progress events
            # We'll need to modify council_orchestrator to emit events
            # For now, we'll simulate the workflow
            
            contributions = []
            research_findings = None
            
            # Perplexity research phase
            if profile:
                yield sse_event("research_started", {
                    "message": "Conducting market research..."
                })
                
                from perplexity_research import PerplexityResearch
                perplexity = PerplexityResearch()
                try:
                    research_result = await perplexity.research(
                        problem=data.problem,
                        profile=profile
                    )
                    research_findings = research_result.get("findings", "")
                    
                    yield sse_event("research_completed", {
                        "message": "Market research complete",
                        "citations": len(research_result.get("sources", []))
                    })
                except Exception as e:
                    yield sse_event("research_failed", {
                        "message": f"Research failed: {str(e)}"
                    })
            
            # Analyze with each expert (emitting events for each)
            from python_backend.crew_council import council_orchestrator
            
            # Process experts sequentially for event emission
            for expert in experts:
                yield sse_event("expert_started", {
                    "expertId": expert.id,
                    "expertName": expert.name,
                    "message": f"{expert.name} is analyzing..."
                })
                
                try:
                    print(f"[Council Stream] Starting analysis for {expert.name}")
                    contribution = await council_orchestrator._get_expert_analysis(
                        expert=expert,
                        problem=data.problem,
                        profile=profile,
                        research_findings=research_findings
                    )
                    contributions.append(contribution)
                    print(f"[Council Stream] Completed analysis for {expert.name}")
                    
                    yield sse_event("expert_completed", {
                        "expertId": expert.id,
                        "expertName": expert.name,
                        "insightCount": len(contribution.keyInsights),
                        "recommendationCount": len(contribution.recommendations)
                    })
                except Exception as e:
                    print(f"[Council Stream] Expert {expert.name} failed: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    yield sse_event("expert_failed", {
                        "expertId": expert.id,
                        "expertName": expert.name,
                        "error": str(e)
                    })
            
            if not contributions:
                yield sse_event("error", {"message": "All expert analyses failed"})
                return
            
            # Synthesize consensus
            yield sse_event("consensus_started", {
                "message": "Synthesizing council consensus..."
            })
            
            print(f"[Council Stream] Synthesizing consensus from {len(contributions)} contributions")
            consensus = await council_orchestrator._synthesize_consensus(
                problem=data.problem,
                contributions=contributions,
                research_findings=research_findings
            )
            print(f"[Council Stream] Consensus generated successfully")
            
            # Create final analysis object
            from python_backend.models import CouncilAnalysis, AgentContribution
            import uuid
            
            analysis = CouncilAnalysis(
                id=str(uuid.uuid4()),
                userId=user_id,
                problem=data.problem,
                profileId=profile.id if profile else None,
                marketResearch=research_findings,
                contributions=contributions,
                consensus=consensus
            )
            
            # Save analysis (temporarily disabled until table is created)
            # await storage.save_council_analysis(analysis)
            
            # Send final complete event
            print(f"[Council Stream] Sending analysis_complete event")
            yield sse_event("analysis_complete", {
                "analysisId": analysis.id,
                "analysis": {
                    "id": analysis.id,
                    "problem": analysis.problem,
                    "contributions": [
                        {
                            "expertId": c.expertId,
                            "expertName": c.expertName,
                            "analysis": c.analysis,
                            "keyInsights": c.keyInsights,
                            "recommendations": c.recommendations
                        }
                        for c in analysis.contributions
                    ],
                    "consensus": analysis.consensus
                }
            })
            print(f"[Council Stream] Stream completed successfully")
            
        except Exception as e:
            print(f"[Council Stream] Fatal error: {str(e)}")
            import traceback
            traceback.print_exc()
            yield sse_event("error", {
                "message": f"Analysis failed: {str(e)}"
            })
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@app.get("/api/council/analyses", response_model=List[CouncilAnalysis])
async def get_council_analyses():
    """Get all council analyses for the current user"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    return await storage.get_council_analyses(user_id)

@app.get("/api/council/analyses/{analysis_id}", response_model=CouncilAnalysis)
async def get_council_analysis(analysis_id: str):
    """Get a specific council analysis by ID"""
    analysis = await storage.get_council_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Council analysis not found")
    return analysis

# ============================================================================
# PERSONA BUILDER ENDPOINTS
# ============================================================================

from python_backend.models_persona import PersonaModern, PersonaModernCreate
from python_backend.reddit_research import reddit_research
from datetime import datetime as dt

@app.post("/api/personas", response_model=PersonaModern)
@limiter.limit("10/hour")  # Max 10 personas criadas por hora
async def create_persona(request: Request, data: PersonaModernCreate):
    """
    Create a modern persona using JTBD + BAG frameworks.
    
    Frameworks:
    - JTBD (Jobs to Be Done): Functional, emotional and social jobs
    - BAG (Behaviors, Aspirations, Goals): Behavioral patterns and aspirations
    - Quantified Pain Points: Measurable impact and costs
    - Modern Journey: Touchpoints and content preferences
    
    Modes:
    - quick: 1-2 min, basic insights
    - strategic: 5-10 min, deep analysis with quantified data
    """
    user_id = "default_user"  # TODO: replace with actual user auth
    
    try:
        # Conduct Reddit research based on mode
        try:
            if data.mode == "quick":
                research_data = await reddit_research.research_quick(
                    target_description=data.targetDescription,
                    industry=data.industry
                )
            else:  # strategic
                research_data = await reddit_research.research_strategic(
                    target_description=data.targetDescription,
                    industry=data.industry,
                    additional_context=data.additionalContext
                )
        except Exception as research_error:
            print(f"Error in research: {str(research_error)}")
            raise HTTPException(status_code=500, detail=f"Error in persona research: {str(research_error)}")
        
        # Generate persona name
        persona_name = f"Persona: {data.targetDescription[:50]}"
        
        # Create persona ID and timestamps
        import uuid
        persona_id = str(uuid.uuid4())
        now = dt.utcnow()
        
        # Prepare persona data with PersonaModern structure
        persona_data = {
            "id": persona_id,
            "userId": user_id,
            "name": persona_name,
            "researchMode": data.mode,
            "created_at": now,
            "updated_at": now
        }
        
        # Merge with research data
        persona_data.update(research_data)
        
        # Convert goals from objects to strings if needed
        if "goals" in persona_data and isinstance(persona_data["goals"], list):
            if persona_data["goals"] and isinstance(persona_data["goals"][0], dict):
                persona_data["goals"] = [
                    g.get("description", str(g)) if isinstance(g, dict) else str(g)
                    for g in persona_data["goals"]
                ]
        
        # Create PersonaModern instance
        persona = PersonaModern(**persona_data)
        
        # Save to database
        saved_persona = await storage.create_persona_modern(user_id, persona)
        
        return saved_persona
    
    except ValueError as e:
        # Missing API keys
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Service temporarily unavailable: {error_msg}"
            )
        raise HTTPException(status_code=400, detail=f"Error in persona research: {error_msg}")
    except httpx.HTTPStatusError as e:
        print(f"[ERROR] Perplexity/Anthropic API HTTP error: {e.response.status_code} - {e.response.text}")
        if "resource_exhausted" in e.response.text.lower():
            raise HTTPException(
                status_code=429,
                detail="Limite de recursos atingido. Por favor, aguarde um momento e tente novamente."
            )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Perplexity/Anthropic API error: {e.response.text}"
        )
    except Exception as e:
        print(f"Error creating persona: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create persona: {str(e)}")

@app.get("/api/personas", response_model=List[PersonaModern])
async def get_personas():
    """Get all modern personas for the current user"""
    user_id = "default_user"
    return await storage.get_personas_modern(user_id)

@app.get("/api/personas/{persona_id}", response_model=PersonaModern)
async def get_persona(persona_id: str):
    """Get a specific modern persona by ID"""
    persona = await storage.get_persona_modern(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

@app.patch("/api/personas/{persona_id}", response_model=PersonaModern)
async def update_persona(persona_id: str, updates: dict):
    """Update a modern persona (e.g., edit name, add notes)"""
    persona = await storage.update_persona_modern(persona_id, updates)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    return persona

@app.delete("/api/personas/{persona_id}")
async def delete_persona(persona_id: str):
    """Delete a modern persona"""
    success = await storage.delete_persona_modern(persona_id)
    if not success:
        raise HTTPException(status_code=404, detail="Persona not found")
    return {"success": True}

@app.get("/api/personas/{persona_id}/download")
async def download_persona(persona_id: str):
    """Download modern persona as JSON"""
    persona = await storage.get_persona_modern(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    # Convert Pydantic model to dict and return as JSON download
    from fastapi.responses import JSONResponse
    return JSONResponse(
        content=persona.model_dump(mode='json'),
        headers={
            "Content-Disposition": f"attachment; filename=persona_{persona_id}.json"
        }
    )

# =============================================================================
# DIAGNOSTIC ENDPOINT
# =============================================================================
@app.get("/api/debug/system-check")
async def system_check():
    """Temporary endpoint for diagnosing the seeding issue."""
    print("--- Running System Check ---")
    
    # 1. Check if DATABASE_URL is loaded
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL is NOT loaded in the environment.")
        raise HTTPException(status_code=500, detail="DATABASE_URL not found.")
    
    print(f"✅ DATABASE_URL is loaded: postgresql://...@{db_url.split('@')[-1]}")
    
    # 2. Check storage type
    storage_type = type(storage).__name__
    print(f"✅ Storage instance type: {storage_type}")
    if storage_type != "PostgresStorage":
        raise HTTPException(status_code=500, detail=f"Incorrect storage type. Expected PostgresStorage, got {storage_type}")

    # 3. Check database connection and count experts
    try:
        if not storage.pool:
            await storage.connect()
        
        async with storage.pool.acquire() as connection:
            count_record = await connection.fetchrow("SELECT COUNT(*) as expert_count FROM experts;")
            expert_count = count_record['expert_count']
            print(f"✅ Database query successful. Found {expert_count} experts.")
            
            # 4. Fetch first 5 experts to verify data
            first_experts_records = await connection.fetch("SELECT id, name FROM experts LIMIT 5;")
            first_experts = [dict(rec) for rec in first_experts_records]
            print(f"✅ First 5 experts in DB: {first_experts}")

    except Exception as e:
        print(f"❌ Database connection or query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection/query failed: {e}")

    return {
        "status": "OK",
        "storage_type": storage_type,
        "database_url_loaded": True,
        "expert_count": expert_count,
        "first_5_experts": first_experts,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
