# 🔧 CONFIGURAÇÃO: API Perplexity para Modo Estratégico

**Data:** 3 de Novembro de 2025  
**Problema:** Modo Estratégico retorna dados genéricos  
**Causa:** PERPLEXITY_API_KEY não configurada  
**Status:** ⚠️ AÇÃO NECESSÁRIA

---

## 🐛 PROBLEMA

O modo **estratégico** de criação de personas está funcionando, mas retorna dados **genéricos de fallback** porque a API Perplexity não está configurada.

**Sintomas:**
- Personas criadas no modo estratégico são muito genéricas
- Sem fontes reais de pesquisa
- `confidence_level: "low"` nos resultados
- Log mostra: `PERPLEXITY_API_KEY environment variable not set`

---

## ✅ SOLUÇÃO

### Passo 1: Obter Chave da API Perplexity

1. Acesse: https://www.perplexity.ai/settings/api
2. Crie uma conta (se não tiver)
3. Gere uma API Key
4. Copie a chave (formato: `pplx-xxxxxxxxxxxxxxxxxxxxxxxx`)

### Passo 2: Adicionar ao Arquivo `.env`

Abra o arquivo `.env` na raiz do projeto e adicione:

```bash
# Perplexity API Key (obrigatória para pesquisa de personas estratégicas)
PERPLEXITY_API_KEY=pplx-sua-chave-aqui
```

**Exemplo completo do `.env`:**
```bash
DATABASE_URL=postgresql://...

# Anthropic Claude API Key
ANTHROPIC_API_KEY=sk-ant-api03-...

# Perplexity API Key (obrigatória para pesquisa de personas estratégicas)
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Passo 3: Reiniciar o Backend

Depois de adicionar a chave:

```bash
# Parar backend Python
lsof -ti:5501 | xargs kill -9

# Reiniciar (vai recarregar automaticamente)
# Aguarde 5 segundos para o backend iniciar
```

Ou simplesmente reinicie o sistema completo:

```bash
./start.sh
```

---

## 🧪 TESTAR

Após configurar a chave, teste criando uma persona no modo estratégico:

### Teste no Terminal:
```bash
curl -X POST http://localhost:5501/api/personas \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "strategic",
    "targetDescription": "CMO de empresa SaaS B2B com equipe de 5-10 pessoas",
    "industry": "SaaS",
    "additionalContext": "Empresa com ARR de $2M, ciclo de vendas de 60 dias"
  }' | jq '.confidence_level, .sources[0]'
