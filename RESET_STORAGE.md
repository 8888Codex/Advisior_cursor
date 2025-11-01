# Como Resetar o Storage e Forçar Novo Seed

Se os experts não aparecem, siga estes passos:

## 1. Pare todos os processos
```bash
# Pare o servidor Node (Ctrl+C)
# Matar processos nas portas
lsof -ti :3001 | xargs kill -9
lsof -ti :5201 | xargs kill -9
```

## 2. Reinicie o servidor
```bash
npm run dev
```

## 3. Verifique os logs do startup
Procure por:
- `[Startup] Seeding marketing legends...`
- `✅ Successfully created X new marketing legends.`
- `📊 Total de experts no storage: X`
- `[Experts Router] get_experts called. Found X experts.`

## 4. Teste o endpoint diretamente
```bash
# Teste o Python backend diretamente
curl http://localhost:5201/api/experts/debug

# Teste via proxy Node
curl http://localhost:3001/api/experts/debug
```

## 5. Se ainda não funcionar
O MemStorage pode estar persistindo entre hot-reloads. 
Solução: Pare completamente e reinicie o Python backend.

