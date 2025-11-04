# 🚀 Deploy - AdvisorIA Elite

## Variáveis de Ambiente Necessárias

### Obrigatórias
```bash
# Anthropic API (para clones de especialistas)
ANTHROPIC_API_KEY=sk-ant-...

# Perplexity API (para pesquisa de personas)
PERPLEXITY_API_KEY=pplx-...

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database
```

### Opcionais
```bash
# Porta do servidor (default: 5500)
PORT=5500

# Porta do backend Python (default: 5501)
PY_PORT=5501

# Ambiente
NODE_ENV=production

# Backend Python externo (se rodar separadamente)
PY_EXTERNAL=http://python-backend-url:5501
```

---

## Deploy no Vercel (Recomendado)

**Para instruções detalhadas, veja [VERCEL_SETUP.md](./VERCEL_SETUP.md)**

### Quick Start:

1. **Criar PostgreSQL:**
   - Na Vercel: Storage → Create Database → Postgres
   - Ou usar Neon/Supabase/Railway

2. **Configurar Variáveis:**
   ```bash
   DATABASE_URL=postgresql://...
   ANTHROPIC_API_KEY=sk-ant-...
   PERPLEXITY_API_KEY=pplx-...
   ```

3. **Deploy:**
   - Push para GitHub → Deploy automático

4. **Popular Especialistas:**
   ```bash
   curl -X POST https://seu-app.vercel.app/api/admin/seed-experts
   ```

5. **Verificar:**
   ```bash
   curl https://seu-app.vercel.app/
   # Deve retornar: "experts_count": 18, "ready": true
   ```

📖 **Guia completo:** [VERCEL_SETUP.md](./VERCEL_SETUP.md)

---

## Deploy no Railway

### 1. Configurar Variáveis de Ambiente

No painel do Railway, adicionar:
- `ANTHROPIC_API_KEY`
- `PERPLEXITY_API_KEY`
- `DATABASE_URL` (Railway fornece automaticamente se adicionar PostgreSQL)
- `PORT` (Railway configura automaticamente)
- `NODE_ENV=production`

### 2. Build Command
```bash
npm run build
```

### 3. Start Command
```bash
npm start
```

### 4. Health Check
```
GET /api/experts
```

Deve retornar lista de especialistas (status 200).

---

## Deploy Manual (VPS/Server)

### 1. Requisitos
- Node.js 20+
- Python 3.11+
- PostgreSQL 14+
- npm 9+

### 2. Instalação
```bash
# Clone
git clone https://github.com/8888Codex/Advisior_cursor.git
cd Advisior_cursor

# Instalar dependências Node
npm install

# Instalar dependências Python
pip install -r python_backend/requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves
```

### 3. Build
```bash
npm run build
```

### 4. Iniciar
```bash
# Produção
npm start

# Desenvolvimento
./start_reliable.sh
```

---

## Portas Expostas

| Serviço | Porta | Público | Descrição |
|---------|-------|---------|-----------|
| Frontend + API | 5500 | Sim | Porta principal (único ponto de entrada) |
| Backend Python | 5501 | Não | Interno (proxy via Node.js) |

**IMPORTANTE:** Apenas a porta 5500 precisa ser exposta publicamente.

---

## Verificação Pós-Deploy

### 1. Health Check Frontend
```bash
curl http://your-domain.com/api/experts
```

Deve retornar JSON com ~22 especialistas.

### 2. Testar Proxy
```bash
curl http://your-domain.com/api/personas
```

Deve retornar lista de personas ou array vazio (status 200).

### 3. Testar Frontend
Acessar no navegador:
```
http://your-domain.com
```

Deve carregar página inicial.

---

## Troubleshooting

### Erro: "Python backend not responding"
**Solução:** Verificar se `PY_PORT` está correto e se Python está rodando

### Erro: "ANTHROPIC_API_KEY not set"
**Solução:** Adicionar variável de ambiente no Railway/servidor

### Erro: "Database connection failed"
**Solução:** Verificar `DATABASE_URL` e conectividade com PostgreSQL

### Erro: "Port already in use"
**Solução:** Mudar `PORT` para porta disponível (Railway configura automaticamente)

---

## Monitoramento

### Logs
```bash
# Ver logs em produção
tail -f /var/log/advisoria.log
```

### Métricas Importantes
- Taxa de sucesso de análises do conselho
- Tempo médio de resposta
- Taxa de erro em criação de personas
- Usage de APIs (Anthropic, Perplexity)

---

## Atualizações

### Para atualizar o sistema:
```bash
git pull origin main
npm install
npm run build
# Reiniciar servidor
```

---

## Suporte

Para problemas de deploy, verificar:
1. Logs do servidor
2. Status das APIs externas
3. Conectividade com banco de dados
4. Variáveis de ambiente configuradas

---

**Última atualização:** 3 de Novembro de 2025  
**Versão:** 2.0.0
