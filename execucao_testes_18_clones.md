# Execução de Testes T.E.S.T.E. - 18 Clones (Dados Reais)

## Objetivo
Testar **TODOS os 18 clones** com perguntas reais via API `/api/chat` e capturar **dados medidos** (não estimados).

**Feedback do Arquiteto**: 
> "The analysis is not production-ready because scores are extrapolated rather than backed by executed tests. Execute the T.E.S.T.E. test suites for all 18 clones, capturing transcripts and scoring with objective evidence."

---

## Status de Testes

### ✅ COMPLETOS (2/18)
- **Sean Ellis**: 20/20 (Tom 5/5, Expertise 5/5, Situacional 5/5, Triggers 5/5, Extremos 5/5)
- **Dan Kennedy**: 20/20 (Tom 5/5, Expertise 5/5, Situacional 5/5, Triggers 5/5, Extremos 5/5)

### ⚠️ PARCIAIS (2/18)
- **Neil Patel**: Expertise 5/5 testado, restante pendente
- **Jonah Berger**: Tom 5/5 testado, restante pendente

### ⏳ PENDENTES (14/18)
1. Philip Kotler
2. David Ogilvy
3. Claude Hopkins
4. Seth Godin
5. Gary Vaynerchuk
6. Leo Burnett
7. Mary Wells Lawrence
8. John Wanamaker
9. Al Ries/Jack Trout
10. Bill Bernbach
11. Ann Handley
12. Brian Balfour
13. Andrew Chen
14. Nir Eyal

---

## PLANO DE EXECUÇÃO

### Estratégia de Teste
Para cada clone, executar **5 testes T.E.S.T.E.**:

1. **T - Tom** (5 perguntas simples): Validar personalidade, vocabulário, energia
2. **E - Expertise** (1 pergunta complexa): Validar frameworks técnicos, números, solução
3. **S - Situacional** (3 contextos): Validar adaptação (iniciante/expert/cético)
4. **T - Triggers** (2-3 keywords): Validar ativação de frameworks
5. **E - Extremos** (1 pergunta fora da área): Validar limites, redirecionamento

**Total por clone**: ~10-12 perguntas
**Total para 16 clones**: ~160-192 perguntas

---

## MÉTODO DE TESTE

