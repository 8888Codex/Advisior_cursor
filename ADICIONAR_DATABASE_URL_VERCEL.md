# 🔑 ADICIONAR DATABASE_URL NA VERCEL

## ⚡ AÇÃO IMEDIATA (1 minuto)

### Passo 1: Acessar Vercel

1. Ir para: https://vercel.com/dashboard
2. Clicar no projeto **`advisior-cursor`**

### Passo 2: Adicionar DATABASE_URL

1. No menu lateral, clicar em **Settings**
2. Clicar em **Environment Variables**
3. Clicar em **"Add New"**

**Configurar:**
- **Key:** `DATABASE_URL`
- **Value:** 
  ```
  postgresql://neondb_owner:npg_nOTlR6gMra9G@ep-quiet-shape-addtxqaq-pooler.c-2.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require
  ```
- **Environments:** Selecionar **Production**, **Preview** e **Development** (todos)

4. Clicar em **Save**

### Passo 3: Aguardar Redeploy Automático

A Vercel vai detectar a nova variável e fazer redeploy automático (~2 minutos)

**Acompanhe em:** https://vercel.com/dashboard → advisior-cursor → Deployments

---

## ✅ APÓS REDEPLOY COMPLETAR

### Verificar Backend

```bash
curl https://advisior-cursor.vercel.app/
```

**Deve retornar:**
```json
{
  "message": "...",
  "status": "running",
  "database_status": "ok",
  "experts_count": 0,
  "ready": false
}
```

Se `database_status: "ok"` → Banco conectado! ✅

---

### Popular com 18 Especialistas

**Abra este link no navegador:**
```
https://advisior-cursor.vercel.app/api/admin/seed-experts
```

**OU use curl:**
```bash
curl -X POST https://advisior-cursor.vercel.app/api/admin/seed-experts
```

**Deve retornar:**
```json
{
  "success": true,
  "total_experts": 18,
  "sample_experts": ["Philip Kotler", "Seth Godin", ...]
}
```

---

### Verificar Especialistas

**Abra no navegador:**
```
https://advisior-cursor.vercel.app/experts
```

🎉 **DEVE MOSTRAR 18 ESPECIALISTAS!**

---

## 🎯 RESUMO

1. ✅ Adicionar DATABASE_URL na Vercel (1 min)
2. ⏳ Aguardar redeploy (2 min)
3. ✅ Popular banco (30 seg)
4. ✅ Ver especialistas! (imediato)

**TOTAL: ~3-4 minutos**

---

## 📊 O QUE VAI ACONTECER

```
[Vercel detecta nova variável]
    ↓
[Trigger redeploy automático]
    ↓
[Build: npm run build] (frontend + server)
    ↓
[Deploy: node dist/index.js]
    ↓
[Server Node.js inicia Python automático]
    ↓
[Python conecta ao Neon via DATABASE_URL]
    ↓
[Sistema online aguardando seed]
```

---

**⚡ FAÇA O PASSO 1-2 AGORA E ME AVISE QUANDO REDEPLOY COMPLETAR!**

Quando completar, eu executo o seed automaticamente via MCP! 🚀

