# Histórico de Versões - AdvisorIA Elite

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [2.0.0] - 2025-11-03

### Crítico - Correções de Bugs

#### Modo Estratégico Completamente Refatorado
**Problema:** Modo "estratégico" era idêntico ao modo "quick"  
**Solução:** Implementação real com 4 fases de pesquisa profunda

**Mudanças:**
- Fase 1: Descoberta de Comunidades (Perplexity Call #1)
- Fase 2: Pain Points Quantificados (Perplexity Call #2)
- Fase 3: Comportamentos e Decisões (Perplexity Call #3)
- Fase 4: Síntese com Claude (Claude Call)

**Arquivos:**
- `python_backend/reddit_research.py` - Função `research_strategic()` reescrita

**Impacto:**
- Qualidade: 2/10 → 10/10
- Fontes reais: 0 → 10-20 URLs
- Comunidades: 0 → 5-10 específicas
- Tempo: ~20s → ~80s (mas vale a pena!)

**Referência:** [MODO_ESTRATEGICO_REFATORADO.md](../MODO_ESTRATEGICO_REFATORADO.md)

---

#### Feature "Melhorar Descrição com IA" - Erro 500 Corrigido
**Problema:** Erro 500 ao clicar "Melhorar com IA"  
**Causa:** Cliente Anthropic não instanciado

**Solução:**
- Instanciação correta do cliente Anthropic
- Prompt expandido para sugerir indústria + contexto
- UI atualizada para mostrar 3 sugestões

**Arquivos:**
- `python_backend/main.py` - Endpoint `/api/personas/enhance-description`
- `client/src/pages/Personas.tsx` - UI e estados

**Impacto:**
- Feature 100% funcional
- Preenche 3 campos automaticamente (descrição + indústria + contexto)
- Melhora conversão de criação de personas

**Referência:** [CORRECAO_ENHANCE_IA.md](../CORRECAO_ENHANCE_IA.md)

---

#### Timeout de Requisições Ajustado
**Problema:** Timeout de 30s muito curto para modo estratégico  
**Solução:** Aumentado para 90s (padrão) e 120s (personas)

**Mudanças:**
- `client/src/lib/queryClient.ts` - DEFAULT_TIMEOUT_MS: 30s → 90s
- `client/src/pages/Personas.tsx` - Timeout específico: 120s

**Impacto:**
- Modo estratégico funciona sem timeout
- Modo quick continua rápido
- Margem de segurança adequada

**Referência:** [TIMEOUT_AJUSTADO.md](../TIMEOUT_AJUSTADO.md)

---

#### Bug do Conselho Sumindo - Corrigido
**Problema:** Especialistas aparecem mas resultados somem  
**Causa:** Lógica invertida no estado `isStreaming`

**Solução:**
```typescript
// Antes (bugado)
isStreaming={useStreaming && (streamState.isStreaming || !streamState.finalAnalysis)}

// Depois (correto)
isStreaming={isAnalyzing}
```

**Arquivos:**
- `client/src/pages/TestCouncil.tsx` - Linha 632-635

**Impacto:**
- Resultados permanecem visíveis após análise
- Funciona em todos os modos (background, streaming, traditional)

**Referência:** [CORRECAO_CONSELHO_SUMINDO.md](../CORRECAO_CONSELHO_SUMINDO.md)

---

### Adicionado

- Documentação completa estruturada em `docs/`
- Índice mestre de navegação (`DOCUMENTATION_INDEX.md`)
- Este CHANGELOG

---

## [1.5.0] - 2025-11-01/02

### Adicionado

#### Sistema de Personas
- Persona Builder com modo Quick (1-2min) e Strategic (5-10min)
- Framework JTBD (Jobs to Be Done)
- Framework BAG (Behaviors, Aspirations, Goals)
- Integração com Perplexity API para pesquisa profunda
- Export de personas em JSON

**Arquivos principais:**
- `client/src/pages/Personas.tsx`
- `python_backend/reddit_research.py`
- `python_backend/models_persona.py`

**Referências:**
- [PERSONA_BUILDER.md](../PERSONA_BUILDER.md)
- [PERSONAS_API.md](../PERSONAS_API.md)
- [FRAMEWORK_PERSONA_PROFUNDA.md](../FRAMEWORK_PERSONA_PROFUNDA.md)

---

#### Auto-Clone de Experts (Framework EXTRACT)
- Criação automática de experts a partir de nomes
- Framework EXTRACT de 20 pontos
- Pesquisa biográfica + síntese cognitiva
- System prompts de alta fidelidade
- Integração com página Create

**Componentes:**
- 20 dimensões de personalidade
- Story banks e callbacks icônicos
- Axiomas e terminologia própria
- Limitações e áreas de expertise

**Arquivos:**
- `python_backend/main.py` - Endpoint `/api/experts/auto-clone`
- `client/src/pages/Create.tsx`

**Referências:**
- [SISTEMA_CLONES_PYTHON_AUTOMATICO.md](../SISTEMA_CLONES_PYTHON_AUTOMATICO.md)
- [ENTREGA_FINAL_CLONES_AUTOMATICOS.md](../ENTREGA_FINAL_CLONES_AUTOMATICOS.md)
- [python_backend/DEEP_CLONE_README.md](../python_backend/DEEP_CLONE_README.md)

---

#### Persistência de Estado do Conselho
- Estado persiste ao navegar entre abas
- Recuperação automática após reload
- Background polling que funciona em tabs inativas
- Indicador visual de estado restaurado

**Hooks:**
- `usePersistedState` - Persistência com localStorage
- `useCouncilBackground` - Polling em background
- `useCouncilStream` - SSE streaming

**Arquivos:**
- `client/src/hooks/usePersistedState.ts`
- `client/src/hooks/useCouncilBackground.ts`
- `client/src/pages/TestCouncil.tsx`

**Referências:**
- [ENTREGA_PERSISTENCIA_ESTADO_COMPLETA.md](../ENTREGA_PERSISTENCIA_ESTADO_COMPLETA.md)
- [SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md](../SOLUCAO_DEFINITIVA_BACKGROUND_POLLING.md)

---

### Melhorado

#### UI/UX Completo
- Design system atualizado
- Animações com Framer Motion
- Feedback visual aprimorado
- Responsividade mobile
- Dark mode melhorado

**Referências:**
- [UI_UX_COMPLETO.md](../UI_UX_COMPLETO.md)
- [MELHORIAS_UI_UX.md](../MELHORIAS_UI_UX.md)

---

## [1.0.0] - 2025-10

### Adicionado - MVP Inicial

#### Sistema de Experts (22 Clones)
22 clones cognitivos de lendas do marketing:
- Philip Kotler, Seth Godin, Gary Vaynerchuk
- Neil Patel, Ann Handley, David Ogilvy
- Al Ries & Jack Trout, Dan Kennedy
- E mais 14 especialistas

**Features:**
- Chat 1-on-1 com cada expert
- System prompts de alta qualidade
- Personalidades distintas e autênticas

**Arquivos:**
- `python_backend/clones/registry.py`
- `python_backend/clones/` - 22 arquivos individuais

---

#### Conselho de IA
- Seleção de múltiplos especialistas
- Análise colaborativa de problemas
- Consensus building
- Action plan gerado automaticamente

**Modos:**
- Traditional (mutation)
- SSE Streaming (tempo real)
- Background Polling (funciona em background)

**Arquivos:**
- `python_backend/crew_council.py`
- `client/src/pages/TestCouncil.tsx`
- `client/src/components/council/`

**Referências:**
- [PLANO_CONSELHO_MELHORADO.md](../PLANO_CONSELHO_MELHORADO.md)

---

#### Chat Individual e em Grupo
- Chat 1-on-1 com especialistas
- Conversas do conselho
- Histórico de mensagens
- Streaming de respostas

**Arquivos:**
- `python_backend/main.py` - Endpoints de chat
- `client/src/pages/CouncilChat.tsx`
- `client/src/hooks/useCouncilChat.ts`

---

#### Infraestrutura Base
- Stack: React + TypeScript + Node.js + FastAPI
- Banco: PostgreSQL (Neon)
- APIs: Anthropic Claude, Perplexity
- Deploy: Railway, Replit
- Proxy automático Node → FastAPI

**Arquivos:**
- `server/index.ts` - Node.js server
- `python_backend/main.py` - FastAPI server
- `client/` - React frontend

---

## Convenções de Versionamento

Este projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Mudanças incompatíveis de API
- **MINOR** (0.X.0): Novas funcionalidades (backward compatible)
- **PATCH** (0.0.X): Correções de bugs

### Categorias de Mudanças

- **Adicionado**: Novas funcionalidades
- **Alterado**: Mudanças em funcionalidades existentes
- **Depreciado**: Funcionalidades que serão removidas
- **Removido**: Funcionalidades removidas
- **Corrigido**: Correções de bugs
- **Segurança**: Vulnerabilidades corrigidas

---

## Roadmap Futuro

### Versão 2.1.0 (Planejado)
- [ ] Autenticação de usuários
- [ ] Perfil de negócio
- [ ] Histórico de consultas
- [ ] Favoritos e bookmarks

### Versão 2.2.0 (Planejado)
- [ ] Exportação de relatórios
- [ ] Integração com CRM
- [ ] API pública
- [ ] Webhooks

### Versão 3.0.0 (Futuro)
- [ ] Multi-tenancy
- [ ] White-label
- [ ] Analytics avançado
- [ ] Mobile app

---

**Mantido por:** Time AdvisorIA Elite  
**Última atualização:** 3 de Novembro de 2025

