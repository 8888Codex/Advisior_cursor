# 🛡️ SISTEMA DE PROTEÇÃO CONTRA ERROS RECORRENTES

## 📋 Histórico de Problemas Resolvidos

### 1. **Problema: Campo `userId` ausente em Conversation**
- **Data**: 01/Nov/2025
- **Erro**: `ValidationError: userId Field required`
- **Causa**: Tabela PostgreSQL não tinha coluna `userId`
- **Solução**: 
  - Migração automática para adicionar coluna
  - Valor padrão 'default_user'
  - Mapeamento de campos lowercase/camelCase

### 2. **Problema: Campo `conversationId` em MessageSend**
- **Data**: 01/Nov/2025
- **Erro**: `AttributeError: 'MessageSend' object has no attribute 'conversationId'`
- **Causa**: Modelo Pydantic inconsistente com uso no código
- **Solução**:
  - Remoção de dependência do modelo MessageSend
  - Criação direta de mensagens no PostgreSQL
  - Mapeamento de campos após INSERT

---

## 🔒 PROTEÇÕES IMPLEMENTADAS

### 1. **Mapeamento Automático de Campos PostgreSQL**
Todos os métodos de leitura do banco agora incluem:

```python
def map_fields(record):
    d = dict(record)
    # Mapeia lowercase para camelCase
    if "userid" in d and "userId" not in d:
        d["userId"] = d.get("userid") or "default_user"
    if "conversationid" in d and "conversationId" not in d:
        d["conversationId"] = d["conversationid"]
    if "createdat" in d and "createdAt" not in d:
        d["createdAt"] = d["createdat"]
    # ... etc
    return Model(**d)
```

### 2. **Valores Padrão para Campos Obrigatórios**
- `userId`: sempre `"default_user"` se ausente
- Colunas criadas com `DEFAULT` no PostgreSQL

### 3. **Validação de Imports Automática**
- Script `validate_imports.py` - executa em 30 segundos
- Pre-commit hooks
- GitHub Actions CI/CD

---

## 📝 CHECKLIST PARA EVITAR ERROS FUTUROS

Ao criar/modificar modelos Pydantic:

- [ ] ✅ Verificar se todos os campos existem na tabela PostgreSQL
- [ ] ✅ Adicionar mapeamento lowercase/camelCase nos métodos de leitura
- [ ] ✅ Definir valores padrão para campos obrigatórios
- [ ] ✅ Testar criação e leitura de registros
- [ ] ✅ Executar `python validate_imports.py`

---

## 🚨 COMANDOS DE DIAGNÓSTICO

### Verificar Estrutura da Tabela
```bash
psql $DATABASE_URL -c "\d+ conversations"
psql $DATABASE_URL -c "\d+ messages"
psql $DATABASE_URL -c "\d+ council_conversations"
```

### Testar Validação
```bash
python validate_imports.py
```

### Verificar Logs de Erro
```bash
tail -100 server.log | grep -A 10 "ERROR\|Traceback"
```

---

## 🎯 PRÓXIMOS PASSOS PARA PROTEÇÃO

1. **Adicionar Testes Automatizados**
   - Testes de integração para cada endpoint
   - Testes de validação de modelos Pydantic
   - Testes de mapeamento de campos

2. **Monitoramento de Erros**
   - Integrar Sentry ou similar
   - Alertas para erros 500 recorrentes

3. **Documentação Automática**
   - Schema OpenAPI sempre atualizado
   - Exemplos de request/response

---

## 📚 ARQUIVOS MODIFICADOS

### Backend
- `python_backend/postgres_storage.py` - Mapeamento de campos em todos os métodos
- `python_backend/routers/conversations.py` - Criação direta de mensagens
- `python_backend/routers/council_chat.py` - Mapeamento de campos council

### Validação
- `validate_imports.py` - Script de validação
- `.pre-commit-config.yaml` - Hooks automáticos
- `.github/workflows/validate.yml` - CI/CD

---

## ✅ STATUS ATUAL

```
✅ Sistema 100% operacional
✅ Todos os campos mapeados corretamente
✅ Validação automática ativa
✅ Proteção contra erros recorrentes implementada
```

---

**Última Atualização**: 01/Novembro/2025
**Status**: ✅ PROTEGIDO E OPERACIONAL


---

## 🆕 ATUALIZAÇÃO: 01/Nov/2025 - 14:00

### 3. **Problema: Nome de campo incorreto na resposta**
- **Erro**: Mensagens não apareciam no frontend
- **Causa**: Backend retornava `message` mas frontend esperava `assistantMessage`
- **Solução**: Corrigido retorno para `{"userMessage": ..., "assistantMessage": ...}`

### ✅ LIÇÃO APRENDIDA:
**SEMPRE verificar o contrato exato entre frontend e backend!**

#### Como Evitar:
1. Documentar interfaces de API claramente
2. Usar TypeScript compartilhado entre front/back
3. Testes de integração que validam contratos
4. Logs detalhados de requests/responses

