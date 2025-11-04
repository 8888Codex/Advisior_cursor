# Catálogo de Features - AdvisorIA Elite

**Versão:** 2.0.0  
**Última Atualização:** 3 de Novembro de 2025

---

## Visão Geral

AdvisorIA Elite oferece 4 features principais:

1. **Sistema de Experts** - 22 clones cognitivos de lendas do marketing
2. **Persona Builder** - Criação de personas ultra-específicas
3. **Conselho de IA** - Análise colaborativa com múltiplos experts
4. **Auto-Clone** - Criação automática de novos experts

---

## Feature 1: Sistema de Experts

### Descrição

22 clones cognitivos de alta fidelidade de lendas do marketing, cada um com personalidade, filosofia e métodos únicos.

### Capabilities

- ✅ Chat 1-on-1 com cada especialista
- ✅ System prompts de 1000-3000 palavras
- ✅ Personalidades distintas e autênticas
- ✅ Categorização por área de expertise
- ✅ Busca e filtragem

### Experts Disponíveis (22 total)

#### Estratégia (4)
- **Philip Kotler** - Pai do Marketing Moderno
- **Al Ries & Jack Trout** - Posicionamento
- **Michael Porter** - Estratégia Competitiva
- **Clayton Christensen** - Inovação Disruptiva

#### Growth Marketing (3)
- **Sean Ellis** - Growth Hacking
- **Andrew Chen** - Network Effects
- **Brian Balfour** - Scalable Growth

#### Branding (2)
- **David Aaker** - Brand Equity
- **Marty Neumeier** - Brand Gap

#### Content Marketing (4)
- **Seth Godin** - Permission Marketing
- **Ann Handley** - Content Rules
- **Joe Pulizzi** - Content Inc
- **Jay Baer** - Youtility

#### Social Media (2)
- **Gary Vaynerchuk** - Jab, Jab, Jab, Right Hook
- **Mari Smith** - Facebook Marketing

#### Performance Marketing (3)
- **Neil Patel** - SEO e Growth
- **Perry Marshall** - Google Ads
- **Rand Fishkin** - SEO e Transparência

#### Advertising (2)
- **David Ogilvy** - Advertising Genius
- **Bill Bernbach** - Creative Revolution

#### Sales (2)
- **Dan Kennedy** - Direct Response
- **Alex Hormozi** - $100M Offers

### Implementação

**Arquivos:**
- `python_backend/clones/registry.py` - Registro central
- `python_backend/clones/*.py` - 22 arquivos individuais

**Endpoint:**
- `GET /api/experts` - Lista todos
- `GET /api/experts/:id` - Busca específico
- `POST /api/experts/:id/chat` - Chat 1-on-1

**Rate Limits:**
- Chat: 60/hora
- List: Sem limite

**Tempo:**
- Chat response: ~3-5s

**Referência:** [CLONES_PYTHON_COMPLETO.md](../CLONES_PYTHON_COMPLETO.md)

---

## Feature 2: Persona Builder

### Descrição

Sistema de criação de personas ultra-específicas usando frameworks JTBD (Jobs to Be Done) e BAG (Behaviors, Aspirations, Goals).

### Capabilities

#### Modo Quick (Rápido)
- ✅ Criação em ~10 segundos
- ✅ Usa apenas Claude (sem pesquisa externa)
- ✅ Qualidade boa para testes
- ✅ Gratuito (só custo de Claude ~$0.02)

#### Modo Strategic (Estratégico) ⭐
- ✅ Pesquisa profunda em 4 fases
- ✅ 3 chamadas Perplexity + 1 Claude
- ✅ Qualidade máxima (10/10)
- ✅ Fontes reais (10-20 URLs)
- ✅ Comunidades específicas (5-10)
- ✅ Pain points quantificados (com R$)
- ✅ Decision criteria completo

### Feature 2.1: Melhorar Descrição com IA ⭐

**Problema que resolve:** Usuários não sabem descrever personas de forma específica

**Como funciona:**
1. Usuário digita descrição vaga
2. Clica "✨ Melhorar Descrição com IA"
3. IA expande e sugere:
   - Descrição ultra-específica
   - Indústria sugerida
   - Contexto adicional
4. Auto-preenche os 3 campos

