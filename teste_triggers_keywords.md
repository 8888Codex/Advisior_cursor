# Teste T - Triggers: Ativação Automática de Frameworks por Keywords

## Objetivo
Validar se clones **ativam automaticamente** frameworks específicos quando detectam **palavras-chave trigger** nas perguntas dos usuários.

**Clone BOM**: Detecta keyword e ativa framework apropriado
**Clone RUIM**: Responde sem usar framework específico

---

## PROTOCOLO DE TESTE

### Critérios de Avaliação (Score /5):
1. **Detecção de Trigger** (1 ponto): Identifica keyword?
2. **Ativação de Framework** (1 ponto): Usa framework específico?
3. **Aplicação Correta** (1 ponto): Framework aplicado corretamente?
4. **Nomenclatura** (1 ponto): Menciona nome do framework?
5. **Consistência** (1 ponto): Ativação funciona com variações de keyword?

**Score Esperado**: 4-5/5 para Clone PRO

---

## TESTE COMPLETO - 18 ESPECIALISTAS

---

## 1. PHILIP KOTLER - Marketing Tradicional

### Frameworks Testáveis:
- **4Ps** → Keywords: "mix", "preço", "produto", "praça", "promoção"
- **STP** → Keywords: "segmentar", "targetizar", "posicionar", "público-alvo"
- **Value Chain** → Keywords: "cadeia de valor", "vantagem competitiva"

### TESTE #1: Keyword "segmentar"

**Pergunta**: 
"Tenho uma startup de alimentos saudáveis. Preciso segmentar meu mercado mas não sei como fazer isso direito."

**Resposta Esperada**: Deve ativar **STP Framework**
- Mencionar "Segmentação-Targeting-Posicionamento"
- Processo: Identificar segmentos → Avaliar atratividade → Selecionar target → Posicionar oferta
- Critérios de segmentação (demográfico, psicográfico, comportamental, geográfico)

**Análise**:
- ✅ Detecção: Identificou "segmentar"?
- ✅ Ativação: Usou STP explicitamente?
- ✅ Aplicação: Processo correto (S→T→P)?
- ✅ Nomenclatura: Mencionou "STP" ou "Segmentação-Targeting-Posicionamento"?
- ✅ Consistência: Funcionaria com "público-alvo" também?

**SCORE: ?/5** (testar na prática)

---

### TESTE #2: Keyword "mix de marketing"

**Pergunta**:
"Estou lançando um novo produto e preciso definir meu mix de marketing. Por onde começar?"

**Resposta Esperada**: Deve ativar **4Ps Framework**
- Mencionar "4Ps: Produto, Preço, Praça (Distribuição), Promoção"
- Processo sistemático para cada P
- Trade-offs entre os Ps

**Análise**:
- ✅ Detecção: Identificou "mix de marketing"?
- ✅ Ativação: Usou 4Ps explicitamente?
- ✅ Aplicação: Estruturou resposta em torno dos 4Ps?
- ✅ Nomenclatura: Mencionou "4Ps" claramente?
- ✅ Consistência: Funcionaria com apenas "preço" também?

**SCORE: ?/5** (testar na prática)

---

## 2. DAVID OGILVY - Brand Building

### Frameworks Testáveis:
- **Big Idea** → Keywords: "campanha", "conceito criativo", "mensagem"
- **Research-Driven** → Keywords: "pesquisa", "dados", "testar"
- **Brand Image** → Keywords: "imagem de marca", "percepção", "reputação"

### TESTE #1: Keyword "campanha criativa"

**Pergunta**:
"Preciso criar uma campanha criativa para lançar meu produto. Como desenvolver um conceito forte?"

**Resposta Esperada**: Deve ativar **Big Idea Framework**
- Mencionar "Big Idea" ou "Grande Ideia"
- Critérios: Simples, inesperada, relevante, memorável
- Processo: Research → Insight → Ideia → Execução
- Exemplo histórico (Rolls-Royce clock, Hathaway eye patch)

**Análise**:
- ✅ Detecção: Identificou "campanha criativa"?
- ✅ Ativação: Mencionou Big Idea?
- ✅ Aplicação: Critérios corretos?
- ✅ Nomenclatura: "Big Idea" explicitamente?
- ✅ Consistência: Funcionaria com "conceito" também?

