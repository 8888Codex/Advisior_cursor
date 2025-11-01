# Debug do Chat - Guia de Diagnóstico

## Status Atual
- ✅ API key configurada
- ✅ Servidor rodando (porta 5201)
- ✅ Deep Clone desabilitado (fallback seguro)
- ✅ Código sintaticamente correto

## Como Diagnosticar o Problema

### 1. Verifique o Console do Navegador
1. Abra a aplicação no navegador
2. Pressione `F12` ou `Cmd+Option+I` (Mac)
3. Vá para a aba "Console"
4. Tente enviar uma mensagem no chat
5. Anote qualquer erro que aparecer

### 2. Verifique os Logs do Servidor Python
No terminal onde o servidor Python está rodando, você verá erros em tempo real.
Procure por mensagens que começam com:
- `[ERROR]`
- `[Deep Clone]`
- `Traceback`

### 3. Teste Direto a API
```bash
# 1. Pegar ID de um expert
curl http://127.0.0.1:5201/api/experts | jq '.[0].id'

# 2. Criar uma conversa (substitua EXPERT_ID)
curl -X POST http://127.0.0.1:5201/api/conversations \
  -H "Content-Type: application/json" \
  -d '{"expertId": "EXPERT_ID", "title": "Teste"}'

# 3. Enviar mensagem (substitua CONVERSATION_ID)
curl -X POST http://127.0.0.1:5201/api/conversations/CONVERSATION_ID/messages \
  -H "Content-Type: application/json" \
  -d '{"content": "Olá"}'
```

### 4. Possíveis Problemas e Soluções

#### Problema: "ANTHROPIC_API_KEY não configurada"
**Solução**: A chave está no .env, mas o servidor precisa ser reiniciado:
```bash
# Pare o servidor (Ctrl+C)
# Reinicie:
python3 -m uvicorn python_backend.main:app --host 127.0.0.1 --port 5201 --reload
```

#### Problema: Timeout ou erro 504
**Solução**: A requisição está demorando muito. Pode ser:
- API da Anthropic lenta
- Problema de rede
- Prompt muito longo

#### Problema: Erro 500 genérico
**Solução**: Verifique os logs do servidor para ver o traceback completo

### 5. Desabilitar Deep Clone Completamente (já feito)
O Deep Clone já está desabilitado por padrão. Se ainda houver problemas, pode ser outra coisa.

## Próximos Passos
1. **Me envie o erro específico** que aparece no console do navegador
2. **Me envie os logs do servidor** quando você tenta enviar mensagem
3. **Teste com curl** usando os comandos acima e me mostre o resultado