**Exemplo:**
```
Input: "profissional b2b com time"

Output:
- Descrição: "CMO ou Diretor Comercial de empresas B2B (SaaS, Tecnologia) com faturamento R$500k-5M/ano, equipe de 3-10 pessoas..."
- Indústria: "SaaS B2B / Tecnologia"
- Contexto: "Ciclo de vendas médio/longo (30-90 dias)"
```

**Implementação:**
- Endpoint: `POST /api/personas/enhance-description`
- Modelo: Claude Sonnet 4
- Tempo: ~5s
- Rate limit: 30/hora

**Referência:** [CORRECAO_ENHANCE_IA.md](../CORRECAO_ENHANCE_IA.md)

### Dados Gerados (Modo Strategic)

Uma persona completa com:
- **Job Statement** - Trabalho principal a ser feito
- **Jobs** - Funcionais (5-7), Emocionais (4-5), Sociais (3-4)
- **Pain Points** - Quantificados com custos em R$ e frequência
- **Behaviors** - Online, compra, consumo de conteúdo
- **Aspirations** - 4-5 aspirações específicas
- **Goals** - 5-7 objetivos mensuráveis
- **Decision Criteria** - Must-have, nice-to-have, deal-breakers
- **Demographics** - Idade, local, cargo, educação, renda
- **Values** - 4-5 valores core
- **Touchpoints** - Canais por stage da jornada
- **Communities** - 5-10 comunidades onde estão ativos
- **Sources** - 10-20 URLs de pesquisa real

### Implementação

**Arquivos:**
- `client/src/pages/Personas.tsx` - Interface
- `python_backend/reddit_research.py` - Engine de pesquisa
- `python_backend/models_persona.py` - Models

**Endpoints:**
- `POST /api/personas` - Criar
- `GET /api/personas` - Listar
- `DELETE /api/personas/:id` - Deletar
- `POST /api/personas/enhance-description` - Melhorar

**Tempo:**
- Quick: ~10s
- Strategic: ~80s
- Enhance: ~5s

**Rate Limits:**
- Create: 10/hora
- Enhance: 30/hora

**Referências:**
- [MODO_ESTRATEGICO_REFATORADO.md](../MODO_ESTRATEGICO_REFATORADO.md)
- [PERSONA_BUILDER.md](../PERSONA_BUILDER.md)
- [FEATURE_MELHORAR_COM_IA.md](../FEATURE_MELHORAR_COM_IA.md)

---

## Feature 3: Conselho de IA

### Descrição

Análise colaborativa de problemas com múltiplos especialistas que chegam a um consenso e geram plano de ação estruturado.

### Capabilities

#### 3 Modos de Operação

**1. Traditional Mode**
- Análise síncrona
- 1 especialista por vez
- Resposta única ao final
- Tempo: ~60s para 3 experts

**2. SSE Streaming Mode**
- Streaming em tempo real
- Visualização do progresso
- Events: expert_started, expert_progress, expert_completed
- Tempo: ~60s com feedback visual

**3. Background Polling Mode** ⭐ Recomendado
- Funciona mesmo em tabs inativas
- Task ID retornado imediatamente
- Polling a cada 3 segundos
- Persiste ao navegar
- Tempo: ~60s com máxima robustez

### Fluxo Completo

```
1. Usuário seleciona persona (OBRIGATÓRIO)
2. Usuário seleciona 2-4 especialistas
   OU usa recomendações automáticas da IA
3. Usuário descreve problema
4. Sistema analisa com cada expert (paralelo)
5. Sistema constrói consensus
6. Sistema gera action plan estruturado
7. Usuário pode continuar conversando
```

### Recomendação Automática de Experts

**Feature adicional:** IA analisa o problema e recomenda os melhores experts.

**Como funciona:**
1. Usuário digita problema
2. Sistema analisa com Claude
3. Retorna 3-5 experts recomendados com:
   - Relevance score (1-5 estrelas)
   - Justificativa
4. Usuário pode aplicar sugestões com 1 clique

**Endpoint:** `POST /api/council/recommend-experts`  
**Tempo:** ~5-8s

### Componentes do Resultado

#### Contributions Individuais
Cada expert fornece:
- **Analysis** - Análise completa do problema
- **Key Insights** - 3-5 insights principais
- **Recommendations** - Recomendações específicas

#### Consensus
- Síntese das principais recomendações
- Pontos de concordância entre experts
- Direcionamento estratégico unificado