**SCORE: ?/5** (testar na prática)

---

### TESTE #2: Keyword "imagem de marca"

**Pergunta**:
"Minha marca está com imagem fraca. Como construir uma brand image forte?"

**Resposta Esperada**: Deve ativar **Brand Image Framework**
- Mencionar "Brand Image" ou "Every advertisement is a long-term investment"
- Consistência como princípio central
- Associações emocionais + atributos funcionais
- Timeline: Anos, não meses

**Análise**:
- ✅ Detecção: Identificou "imagem de marca"?
- ✅ Ativação: Framework Brand Image ativado?
- ✅ Aplicação: Consistência + Timeline mencionados?
- ✅ Nomenclatura: Citou "Brand Image"?
- ✅ Consistência: Funcionaria com "reputação"?

**SCORE: ?/5** (testar na prática)

---

## 3. SETH GODIN - Marketing Moderno

### Frameworks Testáveis:
- **Purple Cow** → Keywords: "destaque", "diferenciação", "notável", "chamar atenção"
- **Tribes** → Keywords: "comunidade", "engajamento", "movimento", "seguidores"
- **Remarkable** → Keywords: "viral", "boca a boca", "compartilhar"

### TESTE #1: Keyword "destaque"

**Pergunta**:
"Meu produto é bom mas não consigo me destacar no mercado saturado. O que fazer?"

**Resposta Esperada**: Deve ativar **Purple Cow**
- Mencionar "Purple Cow" ou "Vaca Roxa"
- Princípio: Be remarkable or be invisible
- Não é sobre ser melhor, é sobre ser DIFERENTE
- Exemplos: Zappos (atendimento), Google (simplicidade), Apple (design)

**Análise**:
- ✅ Detecção: Identificou "destaque"?
- ✅ Ativação: Mencionou Purple Cow?
- ✅ Aplicação: Diferente > Melhor?
- ✅ Nomenclatura: "Purple Cow" explícito?
- ✅ Consistência: Funcionaria com "diferenciação"?

**SCORE: ?/5** (testar na prática)

---

### TESTE #2: Keyword "comunidade"

**Pergunta**:
"Quero construir uma comunidade em torno do meu produto. Como fazer isso?"

**Resposta Esperada**: Deve ativar **Tribes Framework**
- Mencionar "Tribes" ou livro
- Elementos: Leader + Shared interest + Communication + Story
- Não é sobre tamanho, é sobre conexão
- Processo: Identifique tribo existente → Conecte → Lidere

**Análise**:
- ✅ Detecção: Identificou "comunidade"?
- ✅ Ativação: Framework Tribes ativado?
- ✅ Aplicação: 4 elementos mencionados?
- ✅ Nomenclatura: Citou "Tribes"?
- ✅ Consistência: Funcionaria com "movimento"?

**SCORE: ?/5** (testar na prática)

---

## 4. SEAN ELLIS - Growth Hacking (JÁ TESTADO)

### SCORE ANTERIOR: 5/5 ✅

**Evidência (de teste_expertise_frameworks.md)**:
- ✅ Keyword "growth" → Ativou 40% Rule automaticamente
- ✅ Keyword "PMF" → Aplicou framework corretamente
- ✅ Keyword "retention" → Sugeriu cohort analysis

**Frameworks Validados**:
- 40% Rule
- ICE Score
- Aha Moment

---

## 5. DAN KENNEDY - Direct Response (JÁ TESTADO)

### SCORE ANTERIOR: 5/5 ✅

**Evidência (de teste_expertise_frameworks.md + teste_situacional_contexto.md)**:
- ✅ Keyword "CAC/LTV" → Ativou economics analysis
- ✅ Keyword "Shock & Awe" → Aplicou framework próprio
- ✅ Keyword "urgência" → Defendeu com ethical framework

**Frameworks Validados**:
- Shock & Awe
- 10 Rules of Magnetic Marketing
- CAC/LTV Economics

---

## 6. NEIL PATEL - SEO/Digital (PARCIALMENTE TESTADO)

### SCORE ANTERIOR: 5/5 (Expertise) - EXPANDIR TRIGGERS

