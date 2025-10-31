# Guia de Deploy - AdvisorIA Elite

## Variáveis de Ambiente Obrigatórias

Copie `DEPLOY_ENV_EXAMPLE.txt` para `.env` e preencha:

```bash
# Node/Express Server
NODE_ENV=production
PORT=3000                    # Porta do servidor Node (UI + BFF)

# Python Backend (FastAPI)
PY_PORT=5200                 # Porta do backend Python (ou use PY_EXTERNAL se externo)
PY_EXTERNAL=http://...       # Opcional: URL externa do Python backend

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# APIs de IA (obrigatórias)
ANTHROPIC_API_KEY=sk-ant-... # Obrigatório para consenso do conselho

# APIs Opcionais
PERPLEXITY_API_KEY=pplx-...  # Opcional: usado em auto-clone de experts
```

## Scripts Disponíveis

### Desenvolvimento Local

```bash
# Portas padrão: UI 3000, Python 5200
npm run dev:py5200

# Ou customizar portas
PORT=3000 PY_PORT=5300 npm run dev
```

### Build de Produção

```bash
# Build completo (client + server)
npm run build

# Iniciar em produção
npm start
```

### Verificação de Tipos

```bash
npm run check  # TypeScript type checking
```

## Health Checks

- **UI/Frontend**: `GET http://localhost:3000` → deve retornar 200
- **API Backend**: `GET http://localhost:5200/api/health` → `{"status":"ok","service":"AdvisorIA API"}`

## Portas e Configuração

### Portas Padrão

- **3000**: Servidor Node/Express (UI + BFF)
- **5200**: Backend Python (FastAPI/Uvicorn)

### Resolução de Conflitos

Se portas estiverem ocupadas:

```bash
# Liberar portas
lsof -ti :3000 | xargs -r kill -9
lsof -ti :5200 | xargs -r kill -9

# Ou usar portas alternativas
PORT=3001 PY_PORT=5300 npm run dev
```

## Deploy em Railway/Similar

1. Configure variáveis de ambiente acima
2. Build será executado automaticamente via `npm run build`
3. Start será executado via `npm start`
4. Se Python estiver em serviço separado, use `PY_EXTERNAL` em vez de `PY_PORT`

## Troubleshooting

### Erro: "ANTHROPIC_API_KEY não encontrada"
- Verifique se `.env` existe na raiz do projeto
- Confirme que variável está definida: `ANTHROPIC_API_KEY=sk-ant-...`

### Erro: "Address already in use"
- Use scripts para matar processos nas portas antes de iniciar
- Ou configure portas alternativas via variáveis de ambiente

### Erro: "Could not resolve authentication method"
- Backend Python não está encontrando `ANTHROPIC_API_KEY`
- Verifique que `.env` está sendo carregado corretamente no Python