#### Action Plan
Plano estruturado em fases:
```json
{
  "phases": [
    {
      "phaseNumber": 1,
      "name": "Diagnóstico e Setup",
      "duration": "15 dias",
      "objectives": [...],
      "actions": [
        {
          "title": "Auditoria de canais atuais",
          "description": "...",
          "responsible": "CMO",
          "priority": "alta",
          "estimatedTime": "3 dias",
          "tools": ["Google Analytics", "Meta Ads Manager"],
          "steps": [...]
        }
      ],
      "dependencies": [],
      "deliverables": [...]
    }
  ],
  "totalDuration": "90 dias",
  "estimatedBudget": "R$50k-100k",
  "successMetrics": [...]
}
```

### Chat Continuado

Após análise, usuário pode:
- Fazer perguntas de follow-up
- Pedir esclarecimentos
- Refinar o plano
- Discutir implementação

**Funciona como:** Chat em grupo onde todos os experts participam

### Implementação

**Arquivos:**
- `client/src/pages/TestCouncil.tsx` - Interface principal
- `client/src/pages/CouncilChat.tsx` - Chat em grupo
- `client/src/hooks/useCouncilBackground.ts` - Background mode
- `client/src/hooks/useCouncilStream.ts` - SSE mode
- `client/src/components/council/` - Componentes visuais
- `python_backend/crew_council.py` - Orquestração

**Endpoints:**
- `POST /api/council/analyze` - Traditional
- `POST /api/council/analyze-async` - Background
- `POST /api/council/analyze-stream` - SSE
- `GET /api/council/tasks/:id` - Status da task
- `POST /api/council/recommend-experts` - Recomendações
- `POST /api/council/conversations` - Criar chat
- `POST /api/council/conversations/:id/messages` - Enviar msg

**Tempo:**
- 2 experts: ~40s
- 3 experts: ~60s
- 4 experts: ~90s
- 5+ experts: ~120s+

**Rate Limit:** 10/hora

**Referências:**
- [PLANO_CONSELHO_MELHORADO.md](../PLANO_CONSELHO_MELHORADO.md)
- [SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md](../SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md)
- [CORRECAO_CONSELHO_SUMINDO.md](../CORRECAO_CONSELHO_SUMINDO.md)

---

## Feature 4: Auto-Clone de Experts

### Descrição

Criação automática de clones cognitivos de qualquer pessoa pública usando Framework EXTRACT de 20 pontos.

### Framework EXTRACT (20 Pontos)

#### 1-3. EXPERIENCES (Experiências Formativas)
- Momentos decisivos na carreira
- Fracassos e aprendizados
- Sucessos que definiram abordagem

#### 4-6. X-FACTORS (Fatores Únicos)
- Traços de personalidade distintivos
- Abordagem única ao trabalho
- Diferenciais competitivos

#### 7-9. TERMINOLOGY (Terminologia Própria)
- Frases de assinatura
- Conceitos criados
- Jargão específico

#### 10-12. REASONING (Padrões de Raciocínio)
- Como toma decisões
- Frameworks mentais
- Processo de análise

#### 13-15. AXIOMS (Axiomas Pessoais)
- Crenças fundamentais
- Princípios inegociáveis
- Filosofia core

#### 16-17. CALLBACKS (Story Banks)
- Histórias icônicas que conta
- Exemplos favoritos
- Metáforas recorrentes

#### 18-19. TONE (Tom e Estilo)
- Estilo de comunicação
- Nível de formalidade
- Humor e personalidade

#### 20. CONSTRAINTS (Limitações)
- O que NÃO faz
- Áreas fora da expertise
- Limitações conscientes

### Processo de Criação

#### STEP 1: Biographical Research (30-60s)
Pesquisa com Perplexity:
- Biografia completa
- Trabalhos principais
- Filosofia e métodos
- Citações e histórias
- Impacto e legado

#### STEP 2: Cognitive Synthesis (60-90s)
Síntese com Claude Sonnet 4:
- Gera system prompt EXTRACT completo
- Extrai os 20 pontos
- Cria metadata (name, title, expertise)
- Valida autenticidade

#### STEP 3: Testing (usuário)
- Chat de teste integrado
- Validação da personalidade
- Ajuste se necessário

#### STEP 4: Saving (opcional)
- Salva no database
- Disponibiliza para uso
- Pode ser usado em conselho

### Implementação

**Arquivos:**
- `client/src/pages/Create.tsx` - Interface
- `python_backend/main.py` - Endpoint auto-clone
- `python_backend/clone_generator.py` - Geração