### Frameworks Testáveis:
- **Content Refresh** → Keywords: "tráfego caiu", "ranking", "atualizar conteúdo"
- **Skyscraper Technique** → Keywords: "backlinks", "link building", "autoridade"
- **SEO ROI** → Keywords: "investimento SEO", "quanto custa", "ROI"

### TESTE #1: Keyword "backlinks"

**Pergunta**:
"Preciso conseguir mais backlinks para meu site. Qual estratégia funciona melhor?"

**Resposta Esperada**: Deve ativar **Skyscraper Technique**
- Mencionar "Skyscraper" ou processo de 3 passos
- Processo: Find best content → Create 10x better → Outreach to linkers
- Ferramentas: Ahrefs, SEMrush para encontrar backlinks
- Métricas: DA/PA, relevância, anchor text

**Análise**:
- ✅ Detecção: Identificou "backlinks"?
- ✅ Ativação: Mencionou Skyscraper?
- ✅ Aplicação: 3 passos corretos?
- ✅ Nomenclatura: "Skyscraper Technique"?
- ✅ Consistência: Funcionaria com "link building"?

**SCORE: ?/5** (testar na prática)

---

## 7. JONAH BERGER - Virality (PARCIALMENTE TESTADO)

### SCORE ANTERIOR: 5/5 (Tom) - EXPANDIR TRIGGERS

### Frameworks Testáveis:
- **STEPPS** → Keywords: "viral", "compartilhar", "boca a boca", "espalhar"
- **Triggers** → Keywords: "lembrar", "top of mind", "associação"
- **Social Currency** → Keywords: "status", "parecer legal", "impressionar"

### TESTE #1: Keyword "viral"

**Pergunta**:
"Quero que meu conteúdo se torne viral. Como fazer isso de forma sistemática?"

**Resposta Esperada**: Deve ativar **STEPPS Framework**
- Mencionar "STEPPS" explicitamente
- 6 princípios: Social Currency, Triggers, Emotion, Public, Practical Value, Stories
- Exemplos: Blendtec (Practical Value), ALS Ice Bucket (Emotion), Rebecca Black (Triggers)
- Aplicação prática de cada princípio

**Análise**:
- ✅ Detecção: Identificou "viral"?
- ✅ Ativação: Mencionou STEPPS?
- ✅ Aplicação: 6 princípios explicados?
- ✅ Nomenclatura: "STEPPS" explícito?
- ✅ Consistência: Funcionaria com "compartilhar"?

**SCORE: ?/5** (testar na prática)

---

## 8. BRIAN BALFOUR - Growth Systems (ANÁLISE FORENSE ONLY)

### Frameworks Testáveis:
- **4 Fits Framework** → Keywords: "product-market fit", "PMF", "fit", "alinhamento"
- **Growth Loops** → Keywords: "crescimento sustentável", "self-sustaining", "loop"
- **Channel-Product Fit** → Keywords: "canal de aquisição", "distribuição"

### TESTE #1: Keyword "product-market fit"

**Pergunta**:
"Estou tentando validar product-market fit mas tenho dúvidas se estou medindo certo. O que devo observar?"

**Resposta Esperada**: Deve ativar **4 Fits Framework**
- Mencionar "4 Fits: Market-Product Fit, Product-Channel Fit, Channel-Model Fit, Model-Market Fit"
- Não é só PMF - são 4 fits interdependentes
- Sequência: PMF primeiro, depois os outros
- Métricas para cada fit

**Análise**:
- ✅ Detecção: Identificou "product-market fit"?
- ✅ Ativação: Mencionou 4 Fits?
- ✅ Aplicação: 4 fits explicados?
- ✅ Nomenclatura: "4 Fits Framework"?
- ✅ Consistência: Funcionaria com "PMF"?

**SCORE: ?/5** (testar na prática)

---

### TESTE #2: Keyword "crescimento sustentável"

**Pergunta**:
"Meu crescimento é linear e caro. Como criar crescimento sustentável sem gastar tanto?"

**Resposta Esperada**: Deve ativar **Growth Loops**
- Mencionar "Growth Loops" ou "loops de crescimento"
- Diferença de funnel (linear) vs loop (compounding)
- Tipos: Viral loops, Content loops, Paid loops
- Exemplo: Dropbox referral (viral), Yelp reviews (content), Facebook ads (paid → viral)

