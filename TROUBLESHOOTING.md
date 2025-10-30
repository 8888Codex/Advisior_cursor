# 🔧 Guia de Solução de Problemas - AdvisorIA Elite

Este guia contém soluções para problemas comuns que podem ocorrer durante a execução do AdvisorIA Elite.

## 🚨 Erros Comuns

### 1. Erro "Connection failed. If the problem persists, please check your internet connection or VPN"

**Causa**: Este erro geralmente ocorre quando há um problema de comunicação com as APIs externas (Perplexity ou Claude) ou quando o servidor Python não está respondendo corretamente.

**Soluções**:

1. **Verificar chaves de API**:
   - Certifique-se de que as chaves `ANTHROPIC_API_KEY` e `PERPLEXITY_API_KEY` estão corretamente configuradas no arquivo `.env`
   - Verifique se as chaves são válidas e têm créditos suficientes

2. **Verificar versão do modelo**:
   - Os modelos da API podem mudar com o tempo. Se você estiver enfrentando erros como `"model: claude-3-sonnet-20240229"`, atualize para a versão mais recente (ex: `claude-3-sonnet-20240229-v1:0`)

3. **Reiniciar o servidor**:
   ```bash
   # Matar processos nas portas 5000 e 5001
   lsof -ti:5000,5001 | xargs kill -9
   
   # Reiniciar o servidor
   cd /caminho/para/AdvisorIAElite
   npm run dev
   ```

### 2. Erro 500 (Internal Server Error) ao criar personas

**Causa**: Este erro pode ocorrer devido a problemas na validação dos dados, falhas nas chamadas de API externas ou erros no processamento dos dados.

**Soluções**:

1. **Verificar logs do servidor**:
   ```bash
   tail -100 /tmp/uvicorn.log
   ```

2. **Verificar formato dos dados**:
   - Certifique-se de que o modelo de dados corresponde ao esperado pelo backend
   - Campos obrigatórios como `job_statement`, `functional_jobs`, `emotional_jobs`, `social_jobs` e `demographics.occupation` devem estar presentes

3. **Usar dados de fallback**:
   - O sistema foi configurado para usar dados de fallback quando as APIs externas falham
   - Se o erro persistir, verifique se há problemas de indentação ou sintaxe no código

### 3. Erro "listen ENOTSUP" no macOS

**Causa**: Este erro ocorre no macOS quando o servidor tenta usar a opção `reusePort` que não é suportada neste sistema operacional.

**Solução**:
   ```javascript
   // Modificar o servidor.listen em server/index.ts
   const host = process.platform === 'darwin' ? 'localhost' : '0.0.0.0';
   server.listen(port, host, () => {
     log(`serving on port ${port} (host: ${host})`);
   });
   ```

### 4. Erro "EADDRINUSE" (Endereço já em uso)

**Causa**: Este erro ocorre quando a porta que o servidor está tentando usar já está sendo usada por outro processo.

**Solução**:
   ```bash
   # Matar processos usando as portas 5000 e 5001
   lsof -ti:5000,5001 | xargs kill -9
   
   # Reiniciar o servidor
   npm run dev
   ```

### 5. Erro "invalid x-api-key" ou "credit balance too low"

**Causa**: Problemas com a chave da API Anthropic (Claude) ou saldo insuficiente.

**Soluções**:
1. **Verificar chave API**:
   - Certifique-se de que a chave `ANTHROPIC_API_KEY` está correta no arquivo `.env`
   - Verifique se a chave começa com `sk-ant-api03-`

2. **Verificar saldo**:
   - Acesse o console da Anthropic para verificar se você tem créditos suficientes
   - Adicione créditos se necessário

## 🔄 Script de Reinicialização

Para facilitar a reinicialização do servidor, você pode usar o script `start.sh`:

```bash
#!/bin/bash

echo "🧹 Limpando processos antigos nas portas 5000 e 5001..."
lsof -ti:5000 | xargs kill -9 > /dev/null 2>&1
lsof -ti:5001 | xargs kill -9 > /dev/null 2>&1
echo "✅ Processos antigos eliminados."

echo "🚀 Iniciando o servidor..."
NODE_ENV=development tsx server/index.ts > /tmp/advisoria_startup.log 2>&1 &
SERVER_PID=$!
echo "Servidor iniciado com PID: $SERVER_PID. Logs em /tmp/advisoria_startup.log"

echo "⏳ Aguardando 10 segundos para o servidor inicializar..."
sleep 10

echo "🔍 Verificando status do servidor..."
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ Servidor Node.js está respondendo!"
else
    echo "❌ Servidor Node.js NÃO está respondendo."
    echo "Verifique o log em /tmp/advisoria_startup.log para detalhes."
    exit 1
fi

echo "🌐 Projeto rodando em http://localhost:5000"
echo "🛑 Para parar o servidor, use: kill $SERVER_PID"
```

## 📋 Verificação de Ambiente

Se você estiver enfrentando problemas, verifique se o ambiente está configurado corretamente:

1. **Node.js e npm**:
   ```bash
   node --version  # Deve ser v16.x ou superior
   npm --version   # Deve ser v8.x ou superior
   ```

2. **Python**:
   ```bash
   python3 --version  # Deve ser v3.8 ou superior
   pip3 --version     # Deve estar instalado
   ```

3. **Variáveis de ambiente**:
   ```bash
   # Verifique se o arquivo .env existe e contém as chaves necessárias
   cat .env | grep -v '^#' | grep .
   ```

## 🆘 Suporte Adicional

Se você continuar enfrentando problemas após tentar as soluções acima, verifique:

1. Os logs completos em `/tmp/uvicorn.log` e `/tmp/advisoria_startup.log`
2. Possíveis erros no console do navegador (F12 > Console)
3. Problemas de rede ou firewall que possam estar bloqueando as chamadas de API

Para problemas persistentes, entre em contato com o suporte técnico fornecendo os logs e detalhes do ambiente.
