# 🛡️ Guia de Manutenção e Prevenção de Erros

Este guia documenta como evitar que problemas críticos (como erros de importação) quebrem o sistema.

## 🚨 Problema que Resolvemos

Em 1º de novembro de 2025, o sistema ficou inoperante por 2 horas devido a erros de importação em cadeia:
- `MessageCreate` não existia (deveria ser `MessageSend`)
- `BusinessProfile` não existia
- `AgentContribution` deveria ser `ExpertContribution`
- `CategoryInfo` estava faltando

Isso impediu o servidor de iniciar e os especialistas de aparecerem.

## ✅ Solução Implementada

### 1. Script de Validação Automática

Criamos `validate_imports.py` que verifica:
- ✅ Todas as importações funcionam
- ✅ O servidor FastAPI pode iniciar
- ✅ Os especialistas podem ser seedados
- ✅ Todos os modelos Pydantic existem
- ✅ Os prompts estão disponíveis

**Como usar:**

```bash
# Execute antes de qualquer commit
python3 validate_imports.py

# Se tudo passar, você verá:
✅ TODOS OS TESTES PASSARAM! (X/X)
✨ Sistema está pronto para uso!
```

### 2. Pre-commit Hooks (Opcional)

Instalamos hooks que validam automaticamente antes de cada commit:

```bash
# Instalar pre-commit
pip install pre-commit

# Ativar hooks
pre-commit install

# Agora, a cada commit, as validações rodam automaticamente!
```

### 3. GitHub Actions / CI (Recomendado)

Crie `.github/workflows/validate.yml`:

```yaml
name: Validar Sistema

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Validar importações
        run: python3 validate_imports.py
```

## 📋 Checklist Antes de Commits

Sempre que modificar código Python no backend:

- [ ] Execute `python3 validate_imports.py`
- [ ] Verifique se não há erros no console
- [ ] Teste localmente se o servidor inicia: `python3 -m uvicorn python_backend.main:app`
- [ ] Verifique se os especialistas aparecem: `curl http://localhost:8000/api/experts`

## 🔍 Erros Comuns a Evitar

### ❌ NÃO FAÇA:

```python
# Importar algo que não existe em models.py
from python_backend.models import MessageCreate  # ❌ Não existe!

# Usar tipo que não foi importado
async def save_profile(data: BusinessProfile):  # ❌ Não foi importado!
    pass
```

### ✅ FAÇA:

```python
# Sempre verifique se a classe existe em models.py
from python_backend.models import MessageSend  # ✅ Existe!

# Ou use tipos genéricos se não tiver o modelo específico
async def save_profile(data: dict):  # ✅ Funciona sempre!
    pass
```

## 🎯 Regras de Ouro

1. **NUNCA** faça commit sem rodar `validate_imports.py`
2. **SEMPRE** teste localmente antes de push
3. **SE** você criar um novo modelo em `models.py`, atualize todas as importações
4. **SE** você renomear algo, use Find & Replace em todo o projeto
5. **MANTENHA** os tipos consistentes entre storage, models e routers

## 🔧 Como Adicionar Novos Modelos

1. Defina o modelo em `python_backend/models.py`:
```python
class NovoModelo(BaseModel):
    id: str
    nome: str
```

2. Adicione ao script de validação em `validate_imports.py`:
```python
from python_backend.models import (
    # ... outros
    NovoModelo,  # Adicione aqui
)
```

3. Execute validação:
```bash
python3 validate_imports.py
```

## 📊 Monitoramento Contínuo

### Logs do Servidor

Sempre verifique os logs de startup:
```bash
tail -f server.log | grep -E "Error|Import|Started"
```

### Health Check

O endpoint `/api/health` deve sempre retornar 200:
```bash
curl http://localhost:8000/api/health
# Resposta esperada: {"status":"ok","service":"AdvisorIA API"}
```

## 🚀 Deploy Checklist

Antes de fazer deploy para produção:

1. ✅ `python3 validate_imports.py` passou
2. ✅ Todos os testes unitários passaram
3. ✅ Servidor inicia sem erros
4. ✅ `/api/experts` retorna 18+ especialistas
5. ✅ `/api/health` retorna status OK
6. ✅ Frontend conecta com sucesso ao backend

## 🆘 Se Algo Der Errado

1. **Pare tudo e leia os logs**:
   ```bash
   tail -100 server.log | grep -i error
   ```

2. **Execute o validador**:
   ```bash
   python3 validate_imports.py
   ```

3. **Se houver ImportError**, procure no erro qual classe está faltando:
   ```
   ImportError: cannot import name 'XYZ' from 'python_backend.models'
   ```

4. **Corrija**:
   - Se `XYZ` não existe, remova a importação ou crie a classe
   - Se `XYZ` foi renomeada, use o novo nome
   - Se `XYZ` está em outro arquivo, corrija o import path

5. **Re-valide**:
   ```bash
   python3 validate_imports.py
   ```

## 📚 Referências

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Python Import System](https://docs.python.org/3/reference/import.html)

## 🎓 Lições Aprendidas

### O que causou o problema:
1. Refactorings sem validação completa
2. Importações de classes que não existiam
3. Falta de testes de integração
4. Deploy sem verificar se o servidor inicia

### Como prevenir:
1. ✅ Validação automática antes de commits
2. ✅ Testes de importação
3. ✅ Health checks no CI/CD
4. ✅ Este documento! 📖

---

**Lembre-se**: Um minuto de validação previne horas de debugging! 🛡️