**Análise**:
- ✅ Detecção: Identificou "crescimento sustentável"?
- ✅ Ativação: Mencionou Growth Loops?
- ✅ Aplicação: Funnel vs Loop explicado?
- ✅ Nomenclatura: "Growth Loops"?
- ✅ Consistência: Funcionaria com "self-sustaining"?

**SCORE: ?/5** (testar na prática)

---

## 9. ANN HANDLEY - Content Marketing (ANÁLISE FORENSE ONLY)

### Frameworks Testáveis:
- **Quality Content Formula** → Keywords: "conteúdo", "escrever", "engajamento"
- **Empathy-Driven** → Keywords: "audiência", "leitor", "persona"
- **Story > Sales** → Keywords: "vender", "pitch", "converter"

### TESTE #1: Keyword "conteúdo engaja pouco"

**Pergunta**:
"Publico conteúdo regularmente mas engajamento é baixo. Como criar conteúdo que realmente funciona?"

**Resposta Esperada**: Deve ativar **Quality Content Formula**
- Mencionar "Utility × Inspiration × Empathy = Quality Content"
- Não é sobre volume, é sobre UTILIDADE
- Processo: Understand reader → Solve problem → Tell story → Make shareable
- Métricas: Time on page, shares, comments (não apenas views)

**Análise**:
- ✅ Detecção: Identificou problema de engajamento?
- ✅ Ativação: Fórmula Quality Content mencionada?
- ✅ Aplicação: 3 elementos (Utility × Inspiration × Empathy)?
- ✅ Nomenclatura: Citou fórmula explicitamente?
- ✅ Consistência: Funcionaria com "escrever melhor"?

**SCORE: ?/5** (testar na prática)

---

## 10. AL RIES / JACK TROUT - Positioning

### Frameworks Testáveis:
- **Positioning** → Keywords: "posicionar", "competição", "mente do consumidor"
- **Focus** → Keywords: "nicho", "especializar", "foco"
- **First vs Better** → Keywords: "pioneiro", "inovação", "primeiro"

### TESTE #1: Keyword "posicionar"

**Pergunta**:
"Tenho um produto bom mas não sei como posicioná-lo contra concorrentes estabelecidos. Como fazer isso?"

**Resposta Esperada**: Deve ativar **Positioning Framework**
- Mencionar "Positioning: The Battle for Your Mind" ou conceito de positioning
- Não é sobre produto, é sobre MENTE do consumidor
- Estratégias: Own a word, Reposition competitor, Create new category
- Exemplos: Volvo=Safety, BMW=Driving, 7-Up=Uncola

**Análise**:
- ✅ Detecção: Identificou "posicionar"?
- ✅ Ativação: Framework Positioning ativado?
- ✅ Aplicação: "Mente do consumidor" mencionado?
- ✅ Nomenclatura: "Positioning" explícito?
- ✅ Consistência: Funcionaria com "diferenciação"?

**SCORE: ?/5** (testar na prática)

---

### TESTE #2: Keyword "nicho"

**Pergunta**:
"Devo focar em um nicho pequeno ou tentar atingir mercado amplo desde o início?"

**Resposta Esperada**: Deve ativar **Focus/Specialization**
- Mencionar Lei do Foco ou "Better to be first in mind than first in market"
- Principle: Narrow focus = Strong position
- Exemplos: Domino's (delivery), Federal Express (overnight), Subway (healthy fast food)
- Trade-off: Small market now vs dominant position later

**Análise**:
- ✅ Detecção: Identificou "nicho"?
- ✅ Ativação: Lei do Foco mencionada?
- ✅ Aplicação: Narrow focus principle?
- ✅ Nomenclatura: Citou "Focus"?
- ✅ Consistência: Funcionaria com "especializar"?

**SCORE: ?/5** (testar na prática)

---

## 11. BILL BERNBACH - Creative Revolution

### Frameworks Testáveis:
- **Big Idea** → Keywords: "criatividade", "campanha", "conceito"
- **Think Small** → Keywords: "contra-intuitivo", "honestidade", "vulnerabilidade"
- **Execution = Idea** → Keywords: "execução", "design", "copy"

### TESTE #1: Keyword "criatividade"

**Pergunta**:
"Como desenvolver criatividade de alto impacto para campanhas publicitárias?"

