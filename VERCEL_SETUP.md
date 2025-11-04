# 🚀 Setup Vercel + PostgreSQL - AdvisorIA Elite

## Visão Geral

Este guia explica como fazer deploy do AdvisorIA Elite na Vercel com banco de dados PostgreSQL.

---

## 1. Provisionar PostgreSQL

### Opção A: Vercel Postgres (Recomendado)

**Mais fácil e totalmente integrado:**

1. No painel da Vercel, acessar seu projeto
2. Ir em **"Storage"** no menu lateral
3. Clicar em **"Create Database"**
4. Selecionar **"Postgres"**
5. Seguir o wizard de criação
6. ✅ `DATABASE_URL` será configurada automaticamente como variável de ambiente

### Opção B: Neon (Postgres Serverless)

**Gratuito e rápido:**

1. Acessar https://neon.tech
2. Criar conta gratuita
3. Criar novo projeto PostgreSQL
4. Copiar a **connection string** (ex: `postgresql://user:pass@ep-xxx.neon.tech/main`)
5. Adicionar como variável de ambiente `DATABASE_URL` na Vercel

### Opção C: Supabase

**Inclui mais features (auth, storage):**

1. Acessar https://supabase.com
2. Criar projeto
3. Em **Settings → Database**, copiar **Connection String** (modo "Transaction")
4. Adicionar como `DATABASE_URL` na Vercel

### Opção D: Railway

**Boa para apps complexos:**

1. Acessar https://railway.app
2. Criar novo PostgreSQL
3. Copiar `DATABASE_URL`
4. Adicionar na Vercel

---

## 2. Configurar Variáveis de Ambiente na Vercel

### Passo a Passo:

1. No painel da Vercel, ir em **Settings → Environment Variables**
2. Adicionar as seguintes variáveis:

#### Obrigatórias:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
ANTHROPIC_API_KEY=sk-ant-api03-...
PERPLEXITY_API_KEY=pplx-...
```

#### Opcionais (mas recomendadas):

```bash
NODE_ENV=production
PORT=5500
PY_PORT=5501
```

3. Clicar em **"Save"** para cada variável
4. Escolher environment: **Production**, **Preview**, ou **Both** (recomendado: Both)

---

## 3. Conectar ao GitHub e Deploy

### Se ainda não conectou:

1. Na Vercel, clicar em **"Add New Project"**
2. Selecionar **"Import Git Repository"**
3. Escolher o repositório: `8888Codex/Advisior_cursor`
4. Configurar:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist/public`
   - **Install Command:** `npm install`

5. Clicar em **"Deploy"**

### Se já está conectado:

- Push para `main` → Vercel faz redeploy automático

---

## 4. Popular Banco com Especialistas (Importante!)

Após o primeiro deploy bem-sucedido, **o banco estará vazio**. Você precisa popular com os 18 especialistas.

### Método 1: Endpoint de Seeding Manual (Recomendado)

Faça um POST request para o endpoint de admin:

```bash
curl -X POST https://seu-app.vercel.app/api/admin/seed-experts
```

**Ou acesse direto no navegador:**
```
https://seu-app.vercel.app/api/admin/seed-experts
```

**Resposta esperada:**
```json
{
  "success": true,
  "message": "Seeding completado. 18 especialistas adicionados.",
  "experts_before": 0,
  "experts_after": 18,
  "total_experts": 18,
  "sample_experts": ["Philip Kotler", "Seth Godin", "Gary Vaynerchuk", ...]
}
```

### Método 2: Trigger via Redeploy

Se o seeding automático no startup falhou:

1. Na Vercel, ir em **Deployments**
2. Clicar em **"..."** no último deployment
3. Selecionar **"Redeploy"**
4. Sistema tentará fazer seeding automaticamente

---

## 5. Verificar Sucesso do Deploy

### Health Check:

```bash
curl https://seu-app.vercel.app/
```

**Resposta esperada (sucesso):**
```json
{
  "message": "AdvisorIA - Marketing Legends API",
  "status": "running",
  "database_status": "ok",
  "experts_count": 18,
  "expected_experts": 18,
  "ready": true
}
```

### Listar Especialistas:

```bash
curl https://seu-app.vercel.app/api/experts
```

Deve retornar array com 18 especialistas.

### Testar Frontend:

Acessar no navegador:
```
https://seu-app.vercel.app/
```

---

## 6. Troubleshooting

### Problema: `"experts_count": 0`

**Sintoma:** Página de especialistas vazia

**Causa:** Banco não foi populado

**Solução:**
```bash
# Fazer seeding manual
curl -X POST https://seu-app.vercel.app/api/admin/seed-experts
```

---

### Problema: `"database_status": "error"`

**Sintoma:** Erro ao conectar ao banco

