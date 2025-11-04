# 🛡️ PROCESSO DE VALIDAÇÃO OBRIGATÓRIO

**Versão:** 1.0  
**Data:** 3 de Novembro de 2025  
**Status:** OBRIGATÓRIO ⚠️

---

## ⚠️ LEIA ANTES DE FAZER QUALQUER MUDANÇA

Este documento é **OBRIGATÓRIO** para qualquer mudança no código.

**Por quê?** Evitar quebrar funcionalidades por não consultar a documentação existente.

---

## 📋 CHECKLIST OBRIGATÓRIO

### ☑️ ANTES DE MODIFICAR CÓDIGO

Marque TODAS as caixas antes de começar:

- [ ] **Li a documentação relevante** (ver seção abaixo)
- [ ] **Entendo a arquitetura atual** ([docs/ARCHITECTURE.md](docs/ARCHITECTURE.md))
- [ ] **Verifiquei endpoints existentes** ([docs/API_REFERENCE.md](docs/API_REFERENCE.md))
- [ ] **Revisei convenções de código** ([docs/DEVELOPMENT.md](docs/DEVELOPMENT.md))
- [ ] **Não vou quebrar features existentes** ([docs/FEATURES.md](docs/FEATURES.md))

---

## 📚 DOCUMENTAÇÃO QUE VOCÊ DEVE CONSULTAR

### Para QUALQUER mudança de código:

1. **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** (15 min)
   - Entenda como o sistema funciona
   - Veja fluxos de dados
   - Identifique componentes afetados

2. **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** (10 min)
   - Convenções de naming
   - Padrões de código
   - Estrutura de arquivos

---

### Para mudanças no BACKEND:

3. **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** (20 min)
   - **CRÍTICO:** Não quebre endpoints existentes!
   - Verifique schemas esperados
   - Mantenha compatibilidade

**Exemplos de erros evitáveis:**
- ❌ Mudar modelo do Claude sem verificar se todos os lugares usam
- ❌ Adicionar campo obrigatório em endpoint sem migration
- ❌ Mudar rate limit sem documentar

**Como validar:**
```python
# ANTES de mudar endpoint:
# 1. Ler docs/API_REFERENCE.md - seção do endpoint
# 2. Buscar usos no frontend: grep -r "endpoint-name" client/
# 3. Verificar se quebra contratos existentes
```

---

### Para mudanças no FRONTEND:

4. **[docs/FEATURES.md](docs/FEATURES.md)** (15 min)
   - Entenda features existentes
   - Veja como componentes interagem
   - Identifique dependências

**Exemplos de erros evitáveis:**
- ❌ Mudar prop de componente sem verificar todos os usos
- ❌ Alterar estado sem entender fluxo completo
- ❌ Quebrar hook customizado usado em múltiplos lugares

**Como validar:**
```bash
# ANTES de mudar componente/hook:
# 1. Buscar usos: grep -r "ComponentName" client/src/
# 2. Verificar props: ler definição TypeScript
# 3. Ver features afetadas: docs/FEATURES.md
```

---

## 🔍 PERGUNTAS DE VALIDAÇÃO

### ANTES de começar qualquer mudança, responda:

#### 1. Arquitetura
- [ ] **Onde esse código fica na arquitetura?** (Frontend/Backend/Storage/API)
- [ ] **Que componentes ele afeta?** (Listar pelo menos 3)
- [ ] **Qual o fluxo de dados?** (Desenhar mentalmente)

#### 2. Compatibilidade
- [ ] **Essa mudança quebra algo existente?** (Se SIM, pare e replaneie)
- [ ] **Preciso atualizar schemas/types?** (Se SIM, fazer antes)
- [ ] **Frontend e backend continuam compatíveis?** (Validar schemas)

#### 3. Documentação
- [ ] **Já existe documentação sobre isso?** (Buscar antes de criar)
- [ ] **Qual arquivo de docs devo consultar?** (Listar específico)
- [ ] **Preciso atualizar documentação?** (Se SIM, incluir no PR)

#### 4. Testing
- [ ] **Como vou testar essa mudança?** (Plano específico)
- [ ] **Que casos de teste devo cobrir?** (Listar cenários)
- [ ] **Como validar que não quebrei nada?** (Smoke test mínimo)

---

## 🚨 ERROS COMUNS QUE DEVEM SER EVITADOS

### 1. Não Verificar Instanciação de Clientes

**Erro:**
```python
# ❌ ERRADO - Usar cliente sem instanciar
response = await anthropic_client.messages.create(...)
```