**Endpoints:**
- `POST /api/experts/auto-clone` - Criar clone
- `POST /api/experts/test-chat` - Testar clone
- `POST /api/experts` - Salvar clone

**Tempo:** ~120-180 segundos  
**Rate Limit:** 5/hora  
**Cost:** ~$0.30-0.50

**Referências:**
- [SISTEMA_CLONES_PYTHON_AUTOMATICO.md](../SISTEMA_CLONES_PYTHON_AUTOMATICO.md)
- [ENTREGA_FINAL_CLONES_AUTOMATICOS.md](../ENTREGA_FINAL_CLONES_AUTOMATICOS.md)
- [python_backend/DEEP_CLONE_README.md](../python_backend/DEEP_CLONE_README.md)

---

## Features de Suporte

### Persistência de Estado

**Descrição:** Estado do conselho persiste ao navegar entre páginas.

**Capabilities:**
- ✅ Problema, experts selecionados, persona persistem
- ✅ Resultado da análise persiste
- ✅ Funciona mesmo fechando e abrindo a aba
- ✅ Expiração: 24 horas
- ✅ Indicador visual de estado restaurado
- ✅ Botão para limpar estado

**Hook:** `usePersistedState`  
**Storage:** localStorage

**Referência:** [ENTREGA_PERSISTENCIA_ESTADO_COMPLETA.md](../ENTREGA_PERSISTENCIA_ESTADO_COMPLETA.md)

---

### Background Processing

**Descrição:** Análise do conselho continua rodando mesmo em tabs inativas.

**Problema que resolve:**
- Browser throttles JavaScript em tabs inativas
- Timers param, requisições atrasam
- Análise interrompida ao trocar de aba

**Solução:**
- Background polling a cada 3s
- Baseado em Date.now() (não setTimeout)
- Detecta quando usuário volta
- Sincroniza estado automaticamente

**Referência:** [SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md](../SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md)

---

### Activity Feed

**Descrição:** Feed de atividades em tempo real durante análise.

**Mostra:**
- "Iniciando análise com 3 especialistas"
- "Philip Kotler começou a analisar..."
- "Seth Godin completou análise"
- "Construindo consenso..."
- "Gerando plano de ação..."

**Implementação:**
- Componente: `ActivityFeed.tsx`
- Mantém últimas 10 atividades
- Auto-scroll para mais recente

---

### Expert Status Visualization

**Descrição:** Visualização em tempo real do status de cada expert.

**Estados:**
- ⏳ **Waiting** - Aguardando na fila
- 🔍 **Researching** - Pesquisando contexto
- 🧠 **Analyzing** - Analisando problema
- ✅ **Completed** - Análise concluída
- ❌ **Error** - Erro na análise

**Componente:** `ExpertAvatar.tsx`  
**Features:**
- Progress bar (0-100%)
- Animação pulsante quando ativo
- Cores por expert (consistente)

---

### Typing Effect

**Descrição:** Efeito de digitação gradual no consenso.

**Capabilities:**
- Velocidade: 25 caracteres/segundo
- Delay inicial: 500ms
- Pode pular (click anywhere)
- Melhora UX percebida

**Hook:** `useTypingDelay`

---

## Integrações

### Anthropic Claude

**Modelo:** claude-sonnet-4-20250514

**Usado em:**
- Chat 1-on-1 com experts
- Análise do conselho (cada expert)
- Consensus building
- Action plan generation
- Auto-clone synthesis
- Persona enhancement
- Expert recommendations

**Cost por operação:**
- Chat: ~$0.02
- Council (3 experts): ~$0.15
- Auto-clone: ~$0.30
- Enhance description: ~$0.01

---

### Perplexity AI

**Modelos:** sonar-reasoning (primary), sonar, sonar-pro

**Usado em:**
- Persona research (modo strategic)
- Auto-clone biographical research

**Pesquisas Strategic (3 calls):**
1. Discovery de comunidades
2. Pain points quantificados
3. Comportamentos e decisões

**Cost por operação:**
- Persona strategic: ~$0.15 (3 calls)
- Auto-clone: ~$0.05 (1 call)

---

### PostgreSQL (Neon)

**Hosted:** Neon Serverless Postgres  
**Region:** sa-east-1 (São Paulo)

