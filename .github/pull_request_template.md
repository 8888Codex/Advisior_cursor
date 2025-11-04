# Pull Request - AdvisorIA Elite

## Descrição

<!-- Descreva o que essa PR faz em 2-3 frases -->

## Tipo de Mudança

- [ ] 🐛 Bug fix (correção de problema)
- [ ] ✨ Nova feature (funcionalidade nova)
- [ ] 🔧 Refatoração (mudança sem alterar comportamento)
- [ ] 📝 Documentação (apenas docs)
- [ ] 🎨 Style (formatação, sem mudança de lógica)
- [ ] ⚡ Performance (melhoria de performance)

---

## ✅ VALIDAÇÃO OBRIGATÓRIA

### Documentação Consultada

Marque TODAS as documentações que você consultou ANTES de fazer mudanças:

- [ ] **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitetura do sistema
- [ ] **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Referência da API
- [ ] **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Convenções de código
- [ ] **[docs/FEATURES.md](docs/FEATURES.md)** - Features existentes
- [ ] **[PROCESSO_VALIDACAO.md](PROCESSO_VALIDACAO.md)** - Processo obrigatório

**Se NÃO consultou:** PARE e leia antes de continuar! ⚠️

---

## 🔍 Checklist de Validação de Código

### Geral
- [ ] Li a documentação relevante (listada acima)
- [ ] Segui as convenções de código (docs/DEVELOPMENT.md)
- [ ] Adicionei error handling apropriado
- [ ] Adicionei logging estruturado (`[Module] Action: details`)
- [ ] Código testado em desenvolvimento

### Backend (Python)
- [ ] Imports corretos e válidos
- [ ] Modelos Pydantic atualizados (se necessário)
- [ ] Rate limiting configurado (endpoints POST/PUT/DELETE)
- [ ] Modelo Claude correto (`claude-sonnet-4-20250514`)
- [ ] Environment variables validadas antes de uso
- [ ] Docstrings adicionadas (funções públicas)

### Frontend (TypeScript/React)
- [ ] Type check passa (`npm run check`)
- [ ] Props com valores default (componentes React)
- [ ] Hooks seguem padrão existente
- [ ] Estados gerenciados corretamente
- [ ] Timeout apropriado em API calls (90-120s)
- [ ] Loading states implementados
- [ ] Error handling no UI

### Compatibilidade
- [ ] Frontend e backend schemas compatíveis
- [ ] Não quebra features existentes
- [ ] Endpoints mantêm backward compatibility
- [ ] Types TypeScript atualizados (se mudou schema Python)
- [ ] Migrations criadas (se mudou schema DB)

---

## 🧪 Testes Realizados

### Cenários Testados
- [ ] Cenário principal (happy path)
- [ ] Casos de erro (error handling)
- [ ] Edge cases (limites e extremos)
- [ ] Regressões (features existentes ainda funcionam)

### Como Testar Esta PR

<!-- Descreva passo-a-passo como testar suas mudanças -->

```
1. 
2. 
3. 
```

---

## 📝 Documentação Atualizada

### Documentos Atualizados (marque se aplicável)

- [ ] **docs/API_REFERENCE.md** - Novo endpoint ou mudança em schema
- [ ] **docs/FEATURES.md** - Nova feature ou mudança significativa
- [ ] **docs/ARCHITECTURE.md** - Mudança na arquitetura
- [ ] **docs/DEVELOPMENT.md** - Nova convenção ou processo
- [ ] **docs/CHANGELOG.md** - Adicionado em seção [Unreleased]
- [ ] **Nenhum** - Mudança pequena, docs não afetadas

---

## 🔧 Scripts de Validação

Rode ANTES de abrir esta PR:

```bash
# Validação completa
bash scripts/validate-changes.sh
```

### Resultados das Validações

- [ ] ✅ TypeScript type check passou
- [ ] ✅ Python imports validados
- [ ] ✅ Endpoint compatibility OK
- [ ] ✅ Naming conventions seguidas

**Se alguma validação FALHOU:** Corrija antes de marcar como ready!

---

## 📊 Impacto

### Arquivos Modificados

<!-- Lista de arquivos modificados (Git faz isso automaticamente) -->

### Breaking Changes?

- [ ] ❌ NÃO - Backward compatible
- [ ] ⚠️ SIM - Lista abaixo:

<!-- Se SIM, liste mudanças incompatíveis e como migrar -->

---

## 🔗 Referências

### Issues Relacionadas

<!-- Link para issues do GitHub (se houver) -->
Closes #

### Documentação Relacionada

<!-- Links para arquivos de docs que explicam a mudança -->
- [docs/FEATURES.md](docs/FEATURES.md) - Seção X
- [Correção anterior](../CORRECAO_*.md) - Se é fix

### Commits Relevantes

<!-- Se baseia em algum commit/PR anterior, referencie -->

---

## 📸 Screenshots (se aplicável)

<!-- Adicione screenshots de mudanças visuais -->

**Antes:**
<!-- Screenshot ou descrição -->

**Depois:**
<!-- Screenshot ou descrição -->

---

## ✅ Checklist Final do Revisor

### Para o Revisor da PR, verificar:

- [ ] Código segue convenções (docs/DEVELOPMENT.md)
- [ ] Documentação foi consultada (marcado acima)
- [ ] Testes foram realizados (descritos acima)
- [ ] Documentação atualizada (se necessário)
- [ ] Validações automáticas passaram
- [ ] Sem breaking changes não documentados
- [ ] Code review aprovado
- [ ] PR pronta para merge! 🚀

---

## 💬 Notas Adicionais

<!-- Qualquer informação adicional relevante -->

---

**Ao abrir esta PR, você confirma que:**
1. ✅ Consultou a documentação relevante
2. ✅ Seguiu o processo de validação
3. ✅ Testou suas mudanças completamente
4. ✅ Atualizou documentação (se necessário)

**Obrigado por manter a qualidade do código! 🙏**