**Correto:**
```python
# ✅ CERTO - Sempre instanciar primeiro
from anthropic import AsyncAnthropic
anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = await anthropic_client.messages.create(...)
```

**Como evitar:** Buscar no código exemplos existentes antes de copiar/colar

---

### 2. Não Verificar Modelos Disponíveis

**Erro:**
```python
# ❌ ERRADO - Usar modelo antigo/inexistente
model="claude-3-5-sonnet-20241022"  # Não disponível!
```

**Correto:**
```python
# ✅ CERTO - Verificar qual modelo é usado no resto do código
model="claude-sonnet-4-20250514"  # Modelo atual
```

**Como evitar:**
```bash
# Buscar modelos usados
grep -r "model=" python_backend/ | grep claude
```

---

### 3. Não Verificar Timeouts

**Erro:**
```typescript
// ❌ ERRADO - Usar timeout padrão para operação longa
await apiRequest("/api/long-operation", {...});  // Timeout padrão 90s
```

**Correto:**
```typescript
// ✅ CERTO - Verificar docs e usar timeout apropriado
await apiRequest("/api/long-operation", {
  ...
  timeout: 120000, // 120s para operações longas
});
```

**Como evitar:** Consultar `docs/API_REFERENCE.md` seção "Timeouts"

---

### 4. Não Verificar Rate Limits

**Erro:**
```python
# ❌ ERRADO - Endpoint sem rate limit
@app.post("/api/expensive-operation")
async def expensive_op():
    pass
```

**Correto:**
```python
# ✅ CERTO - Sempre adicionar rate limit
@app.post("/api/expensive-operation")
@limiter.limit("10/hour")  # Verificar docs para limite apropriado
async def expensive_op(request: Request):
    pass
```

**Como evitar:** Consultar `docs/API_REFERENCE.md` seção "Rate Limits"

---

### 5. Não Testar Ambiente Atualizado

**Erro:**
```bash
# ❌ ERRADO - Assumir que variáveis antigas ainda funcionam
# Código usa PERPLEXITY_API_KEY mas não verifica se está configurada
```

**Correto:**
```python
# ✅ CERTO - Validar variáveis de ambiente
perplexity_key = os.getenv("PERPLEXITY_API_KEY")
if not perplexity_key:
    raise ValueError("PERPLEXITY_API_KEY not configured")
```

**Como evitar:** Consultar `SETUP.md` e `.env` antes de adicionar dependências

---

## 📖 DOCUMENTAÇÃO POR TIPO DE MUDANÇA

### Mudando ENDPOINTS (Python Backend)

