# Guia de Desenvolvimento - AdvisorIA Elite

**Versão:** 2.0.0  
**Última Atualização:** 3 de Novembro de 2025

---

## Índice

1. [Setup do Ambiente](#setup-do-ambiente)
2. [Estrutura do Código](#estrutura-do-codigo)
3. [Convenções de Código](#convencoes-de-codigo)
4. [Testing](#testing)
5. [Debugging](#debugging)
6. [Contribuindo](#contribuindo)
7. [Deploy](#deploy)

---

## Setup do Ambiente

### Pré-requisitos

```bash
Node.js: >= 20.x < 21
Python: >= 3.12
PostgreSQL: 15+ (ou conta Neon)
```

### 1. Clone o Repositório

```bash
git clone <repo-url>
cd AdvisorIAElite
```

### 2. Instale Dependências

#### Node.js
```bash
npm install
```

#### Python
```bash
cd python_backend
pip install -r requirements.txt
# ou com uv (mais rápido)
uv pip install -r requirements.txt
```

### 3. Configure Variáveis de Ambiente

Crie arquivo `.env` na raiz:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database

# APIs (obrigatórias)
ANTHROPIC_API_KEY=sk-ant-api03-...
PERPLEXITY_API_KEY=pplx-...

# Portas (desenvolvimento)
PORT=5500
PY_PORT=5501
NODE_ENV=development
```

**Obtenha as chaves:**
- Anthropic: https://console.anthropic.com/
- Perplexity: https://www.perplexity.ai/settings/api
- Database: https://neon.tech/ (free tier disponível)

### 4. Inicialize o Banco de Dados

```bash
# Rodar migrations (se necessário)
cd python_backend
python create_tables.py
```

### 5. Inicie o Servidor

```bash
# Volta para raiz
cd ..

# Inicia tudo (Node.js + Python + Frontend)
./start.sh

# Ou manualmente
npm run dev
```

### 6. Acesse o Sistema

```
Frontend: http://localhost:5500
Backend Python: http://localhost:5501
Backend Node: http://localhost:5500 (mesmo port, proxy automático)
```

---

## Estrutura do Código

### Frontend (`client/`)

```
client/
├── src/
│   ├── components/          # Componentes React
│   │   ├── ui/             # shadcn/ui base components
│   │   ├── council/        # Componentes específicos do conselho
│   │   ├── settings/       # Componentes de configuração
│   │   ├── AnimatedPage.tsx
│   │   └── ExpertCard.tsx
│   │
│   ├── hooks/              # React hooks customizados
│   │   ├── useCouncilStream.ts      # SSE streaming
│   │   ├── useCouncilBackground.ts  # Background polling
│   │   ├── useCouncilChat.ts        # Chat em grupo
│   │   ├── usePersistedState.ts     # Persistência localStorage
│   │   ├── useDebounce.ts           # Debounce
│   │   └── useTypingDelay.ts        # Efeito typing
│   │
│   ├── lib/                # Utilitários
│   │   ├── queryClient.ts  # TanStack Query setup
│   │   ├── errors.ts       # Error handling
│   │   └── validation.ts   # Validações
│   │
│   ├── pages/              # Páginas da aplicação
│   │   ├── Home.tsx        # Landing page
│   │   ├── Experts.tsx     # Lista de experts
│   │   ├── Personas.tsx    # CRUD de personas
│   │   ├── Create.tsx      # Auto-clone de experts
│   │   ├── TestCouncil.tsx # Interface do conselho
│   │   └── CouncilChat.tsx # Chat em grupo
│   │
│   ├── types/              # TypeScript types
│   │   └── council.ts      # Types do conselho
│   │
│   ├── App.tsx             # App root com routing
│   └── main.tsx            # Entry point
│
└── index.html              # HTML template
```

---

### Backend Python (`python_backend/`)

```
python_backend/
├── main.py                 # FastAPI app principal (~2700 linhas)
│
├── models.py               # Pydantic models (Expert, Conversation, Message)
├── models_persona.py       # PersonaModern model
├── models_persona_deep.py  # PersonaDeep model (futuro)
│
├── storage.py              # Interface abstrata de storage
├── postgres_storage.py     # Implementação PostgreSQL (~600 linhas)
│
├── crew_council.py         # Orquestração do conselho (~1048 linhas)
├── reddit_research.py      # Engine de pesquisa de personas (~740 linhas)
├── clone_generator.py      # Auto-clone de experts
│
├── clones/                 # Sistema de experts
│   ├── registry.py         # Registro de 22 experts
│   ├── philip_kotler.py
│   ├── seth_godin.py
│   └── ... (22 arquivos)
│
├── routers/
│   └── experts.py          # Router de experts
│
└── migrations/             # SQL migrations
    └── create_personas_deep_table.sql
```

---

### Backend Node.js (`server/`)

```
server/
└── index.ts                # Express server + proxy (~300 linhas)
    ├── Proxy HTTP para Python
    ├── SSE proxy especial
    ├── Serve frontend Vite
    └── Session management
```

---

## Convenções de Código

### TypeScript/React

#### Naming
```typescript
// Components: PascalCase
export function ExpertCard() {}

// Hooks: camelCase com 'use' prefix
export function useCouncilStream() {}

// Utils: camelCase
export function formatCurrency() {}

// Constants: UPPER_SNAKE_CASE
const DEFAULT_TIMEOUT_MS = 90000;

// Types/Interfaces: PascalCase
interface CouncilAnalysis {}
```

#### Imports
```typescript
// Ordem: React → Third-party → Local components → Local utils → Types
import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { apiRequest } from "@/lib/queryClient";
import type { Expert } from "@shared/schema";
```

#### Component Structure
```typescript
// 1. Props interface
interface ComponentProps {
  prop1: string;
  prop2?: number;
}

// 2. Component
export function Component({ prop1, prop2 }: ComponentProps) {
  // 3. Hooks
  const [state, setState] = useState();
  const { data } = useQuery();
  
  // 4. Effects
  useEffect(() => {}, []);
  
  // 5. Handlers
  const handleClick = () => {};
  
  // 6. Render
  return <div>...</div>;
}
```

---

### Python

#### Naming
```python
# Functions/methods: snake_case
def analyze_problem():
    pass

# Classes: PascalCase
class RedditResearchEngine:
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_CACHE_TTL = 86400

# Private: _prefix
def _internal_helper():
    pass
```

#### Type Hints
```python
from typing import Dict, List, Optional

async def research_quick(
    target_description: str, 
    industry: Optional[str] = None
) -> Dict:
    pass
```

#### Docstrings
```python
def function_name(param: str) -> Dict:
    """
    Short description.
    
    Args:
        param: Description of parameter
    
    Returns:
        Dict with result data
        
    Raises:
        ValueError: When param is invalid
    """
    pass
```

#### Logging
```python
# Pattern: [Module] Action: details
print(f"[RedditResearch] Starting strategic research for '{target}'")
print(f"[Council] Expert {name} completed analysis")
print(f"[Storage] Saved persona with ID {id}")
```

---

## Testing

### Frontend Tests (Futuro)

```bash
# Unit tests
npm test

# E2E tests
npm run test:e2e
```

### Backend Tests

#### Testes Python Existentes
```bash
# Testar auto-clone de Philip Kotler
python test_philip_kotler.py

# Testar todos os 18 clones
python test_all_remaining_clones.py

# Validação final
python test_validation_final.py
```

#### Smoke Tests
```bash
# Testar endpoints principais
bash scripts/smoke-test.sh
```

### Manual Testing

#### Endpoints
```bash
# Health check
curl http://localhost:5501/health

# List experts
curl http://localhost:5501/api/experts

# Create persona (quick mode)
curl -X POST http://localhost:5501/api/personas \
  -H "Content-Type: application/json" \
  -d '{"mode":"quick","targetDescription":"CEO de SaaS"}'
```

---

## Debugging

### Frontend

#### Chrome DevTools
```javascript
// Console logs estruturados
console.log('[Component] Action:', data);

// React Query DevTools
// Já incluído em desenvolvimento
// Acesse: Bottom left corner
```

#### Network Tab
- Verificar chamadas API
- Timing de requisições
- Payloads de request/response

#### React DevTools
- Inspecionar component tree
- Ver props e state
- Profiling de performance

---

### Backend Python

#### Logs Estruturados
```python
# Ver logs em tempo real
tail -f dev.local.log

# Filtrar por módulo
tail -f dev.local.log | grep "RedditResearch"

# Ver apenas erros
tail -f dev.local.log | grep -i "error"
```

#### Debug Mode
```python
# Adicionar breakpoints com ipdb
import ipdb; ipdb.set_trace()

# Ou usar print debugging
print(f"[DEBUG] Variable value: {variable}")
```

#### Verificar Estado da API
```bash
# Ver se backend está rodando
ps aux | grep uvicorn

# Ver portas ocupadas
lsof -i :5501
```

---

### Common Debug Scenarios

#### "Frontend não conecta ao backend"

**Verificar:**
```bash
# Backend Python rodando?
curl http://localhost:5501/api/experts

# Proxy Node.js configurado?
grep "PY_TARGET" server/index.ts
```

#### "Perplexity não funciona"

**Verificar:**
```bash
# Chave configurada?
grep PERPLEXITY_API_KEY .env

# Backend carregou a chave?
grep "PERPLEXITY" dev.local.log

# Testar chave diretamente
curl -X POST https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer pplx-your-key" \
  -H "Content-Type: application/json" \
  -d '{"model":"sonar","messages":[{"role":"user","content":"test"}]}'
```

#### "Conselho não funciona"

**Verificar:**
```bash
# Persona foi selecionada?
# Ver console do navegador

# Backend processando?
tail -f dev.local.log | grep Council

# Rate limit?
# Ver headers de response
```

---

## Contribuindo

### Workflow

1. **Fork** o repositório
2. **Crie branch** para feature: `git checkout -b feature/nova-feature`
3. **Faça commits** descritivos: `git commit -m "feat: adiciona nova feature"`
4. **Push**: `git push origin feature/nova-feature`
5. **Crie Pull Request**

### Commit Messages

Siga Conventional Commits:

```bash
feat: adiciona nova funcionalidade
fix: corrige bug específico
docs: atualiza documentação
style: formatação, sem mudança de lógica
refactor: refatora código sem mudar comportamento
test: adiciona ou corrige testes
chore: tarefas de manutenção
```

**Exemplos:**
```bash
git commit -m "feat: adiciona modo estratégico com 4 fases"
git commit -m "fix: corrige timeout de 30s para 120s"
git commit -m "docs: atualiza guia do usuário"
```

---

### Code Review Checklist

#### Frontend
- [ ] TypeScript sem erros (`npm run check`)
- [ ] Sem console.logs desnecessários
- [ ] Componentes seguem padrão existente
- [ ] Hooks customizados documentados
- [ ] Error handling implementado
- [ ] Loading states implementados

#### Backend Python
- [ ] Type hints em todas funções
- [ ] Docstrings em funções públicas
- [ ] Error handling com HTTPException
- [ ] Logs estruturados com prefixo [Module]
- [ ] Rate limiting configurado
- [ ] Validação de inputs com Pydantic

#### Geral
- [ ] Sem dados sensíveis commitados
- [ ] .env.example atualizado (se necessário)
- [ ] Documentação atualizada
- [ ] Testes passando (quando houver)

---

## Adicionando Novo Expert (Manual)

### Passo 1: Criar arquivo do clone

```bash
cd python_backend/clones
cp philip_kotler.py novo_expert.py
```

### Passo 2: Editar conteúdo

```python
# python_backend/clones/novo_expert.py

EXPERT_ID = "novo-expert"
EXPERT_NAME = "Nome do Expert"
EXPERT_TITLE = "Título/Especialidade"
EXPERT_EXPERTISE = ["área1", "área2", "área3"]
EXPERT_BIO = """
Biografia completa do expert...
"""

SYSTEM_PROMPT = """
Você é [Nome do Expert], [descrição].

# CARACTERÍSTICAS PRINCIPAIS
- Característica 1
- Característica 2

# FILOSOFIA
Filosofia principal...

# MÉTODO
Abordagem específica...

# TOM
Tom de comunicação...

RESPONDA SEMPRE como [Nome], usando:
- Terminologia específica
- Exemplos concretos
- Referências a trabalhos
"""

EXPERT_CATEGORY = "categoria"  # estrategia, growth, content, etc
```

### Passo 3: Registrar no registry

```python
# python_backend/clones/registry.py

from python_backend.clones import novo_expert

EXPERT_CLONES = [
    # ... experts existentes
    novo_expert,
]
```

### Passo 4: Reiniciar backend

```bash
# Backend recarrega automaticamente com --reload
# Ou force restart:
lsof -ti:5501 | xargs kill -9
```

### Passo 5: Verificar

```bash
curl http://localhost:5501/api/experts | jq '.[] | select(.id=="novo-expert")'
```

---

## Adicionando Nova Feature

### Exemplo: Nova página

#### 1. Criar componente de página

```typescript
// client/src/pages/NovaPage.tsx
export default function NovaPage() {
  return (
    <AnimatedPage>
      <div className="container mx-auto py-8">
        <h1>Nova Página</h1>
      </div>
    </AnimatedPage>
  );
}
```

#### 2. Adicionar rota

```typescript
// client/src/App.tsx
import NovaPage from "@/pages/NovaPage";

// No routing
<Route path="/nova-page" component={NovaPage} />
```

#### 3. Adicionar link na navegação

```typescript
// Adicionar em menu/navegação existente
<Link to="/nova-page">Nova Página</Link>
```

---

### Exemplo: Novo endpoint

#### 1. Adicionar endpoint no FastAPI

```python
# python_backend/main.py

@app.get("/api/nova-feature")
@limiter.limit("30/hour")
async def nova_feature(request: Request):
    """
    Descrição do endpoint.
    
    Returns:
        Dict com resultado
    """
    try:
        # Implementação
        result = await process_something()
        return {"data": result}
    except Exception as e:
        print(f"[NovaFeature] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

#### 2. Criar hook no frontend

```typescript
// client/src/hooks/useNovaFeature.ts
export function useNovaFeature() {
  return useQuery({
    queryKey: ["/api/nova-feature"],
  });
}
```

#### 3. Usar no componente

```typescript
const { data, isLoading } = useNovaFeature();
```

---

## Environment Variables

### Desenvolvimento

```bash
# .env (raiz)
DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...
PORT=5500
PY_PORT=5501
NODE_ENV=development
```

### Produção (Railway)

```bash
DATABASE_URL=postgresql://...
ANTHROPIC_API_KEY=sk-ant-...
PERPLEXITY_API_KEY=pplx-...
PORT=5000          # Railway assign automaticamente
PY_PORT=5001
NODE_ENV=production
```

---

## Debugging Tips

### Frontend não atualiza após mudança

```bash
# Limpar cache
rm -rf node_modules/.vite
npm run dev
```

### Backend Python não recarrega

```bash
# Verificar se --reload está ativo
ps aux | grep uvicorn

# Forçar reload
touch python_backend/main.py
```

### Erro de import no Python

```bash
# Verificar PYTHONPATH
echo $PYTHONPATH

# Rodar da raiz
cd /path/to/AdvisorIAElite
python -m python_backend.main
```

### Database connection issues

```bash
# Testar conexão
python -c "
import psycopg2
conn = psycopg2.connect('postgresql://...')
print('Connected!')
"
```

---

## Performance Optimization

### Frontend

#### Code Splitting
```typescript
// Lazy load pages
const HeavyPage = lazy(() => import("@/pages/HeavyPage"));

// Use in route
<Route path="/heavy" component={HeavyPage} />
```

#### Memoization
```typescript
// Componentes pesados
const MemoizedComponent = memo(Component);

// Callbacks
const handleClick = useCallback(() => {}, [deps]);

// Valores computados
const expensiveValue = useMemo(() => compute(), [deps]);
```

#### Debouncing
```typescript
const debouncedValue = useDebounce(inputValue, 500);
```

---

### Backend

#### Caching
```python
# Em reddit_research.py
cache_key = self._get_cache_key("method", **params)
cached = self._get_cached_result(cache_key)
if cached:
    return cached
```

#### Parallel Execution
```python
# Executar experts em paralelo
results = await asyncio.gather(
    expert_analysis_1(),
    expert_analysis_2(),
    expert_analysis_3(),
)
```

#### Connection Pooling
```python
# PostgreSQL já usa pooling via Neon
# Limite de conexões: configurar no Neon dashboard
```

---

## Deploy

### Railway (Recomendado)

#### Passo 1: Criar Projeto
```bash
railway init
```

#### Passo 2: Adicionar PostgreSQL
```bash
railway add postgresql
# Copiar DATABASE_URL
```

#### Passo 3: Configurar Variáveis
```bash
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set PERPLEXITY_API_KEY=pplx-...
railway variables set NODE_ENV=production
railway variables set PORT=5000
railway variables set PY_PORT=5001
```

#### Passo 4: Deploy
```bash
railway up
```

**Documentação completa:** [RAILWAY.md](../RAILWAY.md)

---

### Replit

Veja: [replit.md](../replit.md)

---

## Troubleshooting

### Build Errors

#### "Module not found"
```bash
# Limpar e reinstalar
rm -rf node_modules package-lock.json
npm install
```

#### "Python module not found"
```bash
# Reinstalar dependências Python
pip install -r python_backend/requirements.txt
```

---

### Runtime Errors

#### "Port already in use"
```bash
# Matar processo na porta
lsof -ti:5500 | xargs kill -9
lsof -ti:5501 | xargs kill -9
```

#### "Database connection failed"
```bash
# Verificar DATABASE_URL no .env
# Testar conexão
psql $DATABASE_URL
```

---

## Hot Reload

### Desenvolvimento

- **Vite (Frontend):** Hot Module Replacement automático
- **Uvicorn (Python):** `--reload` flag ativada
- **Node.js:** tsx com watch mode

**Salve qualquer arquivo → Recarrega automaticamente!**

---

## Linting e Formatting

### TypeScript
```bash
# Type check
npm run check

# Futuro: ESLint
npm run lint

# Futuro: Prettier
npm run format
```

### Python
```bash
# Futuro: Black
black python_backend/

# Futuro: Flake8
flake8 python_backend/

# Futuro: mypy
mypy python_backend/
```

---

## Estrutura de Branches (Futuro)

```
main          # Produção estável
├── develop   # Desenvolvimento ativo
├── feature/* # Features em desenvolvimento
├── fix/*     # Correções de bugs
└── release/* # Preparação de releases
```

---

## CI/CD (Futuro)

### GitHub Actions
- Run tests on PR
- Type checking
- Linting
- Deploy to staging on merge to develop
- Deploy to production on tag

---

## Monitoramento (Produção)

### Logs
```bash
# Railway
railway logs

# Ver logs em tempo real
railway logs --follow
```

### Métricas
- Response time por endpoint
- Error rate
- API usage (Anthropic, Perplexity)
- Database query performance

### Alertas
- Erro rate > 5%
- Response time > 10s
- Database connections > 80%
- API budget > 80%

---

## Recursos

### Documentação Interna
- [Architecture](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [User Guide](USER_GUIDE.md)
- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

### Ferramentas
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Query](https://tanstack.com/query/latest)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Happy Coding!** 🚀

**Mantido por:** Time AdvisorIA Elite  
**Última revisão:** 3 de Novembro de 2025

