# ✅ CHECKLIST DE PRODUÇÃO - AdvisorIA

## 🎯 PRÉ-DEPLOY

### Sistema Local
- [x] 18 especialistas no banco Neon
- [x] Chat 1-on-1 funcional (tabelas conversations/messages)
- [x] Conselho de especialistas funcional
- [x] Todas correções commitadas
- [x] Push para GitHub realizado

### GitHub
- [x] Repositório atualizado
- [x] Commit: `fix: corrigido chat com tabelas conversations e messages`
- [x] Branch: `main`

---

## 🚀 DEPLOY EM ANDAMENTO

### Backend Render.com
- [x] Redeploy triggerado via push
- [ ] **AGUARDANDO:** Build completar (10-15 min)
- [ ] Status 200 OK no health check
- [ ] API `/api/experts` retornando 18 especialistas
- [ ] Tabelas conversations/messages criadas
- [ ] Banco Neon conectado

**Verificar:**
- Status do deploy em: https://render.com/dashboard
- Logs de build/erro
- Variáveis de ambiente configuradas

### Frontend Vercel
- [x] Já está online (https://advisior-cursor.vercel.app)
- [ ] Variável `PY_EXTERNAL` configurada
- [ ] Redeploy após Render ficar online
- [ ] Conectado ao backend Render

---

## 🧪 TESTES DE PRODUÇÃO

### 1. Backend Render
```bash
# Health check
curl https://advisior-cursor.onrender.com/
# Espera: { "message": "AdvisorIA - Marketing Legends API", "status": "running", ... }

# Especialistas
curl https://advisior-cursor.onrender.com/api/experts
# Espera: Array com 18 especialistas

# Popular banco (se vazio)
curl -X POST https://advisior-cursor.onrender.com/api/admin/seed-experts
```

- [ ] Health check retorna 200
- [ ] 18 especialistas disponíveis
- [ ] Database status: OK

### 2. Frontend Vercel
```bash
# Homepage
curl https://advisior-cursor.vercel.app/
# Espera: HTML da aplicação

# API proxy
curl https://advisior-cursor.vercel.app/api/experts
# Espera: Array com 18 especialistas (proxy para Render)
```

- [ ] Homepage carrega (200)
- [ ] API proxy funciona (Vercel → Render)
- [ ] Sem erros 404/500

### 3. Chat Individual (Browser)
1. [ ] Abrir https://advisior-cursor.vercel.app/experts
2. [ ] Clicar em um especialista (ex: Al Ries & Jack Trout)
3. [ ] Página de chat carrega
4. [ ] Enviar mensagem: "Olá, qual seu nome?"
5. [ ] IA responde em ~10 segundos
6. [ ] Resposta é personalizada ao especialista
7. [ ] Mensagens persistem ao recarregar página

### 4. Conselho de Especialistas (Browser)
1. [ ] Abrir https://advisior-cursor.vercel.app/personas
2. [ ] Criar uma persona (Nome: "Teste", Empresa: "ABC", etc.)
3. [ ] Ir para "Consultar Conselho"
4. [ ] Inserir problema: "Como aumentar vendas?"
5. [ ] Selecionar 3+ especialistas
6. [ ] Clicar "Consultar Conselho"
7. [ ] Animação dos especialistas aparece
8. [ ] Especialistas "conversam" (activity feed)
9. [ ] Resultado completo é exibido (~60s)
10. [ ] Resultado contém contribuições dos especialistas

### 5. Persistência de Dados
1. [ ] Criar conversa
2. [ ] Enviar mensagem
3. [ ] Fechar browser
4. [ ] Abrir novamente
5. [ ] Conversa e mensagens ainda existem

---

## 🔧 VARIÁVEIS DE AMBIENTE

### Render.com - Backend Python
- [ ] `DATABASE_URL` (Neon PostgreSQL)
- [ ] `ANTHROPIC_API_KEY`
- [ ] `PERPLEXITY_API_KEY`

### Vercel - Frontend React
- [ ] `PY_EXTERNAL` = `https://advisior-cursor.onrender.com`

---

## ✅ CRITÉRIOS DE SUCESSO

Sistema está em produção quando **TODOS** checados:

### Infraestrutura
- [ ] Frontend Vercel: Status 200
- [ ] Backend Render: Status 200
- [ ] Banco Neon: Conectado e populado

### Funcionalidades
- [ ] 18 especialistas visíveis
- [ ] Chat 1-on-1 funciona
- [ ] IA responde corretamente
- [ ] Conselho multi-especialista funciona
- [ ] Animações carregam
- [ ] Dados persistem no banco

### Qualidade
- [ ] Console sem erros críticos
- [ ] Sem 404/500 em produção
- [ ] Performance aceitável (<5s para carregar)
- [ ] Mobile responsivo

---

## 🆘 TROUBLESHOOTING

### Render retorna 502
**Causas possíveis:**
- Build ainda em andamento
- Erro no build Python
- Variáveis de ambiente faltando
- Porta incorreta

**Solução:**
1. Verificar logs no dashboard
2. Confirmar variáveis de ambiente
3. Verificar Start Command: `python3 -m uvicorn python_backend.main:app --host 0.0.0.0 --port $PORT`

### Vercel não conecta ao Render
**Causas possíveis:**
- `PY_EXTERNAL` não configurado
- Render offline
- CORS bloqueando

**Solução:**
1. Adicionar `PY_EXTERNAL` nas env vars
2. Redeploy Vercel
3. Testar Render diretamente primeiro

### Especialistas não aparecem
**Causas possíveis:**
- Banco não populado
- Erro na query SQL
- Tabela `experts` não existe

**Solução:**
1. Popular via: `curl -X POST .../api/admin/seed-experts`
2. Verificar logs de erro
3. Confirmar DATABASE_URL correto

### Chat não funciona
**Causas possíveis:**
- Tabelas `conversations`/`messages` não criadas
- Código antigo sem as correções
- ANTHROPIC_API_KEY inválida

**Solução:**
1. Verificar se código está atualizado (commit `71de901`)
2. Redeploy Render
3. Testar API key localmente

---

## 📊 MONITORAMENTO PÓS-DEPLOY

### Primeira Hora
- [ ] Verificar logs Render a cada 15 min
- [ ] Testar chat 3x
- [ ] Testar conselho 2x
- [ ] Verificar erros no Vercel dashboard

### Primeiro Dia
- [ ] Verificar uptime Render
- [ ] Monitorar uso de recursos
- [ ] Testar em mobile
- [ ] Verificar performance

### Primeira Semana
- [ ] Coletar feedback de usuários
- [ ] Monitorar erros recorrentes
- [ ] Otimizar queries lentas
- [ ] Melhorar tempos de resposta

---

## 🎉 DEPLOY COMPLETO

Quando todos os itens estiverem checados:

1. [ ] Documentar data e hora do deploy
2. [ ] Notificar stakeholders
3. [ ] Criar backup do banco
4. [ ] Ativar monitoramento contínuo
5. [ ] Celebrar! 🎊

---

**Data de Criação:** 4 Nov 2025  
**Última Atualização:** Aguardando Render completar build  
**Status:** 40% Completo

