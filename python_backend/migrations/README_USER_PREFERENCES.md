# User Preferences - PostgreSQL Integration

Este documento descreve como usar o sistema de persistência de preferências do usuário com PostgreSQL.

## Arquitetura

O sistema de preferências funciona de forma híbrida:

- **MemStorage (desenvolvimento)**: Armazena preferências em memória durante a execução
- **PostgresStorage (produção)**: Armazena preferências no PostgreSQL de forma persistente

## Configuração

### 1. Variável de Ambiente

Configure a variável `DATABASE_URL` para usar PostgreSQL:

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

Se `DATABASE_URL` não estiver configurada, o sistema usa `MemStorage` automaticamente.

### 2. Schema da Tabela

A tabela `user_preferences` é criada automaticamente quando você conecta ao PostgreSQL pela primeira vez.

Se preferir criar manualmente, execute o script SQL:

```bash
psql -U user -d dbname -f python_backend/migrations/001_create_user_preferences.sql
```

## Estrutura da Tabela

```sql
CREATE TABLE user_preferences (
    user_id VARCHAR(255) PRIMARY KEY,
    style_preference VARCHAR(20) CHECK (style_preference IN ('objetivo', 'detalhado')),
    focus_preference VARCHAR(20) CHECK (focus_preference IN ('ROI-first', 'brand-first')),
    tone_preference VARCHAR(20) CHECK (tone_preference IN ('prático', 'estratégico')),
    communication_preference VARCHAR(20) CHECK (communication_preference IN ('bullets', 'blocos')),
    conversation_style VARCHAR(20) CHECK (conversation_style IN ('coach', 'consultor', 'direto')),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### GET `/api/user/preferences`
Retorna as preferências do usuário autenticado.

**Requires**: Bearer token

**Response**:
```json
{
  "style_preference": "objetivo",
  "focus_preference": "ROI-first",
  "tone_preference": "prático",
  "communication_preference": "bullets",
  "conversation_style": "direto",
  "updated_at": "2024-01-01T12:00:00"
}
```

### PUT `/api/user/preferences`
Atualiza as preferências do usuário.

**Requires**: Bearer token

**Body**:
```json
{
  "style_preference": "detalhado",
  "tone_preference": "estratégico"
}
```

### DELETE `/api/user/preferences`
Remove todas as preferências do usuário.

**Requires**: Bearer token

## Uso no Código

### Backend (Python)

```python
from python_backend.storage import storage

# Obter preferências
preferences = await storage.get_user_preferences(user_id)

# Salvar preferências
from python_backend.models import UserPreferencesUpdate
update = UserPreferencesUpdate(
    tone_preference="prático",
    conversation_style="direto"
)
preferences = await storage.save_user_preferences(user_id, update)

# Deletar preferências
deleted = await storage.delete_user_preferences(user_id)
```

### Frontend (React/TypeScript)

```typescript
import { useUserPreferences } from "@/hooks/useUserPreferences";

function MyComponent() {
  const { preferences, savePreferences, isLoading } = useUserPreferences(
    userId,        // opcional
    isAuthenticated // true se autenticado
  );
  
  // As preferências são sincronizadas automaticamente com o backend
  // quando isAuthenticated = true
}
```

## Migração de Dados

Se você já tem preferências em `MemStorage` e quer migrar para PostgreSQL:

1. Exporte as preferências do MemStorage
2. Execute um script de migração que insere no PostgreSQL
3. Configure `DATABASE_URL` para usar PostgreSQL

## Troubleshooting

### Tabela não criada automaticamente

Se a tabela não for criada automaticamente, verifique:

1. Permissões do usuário PostgreSQL
2. Logs do servidor para erros
3. Execute manualmente: `python_backend/migrations/001_create_user_preferences.sql`

### Preferências não sincronizam

Verifique:

1. Se `isAuthenticated = true` no frontend
2. Se o token JWT está válido
3. Se o endpoint `/api/user/preferences` está acessível
4. Logs do servidor para erros

## Performance

- A tabela tem índice em `user_id` para consultas rápidas
- O trigger atualiza `updated_at` automaticamente
- As preferências são cacheadas no frontend (localStorage)