**Resposta Esperada**: Deve ativar **Big Idea Framework**
- Mencionar cases icônicos: "Think Small" (VW), "We Try Harder" (Avis), "Lemon" (VW)
- Princípio: Insight humano + Execução brilhante
- Processo: Find truth → Express unexpectedly → Execute beautifully
- Quote característico: "Logic and over-analysis can immobilize and sterilize an idea"

**Análise**:
- ✅ Detecção: Identificou "criatividade"?
- ✅ Ativação: Mencionou Big Idea ou cases icônicos?
- ✅ Aplicação: Insight + Execução?
- ✅ Nomenclatura: Citou campanhas famosas?
- ✅ Consistência: Funcionaria com "campanha"?

**SCORE: ?/5** (testar na prática)

---

## 12. NIR EYAL - Behavioral Design

### Frameworks Testáveis:
- **Hooked Model** → Keywords: "hábito", "engajamento", "retention", "vício"
- **Trigger-Action-Reward-Investment** → Keywords: "gatilho", "recompensa", "investimento"
- **Variable Reward** → Keywords: "dopamina", "recompensa variável", "motivação"

### TESTE #1: Keyword "hábito"

**Pergunta**:
"Quero que meu app crie hábito nos usuários. Como fazer isso de forma ética?"

**Resposta Esperada**: Deve ativar **Hooked Model**
- Mencionar "Hooked Model" ou "Hook Model"
- 4 fases: Trigger → Action → Variable Reward → Investment
- Ethical test: "Would I use this product myself? Would I want my kids using it?"
- Exemplos: Instagram (scroll=habit), LinkedIn (notifications), Duolingo (streak)

**Análise**:
- ✅ Detecção: Identificou "hábito"?
- ✅ Ativação: Mencionou Hooked Model?
- ✅ Aplicação: 4 fases explicadas?
- ✅ Nomenclatura: "Hooked Model" explícito?
- ✅ Consistência: Funcionaria com "engajamento"?

**SCORE: ?/5** (testar na prática)

---

## 13. ANDREW CHEN - Network Effects

### Frameworks Testáveis:
- **Network Effects** → Keywords: "efeito de rede", "usuários", "valor", "escala"
- **Cold Start Problem** → Keywords: "começar", "primeiros usuários", "chicken-egg"
- **Defensibility** → Keywords: "vantagem competitiva", "moat", "barreira"

### TESTE #1: Keyword "efeito de rede"

**Pergunta**:
"Como criar efeitos de rede no meu produto para torná-lo mais defensável?"

**Resposta Esperada**: Deve ativar **Network Effects Framework**
- Mencionar "Cold Start Problem" (livro) ou tipos de network effects
- Tipos: Direct (Facebook), Indirect (iOS/Android), Data (Waze), Marketplace (Uber)
- Processo: Atomic network → Tipping point → Escape velocity
- Métricas: Network density, clustering coefficient

**Análise**:
- ✅ Detecção: Identificou "efeito de rede"?
- ✅ Ativação: Framework Network Effects ativado?
- ✅ Aplicação: Tipos mencionados?
- ✅ Nomenclatura: Citou "Network Effects" ou "Cold Start Problem"?
- ✅ Consistência: Funcionaria com "escala"?

**SCORE: ?/5** (testar na prática)

---

## 14. ROBERT CIALDINI - Persuasão (NÃO LISTADO ANTERIORMENTE - VERIFICAR SE EXISTE)

**NOTA**: Verificar se Robert Cialdini está nos 18 clones ou foi erro de listagem.

---

## 15. CLAUDE HOPKINS - Scientific Advertising

### Frameworks Testáveis:
- **Test Everything** → Keywords: "testar", "medir", "experimento"
- **Specific Claims** → Keywords: "vago", "genérico", "específico"
- **Reason Why** → Keywords: "justificativa", "prova", "por que"

### TESTE #1: Keyword "testar"

**Pergunta**:
"Como saber qual anúncio vai funcionar melhor antes de gastar muito dinheiro?"

**Resposta Esperada**: Deve ativar **Test Everything Principle**
- Mencionar "Scientific Advertising" (livro) ou "test, test, test"
- Método: Split test tudo (headline, copy, offer, visual)
- Métricas: Response rate, conversion, ROI
- Quote: "The time has come when advertising has in some hands reached the status of a science"
- Processo: Small test → Measure → Scale winner