```

**✅ Resultado esperado:**
```json
"confidence_level": "high"  // ← deve ser "high" ao invés de "low"
"sources": ["reddit.com/r/...", "..."]  // ← deve ter fontes reais
```

### Teste no Navegador:
1. Acesse: http://localhost:5500/personas
2. Selecione modo: **Estratégica**
3. Preencha:
   - Público-Alvo: "CMO de empresa SaaS B2B com equipe de 5-10 pessoas"
   - Indústria: "SaaS"
   - Contexto Adicional: "Empresa com ARR de $2M"
4. Clique: "Criar Persona"
5. ✅ Aguarde 20-40 segundos
6. ✅ Persona deve ter dados **específicos** e **fontes reais**

---

## 📊 DIFERENÇA: Com vs Sem Perplexity

| Aspecto | Sem Perplexity (Fallback) | Com Perplexity (Real) |
|---------|---------------------------|----------------------|
| **Qualidade** | ⚠️ Genérica | ✅ Ultra-específica |
| **Fontes** | ❌ Nenhuma | ✅ Reddit, fóruns, sites |
| **Confidence** | `"low"` | `"high"` |
| **Jobs/Pain Points** | Genéricos | Específicos do público |
| **Tempo** | ~2s (instantâneo) | ~20-40s (pesquisa real) |

---

## 🔍 VERIFICAR SE CONFIGURAÇÃO ESTÁ OK

### Verificar se a chave está no .env:
```bash
grep "PERPLEXITY_API_KEY" .env
```

**✅ Deve mostrar:**
```
PERPLEXITY_API_KEY=pplx-xxxxxxxxxxxxxxxxxxxxxxxx
```

### Verificar se o backend está carregando:
```bash
# Criar persona de teste e ver logs
tail -f dev.local.log | grep -i perplexity
```

**✅ Deve mostrar:**
```
[RedditResearch] Calling Perplexity API with sonar-reasoning...
[RedditResearch] Perplexity API call successful
```

**❌ Se mostrar:**
```
[RedditResearch] Error in quick research: PERPLEXITY_API_KEY environment variable not set
[RedditResearch] Gerando dados de fallback
```

→ Significa que a chave não está configurada ou o backend não foi reiniciado.

---

## 💰 CUSTO DA API PERPLEXITY

| Plano | Custo | Requisições/Mês | Ideal Para |
|-------|-------|-----------------|------------|
| **Free** | $0 | ~5 requisições | Desenvolvimento/teste |
| **Starter** | $20/mês | ~1000 requisições | Produção pequena |
| **Pro** | $200/mês | ~20000 requisições | Produção escala |

**Cada persona estratégica = 1-2 requisições**

💡 Dica: Use **modo Quick** para testes/desenvolvimento (não usa Perplexity) e **modo Strategic** só quando precisar de qualidade máxima.

---

## 🎯 MODOS EXPLICADOS

### Modo Quick (Rápido)
- ⚡ Resposta instantânea (~2 segundos)
- 🤖 Usa apenas Claude (sem pesquisa externa)
- 💰 Custo: Apenas Claude (~$0.02)
- ✅ Ideal para: Testes, iteração rápida
- ⚠️ Qualidade: Boa, mas genérica

### Modo Strategic (Estratégico)
- 🔍 Pesquisa profunda (~20-40 segundos)
- 🌐 Usa Perplexity + Claude
- 💰 Custo: Perplexity + Claude (~$0.20)
- ✅ Ideal para: Produção, personas finais
- 🎯 Qualidade: Excelente, ultra-específica

---

## 🚨 TROUBLESHOOTING

### Problema: "PERPLEXITY_API_KEY environment variable not set"
**Solução:**
1. Verificar se a chave está no `.env`
2. Reiniciar o backend Python
3. Aguardar 5 segundos para o backend iniciar completamente

### Problema: Personas ainda genéricas mesmo com chave configurada
**Solução:**
1. Verificar logs: `tail -f dev.local.log | grep Perplexity`
2. Se mostrar erro 401/403: Chave inválida ou sem créditos
3. Se mostrar erro 429: Rate limit atingido
4. Se mostrar erro 5xx: Perplexity API temporariamente indisponível

### Problema: "Error code: 401 - Authentication failed"
**Solução:**
- Chave inválida ou expirada
- Gerar nova chave em https://www.perplexity.ai/settings/api
- Substituir no `.env` e reiniciar

### Problema: "Error code: 429 - Rate limit exceeded"
**Solução:**
- Aguardar alguns minutos
- Ou atualizar plano Perplexity
- Ou usar modo Quick temporariamente

---

## 📝 CHECKLIST DE CONFIGURAÇÃO

- [ ] Criar conta no Perplexity.ai
- [ ] Gerar API Key
- [ ] Adicionar PERPLEXITY_API_KEY ao `.env`
- [ ] Reiniciar backend Python (matar porta 5501)
- [ ] Aguardar 5 segundos
- [ ] Testar criação de persona no modo estratégico
- [ ] Verificar `confidence_level: "high"` no resultado
- [ ] Verificar fontes reais no campo `sources`

---

## 🎉 APÓS CONFIGURAÇÃO

Quando configurado corretamente, o modo estratégico vai:

✅ Pesquisar em Reddit, fóruns e sites reais  
✅ Extrair dores e jobs específicos do público  
✅ Identificar comunidades e influenciadores  
✅ Gerar personas com dados quantificados  
✅ Retornar `confidence_level: "high"`  
✅ Incluir fontes reais no campo `sources`

**Resultado:** Personas 10x mais específicas e acionáveis! 🎯

---

## 🔗 LINKS ÚTEIS

- **Perplexity API:** https://www.perplexity.ai/settings/api
- **Documentação:** https://docs.perplexity.ai/
- **Pricing:** https://www.perplexity.ai/pricing
- **Status:** https://status.perplexity.ai/

---

**AÇÃO NECESSÁRIA:** Adicione a chave do Perplexity ao `.env` para ativar o modo estratégico completo! 🚀

