# 🚀 Novas Portas de Acesso - AdvisorIA Elite

## ✅ Portas Configuradas

As portas foram atualizadas para evitar conflitos:

- **🌐 Aplicação Principal (Frontend + API):** `http://localhost:5500`
- **🐍 Backend Python (API):** `http://localhost:5501`

## 📝 Como Iniciar o Sistema

### Opção 1: Script Automático (Recomendado)
```bash
./start.sh
```

### Opção 2: NPM Diretamente
```bash
npm run dev
```

### Opção 3: Comando Manual
```bash
PORT=5500 PY_PORT=5501 NODE_ENV=development npm run dev
```

## 🔗 URLs de Acesso

Após iniciar o sistema, acesse:

### Frontend Principal
```
http://localhost:5500
```

### Páginas Específicas
- 🏠 Home: `http://localhost:5500/`
- 👥 Especialistas: `http://localhost:5500/experts`
- 🎯 Criar Clone: `http://localhost:5500/create`
- 💬 Conselho: `http://localhost:5500/test-council`
- 🎭 Personas: `http://localhost:5500/personas`

### Backend Python (API)
```
http://localhost:5501/docs
```

## 🛠️ Liberar Portas Manualmente

Se as portas ainda estiverem ocupadas, use:

```bash
# Liberar porta 5500
lsof -ti:5500 | xargs kill -9

# Liberar porta 5501
lsof -ti:5501 | xargs kill -9
```

## ⚙️ Variáveis de Ambiente

As seguintes variáveis estão configuradas:

```env
PORT=5500          # Porta do servidor Node.js
PY_PORT=5501       # Porta do backend Python
NODE_ENV=development
```

## 🐛 Solução de Problemas

### Erro: "Port already in use"
```bash
# Execute o script start.sh que já libera as portas automaticamente
./start.sh
```

### Erro: "Cannot connect to Python backend"
```bash
# Verifique se o Python 3 está instalado
python3 --version

# Instale as dependências Python
pip install -r requirements.txt
```

### Erro: "Module not found"
```bash
# Reinstale as dependências Node.js
npm install
```

## 📊 Status do Sistema

Para verificar se os servidores estão rodando:

```bash
# Verificar porta 5500 (Node.js)
lsof -i:5500

# Verificar porta 5501 (Python)
lsof -i:5501
```

## 🎉 Pronto!

Após iniciar com sucesso, você verá:

```
🚀 Iniciando AdvisorIA Elite...
✅ Portas livres!
🎯 Iniciando servidor...
📍 Acesse: http://localhost:5500
```

**Acesse agora:** [http://localhost:5500](http://localhost:5500)

