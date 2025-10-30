# 🚀 Como Iniciar o Projeto - AdvisorIA Elite

## ✅ Status da Configuração

Seu projeto está **100% CONFIGURADO** e pronto para rodar! 🎉

### O que já foi feito:
- ✅ Dependências npm instaladas
- ✅ Dependências Python instaladas
- ✅ API Keys configuradas (.env)
- ✅ Banco de dados Neon conectado
- ✅ Tabelas criadas no banco
- ✅ Código TypeScript compilando
- ✅ Tudo pronto para rodar!

---

## 🚀 Iniciar o Projeto

### Comando Principal:
```bash
npm run dev
```

Isso irá:
1. ✅ Iniciar o servidor Node.js/Express na porta **5000**
2. ✅ Iniciar automaticamente o backend Python na porta **5001**
3. ✅ Abrir o projeto com hot-reload ativo

### Acesse no navegador:
```
http://localhost:5000
```

---

## 📋 Estrutura do Projeto Rodando

```
┌─────────────────────────────────────┐
│   Frontend (React + TypeScript)    │
│         http://localhost:5000       │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│    Backend Node.js (Express)        │
│         Port 5000 (API Proxy)       │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Backend Python (FastAPI + IA)      │
│         Port 5001 (Experts IA)      │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│    Database Neon (PostgreSQL)       │
│    Região: South America (AWS)      │
└─────────────────────────────────────┘
```

---

## 🎯 Funcionalidades Disponíveis

Após iniciar o projeto, você terá acesso a:

### 1. **Página Inicial (Landing)**
- Hero section com apresentação
- Galeria de experts
- Sistema de categorias

### 2. **Experts de Marketing**
- 18+ clones cognitivos de lendas do marketing
- Philip Kotler, Seth Godin, Gary Vaynerchuk, etc.
- Cada expert com personalidade única

### 3. **Chat com IA**
- Conversa natural com experts
- Respostas baseadas em Claude Sonnet 4
- Contexto de negócio personalizado

### 4. **Conselho de Experts**
- Análise colaborativa de múltiplos experts
- Pesquisa automática com Perplexity
- Síntese de recomendações

### 5. **Criação de Personas**
- Builder de personas usando Reddit
- Pesquisa rápida ou estratégica
- Insights de público-alvo

### 6. **Auto-Clone de Experts**
- Criar novos experts a partir de nomes
- Pesquisa automática via Perplexity
- System prompt gerado por IA

---

## 🛠️ Comandos Úteis

### Desenvolvimento:
```bash
# Iniciar projeto completo (Node + Python)
npm run dev

# Apenas frontend (sem backend)
npm run dev:client

# Verificar erros TypeScript
npm run check

# Build para produção
npm run build
```

### Backend Python (manual):
```bash
cd python_backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

### Banco de Dados:
```bash
# Aplicar migrations (criar/atualizar tabelas)
npm run db:push

# Ver status do banco
npm run db:studio
```

---

## 🔍 Verificar se Está Funcionando

### 1. Teste de API:
```bash
curl http://localhost:5001/api/experts
```

Deve retornar JSON com lista de experts.

### 2. Teste do Frontend:
Acesse: http://localhost:5000

Você deve ver a landing page com os experts.

### 3. Teste do Chat:
1. Clique em um expert
2. Digite uma pergunta
3. Aguarde a resposta da IA

---

## 📊 Monitorar Logs

### Terminal 1 - Servidor Principal:
Ao rodar `npm run dev`, você verá:
```
[Server] serving on port 5000
[Python Backend] Uvicorn running on http://0.0.0.0:5001
```

### Ver requisições:
```
GET /api/experts 200 in 45ms
POST /api/conversations 201 in 123ms
```

---

## 🐛 Problemas Comuns

### Erro: "Port 5000 already in use"
**Solução:** Mate o processo ou mude a porta no .env:
```bash
# Encontrar processo
lsof -ti:5000

# Matar processo
kill -9 $(lsof -ti:5000)

# Ou mudar porta no .env
PORT=5001
```

### Erro: "ANTHROPIC_API_KEY required"
**Solução:** Verifique se o .env tem a chave correta:
```bash
cat .env | grep ANTHROPIC_API_KEY
```

### Erro: "Database connection failed"
**Solução:** Verifique a DATABASE_URL:
```bash
cat .env | grep DATABASE_URL
```

### Backend Python não inicia:
**Solução:** Inicie manualmente:
```bash
cd python_backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 5001 --reload
```

---

## 🎨 Personalizações

### Adicionar Novo Expert:
Edite: `python_backend/prompts/legends.py`

### Modificar Frontend:
Arquivos em: `client/src/`

### Ajustar Comportamento da IA:
Edite system prompts em: `python_backend/prompts/legends.py`

---

## 📚 Documentação Adicional

- **SETUP.md** - Guia completo de instalação
- **DATABASE_OPTIONS.md** - Opções de banco de dados
- **SUPABASE_SETUP.md** - (Alternativa ao Neon)
- **design_guidelines.md** - Guidelines de design

---

## 🎉 Está Tudo Pronto!

Execute agora:

```bash
npm run dev
```

Acesse: **http://localhost:5000**

E comece a interagir com os experts de marketing! 🚀

---

## 💡 Dica Final

Use o **Dark Mode** no canto superior direito para uma experiência mais agradável! 🌙

---

## 🆘 Precisa de Ajuda?

Se algo não funcionar:
1. Verifique os logs no terminal
2. Consulte a seção "Problemas Comuns" acima
3. Verifique se todas as variáveis do .env estão configuradas

**Boa sorte com seu projeto!** 🎊