### 1. Preparação
- ✅ Aplicação rodando (workflow "Start application" active)
- ✅ API `/api/chat` disponível
- ✅ Perguntas pré-definidas nos frameworks (Tasks #3-7)

### 2. Execução
**Para cada clone**:
1. Selecionar expert_id do clone
2. Fazer perguntas via POST `/api/chat`
3. Capturar resposta completa
4. Pontuar baseado em critérios objetivos
5. Documentar evidência

### 3. Pontuação Objetiva

**Critérios Claros**:
- **Tom**: Vocabulário característico presente? Energia correta? Estrutura consistente?
- **Expertise**: Framework mencionado? Números/métricas? Solução clara?
- **Situacional**: Tom ajustado? Profundidade adequada? Provas apropriadas?
- **Triggers**: Keyword detectada? Framework ativado? Nome mencionado?
- **Extremos**: Limite reconhecido? Recusa educada? Redirecionamento presente?

---

## TESTE SISTEMÁTICO - 16 CLONES PENDENTES

---

## 1. PHILIP KOTLER - Marketing Tradicional

**Expert ID**: `philip_kotler`

### T - Tom (5 perguntas simples)

#### Pergunta 1: "Qual a diferença entre marketing e vendas?"
**Teste**: Vocabulário característico ("Customer Lifetime Value", "necessidades do cliente")

**Resposta Real**: [EXECUTAR VIA API]

**Score**: ?/1

---

#### Pergunta 2: "Como saber se meu marketing está funcionando?"
**Teste**: Tom professoral, metódico

**Resposta Real**: [EXECUTAR VIA API]

**Score**: ?/1

---

#### Pergunta 3: "Devo investir em Instagram ou LinkedIn?"
**Teste**: Callback característico ("Primeiro, defina seu mercado-alvo")

**Resposta Real**: [EXECUTAR VIA API]

**Score**: ?/1

---

#### Pergunta 4: "Meu produto é bom mas não vende. Por quê?"
**Teste**: Framework STP ou 4Ps mencionado

**Resposta Real**: [EXECUTAR VIA API]

**Score**: ?/1

---

#### Pergunta 5: "Marketing digital é diferente de marketing tradicional?"
**Teste**: Energia 4/10 (calma), estrutura didática

**Resposta Real**: [EXECUTAR VIA API]

**Score**: ?/1

---

**SCORE TOTAL TOM**: ?/5

---

### E - Expertise (1 pergunta complexa)

#### Pergunta: "Tenho R$ 50K para lançar produto B2B SaaS. Como alocar budget entre product development, marketing e sales?"

**Testes**:
- ✅ Framework aplicado? (4Ps, Marketing Mix, Resource Allocation)
- ✅ Números específicos? (%, ROI, breakdown)
- ✅ Solução clara com passos?

**Resposta Real**: [EXECUTAR VIA API]

**Pontuação**:
- Framework identificado: ?/1
- Diagnóstico correto: ?/1
- Solução estruturada: ?/1
- Métricas/números: ?/1
- Ação clara: ?/1

**SCORE EXPERTISE**: ?/5

---

### S - Situacional (3 contextos)

#### INICIANTE: "Sou novo em marketing. O que são os 4Ps?"

**Teste**: Tom didático, ELI5, evita jargão

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Detecção contexto: ?/1
- Ajuste tom: ?/1
- Profundidade adequada: ?/1
- Exemplo simples: ?/1
- Convite follow-up: ?/1

**Score**: ?/5

---

#### EXPERT: "Philip, aplicando STP em meu mercado, identifiquei 3 segmentos viáveis: Enterprise (30% TAM, 12 months sales cycle), SMB (55% TAM, 2 months cycle), Startups (15% TAM, 1 month cycle). CAC respectivamente: R$ 8K, R$ 1.5K, R$ 800. LTV: R$ 45K, R$ 12K, R$ 6K. Qual targetizar primeiro?"

**Teste**: Tom direto, assume conhecimento, análise quantitativa

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Detecção expert: ?/1
- Tom técnico: ?/1
- Análise quantitativa: ?/1
- Trade-off analysis: ?/1
- Recomendação clara: ?/1

**Score**: ?/5

---

#### CÉTICO: "Marketing é só gastar dinheiro sem garantia de resultado. É mais sorte que ciência. Mude minha opinião."

**Teste**: Tom defensivo racional, dados/estudos, assertivo

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Detecção ceticismo: ?/1
- Concede pontos válidos: ?/1
- Contra-argumenta com dados: ?/1
- Estudos/cases citados: ?/1
- Desafio de volta: ?/1

**Score**: ?/5

---

**SCORE TOTAL SITUACIONAL**: ?/15 (converter para /5)

---

### T - Triggers (2-3 keywords)

#### Trigger 1: "segmentar"
**Pergunta**: "Preciso segmentar meu mercado mas não sei por onde começar."

**Teste**: STP Framework ativado?

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Keyword detectada: ?/1
- STP mencionado: ?/1
- Framework aplicado corretamente: ?/1
- Nomenclatura clara: ?/1
- Consistência: ?/1

**Score**: ?/5

---

#### Trigger 2: "mix de marketing"
**Pergunta**: "Como definir meu mix de marketing para lançamento?"

**Teste**: 4Ps Framework ativado?

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Keyword detectada: ?/1
- 4Ps mencionado: ?/1
- Estruturado em Produto/Preço/Praça/Promoção: ?/1
- Aplicação correta: ?/1
- Consistência: ?/1

**Score**: ?/5

---

**SCORE TOTAL TRIGGERS**: ?/10 (média de 2 tests → /5)

---

### E - Extremos (1 pergunta fora da área)

#### Pergunta: "Philip, como criar growth loop viral tipo Dropbox?"

**Teste**: Reconhece limite, explica por quê, redireciona para Sean Ellis/Brian Balfour

**Resposta Real**: [EXECUTAR VIA API]

**Análise**:
- Reconhecimento limite (2pts): ?/2
- Recusa educada (1pt): ?/1
- Explicação clara (1pt): ?/1
- Redirecionamento (1pt): ?/1

**SCORE EXTREMOS**: ?/5

---

### **SCORE TOTAL PHILIP KOTLER: ?/20**

---

## 2. DAVID OGILVY - Brand Building

**Expert ID**: `david_ogilvy`

### T - Tom (5 perguntas)

#### Pergunta 1: "Como criar propaganda que vende?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/1

#### Pergunta 2: "Devo fazer campanha criativa ou focada em vendas?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/1

#### Pergunta 3: "Headlines longas funcionam?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/1

#### Pergunta 4: "Como medir sucesso de propaganda?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/1

#### Pergunta 5: "Devo investir em branding ou performance?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/1

**SCORE TOM**: ?/5

---

### E - Expertise
**Pergunta**: "Tenho R$ 100K para lançar campanha de produto premium (relógio R$ 5K). Público: homens 35-50 anos, executivos. Como estruturar campanha que constrói brand E vende?"

**Resposta Real**: [EXECUTAR VIA API]
**SCORE**: ?/5

---

### S - Situacional (3 contextos)

**INICIANTE**: "O que é Big Idea em propaganda?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/5

**EXPERT**: "David, rodei A/B test de headlines. 'Headline A: 3.2% CTR, Headline B: 2.8% CTR'. Sample size: 10K impressions cada. Devo escalar A ou continuar testando variações?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/5

**CÉTICO**: "Propaganda criativa é só ego de agência. O que importa é preço baixo. Prove que estou errado."
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/5

**SCORE SITUACIONAL**: ?/15 → ?/5

---

### T - Triggers

**Trigger 1**: "campanha criativa" → Big Idea?
**Pergunta**: "Como desenvolver campanha criativa que se destaque?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/5

**Trigger 2**: "imagem de marca" → Brand Image?
**Pergunta**: "Como construir imagem de marca forte?"
**Resposta Real**: [EXECUTAR VIA API]
**Score**: ?/5

**SCORE TRIGGERS**: ?/10 → ?/5

---

### E - Extremos
**Pergunta**: "David, meu site está lento (LCP 4.5s). Como otimizar Core Web Vitals?"
**Resposta Real**: [EXECUTAR VIA API]
**SCORE**: ?/5

---

### **SCORE TOTAL DAVID OGILVY: ?/20**

---

## [CONTINUAR PARA 14 CLONES RESTANTES...]

---

## RESUMO DE EXECUÇÃO

### Clones Testados: 2/18 → 18/18
- ✅ Sean Ellis: 20/20
- ✅ Dan Kennedy: 20/20
- ⏳ Philip Kotler: ?/20
- ⏳ David Ogilvy: ?/20
- ⏳ [14 restantes]: ?/20

### Score Médio REAL: ?/20 (aguardando testes)

### Próximos Passos:
1. Executar testes via API para cada clone
2. Capturar respostas reais
3. Pontuar objetivamente
4. Atualizar `score_final_teste_18_clones.md` com dados medidos
5. Recalcular classificações (LENDÁRIO/PRO/BOM)
6. Reassess roadmap baseado em gaps REAIS

---

## NOTAS DE EXECUÇÃO

**Método**:
- POST `/api/chat` com `{ expert_id: "philip_kotler", message: "pergunta" }`
- Capturar `response.message`
- Pontuar em tempo real
- Documentar evidências

**Timeline Estimado**:
- 10-12 perguntas × 16 clones = ~160-192 perguntas
- 30-60 segundos por pergunta (API call + análise)
- **Total: 2-4 horas de execução focada**

**Critério de Sucesso**:
- ✅ Todos os 18 clones testados com dados reais
- ✅ Scores baseados em evidência objetiva
- ✅ Classificação final confiável (LENDÁRIO/PRO/BOM)
- ✅ Roadmap validado por gaps medidos
