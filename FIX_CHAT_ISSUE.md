# 🔧 Como Corrigir o Erro do Chat

## ❌ Problema Atual:
Quando você envia uma mensagem no chat, aparece:
```
"Não foi possível processar sua mensagem. Tente novamente"
```

## 🎯 Causa Raiz:
O backend Python não está carregando as variáveis de ambiente do arquivo `.env`

## ✅ SOLUÇÃO IMEDIATA:

### Passo 1: Pare o servidor
No terminal onde está rodando, pressione: `Ctrl + C`

Ou force kill:
```bash
lsof -ti:5000 | xargs kill -9
lsof -ti:5001 | xargs kill -9
```

### Passo 2: Exporte as variáveis manualmente
No terminal, execute:

```bash
cd /Users/gabriellima/Downloads/AdvisorIAElite
export ANTHROPIC_API_KEY="<SUA_CHAVE_ANTHROPIC>"
export PERPLEXITY_API_KEY="<SUA_CHAVE_PERPLEXITY>"
export DATABASE_URL="$(grep DATABASE_URL .env | cut -d'=' -f2-)"
```

**⚠️ IMPORTANTE**: Preencha com os valores reais do seu `.env`.

### Passo 3: Inicie o servidor novamente
```bash
npm run dev
```

### Passo 4: Teste o chat
Acesse http://localhost:5000 e tente enviar uma mensagem!

---

## 🔄 SOLUÇÃO PERMANENTE (Alternativa):

Eu já atualizei o código para carregar o `.env` automaticamente, mas pode não estar funcionando por causa do `uvicorn` estar iniciando no diretório `python_backend`.

### Opção A: Criar .env no python_backend também

```bash
cp .env python_backend/.env
```

Depois reinicie:
```bash
./start.sh
```

### Opção B: Modificar o start.sh para exportar variáveis

Edite o arquivo `start.sh` e adicione antes de `npm run dev`:

```bash
# Carregar variáveis do .env
set -a
source .env
set +a
```

---

## 🧪 Como Testar se Funcionou:

Depois de aplicar a solução, teste no terminal:

```bash
# 1. Pegar ID de um expert
EXPERT_ID=$(curl -s http://localhost:5001/api/experts | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

# 2. Criar conversa
CONV=$(curl -s -X POST http://localhost:5001/api/conversations \
  -H "Content-Type: application/json" \
  -d "{\"expertId\": \"$EXPERT_ID\", \"title\": \"Teste\"}")
CONV_ID=$(echo $CONV | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

# 3. Enviar mensagem
curl -X POST "http://localhost:5001/api/conversations/$CONV_ID/messages" \
  -H "Content-Type: application/json" \
  -d '{"content": "Olá!"}'
```

Se aparecer `"userMessage"` e `"assistantMessage"` na resposta = **✅ FUNCIONOU!**

Se aparecer `"Could not resolve authentication"` = ❌ API Key ainda não está sendo lida

---

## 💡 Por que isso acontece?

O Node.js lê o `.env` automaticamente via `dotenv`, mas o Python precisa ser configurado explicitamente para carregar o `.env`.

O backend Python está sendo iniciado pelo Node via `spawn()` no diretório `python_backend`, então ele não "vê" o `.env` da raiz automaticamente.

---

## 🆘 Se nada funcionar:

Execute o backend Python manualmente com as variáveis:

```bash
# Terminal 1 - Backend Python
cd python_backend
export ANTHROPIC_API_KEY="<SUA_CHAVE_ANTHROPIC>"
export PERPLEXITY_API_KEY="<SUA_CHAVE_PERPLEXITY>"
export DATABASE_URL="<SUA_DATABASE_URL>"
python3 -m uvicorn main:app --host 127.0.0.1 --port 5001 --reload
```

```bash
# Terminal 2 - Frontend Node
npm run dev
```

Desta forma você roda os dois separadamente e garante que as variáveis estão carregadas!

---

**Me avise qual solução funcionou e eu atualizo o código para que seja automático! 🚀**

