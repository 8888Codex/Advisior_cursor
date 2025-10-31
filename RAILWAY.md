# Deploy no Railway (MVP sem Auth)

## 1) Criar Projeto e Banco
1. Acesse Railway e crie um projeto.
2. Adicione um Postgres (Plugin → Database → Postgres) e copie a `DATABASE_URL`.

## 2) Conectar Repositório
1. Add New → GitHub Repo → `8888Codex/Advisior_cursor`.
2. Build default (Nixpacks) já funciona.

## 3) Variáveis de Ambiente (Service → Variables)
- NODE_ENV=production
- PORT=5000
- PY_PORT=5001
- DATABASE_URL=postgresql://... (do Postgres do Railway)
- ANTHROPIC_API_KEY=...
- PERPLEXITY_API_KEY=...

## 4) Start Command
- Start command: `npm start`

## 5) Deploy
- Clique em Deploy. Ao finalizar, abra o domínio gerado.

## 6) Smoke test (produção)
- GET `/` → deve carregar o app (frontend).
- GET `/api/experts` → lista de experts.
- Criar conversa e enviar mensagem (pela UI) → resposta da IA.
- Council (SSE) → verificar barra de progresso e eventos.
- Personas (modo quick) → criar e listar.

## Notas
- Não precisa Nginx no Railway (SSE funciona via Node proxy).
- Auth ficará para depois (migrar tabelas antes).