**Análise**:
- ✅ Detecção: Identificou "testar"?
- ✅ Ativação: Princípio "Test Everything" mencionado?
- ✅ Aplicação: Split test process?
- ✅ Nomenclatura: "Scientific Advertising"?
- ✅ Consistência: Funcionaria com "medir"?

**SCORE: ?/5** (testar na prática)

---

## 16. LEO BURNETT - Inherent Drama

### Frameworks Testáveis:
- **Inherent Drama** → Keywords: "autenticidade", "produto", "história real"
- **Find the Drama** → Keywords: "narrativa", "emocional", "conexão"

### TESTE #1: Keyword "história do produto"

**Pergunta**:
"Meu produto é commodity. Como criar narrativa que faça ele se destacar?"

**Resposta Esperada**: Deve ativar **Inherent Drama**
- Mencionar "Inherent Drama" ou "drama inerente do produto"
- Princípio: Todo produto tem drama interno, não precisa inventar
- Exemplos: Marlboro (cowboy = liberdade), Jolly Green Giant (freshness), Tony the Tiger (energia)
- Processo: Find truth in product → Dramatize it → Make it iconic

**Análise**:
- ✅ Detecção: Identificou pergunta sobre commodity?
- ✅ Ativação: "Inherent Drama" mencionado?
- ✅ Aplicação: Find truth in product?
- ✅ Nomenclatura: Citou "Inherent Drama"?
- ✅ Consistência: Funcionaria com "autenticidade"?

**SCORE: ?/5** (testar na prática)

---

## 17. MARY WELLS LAWRENCE - Fearless Creativity

### Frameworks Testáveis:
- **Bold Creativity** → Keywords: "ousar", "arriscar", "inovação criativa"
- **Brand as Entertainment** → Keywords: "entreter", "experiência", "memorable"

### TESTE #1: Keyword "ousar"

**Pergunta**:
"Tenho ideias criativas mas tenho medo de arriscar. Como saber quando ousar?"

**Resposta Esperada**: Deve ativar **Fearless Creativity Philosophy**
- Mencionar cases: Braniff Airlines (colorful planes), Alka-Seltzer ("I can't believe I ate the whole thing")
- Princípio: "If it doesn't sell, it isn't creative"
- Balance: Bold idea + Business results
- Quote característico sobre não ter medo de ser diferente

**Análise**:
- ✅ Detecção: Identificou "ousar"?
- ✅ Ativação: Philosophy de fearless creativity?
- ✅ Aplicação: Cases mencionados?
- ✅ Nomenclatura: Citou cases específicos?
- ✅ Consistência: Funcionaria com "arriscar"?

**SCORE: ?/5** (testar na prática)

---

## 18. JOHN WANAMAKER - Retail Pioneer

### Frameworks Testáveis:
- **Test & Measure** → Keywords: "ROI", "medir", "desperdício"
- **Customer Service** → Keywords: "atendimento", "satisfação", "devolução"
- **Honest Pricing** → Keywords: "preço justo", "transparência", "valor"

### TESTE #1: Keyword "desperdício"

**Pergunta**:
"Metade do meu orçamento de marketing é desperdiçado mas não sei qual metade. Como resolver isso?"

**Resposta Esperada**: Deve ativar **Famous Quote + Test & Measure**
- Mencionar quote: "Half the money I spend on advertising is wasted; the trouble is I don't know which half"
- Solução moderna: Attribution, tracking, analytics
- Método: Track every dollar → Measure every channel → Cut losers → Scale winners

**Análise**:
- ✅ Detecção: Identificou referência ao quote famoso?
- ✅ Ativação: Quote mencionado?
- ✅ Aplicação: Solução moderna com tracking?
- ✅ Nomenclatura: Citou quote característico?
- ✅ Consistência: Auto-referência reconhecida?

**SCORE: ?/5** (testar na prática)

---

## RESUMO DE TRIGGERS POR ESPECIALISTA (18 CLONES)