**Causa:** `DATABASE_URL` não configurada ou inválida

**Solução:**
1. Verificar se `DATABASE_URL` está configurada na Vercel
2. Testar connection string localmente:
   ```bash
   psql "postgresql://user:pass@host:port/db"
   ```
3. Se Vercel Postgres: verificar se database foi criada
4. Se externo (Neon/Supabase): verificar se projeto está ativo

---

### Problema: `"database_url_configured": false`

**Sintoma:** Diagnóstico mostra DATABASE_URL não setada

**Causa:** Variável de ambiente não configurada ou com nome errado

**Solução:**
1. Ir em **Settings → Environment Variables** na Vercel
2. Adicionar `DATABASE_URL=postgresql://...`
3. Salvar e fazer redeploy

---

### Problema: Build falha no Vercel

**Sintoma:** Deploy não completa, erro no build

**Possíveis causas:**
- Arquivo faltando (verificar se todos foram commitados)
- Dependência faltando (verificar `package.json`)
- Erro de TypeScript (rodar `npm run check` localmente)

**Solução:**
1. Ver logs completos do build na Vercel
2. Reproduzir localmente:
   ```bash
   npm run build
   ```
3. Corrigir erros e fazer novo push

---

### Problema: Frontend carrega mas API não responde

**Sintoma:** Página principal funciona mas `/api/experts` retorna 404

**Causa:** Proxy Node.js → Python não está funcionando

**Solução:**
1. Verificar se Python backend está rodando
2. Ver logs de runtime na Vercel
3. Verificar se `PY_PORT` está configurada
4. Verificar se `server/index.ts` está configurado corretamente

---

## 7. Diagnóstico Completo

Use o endpoint de diagnóstico para ver status detalhado:

```bash
curl https://seu-app.vercel.app/api/admin/db-status
```

**Resposta esperada (tudo OK):**
```json
{
  "database_url_configured": true,
  "connection_ok": true,
  "experts_table_exists": true,
  "experts_count": 18,
  "sample_experts": [
    "Philip Kotler",
    "Seth Godin",
    "Gary Vaynerchuk",
    "Neil Patel",
    "Alex Hormozi"
  ],
  "errors": []
}
```

---

## 8. Logs e Monitoramento

### Ver Logs na Vercel:

1. Ir em **Deployments**
2. Clicar no deployment ativo
3. Clicar em **"Function Logs"** ou **"Build Logs"**

### Logs do Startup:

Procurar por:
- `[Startup] ✅ Connected to PostgreSQL database`
- `[Startup] ✅ Seeded 18 marketing legends successfully`
- `[Startup] ✅ Sample experts: ['Philip Kotler', ...]`

Se ver:
- `[Startup] ❌ Failed to connect to database`
- `[Startup] ⚠️ Sistema irá iniciar mas sem especialistas!`

→ Verificar DATABASE_URL e fazer seeding manual

---

## 9. Checklist Final

Antes de considerar deploy completo, verificar:

- [ ] Deploy completou sem erros
- [ ] `DATABASE_URL` configurada
- [ ] Banco PostgreSQL provisionado e acessível
- [ ] `ANTHROPIC_API_KEY` configurada
- [ ] `PERPLEXITY_API_KEY` configurada
- [ ] Health check retorna `"ready": true`
- [ ] `/api/experts` retorna 18 especialistas
- [ ] Frontend carrega corretamente
- [ ] Consegue criar personas
- [ ] Consegue consultar conselho
- [ ] Chat com especialistas funciona

---

## 10. Próximos Passos

Após deploy bem-sucedido:

1. **Configurar domínio customizado** (opcional)
   - Na Vercel, ir em **Settings → Domains**
   - Adicionar seu domínio
   - Configurar DNS conforme instruções

2. **Configurar alertas** (opcional)
   - Monitorar uptime
   - Alertas de erro

3. **Backup do banco** (importante!)
   - Configurar backups automáticos no provider PostgreSQL
   - Neon, Supabase e Railway oferecem isso nativamente

---

## 🆘 Suporte

**Se nada funcionar:**

1. Verificar logs completos na Vercel
2. Testar localmente:
   ```bash
   ./start_reliable.sh
   # Acessa: http://localhost:5500
   ```
3. Verificar se todas as variáveis de ambiente estão setadas
4. Usar endpoint de diagnóstico:
   ```bash
   curl https://seu-app.vercel.app/api/admin/db-status
   ```

---

**Documentação Adicional:**
- [DEPLOY.md](./DEPLOY.md) - Instruções gerais de deploy
- [README.md](./README.md) - Visão geral do sistema
- [Vercel Docs](https://vercel.com/docs) - Documentação oficial

---

**Última atualização:** 4 de Novembro de 2025  
**Versão:** 2.1.0