**Tabelas:**
- `experts` - Especialistas
- `personas` - Personas antigas
- `personas_modern` - Personas com JTBD/BAG
- `personas_deep` - Personas profundas (futuro)
- `conversations` - Conversas
- `messages` - Mensagens
- `council_tasks` - Tasks de background
- `user_preferences` - Preferências

**Features:**
- Connection pooling
- SSL obrigatório
- Backups automáticos
- 0.5 GB free tier

---

## UI/UX Features

### Design System

**Base:** shadcn/ui + Tailwind CSS

**Componentes:**
- 50+ componentes UI reutilizáveis
- Dark mode support
- Responsive design
- Accessibility (A11Y)

**Referência:** [UI_UX_COMPLETO.md](../UI_UX_COMPLETO.md)

---

### Animações

**Biblioteca:** Framer Motion

**Animações principais:**
- Page transitions
- Card hover effects
- Loading states
- Success celebrations (confetti!)
- Expert avatar pulse
- Activity feed entrance

**Configuração:**
```typescript
const pageVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};
```

---

### Loading States

Todos os estados de loading implementados:
- ⏳ Skeleton loaders
- 🔄 Spinners (Loader2 icon)
- 📊 Progress bars (0-100%)
- ⏱️ Tempo decorrido (mm:ss)
- 💬 Mensagens de progresso

**Exemplo:**
```
🔍 Pesquisando... (0:15)
🧠 Analisando... (0:45)
✨ Sintetizando... (1:30)
```

---

## Roadmap de Features

### Versão 2.1 (Próximo)
- [ ] Autenticação de usuários
- [ ] Perfil de negócio
- [ ] Histórico de consultas
- [ ] Favoritos e bookmarks
- [ ] Exportação de relatórios (PDF)

### Versão 2.2
- [ ] Integração com CRM (HubSpot, Salesforce)
- [ ] API pública com documentação OpenAPI
- [ ] Webhooks para eventos
- [ ] Analytics dashboard

### Versão 3.0
- [ ] Multi-tenancy
- [ ] White-label
- [ ] Custom experts por cliente
- [ ] Mobile app (React Native)

---

## Métricas de Qualidade

### Personas

| Métrica | Modo Quick | Modo Strategic |
|---------|------------|----------------|
| **Especificidade** | 6/10 | 10/10 |
| **Fontes Reais** | 0 | 10-20 URLs |
| **Comunidades** | 0 | 5-10 |
| **Pain Points** | Genéricos | Quantificados |
| **Confidence** | Medium | High |

### Experts (Auto-Clone)

| Métrica | Score |
|---------|-------|
| **Fidelidade EXTRACT** | 20/20 |
| **Autenticidade** | 9/10 |
| **Utilidade** | 9/10 |
| **Consistência** | 10/10 |

### Conselho

| Métrica | Valor |
|---------|-------|
| **Consensus Quality** | 9/10 |
| **Action Plan Utility** | 9/10 |
| **Response Time** | ~60s |
| **User Satisfaction** | Alta |

---

## Custos Operacionais

### Por Feature (estimado)

| Feature | Cost por Uso |
|---------|--------------|
| Chat 1-on-1 | ~$0.02 |
| Persona Quick | ~$0.02 |
| Persona Strategic | ~$0.20 |
| Enhance Description | ~$0.01 |
| Council (3 experts) | ~$0.20 |
| Auto-Clone | ~$0.40 |

### Otimizações de Custo

- ✅ Cache de 24h em pesquisas
- ✅ Fallback models (Perplexity)
- ✅ Rate limiting
- ✅ Modo quick gratuito disponível

---

## Próximas Features Planejadas

### Curto Prazo (1-2 semanas)
1. Exportação de personas em PDF
2. Histórico de análises do conselho
3. Templates de problemas comuns
4. Busca avançada de experts

### Médio Prazo (1-2 meses)
1. Múltiplos idiomas (EN, ES)
2. Voice input (Speech-to-Text)
3. Análise de concorrentes
4. Market research integrado

### Longo Prazo (3-6 meses)
1. Custom experts por usuário
2. API pública
3. Integrações (Slack, Teams)
4. Mobile app

---

## Referências

- [Architecture](ARCHITECTURE.md) - Arquitetura do sistema
- [API Reference](API_REFERENCE.md) - Documentação da API
- [User Guide](USER_GUIDE.md) - Guia do usuário
- [Changelog](CHANGELOG.md) - Histórico de versões

---

**Mantido por:** Time AdvisorIA Elite  
**Última revisão:** 3 de Novembro de 2025

