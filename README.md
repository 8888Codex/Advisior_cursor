# AdvisorIA Elite

**Versão:** 2.0.0  
**Status:** Produção  
**Última Atualização:** 3 de Novembro de 2025

Plataforma de consultoria de marketing com IA baseada em clones cognitivos de 22 lendas do marketing.

---

## Funcionalidades Principais

### 🧠 22 Clones Cognitivos de Alta Fidelidade
Converse 1-on-1 com lendas do marketing:
- Philip Kotler, Seth Godin, Gary Vaynerchuk
- Neil Patel, Alex Hormozi, David Ogilvy
- E mais 16 especialistas!

### 👥 Conselho de IA com Múltiplos Experts
Obtenha análise colaborativa:
- Selecione 2-8 especialistas
- Análise paralela do seu problema
- Consensus automático
- Plano de ação estruturado
- Chat continuado em grupo

### 🎭 Persona Builder Ultra-Específico
Crie personas de qualidade máxima:
- **Modo Quick:** 10s - Bom para testes
- **Modo Strategic:** 80s - Pesquisa profunda com 3 chamadas Perplexity
- **IA Enhancement:** Transforma descrições vagas em ultra-específicas
- Frameworks: JTBD + BAG + Pain Points Quantificados

### 🤖 Auto-Clone de Experts
Crie novos especialistas automaticamente:
- Framework EXTRACT de 20 pontos
- Pesquisa biográfica profunda
- System prompts de alta fidelidade
- Chat de teste integrado

---

## Quick Start

### Instalação

```bash
# 1. Instalar dependências
npm install
pip install -r python_backend/requirements.txt

# 2. Configurar .env
cp DEPLOY_ENV_EXAMPLE.txt .env
# Edite .env com suas API keys

# 3. Iniciar
./start.sh
```

### Acessar

```
http://localhost:5500
```

### Primeiros Passos

1. **Crie uma Persona** → `/personas`
2. **Consulte o Conselho** → `/test-council`
3. **Chat com Expert** → `/experts`
4. **Crie Novo Expert** → `/create`

---

## Tecnologias

### Stack
- **Frontend:** React 18 + TypeScript + Vite + TailwindCSS
- **Backend:** FastAPI (Python) + Express (Node.js)
- **Database:** PostgreSQL (Neon)
- **AI:** Anthropic Claude Sonnet 4 + Perplexity AI

### APIs
- **Anthropic:** Chat, análise, síntese
- **Perplexity:** Pesquisa de personas e biografias

---

## Documentação

### Principais
- 📖 [Guia do Usuário](docs/USER_GUIDE.md) - Como usar o sistema
- 🏗️ [Arquitetura](docs/ARCHITECTURE.md) - Estrutura técnica
- 🔌 [API Reference](docs/API_REFERENCE.md) - Endpoints e schemas
- 💻 [Development Guide](docs/DEVELOPMENT.md) - Para desenvolvedores
- 📝 [Changelog](docs/CHANGELOG.md) - Histórico de versões
- ⭐ [Features](docs/FEATURES.md) - Catálogo completo

### Setup e Deploy
- [SETUP.md](SETUP.md) - Configuração detalhada
- [DEPLOY.md](DEPLOY.md) - Deploy (Railway, Replit)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solução de problemas

### Navegação Completa
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Índice de toda documentação

---

## Variáveis de Ambiente

Crie arquivo `.env` na raiz:

```bash
# Database (obrigatório)
DATABASE_URL=postgresql://user:password@host:port/database

# APIs (obrigatórias)
ANTHROPIC_API_KEY=sk-ant-api03-...
PERPLEXITY_API_KEY=pplx-...

# Portas (opcional - usa padrão se não definir)
PORT=5500
PY_PORT=5501
NODE_ENV=development
```

**Como obter:**
- **Database:** https://neon.tech/ (free tier)
- **Anthropic:** https://console.anthropic.com/
- **Perplexity:** https://www.perplexity.ai/settings/api

---

## Scripts Disponíveis

```bash
# Desenvolvimento
npm run dev              # Inicia frontend + backend
./start.sh              # Script completo (mata portas + inicia)

# Build
npm run build           # Build para produção

# Start produção
npm start               # Após build

# Utilities
npm run check           # TypeScript type checking
bash scripts/smoke-test.sh  # Teste de endpoints
```