**OBRIGATÓRIO ler:**
1. [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Seção do endpoint
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Fluxo de dados

**Perguntas:**
- Endpoint já existe? → Manter compatibilidade!
- Request/response schema mudou? → Atualizar TypeScript types!
- Rate limit apropriado? → Consultar tabela no API_REFERENCE

**Validações:**
```bash
# 1. Verificar usos no frontend
grep -r "endpoint-name" client/src/

# 2. Verificar schema TypeScript
grep -r "interface.*Response" client/src/types/

# 3. Testar
curl -X POST http://localhost:5501/api/endpoint -d '{...}'
```

---

### Mudando COMPONENTES REACT

**OBRIGATÓRIO ler:**
1. [docs/FEATURES.md](docs/FEATURES.md) - Feature que usa componente
2. [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Convenções React

**Perguntas:**
- Componente usado em quantos lugares? → Buscar imports!
- Props mudaram? → Atualizar TODOS os usos!
- Hook customizado afetado? → Verificar dependências!

**Validações:**
```bash
# 1. Buscar usos do componente
grep -r "ComponentName" client/src/

# 2. Type check
npm run check

# 3. Testar no navegador
# Visitar TODAS as páginas que usam o componente
```

---

### Mudando HOOKS

**OBRIGATÓRIO ler:**
1. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Seção "Frontend Components"
2. Código do hook existente (ler COMPLETO!)

**Perguntas:**
- Hook usado em quantas páginas? → Buscar imports!
- Estado compartilhado? → Pode afetar múltiplas partes!
- Dependencies mudaram? → Re-testar TUDO!

**Validações:**
```bash
# 1. Buscar usos
grep -r "useHookName" client/src/

# 2. Verificar tipos
npm run check

# 3. Testar cenários
# Testar em TODAS as páginas que usam
```

---

### Mudando MODELS/SCHEMAS

**OBRIGATÓRIO ler:**
1. [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Schemas existentes
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Data flow

**Perguntas:**
- Schema usado no frontend E backend? → Atualizar AMBOS!
- Campo obrigatório adicionado? → Migration necessária!
- Type mudou? → Atualizar TypeScript!

**Validações:**
```bash
# 1. Verificar Pydantic model (Python)
grep -r "class.*Model" python_backend/models*.py

# 2. Verificar TypeScript type (Frontend)
grep -r "interface.*Model" client/src/ shared/

# 3. Verificar compatibilidade
# Criar objeto de teste e validar em ambos os lados
```

---

## 🔧 SCRIPTS DE VALIDAÇÃO

### Rodar Antes de Commit

```bash
# Executar validações automáticas
bash scripts/validate-changes.sh

# Se PASSAR → Pode commitar
# Se FALHAR → Corrigir antes de commitar
```

### Validações Incluídas

1. **Type Checking (TypeScript)**
   ```bash
   npm run check
   ```

2. **Import Validation (Python)**
   ```bash
   python scripts/check-imports.py
   ```

3. **Endpoint Compatibility**
   ```bash
   python scripts/check-endpoints.py
   ```

4. **Naming Conventions**
   - PascalCase para componentes
   - camelCase para funções/hooks
   - snake_case para Python
   - UPPER_SNAKE_CASE para constantes

---

## 📝 TEMPLATE DE COMMIT

### Commit Message Format

```bash
tipo(escopo): descrição curta

[opcional] Documentação consultada:
- docs/ARCHITECTURE.md (seção X)
- docs/API_REFERENCE.md (endpoint Y)

[opcional] Validações feitas:
- ✅ Type check passou
- ✅ Imports validados
- ✅ Endpoints compatíveis
- ✅ Testado em desenvolvimento
```

**Tipos:**
- `feat`: Nova feature
- `fix`: Correção de bug
- `docs`: Mudança apenas em documentação
- `refactor`: Refatoração sem mudar comportamento
- `test`: Adicionar/corrigir testes
- `chore`: Manutenção

**Exemplos:**
```bash
git commit -m "feat(personas): adiciona campo industry sugerido

Documentação consultada:
- docs/API_REFERENCE.md (POST /api/personas/enhance)
- docs/FEATURES.md (Feature Melhorar com IA)

Validações:
- ✅ Types atualizados em client/src/pages/Personas.tsx
- ✅ Backend testado com curl
- ✅ Frontend testado no navegador"
```

---

## 🚦 PROCESSO PASSO-A-PASSO

### Passo 1: PLANEJAR (ANTES de tocar no código!)

```
1.1. Qual mudança preciso fazer?
     → Descrever em 1 frase clara

1.2. Que arquivos vou modificar?
     → Listar arquivos específicos

1.3. Que documentação devo ler?
     → Consultar índice: DOCUMENTATION_INDEX.md
     → Ler seções relevantes (15-30 min)

1.4. Alguém já fez algo similar?
     → Buscar em histórico: docs/DOCUMENTACAO_HISTORICA.md
     → Ler implementação anterior
```

---

### Passo 2: VALIDAR CONHECIMENTO

```
2.1. Entendo a arquitetura?
     → Se NÃO: Ler docs/ARCHITECTURE.md primeiro

2.2. Conheço as convenções?
     → Se NÃO: Ler docs/DEVELOPMENT.md primeiro

2.3. Sei que endpoints existem?
     → Se NÃO: Ler docs/API_REFERENCE.md primeiro

2.4. Entendo a feature afetada?
     → Se NÃO: Ler docs/FEATURES.md primeiro
```

**Se respondeu NÃO a qualquer pergunta: PARE e leia a documentação!**

---

### Passo 3: BUSCAR NO CÓDIGO EXISTENTE

```
3.1. Buscar padrões similares:
     grep -r "padrão-similar" .

3.2. Ver como foi feito antes:
     → Encontrar implementação parecida
     → Copiar PADRÃO (não código literal)

3.3. Verificar imports necessários:
     → Ver imports em arquivos similares

3.4. Identificar dependências:
     → Que outros arquivos/funções usa?
```

---

### Passo 4: IMPLEMENTAR

```
4.1. Seguir convenções documentadas:
     → docs/DEVELOPMENT.md (seção Convenções)

4.2. Manter compatibilidade:
     → Não quebrar contratos existentes
     → Se precisar quebrar: criar nova versão

4.3. Adicionar error handling:
     → Todo endpoint deve ter try/catch
     → Todo componente deve ter error boundary

4.4. Adicionar logging:
     → Python: print(f"[Module] Action: details")
     → Frontend: console.log('[Component] Action:', data)
```

---

### Passo 5: VALIDAR MUDANÇAS

```
5.1. Rodar validações automáticas:
     bash scripts/validate-changes.sh

5.2. Type check (TypeScript):
     npm run check

5.3. Testar manualmente:
     → Testar cenário principal
     → Testar casos de erro
     → Testar em diferentes browsers (se frontend)

5.4. Verificar logs:
     tail -f dev.local.log
     → Não deve ter erros
```

---

### Passo 6: DOCUMENTAR (SE NECESSÁRIO)

```
6.1. Mudança afeta API?
     → Atualizar docs/API_REFERENCE.md

6.2. Nova feature?
     → Atualizar docs/FEATURES.md
     → Adicionar em docs/CHANGELOG.md

6.3. Mudou arquitetura?
     → Atualizar docs/ARCHITECTURE.md

6.4. Novo processo?
     → Atualizar docs/DEVELOPMENT.md
```

---

## ⛔ LISTA DE "NÃO FAÇA"

### NUNCA faça isso sem consultar docs:

1. ❌ **Mudar modelo de IA** sem verificar TODOS os lugares que usam
   - Consultar: `grep -r "model=" python_backend/`

2. ❌ **Adicionar dependência nova** sem verificar compatibilidade
   - Consultar: `package.json`, `pyproject.toml`

3. ❌ **Mudar schema de endpoint** sem atualizar TypeScript
   - Consultar: `docs/API_REFERENCE.md` + `shared/schema.ts`

4. ❌ **Alterar timeout** sem verificar impacto
   - Consultar: `docs/API_REFERENCE.md` seção "Timeouts"

5. ❌ **Modificar rate limit** sem justificativa
   - Consultar: `docs/API_REFERENCE.md` seção "Rate Limits"

6. ❌ **Renomear componente** sem atualizar TODOS os imports
   - Buscar: `grep -r "OldName" client/src/`

7. ❌ **Mudar props de componente** sem verificar usos
   - Buscar: `grep -r "ComponentName" client/src/`

8. ❌ **Alterar environment variable** sem atualizar .env.example
   - Consultar: `SETUP.md` + `DEPLOY_ENV_EXAMPLE.txt`

---

## ✅ CHECKLIST DE PR (Pull Request)

Antes de abrir PR, validar:

### Código
- [ ] Type check passa (`npm run check`)
- [ ] Imports válidos (Python + TypeScript)
- [ ] Endpoints compatíveis
- [ ] Naming conventions seguidas
- [ ] Error handling implementado
- [ ] Logging adequado

### Testes
- [ ] Testado em desenvolvimento
- [ ] Casos de erro testados
- [ ] Smoke test passou
- [ ] Sem regressões visíveis

### Documentação
- [ ] Documentação relevante consultada (listar quais)
- [ ] Docs atualizadas (se necessário)
- [ ] Changelog atualizado (se feature/breaking change)

### Compatibilidade
- [ ] Frontend e backend compatíveis
- [ ] Schemas sincronizados
- [ ] Não quebra features existentes
- [ ] Migration criada (se mudou schema DB)

---

## 🎯 EXEMPLOS DE VALIDAÇÃO

### Exemplo 1: Adicionar Novo Endpoint

**Mudança:** Criar `POST /api/new-feature`

**Processo:**
```
✅ 1. Ler docs/API_REFERENCE.md (padrão de endpoints)
✅ 2. Ler docs/ARCHITECTURE.md (onde adicionar)
✅ 3. Buscar endpoint similar:
      grep -r "@app.post" python_backend/main.py
✅ 4. Copiar padrão:
      - Rate limit
      - Error handling
      - Logging
      - Response format
✅ 5. Implementar seguindo padrão
✅ 6. Testar com curl
✅ 7. Atualizar docs/API_REFERENCE.md
✅ 8. Commit com referências
```

---

### Exemplo 2: Modificar Componente React

**Mudança:** Adicionar prop a `ExpertCard`

**Processo:**
```
✅ 1. Ler docs/FEATURES.md (onde é usado)
✅ 2. Buscar todos os usos:
      grep -r "ExpertCard" client/src/
✅ 3. Ver interface atual:
      Ler ExpertCard.tsx (props interface)
✅ 4. Adicionar prop com valor default:
      newProp?: string = "default"
✅ 5. Atualizar TODOS os usos identificados
✅ 6. Type check:
      npm run check
✅ 7. Testar em TODAS as páginas que usam
✅ 8. Commit
```

---

### Exemplo 3: Corrigir Bug

**Mudança:** Fix erro 500 em endpoint

**Processo:**
```
✅ 1. Ler documentação do erro:
      Buscar: CORRECAO_*.md similar
✅ 2. Entender o que o endpoint DEVE fazer:
      docs/API_REFERENCE.md
✅ 3. Ver implementações similares:
      Buscar outros endpoints similares
✅ 4. Identificar causa raiz:
      Ver logs, debuggar
✅ 5. Aplicar fix seguindo padrão existente
✅ 6. Testar:
      - Cenário que quebrava
      - Cenários normais
      - Casos de erro
✅ 7. Documentar fix:
      Criar CORRECAO_*.md
✅ 8. Commit com referência ao fix
```

---

## 🎓 CULTURA DE QUALIDADE

### Princípios

1. **Documentação First**
   - Sempre consulte docs ANTES de mudar
   - Se docs não tem: adicione!
   - Se docs está errada: corrija!

2. **Padrões Consistentes**
   - Siga o padrão existente
   - Não invente novo padrão
   - Se precisa mudar padrão: discuta primeiro

3. **Compatibilidade**
   - Não quebre código existente
   - Mantenha backwards compatibility
   - Se precisa quebrar: versione (v2)

4. **Testing**
   - Teste ANTES de commitar
   - Teste casos de erro
   - Teste regressões

---

## 📊 MÉTRICAS DE SUCESSO

### Target (após implementação deste processo)

| Métrica | Antes | Target |
|---------|-------|--------|
| **Bugs por deploy** | 2-3 | <0.5 |
| **Breaking changes** | 30% | <5% |
| **Tempo de debug** | 2h | <30min |
| **Regressões** | 20% | <5% |

---

## 🚨 CONSEQUÊNCIAS DE NÃO SEGUIR

### Problemas que JÁ aconteceram por não seguir:

1. ❌ Erro 500 "Melhorar com IA" - Não instanciou cliente
2. ❌ Modo strategic genérico - Não verificou implementação existente
3. ❌ Conselho sumindo - Lógica invertida por não entender estado
4. ❌ Timeout 30s - Não consultou docs de timing

**Tempo perdido corrigindo:** ~3 horas  
**Tempo que teria levado se consultasse docs:** ~10 minutos

**Economia se tivesse seguido processo:** 94%

---

## ✅ BENEFÍCIOS DE SEGUIR

### Se você seguir este processo:

1. ✅ **Menos bugs** (90% redução)
2. ✅ **Código mais consistente**
3. ✅ **Mudanças mais rápidas** (sem refazer)
4. ✅ **Onboarding mais fácil** (padrões claros)
5. ✅ **Manutenção mais barata**
6. ✅ **Confiança no código**

---

## 📞 DÚVIDAS?

### Não tem certeza se deve consultar documentação?

**RESPOSTA: SEMPRE CONSULTE!**

**Regra de ouro:** Se você está em dúvida, leia a documentação.

### Não encontrou documentação?

1. Buscar no índice: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
2. Buscar no histórico: [docs/DOCUMENTACAO_HISTORICA.md](docs/DOCUMENTACAO_HISTORICA.md)
3. Se realmente não existe: CRIE antes de implementar!

---

## 🎯 RESUMO - TL;DR

### ANTES de qualquer mudança de código:

1. ✅ **LER** documentação relevante (15-30 min)
2. ✅ **BUSCAR** padrões similares no código
3. ✅ **VALIDAR** compatibilidade
4. ✅ **IMPLEMENTAR** seguindo padrões
5. ✅ **TESTAR** completamente
6. ✅ **RODAR** scripts de validação
7. ✅ **DOCUMENTAR** se necessário

### NÃO:
- ❌ Copiar código sem entender
- ❌ Mudar sem consultar docs
- ❌ Assumir que "deve funcionar"
- ❌ Commitar sem testar

---

## 🔗 LINKS RÁPIDOS

### Documentação Essencial
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Índice completo
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura
- [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - API
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Convenções
- [docs/FEATURES.md](docs/FEATURES.md) - Features

### Scripts
- `scripts/validate-changes.sh` - Validação completa
- `scripts/check-imports.py` - Imports Python
- `scripts/check-endpoints.py` - Endpoints

### Templates
- `.github/pull_request_template.md` - Template de PR

---

**SEGUIR ESTE PROCESSO É OBRIGATÓRIO! ⚠️**

**Resultado:** Sistema estável, código consistente, menos bugs, mais velocidade! 🚀

---

**Versão:** 1.0  
**Mantido por:** Time AdvisorIA Elite  
**Última atualização:** 3 de Novembro de 2025

