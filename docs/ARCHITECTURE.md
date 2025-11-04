# Arquitetura do Sistema - AdvisorIA Elite

**Versão:** 2.0.0  
**Última Atualização:** 3 de Novembro de 2025

---

## Visão Geral

AdvisorIA Elite é uma plataforma de consultoria com IA baseada em clones cognitivos de especialistas reais. O sistema permite:

1. **Consultar especialistas individuais** via chat 1-on-1
2. **Consultar conselho de múltiplos experts** com análise colaborativa
3. **Criar personas ultra-específicas** com pesquisa profunda
4. **Auto-clonar especialistas** via Framework EXTRACT de 20 pontos

---

## Stack Tecnológico

### Frontend
```
React 18.3.1 + TypeScript 5.6.3
├── Vite 5.4.20 (build tool)
├── Wouter 3.3.5 (routing)
├── TanStack Query 5.60.5 (data fetching)
├── Framer Motion 11.13.1 (animations)
├── Tailwind CSS 3.4.17 + shadcn/ui (UI components)
└── Lucide React (icons)
```

**Port:** 5500 (desenvolvimento)

### Backend Node.js (Proxy Server)
```
Express 4.21.2 + TypeScript
├── tsx 4.20.5 (runtime)
├── http-proxy-middleware 3.0.5 (proxy para Python)
├── express-session (session management)
└── ws 8.18.0 (WebSocket support)
```

**Port:** 5500 (serve frontend + proxy)  
**Target:** http://localhost:5501 (Python backend)

### Backend Python (API Core)
```
FastAPI + Uvicorn
├── Python 3.12
├── Anthropic SDK (Claude Sonnet 4)
├── httpx (Perplexity API calls)
├── Pydantic (data validation)
├── slowapi (rate limiting)
└── asyncio (async operations)
```

**Port:** 5501 (desenvolvimento)

### Banco de Dados
```
PostgreSQL (Neon)
├── Hosted: Neon Serverless Postgres
├── Region: sa-east-1 (São Paulo)
├── Connection Pooling: Enabled
└── SSL: Required
```

### APIs Externas
```
Anthropic Claude
├── Modelo: claude-sonnet-4-20250514
├── Uso: Chat, síntese, análise
└── Cost: ~$0.02-0.20 por requisição

Perplexity AI
├── Modelo: sonar-reasoning (primary)
├── Fallback: sonar, sonar-pro
├── Uso: Pesquisa de personas
└── Cost: ~$0.005 por call
```

---

## Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────┐
│                    USUÁRIO (Browser)                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ HTTP/WSS
                      ↓
┌─────────────────────────────────────────────────────────┐
│               Frontend (React + Vite)                   │
│                    Port: 5500                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Pages: Home, Experts, Personas, Create,          │  │
│  │        TestCouncil, CouncilChat                  │  │
│  │                                                   │  │
│  │ Hooks: useCouncilStream, useCouncilBackground,   │  │
│  │        usePersistedState, useCouncilChat         │  │
│  │                                                   │  │
│  │ Components: CouncilAnimation, ExpertCard,        │  │
│  │             CouncilResultDisplay, ActivityFeed   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ Proxy HTTP
                      ↓
