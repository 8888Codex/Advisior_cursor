# 🛡️ Sistema de Validação Automática

## Como Usar

### Validação Rápida (1 comando)

```bash
python3 validate_imports.py
```

Se tudo estiver OK, você verá:
```
✅ TODOS OS TESTES PASSARAM! (13/13)
✨ Sistema está pronto para uso!
```

### Configurar Pre-commit Hooks (Recomendado)

```bash
# 1. Instalar pre-commit
pip install pre-commit

# 2. Ativar hooks
pre-commit install

# Pronto! Agora a validação roda automaticamente antes de cada commit
```

## O Que é Validado

✅ **Importações Python** - Verifica se todos os módulos podem ser importados  
✅ **FastAPI App** - Garante que o servidor pode iniciar  
✅ **Storage** - Testa conexão com banco de dados/memória  
✅ **Seed** - Verifica se os 18 especialistas são criados  
✅ **Modelos Pydantic** - Confirma que todos os modelos existem  
✅ **Prompts** - Valida que os prompts das lendas estão disponíveis  

## Quando Executar

Execute **SEMPRE** antes de:
- ✅ Fazer commit
- ✅ Fazer push para repositório
- ✅ Fazer deploy para produção
- ✅ Fazer merge de branches

## Integração com Git

Adicione ao seu workflow:

```bash
# Antes de commit
python3 validate_imports.py && git commit -m "sua mensagem"

# Ou use pre-commit hooks (recomendado)
git commit -m "sua mensagem"  # Validação automática!
```

## Troubleshooting

### ❌ Se falhar com ImportError

```bash
ImportError: cannot import name 'XYZ' from 'python_backend.models'
```

**Solução:**
1. Verifique se a classe `XYZ` existe em `python_backend/models.py`
2. Se não existir, remova a importação ou crie a classe
3. Se foi renomeada, atualize o nome em todos os arquivos

### ❌ Se falhar no Seed

```bash
Seed: AVISO - Apenas X especialistas (esperado 18+)
```

**Solução:**
1. Verifique `python_backend/prompts/legends.py`
2. Garanta que `LEGENDS_PROMPTS` tem 18 entradas
3. Verifique `python_backend/seed.py`

### ❌ Se o servidor não iniciar

```bash
FastAPI App: FALHA
```

**Solução:**
1. Leia o erro completo
2. Geralmente é um erro de importação
3. Corrija as importações e re-execute

## Scripts Úteis

```bash
# Validação completa
python3 validate_imports.py

# Testar apenas importações
python3 -c "from python_backend.main import app; print('OK')"

# Testar seed
python3 -c "import asyncio; from python_backend.storage import storage; from python_backend.seed import seed_legends; asyncio.run(seed_legends(storage))"

# Testar servidor
python3 -m uvicorn python_backend.main:app --host 127.0.0.1 --port 8000
```

## Arquivos Criados

- `validate_imports.py` - Script principal de validação
- `.pre-commit-config.yaml` - Configuração de hooks
- `GUIA_MANUTENCAO.md` - Documentação completa
- `VALIDACAO_SISTEMA.md` - Este arquivo (guia rápido)

## Benefícios

✅ **Previne** erros de produção  
✅ **Detecta** problemas antes do commit  
✅ **Economiza** horas de debugging  
✅ **Garante** qualidade do código  
✅ **Automatiza** verificações manuais  

---

**Lembre-se:** 1 minuto de validação = Horas de tranquilidade! 🛡️