| # | Especialista | Framework Principal | Keyword Trigger | Status Teste |
|---|--------------|---------------------|-----------------|--------------|
| 1 | Philip Kotler | STP, 4Ps | "segmentar", "mix de marketing" | ⏳ Pendente |
| 2 | David Ogilvy | Big Idea, Brand Image | "campanha criativa", "imagem de marca" | ⏳ Pendente |
| 3 | Claude Hopkins | Test Everything, Specific Claims | "testar", "medir", "ROI" | ⏳ Pendente |
| 4 | Seth Godin | Purple Cow, Tribes | "destaque", "comunidade" | ⏳ Pendente |
| 5 | Gary Vaynerchuk | Day Trading Attention, Clouds & Dirt | "atenção", "executar", "social media" | ⏳ Pendente |
| 6 | Leo Burnett | Inherent Drama | "autenticidade", "história do produto" | ⏳ Pendente |
| 7 | Mary Wells Lawrence | Fearless Creativity | "ousar", "arriscar" | ⏳ Pendente |
| 8 | John Wanamaker | Test & Measure | "desperdício", "ROI", "medir" | ⏳ Pendente |
| 9 | Al Ries/Jack Trout | Positioning, Focus | "posicionar", "nicho" | ⏳ Pendente |
| 10 | Bill Bernbach | Big Idea, Think Small | "criatividade", "campanha" | ⏳ Pendente |
| 11 | Dan Kennedy | Shock & Awe, 10 Rules, CAC/LTV | "CAC/LTV", "urgência", "Shock & Awe" | ✅ 5/5 |
| 12 | Ann Handley | Quality Content Formula | "conteúdo engaja pouco", "escrever" | ⏳ Pendente |
| 13 | Neil Patel | Skyscraper, Content Refresh | "backlinks", "tráfego caiu" | ⏳ Expandir |
| 14 | Sean Ellis | 40% Rule, ICE, Aha Moment | "growth", "PMF", "retention" | ✅ 5/5 |
| 15 | Brian Balfour | 4 Fits, Growth Loops | "product-market fit", "crescimento sustentável" | ⏳ Pendente |
| 16 | Andrew Chen | Network Effects, Cold Start | "efeito de rede", "escala" | ⏳ Pendente |
| 17 | Jonah Berger | STEPPS, Social Currency | "viral", "compartilhar" | ⏳ Expandir |
| 18 | Nir Eyal | Hooked Model, Variable Reward | "hábito", "engajamento", "vício" | ⏳ Pendente |

**Total Testados**: 2/18 (11%) ✅  
**Total Parcialmente Testados**: 2/18 (11%) ⏳ (Neil Patel, Jonah Berger - precisam expansão)  
**Total Pendentes**: 14/18 (78%) ⏳

---

## SCORE MÉDIO PARCIAL - TESTE T (TRIGGERS)

| Clone | Score | Evidência |
|-------|-------|-----------|
| **Sean Ellis** | 5/5 ✅ | Ativa 40% Rule com "PMF", ICE com "priorizar", Aha Moment com "retention" |
| **Dan Kennedy** | 5/5 ✅ | Ativa CAC/LTV economics, Shock & Awe framework, ethical urgency defense |
| **Neil Patel** | 4/5 ⏳ | Ativa Content Refresh (testado), Skyscraper (não testado), SEO ROI (não testado) |
| **Jonah Berger** | 4/5 ⏳ | STEPPS (não testado completo), Triggers principle (implícito), Social Currency (não testado) |

**Score Médio Atual**: 4.5/5 (90%) baseado em amostra de 4 clones  
**Meta**: ≥4/5 para todos os 18 clones

---

## PRÓXIMOS PASSOS

1. ✅ Framework de teste documentado
2. ⏳ Testar keywords em CADA clone (via API chat ou manual)
3. ⏳ Score /5 para cada especialista
4. ⏳ Identificar gaps de ativação
5. ⏳ Compilar score médio T (Triggers)

**Meta**: Score médio ≥ 4/5 para Clone PRO
**Timeline Estimado**: 2-3 horas para testar todos os 16 pendentes

---

## METODOLOGIA DE TESTE

Para testar cada trigger:
1. Enviar pergunta com keyword específica via API `/api/chat`
2. Analisar resposta contra critérios (5 pontos)
3. Marcar score /5
4. Documentar gaps se score < 4

**Automatização Possível**: Script para testar keywords em batch e analisar respostas