---

## Deploy

### Railway (Recomendado)

```bash
# 1. Criar PostgreSQL no Railway
railway add postgresql

# 2. Configurar variáveis
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set PERPLEXITY_API_KEY=pplx-...
railway variables set NODE_ENV=production

# 3. Deploy
railway up
```

**Documentação:** [RAILWAY.md](RAILWAY.md)

---

### Replit

Veja instruções em: [replit.md](replit.md)

---

## Arquitetura

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ↓
┌─────────────────────────┐
│  Node.js (Port 5500)    │
│  ├── Serve Frontend     │
│  └── Proxy → Python     │
└──────┬──────────────────┘
       │ Proxy
       ↓
┌─────────────────────────┐
│  FastAPI (Port 5501)    │
│  ├── Experts API        │
│  ├── Personas API       │
│  └── Council API        │
└──────┬──────────────────┘
       │
       ├──→ Anthropic Claude (Chat/Analysis)
       ├──→ Perplexity AI (Research)
       └──→ PostgreSQL (Storage)
```

**Detalhes:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Estrutura de Pastas

```
AdvisorIAElite/
├── client/              # React frontend
├── server/              # Node.js proxy
├── python_backend/      # FastAPI backend
├── shared/              # Tipos compartilhados
├── docs/                # Documentação estruturada
├── scripts/             # Scripts utilitários
└── [108 arquivos .md]   # Docs de implementação
```

---

## Rate Limits

| Operação | Limite |
|----------|--------|
| Criar Persona | 10/hora |
| Melhorar com IA | 30/hora |
| Auto-clone Expert | 5/hora |
| Consultar Conselho | 10/hora |
| Chat 1-on-1 | 60/hora |

---

## Custos Estimados

### Por Operação

| Feature | Tempo | Custo |
|---------|-------|-------|
| Chat 1-on-1 | ~5s | $0.02 |
| Persona Quick | ~10s | $0.02 |
| Persona Strategic | ~80s | $0.20 |
| Enhance Description | ~5s | $0.01 |
| Council (3 experts) | ~60s | $0.20 |
| Auto-Clone | ~150s | $0.40 |

### Mensal (uso moderado)

- **Desenvolvimento:** ~$20/mês
- **Produção (100 users):** ~$200-500/mês

---

## Troubleshooting

### Problemas Comuns

**"Port already in use"**
```bash
./start.sh  # Script já mata processos antigos
```

**"PERPLEXITY_API_KEY not found"**
```bash
# Adicione ao .env
PERPLEXITY_API_KEY=pplx-sua-chave
```

**"Timeout após 30000ms"**
- Corrigido na v2.0.0! Timeout agora é 120s.
- Recarregue a página (Cmd+Shift+R)

**"Conselho aparece e some"**
- Corrigido na v2.0.0!
- Recarregue a página

**Mais soluções:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/):
- **MAJOR:** Mudanças incompatíveis
- **MINOR:** Novas funcionalidades
- **PATCH:** Correções de bugs

**Versão atual:** 2.0.0

**Histórico completo:** [docs/CHANGELOG.md](docs/CHANGELOG.md)

---

## Contribuindo

Contribuições são bem-vindas!

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m "feat: adiciona nova feature"`
4. Push: `git push origin feature/nova-feature`
5. Abra Pull Request

**Guia completo:** [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

## Licença

MIT License

---

## Suporte

- 📖 [Documentação Completa](DOCUMENTATION_INDEX.md)
- 🐛 [Issues](TROUBLESHOOTING.md)
- 💬 [Discussões](#) (futuro)

---

## Autores

**Time AdvisorIA Elite**

---

## Agradecimentos

- Anthropic pelo Claude Sonnet 4
- Perplexity AI pela API de pesquisa
- Neon pelo PostgreSQL serverless
- Todas as 22 lendas do marketing que inspiraram os clones

---

**Versão:** 2.0.0  
**Build:** Estável  
**Status:** ✅ Produção Ready

**[Ver Documentação Completa →](DOCUMENTATION_INDEX.md)**