┌─────────────────────────────────────────────────────────┐
│            Node.js Server (Express)                     │
│                   Port: 5500                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Proxy: /api/* → http://localhost:5501            │  │
│  │ Proxy: /api/council/analyze-stream (SSE)         │  │
│  │ Static: Serve Vite frontend                      │  │
│  │ Session: express-session + MemoryStore           │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ HTTP Proxy
                      ↓
┌─────────────────────────────────────────────────────────┐
│          Python Backend (FastAPI)                       │
│                  Port: 5501                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Routers:                                          │  │
│  │  - /api/experts (CRUD + auto-clone)              │  │
│  │  - /api/experts/chat (1-on-1 chat)               │  │
│  │  - /api/council (analyze, stream, async)         │  │
│  │  - /api/personas (CRUD + enhance)                │  │
│  │  - /api/council/conversations (group chat)       │  │
│  │                                                   │  │
│  │ Modules:                                          │  │
│  │  - clones/ (22 expert definitions)               │  │
│  │  - crew_council.py (council orchestration)       │  │
│  │  - reddit_research.py (persona research)         │  │
│  │  - storage.py / postgres_storage.py              │  │
│  └──────────────────────────────────────────────────┘  │
└───┬─────────────────────────────────────┬───────────────┘
    │                                     │
    │ API Calls                           │ SQL Queries
    ↓                                     ↓
┌──────────────────────┐      ┌──────────────────────────┐
│  Anthropic Claude    │      │    PostgreSQL (Neon)     │
│  claude-sonnet-4     │      │  ┌────────────────────┐  │
│                      │      │  │ Tables:            │  │
│  - Chat responses    │      │  │  - experts         │  │
│  - Synthesis         │      │  │  - personas        │  │
│  - Analysis          │      │  │  - conversations   │  │
│  - Auto-clone        │      │  │  - messages        │  │
└──────────────────────┘      │  │  - council_tasks   │  │
                              │  └────────────────────┘  │
┌──────────────────────┐      └──────────────────────────┘
│   Perplexity AI      │
│   sonar-reasoning    │
│                      │
│  - Persona research  │
│  - Community discovery│
│  - Pain point analysis│
└──────────────────────┘
```

---

## Estrutura de Diretórios

```
AdvisorIAElite/
├── client/                          # Frontend React
│   ├── src/
│   │   ├── components/              # Componentes reutilizáveis
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   └── council/             # Componentes do conselho
│   │   ├── hooks/                   # React hooks customizados
│   │   ├── lib/                     # Utilitários
│   │   ├── pages/                   # Páginas da aplicação
│   │   │   ├── Home.tsx
│   │   │   ├── Experts.tsx
│   │   │   ├── Personas.tsx
│   │   │   ├── Create.tsx
│   │   │   ├── TestCouncil.tsx
│   │   │   └── CouncilChat.tsx
│   │   └── types/                   # TypeScript types
│   └── index.html
│
├── server/                          # Node.js proxy server
│   └── index.ts                     # Express server + proxy
│
├── python_backend/                  # FastAPI backend
│   ├── main.py                      # Main FastAPI app
│   ├── models.py                    # Pydantic models
│   ├── storage.py                   # Storage abstraction
│   ├── postgres_storage.py          # PostgreSQL implementation
│   ├── crew_council.py              # Council orchestration
│   ├── reddit_research.py           # Persona research engine
│   ├── clone_generator.py           # Auto-clone generator
│   ├── clones/
│   │   ├── registry.py              # Clone registry
│   │   └── *.py                     # 22 expert definitions
│   ├── routers/
│   │   └── experts.py               # Expert endpoints
│   └── migrations/                  # SQL migrations
│
├── shared/                          # Código compartilhado
│   └── schema.ts                    # Types compartilhados
│
├── docs/                            # Documentação estruturada
│   ├── ARCHITECTURE.md              # Este arquivo
│   ├── API_REFERENCE.md             # Referência da API
│   ├── USER_GUIDE.md                # Guia do usuário
│   ├── DEVELOPMENT.md               # Guia de desenvolvimento
│   ├── FEATURES.md                  # Catálogo de features
│   └── CHANGELOG.md                 # Histórico de versões
│
└── [108 arquivos .md]               # Docs de implementação/correções
```

---

## Fluxos de Dados

### 1. Chat Individual com Expert

```
User Input (Browser)
    ↓
React Page (Chat)
    ↓ POST /api/experts/{id}/chat
Express Proxy
    ↓ → http://localhost:5501/api/experts/{id}/chat
FastAPI Backend
    ↓
Load Expert System Prompt (from clones/)
    ↓
Call Anthropic Claude API
    ↓ Response
Update Conversation in PostgreSQL
    ↓
Return to Frontend
    ↓
Display in Chat UI
```

**Tempo:** ~2-5 segundos  
**Cost:** ~$0.02

---

### 2. Conselho de IA (Background Polling Mode)

```
User Selects Experts + Persona + Problem
    ↓
Click "Consultar Conselho"
    ↓ POST /api/council/analyze-async
FastAPI Backend
    ↓
Create Background Task
    ↓ Return task_id immediately
Frontend starts polling
    ↓ GET /api/council/tasks/{task_id} (every 3s)
    
Meanwhile, Backend:
    ↓
crew_council.py orchestrates
    ↓
For each expert (parallel):
    ├── Load system prompt
    ├── Call Claude with persona context
    └── Extract contribution
    ↓
Build consensus (Claude)
    ↓
Generate action plan (Claude)
    ↓
Save analysis to PostgreSQL
    ↓
Task status: "completed"
    
Frontend polling detects completion
    ↓
Display results
    ↓
User can start group chat
```

**Tempo:** ~60-90 segundos  
**Cost:** ~$0.10-0.30

---

### 3. Criação de Persona (Modo Estratégico)

```
User Fills Form (Target + Industry + Context)
    ↓
(Optional) Click "Melhorar com IA"
    ↓ POST /api/personas/enhance-description
    ├── Claude expands description
    ├── Suggests industry
    └── Suggests context
    ↓ Apply suggestions
    
Click "Criar Persona"
    ↓ POST /api/personas (mode: strategic)
FastAPI Backend
    ↓
reddit_research.research_strategic()
    
FASE 1: Discovery (Perplexity #1)
    ├── Find communities
    ├── Extract topics
    └── Identify language patterns
    (~15-20s)
    
FASE 2: Pain Points (Perplexity #2)
    ├── Quantify problems
    ├── Estimate costs
    └── Map metrics
    (~15-20s)
    
FASE 3: Behaviors (Perplexity #3)
    ├── Decision process
    ├── Purchase criteria
    └── Objections
    (~15-20s)
    
FASE 4: Synthesis (Claude)
    ├── Combine all research
    ├── Generate structured persona
    └── Add metadata
    (~20-30s)
    ↓
Save to PostgreSQL
    ↓
Return to Frontend
    ↓
Display Persona
```

**Tempo Total:** ~80-100 segundos  
**Cost:** ~$0.20

---

### 4. Auto-Clone de Expert

```
User Enters Name (ex: "Steve Jobs")
    ↓
Click "Criar Clone Automático"
    ↓ POST /api/experts/auto-clone
FastAPI Backend
    ↓
STEP 1: Biographical Research (Perplexity)
    ├── Search biography
    ├── Find key achievements
    ├── Extract philosophy
    └── Identify methods
    (~30s)
    ↓
STEP 2: Cognitive Synthesis (Claude)
    ├── Framework EXTRACT (20 points):
    │   ├── Experiences (formative experiences)
    │   ├── X-factors (unique traits)
    │   ├── Terminology (signature phrases)
    │   ├── Reasoning (decision patterns)
    │   ├── Axioms (core beliefs)
    │   ├── Callbacks (story banks)
    │   └── Tone (communication style)
    ├── Generate system prompt
    └── Create metadata
    (~60-90s)
    ↓
Return Expert Data (NOT saved yet)
    ↓
User tests in test chat
    ↓
User clicks "Salvar"
    ↓ POST /api/experts
Save to PostgreSQL
```

**Tempo:** ~120-180 segundos  
**Cost:** ~$0.30-0.50

---

## Componentes Principais

### Frontend Components

#### Pages (`client/src/pages/`)
| Página | Rota | Descrição |
|--------|------|-----------|
| Home.tsx | `/` | Landing page com overview |
| Experts.tsx | `/experts` | Lista e gerenciamento de experts |
| Personas.tsx | `/personas` | Lista e criação de personas |
| Create.tsx | `/create` | Auto-clone de experts |
| TestCouncil.tsx | `/test-council` | Interface do conselho |
| CouncilChat.tsx | `/council-chat/:id` | Chat em grupo |

#### Hooks Principais (`client/src/hooks/`)
| Hook | Funcionalidade |
|------|----------------|
| useCouncilStream | SSE streaming para conselho |
| useCouncilBackground | Background polling (funciona em tabs inativas) |
| useCouncilChat | Chat em grupo do conselho |
| usePersistedState | Persistência com localStorage |
| useDebounce | Debounce de inputs |
| useTypingDelay | Efeito de digitação gradual |

#### Components Específicos (`client/src/components/council/`)
| Componente | Descrição |
|------------|-----------|
| CouncilAnimation | Visualização dos experts analisando |
| CouncilResultDisplay | Exibição dos resultados |
| ExpertAvatar | Avatar com status e progresso |
| ActivityFeed | Feed de atividades em tempo real |
| ExpertSelector | Seletor de experts com recomendações |
| ActionPlanDisplay | Plano de ação estruturado |

---

### Backend Modules

#### FastAPI App (`python_backend/main.py`)
- **Linhas:** ~2700
- **Endpoints:** ~30
- **Rate Limiting:** slowapi (10-30/hora por endpoint)

#### Expert System (`python_backend/clones/`)
- **Registry:** `registry.py` - Registro de 22 experts
- **Clones:** 22 arquivos individuais com prompts
- **Framework EXTRACT:** 20 dimensões de personalidade

#### Council Orchestration (`python_backend/crew_council.py`)
- **Linhas:** ~1048
- **Funções:**
  - `analyze_problem_with_council()` - Análise síncrona
  - `analyze_problem_stream()` - SSE streaming
  - `analyze_problem_async()` - Background task
  - `build_council_consensus()` - Consensus building
  - `generate_action_plan()` - Plano de ação

#### Persona Research (`python_backend/reddit_research.py`)
- **Linhas:** ~740
- **Modos:**
  - `research_quick()` - Pesquisa rápida (1 Perplexity call)
  - `research_strategic()` - Pesquisa profunda (3 Perplexity + 1 Claude)
- **Features:**
  - Cache (24h TTL)
  - Fallback models
  - Error handling robusto

#### Storage Layer (`python_backend/postgres_storage.py`)
- **Interface:** Abstração de storage
- **Implementação:** PostgreSQL via psycopg2
- **Tabelas:**
  - `experts` - Especialistas
  - `personas` - Personas criadas
  - `personas_modern` - Personas com JTBD/BAG
  - `conversations` - Conversas de chat
  - `messages` - Mensagens
  - `council_tasks` - Tasks de background
  - `user_preferences` - Preferências

---

## Padrões de Design

### Frontend

#### State Management
```typescript
// TanStack Query para server state
const { data: experts } = useQuery({
  queryKey: ["/api/experts"],
});

// useState para UI state
const [showResults, setShowResults] = useState(false);

// usePersistedState para estado que deve persistir
const [problem, setProblem] = usePersistedState("council-problem", "");
```

#### API Calls
```typescript
// Wrapper com timeout e error handling
const response = await apiRequest("/api/endpoint", {
  method: "POST",
  body: JSON.stringify(data),
  timeout: 120000, // 120s para operações longas
});
```

#### Realtime Updates
```typescript
// SSE Streaming
const eventSource = new EventSource("/api/council/analyze-stream");
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle event
};

// Background Polling
const interval = setInterval(() => {
  pollTaskStatus(taskId);
}, 3000);
```

---

### Backend

#### Rate Limiting
```python
from slowapi import Limiter

@app.post("/api/endpoint")
@limiter.limit("10/hour")  # Max 10 requisições/hora
async def endpoint(request: Request):
    pass
```

#### Error Handling
```python
try:
    result = await expensive_operation()
except Exception as e:
    print(f"[Module] Error: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
```

#### Async Operations
```python
# Parallel execution
results = await asyncio.gather(
    expert_analysis_1(),
    expert_analysis_2(),
    expert_analysis_3(),
)
```

---

## Segurança

### Rate Limiting (slowapi)
| Endpoint | Limite | Motivo |
|----------|--------|--------|
| `/api/experts/auto-clone` | 5/hora | Custoso (Perplexity + Claude) |
| `/api/personas` | 10/hora | Custoso (Perplexity + Claude) |
| `/api/personas/enhance` | 30/hora | Rápido, ajuda UX |
| `/api/council/analyze` | 10/hora | Custoso (múltiplos Claude calls) |
| `/api/experts/chat` | 60/hora | Chat 1-on-1 |

### CORS
- Configurado via Express
- Permite credenciais
- Whitelist de origens em produção

### Environment Variables
- Chaves de API nunca commitadas
- `.env` em `.gitignore`
- Validação na inicialização

### SQL Injection
- Prepared statements via psycopg2
- Pydantic validation em todos os inputs
- Sanitização de inputs

---

## Performance

### Otimizações Frontend
- Code splitting (Vite)
- Lazy loading de componentes
- Memoização com useMemo/useCallback
- Debounce em inputs
- Virtual scrolling (ScrollArea)

### Otimizações Backend
- Cache de pesquisas (24h TTL)
- Parallel execution (asyncio.gather)
- Connection pooling (PostgreSQL)
- Timeouts apropriados
- Lazy loading de módulos

### Otimizações de API
- Timeout: 120s para operações longas
- Retry com backoff exponencial
- Fallback models (Perplexity)
- Streaming para respostas longas

---

## Monitoramento e Logs

### Logging Pattern
```python
# Structured logging com prefixos
print(f"[Module] Action: details")
print(f"[RedditResearch] Starting strategic research...")
print(f"[Council] Expert analysis completed")
```

### Logs Principais
- `dev.local.log` - Logs de desenvolvimento
- Console do navegador - Debug frontend
- Railway logs - Logs de produção

### Métricas Monitoradas
- Tempo de resposta por endpoint
- Taxa de erro por operação
- Uso de API (Anthropic, Perplexity)
- Cache hit rate
- Tempo de análise do conselho

---

## Dependências Críticas

### Frontend
```json
{
  "@tanstack/react-query": "5.60.5",  // Data fetching
  "framer-motion": "11.13.1",          // Animations
  "wouter": "3.3.5",                   // Routing
  "react": "18.3.1"                    // Core
}
```

### Backend Python
```toml
anthropic = "^0.37.0"     # Claude API
httpx = "^0.27.0"         # HTTP client
fastapi = "^0.115.0"      # Web framework
uvicorn = "^0.32.0"       # ASGI server
psycopg2-binary = "^2.9"  # PostgreSQL driver
slowapi = "^0.1.9"        # Rate limiting
pydantic = "^2.0"         # Validation
```

### Backend Node.js
```json
{
  "express": "4.21.2",                  // Web server
  "http-proxy-middleware": "3.0.5",     // Proxy
  "tsx": "4.20.5"                       // TypeScript runtime
}
```

---

## Escalabilidade

### Horizontal Scaling
- Frontend: Stateless, pode escalar infinitamente
- Node.js: Stateless (session em PostgreSQL ou Redis)
- Python: Stateless, pode escalar horizontalmente
- PostgreSQL: Connection pooling + read replicas

### Vertical Scaling
- Python backend pode precisar mais CPU (Claude calls)
- PostgreSQL pode precisar mais memória (cache)

### Limitações Atuais
- Session em MemoryStore (trocar por PostgreSQL/Redis em produção)
- Cache em memória (trocar por Redis em produção)
- Sem CDN para assets (adicionar em produção)

---

## Segurança e Compliance

### API Keys
- Armazenadas em variáveis de ambiente
- Nunca logadas ou expostas
- Rotacionadas regularmente

### Dados de Usuários
- Stored em PostgreSQL com SSL
- Sem PII sensível por enquanto
- LGPD compliance quando adicionar auth

### Rate Limiting
- Proteção contra abuse
- Limites por IP (via slowapi)
- Custos controlados

---

## Tecnologias Futuras (Roadmap)

### Versão 2.1+
- Redis para cache distribuído
- PostgreSQL session store
- WebSockets para chat em tempo real
- Bull Queue para background jobs

### Versão 3.0+
- Kubernetes para orquestração
- Microservices architecture
- Event-driven com message broker
- Observabilidade (Datadog, Sentry)

---

## Referências Técnicas

### Documentação Externa
- [FastAPI](https://fastapi.tiangolo.com/)
- [React Query](https://tanstack.com/query/latest)
- [Anthropic API](https://docs.anthropic.com/)
- [Perplexity API](https://docs.perplexity.ai/)

### Documentação Interna
- [API Reference](API_REFERENCE.md)
- [Development Guide](DEVELOPMENT.md)
- [User Guide](USER_GUIDE.md)

---

**Mantido por:** Time AdvisorIA Elite  
**Última revisão:** 3 de Novembro de 2025

