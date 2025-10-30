# AdvisorIA Elite

MVP pronto para publicação (sem Auth por enquanto). Frontend React + Node/Express (porta 5000) e backend FastAPI (porta 5001) com proxy automático.

## Rodar local

```bash
bash start.sh
```

## Variáveis de ambiente
Veja `DEPLOY_ENV_EXAMPLE.txt` e crie seu `.env` com as chaves e o DATABASE_URL.

## Deploy recomendado (Railway)
1. Crie um Postgres no Railway e copie a `DATABASE_URL`.
2. Crie um serviço a partir deste repositório e defina:
   - `NODE_ENV=production`
   - `PORT=5000`
   - `PY_PORT=5001`
   - `DATABASE_URL=...`
   - `ANTHROPIC_API_KEY=...`
   - `PERPLEXITY_API_KEY=...`
3. Start command: `npm start`
4. Abra o domínio gerado e faça o smoke test: Experts, Chat, Council (SSE), Personas.

## Observações
- SSE funciona via proxy do Node; não precisa Nginx no Railway.
- Auth e Perfil de Negócio serão habilitados depois (migrar tabelas antes).
