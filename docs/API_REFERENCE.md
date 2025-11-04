# Referência da API - AdvisorIA Elite

**Versão:** 2.0.0  
**Base URL:** `http://localhost:5501` (desenvolvimento)  
**Última Atualização:** 3 de Novembro de 2025

---

## Índice

1. [Autenticação](#autenticacao)
2. [Experts API](#experts-api)
3. [Personas API](#personas-api)
4. [Council API](#council-api)
5. [Conversations API](#conversations-api)
6. [Models e Schemas](#models-e-schemas)
7. [Rate Limits](#rate-limits)
8. [Error Handling](#error-handling)

---

## Autenticação

**Status Atual:** Sem autenticação (MVP)

**Futuro (v2.1):**
- Bearer token authentication
- Session-based auth
- OAuth 2.0

**Usuário Padrão:**
```json
{
  "userId": "default_user"
}
```

---

## Experts API

### GET /api/experts

Lista todos os especialistas disponíveis.

**Query Parameters:**
- `category` (optional): Filtrar por categoria

**Response:**
```json
[
  {
    "id": "philip-kotler",
    "name": "Philip Kotler",
    "title": "Pai do Marketing Moderno",
    "expertise": ["Estratégia", "Segmentação", "Posicionamento"],
    "bio": "Philip Kotler é reconhecido como...",
    "category": "estrategia",
    "systemPrompt": "Você é Philip Kotler...",
    "avatar": null
  }
]
```

**Status Codes:**
- `200 OK` - Sucesso
- `500 Internal Server Error` - Erro no servidor

---

### GET /api/experts/:id

Busca um especialista específico.

**Parameters:**
- `id` (path): ID do especialista

**Response:**
```json
{
  "id": "philip-kotler",
  "name": "Philip Kotler",
  "title": "Pai do Marketing Moderno",
  "expertise": ["Estratégia", "Segmentação"],
  "bio": "Philip Kotler...",
  "category": "estrategia",
  "systemPrompt": "Você é Philip Kotler...",
  "avatar": null
}
```

**Status Codes:**
- `200 OK` - Expert encontrado
- `404 Not Found` - Expert não existe

---

### POST /api/experts

Cria um novo especialista (manual).

**Rate Limit:** 10/hora

**Request Body:**
```json
{
  "name": "Nome do Expert",
  "title": "Título/Especialidade",
  "expertise": ["área1", "área2"],
  "bio": "Biografia completa...",
  "systemPrompt": "System prompt para Claude...",
  "category": "estrategia"
}
```

**Response:**
```json
{
  "id": "generated-id",
  "name": "Nome do Expert",
  "title": "Título/Especialidade",
  ...
}
```

**Status Codes:**
- `200 OK` - Expert criado
- `400 Bad Request` - Dados inválidos
- `429 Too Many Requests` - Rate limit excedido
- `500 Internal Server Error` - Erro no servidor

---

### POST /api/experts/auto-clone

Auto-clona um especialista usando Framework EXTRACT.

**Rate Limit:** 5/hora  
**Timeout:** 180 segundos

**Request Body:**
```json
{
  "targetName": "Steve Jobs",
  "context": "Fundador da Apple, foco em design" // opcional
}
```

**Response:**
```json
{
  "name": "Steve Jobs",
  "title": "Co-fundador da Apple, Visionário em Design e Tecnologia",
  "expertise": ["Design de Produtos", "Inovação", "Storytelling"],
  "bio": "Steve Jobs foi...",
  "systemPrompt": "# FRAMEWORK EXTRACT COMPLETO\n\n## EXPERIENCES...",
  "category": "inovacao"
}
```

**Status Codes:**
- `200 OK` - Clone criado (NÃO salvo ainda)
- `400 Bad Request` - targetName obrigatório
- `429 Too Many Requests` - Rate limit
- `500 Internal Server Error` - Erro na clonagem

**Tempo:** ~120-180 segundos

---

### POST /api/experts/:id/chat

Chat 1-on-1 com um especialista.

**Rate Limit:** 60/hora

**Request Body:**
```json
{
  "message": "Como reduzir meu CAC?"
}
```

**Response:**
```json
{
  "role": "assistant",
  "content": "Resposta do especialista...",
  "expertId": "philip-kotler",
  "expertName": "Philip Kotler"
}
```

**Status Codes:**
- `200 OK` - Resposta gerada
- `404 Not Found` - Expert não existe
- `429 Too Many Requests` - Rate limit
- `500 Internal Server Error` - Erro na geração

**Tempo:** ~3-5 segundos

---

### POST /api/experts/test-chat

Testa um expert não salvo (usado na página Create).

**Request Body:**
```json
{
  "systemPrompt": "System prompt do expert...",
  "message": "Sua pergunta",
  "history": [
    {"role": "user", "content": "pergunta anterior"},
    {"role": "assistant", "content": "resposta anterior"}
  ]
}
```

**Response:**
```json
{
  "response": "Resposta do expert..."
}
```

**Tempo:** ~3-5 segundos

---

## Personas API

### GET /api/personas

Lista todas as personas do usuário.

**Response:**
```json
[
  {
    "id": "uuid",
    "userId": "default_user",
    "name": "Persona: CMO de SaaS B2B",
    "researchMode": "strategic",
    "job_statement": "Acelerar aquisição de clientes...",
    "functional_jobs": [...],
    "emotional_jobs": [...],
    "social_jobs": [...],
    "pain_points_quantified": [...],
    "demographics": {...},
    "communities": [...],
    "research_data": {
      "sources": [...],
      "confidence_level": "high"
    },
    "created_at": "2025-11-03T19:47:21.947922",
    "updated_at": "2025-11-03T19:47:21.947922"
  }
]
```

---

### POST /api/personas

Cria uma nova persona.

**Rate Limit:** 10/hora  
**Timeout:** 120 segundos

**Request Body:**
```json
{
  "mode": "strategic",  // "quick" ou "strategic"
  "targetDescription": "CMO de SaaS B2B com equipe de 8 pessoas",
  "industry": "SaaS",  // opcional
  "additionalContext": "ARR $2M, ciclo 60 dias"  // opcional
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Persona: CMO de SaaS B2B...",
  "researchMode": "strategic",
  "job_statement": "...",
  "functional_jobs": [...],
  "emotional_jobs": [...],
  "social_jobs": [...],
  "behaviors": {
    "online": [...],
    "purchasing": [...],
    "content_consumption": [...]
  },
  "aspirations": [...],
  "goals": [...],
  "pain_points_quantified": [
    {
      "description": "CAC de R$2.5k vs target R$1.2k",
      "impact": "Margem de 20% vs target 40%",
      "cost": "R$52k/mês de oportunidade perdida",
      "frequency": "Mensal"
    }
  ],
  "decision_criteria": {
    "must_have": [...],
    "nice_to_have": [...],
    "deal_breakers": [...]
  },
  "demographics": {...},
  "values": [...],
  "touchpoints": [...],
  "content_preferences": {...},
  "communities": [...],
  "research_data": {
    "sources": ["url1", "url2", ...],
    "confidence_level": "high",
    "perplexity_calls": 3,
    "research_depth": "strategic"
  }
}
```

**Tempo:**
- Modo Quick: ~10 segundos
- Modo Strategic: ~80 segundos

---

### POST /api/personas/enhance-description

Melhora descrição vaga com IA (Claude).

**Rate Limit:** 30/hora  
**Timeout:** 90 segundos

**Request Body:**
```json
{
  "description": "profissional b2b com time",
  "industry": "",  // opcional
  "context": ""    // opcional
}
```

**Response:**
```json
{
  "original": "profissional b2b com time",
  "enhanced": "CMO, Diretor Comercial ou Head de Marketing de empresas B2B...",
  "suggested_industry": "SaaS B2B / Tecnologia",
  "suggested_context": "Empresas em fase de scale-up...",
  "improvements": {
    "added_specificity": true,
    "character_count": {
      "before": 25,
      "after": 522
    },
    "estimated_quality_boost": "high"
  },
  "confidence": 0.85
}
```

**Tempo:** ~3-5 segundos

---

### DELETE /api/personas/:id

Deleta uma persona.

**Parameters:**
- `id` (path): ID da persona

**Response:**
```json
{
  "success": true
}
```

---

## Council API

### POST /api/council/analyze

Análise síncrona do conselho (modo traditional).

**Rate Limit:** 10/hora  
**Timeout:** 180 segundos

**Request Body:**
```json
{
  "problem": "Seu problema detalhado aqui...",
  "expertIds": ["philip-kotler", "seth-godin"],
  "personaId": "persona-uuid"  // OBRIGATÓRIO
}
```

**Response:**
```json
{
  "id": "analysis-uuid",
  "problem": "Seu problema...",
  "personaId": "persona-uuid",
  "contributions": [
    {
      "expertId": "philip-kotler",
      "expertName": "Philip Kotler",
      "analysis": "Análise completa...",
      "keyInsights": ["insight1", "insight2"],
      "recommendations": ["rec1", "rec2"]
    }
  ],
  "consensus": "Consenso entre os especialistas...",
  "actionPlan": {
    "phases": [...],
    "totalDuration": "90 dias",
    "successMetrics": [...]
  }
}
```

**Tempo:** ~60-90 segundos (depende do número de experts)

---

### POST /api/council/analyze-async

Análise assíncrona (background mode).

**Rate Limit:** 10/hora

**Request Body:**
```json
{
  "problem": "Seu problema...",
  "expertIds": ["philip-kotler", "seth-godin", "gary-vaynerchuk"],
  "personaId": "persona-uuid"
}
```

**Response (Imediata):**
```json
{
  "id": "task-uuid",
  "status": "processing",
  "created_at": "2025-11-03T19:00:00Z"
}
```

**Tempo:** < 1 segundo (retorna task ID)

---

### GET /api/council/tasks/:taskId

Verifica status de uma task em background.

**Parameters:**
- `taskId` (path): ID da task

**Response (Processing):**
```json
{
  "id": "task-uuid",
  "status": "processing",
  "progress": 0.45,
  "message": "Analyzing with expert 2/3...",
  "expert_statuses": [
    {
      "expertId": "philip-kotler",
      "status": "completed",
      "progress": 100
    },
    {
      "expertId": "seth-godin",
      "status": "analyzing",
      "progress": 50
    },
    {
      "expertId": "gary-vaynerchuk",
      "status": "waiting",
      "progress": 0
    }
  ]
}
```

**Response (Completed):**
```json
{
  "id": "task-uuid",
  "status": "completed",
  "progress": 1.0,
  "result": {
    "id": "analysis-uuid",
    "problem": "...",
    "contributions": [...],
    "consensus": "...",
    "actionPlan": {...}
  }
}
```

**Response (Error):**
```json
{
  "id": "task-uuid",
  "status": "error",
  "error": "Error message..."
}
```

**Polling:** Recomendado a cada 3 segundos

---

### POST /api/council/analyze-stream

Análise com SSE streaming (tempo real).

**Rate Limit:** 10/hora

**Request:** Standard POST
**Response:** SSE stream

**Events:**
```
event: analysis_started
data: {"expertCount": 3, "experts": [...]}

event: expert_started
data: {"expertId": "...", "expertName": "...", "index": 1}

event: expert_progress
data: {"expertId": "...", "progress": 0.5, "message": "..."}

event: expert_completed
data: {"expertId": "...", "contribution": {...}}

event: consensus_started
data: {"message": "Building consensus..."}

event: consensus_completed
data: {"consensus": "..."}

event: action_plan_completed
data: {"actionPlan": {...}}

event: analysis_completed
data: {"analysis": {...}}

event: error
data: {"message": "Error message..."}
```

**Tempo:** ~60-90 segundos (streaming em tempo real)

---

### POST /api/council/recommend-experts

Recomenda especialistas para um problema (usando IA).

**Request Body:**
```json
{
  "problem": "Preciso reduzir meu CAC de R$800..."
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "expertId": "philip-kotler",
      "expertName": "Philip Kotler",
      "relevanceScore": 5,
      "justification": "Expert em estratégia de segmentação..."
    },
    {
      "expertId": "alex-hormozi",
      "expertName": "Alex Hormozi",
      "relevanceScore": 4,
      "justification": "Especialista em otimização de ofertas..."
    }
  ]
}
```

**Tempo:** ~5-8 segundos

---

## Personas API

### GET /api/personas

Lista todas as personas do usuário.

**Response:** Array de personas (ver schema)

---

### POST /api/personas

Cria uma nova persona.

**Rate Limit:** 10/hora  
**Timeout:** 120 segundos

**Request Body:**
```json
{
  "mode": "strategic",
  "targetDescription": "CMO de SaaS B2B com equipe de 8 pessoas e investe R$30k/mês",
  "industry": "SaaS B2B",
  "additionalContext": "ARR $2M, ciclo de vendas 60 dias, ticket R$5k/mês"
}
```

**Response:** PersonaModern object (ver schema)

**Tempo:**
- Quick: ~10s
- Strategic: ~80s

---

### POST /api/personas/enhance-description

Melhora descrição vaga com IA.

**Rate Limit:** 30/hora

**Request Body:**
```json
{
  "description": "profissional b2b com time comercial",
  "industry": "",
  "context": ""
}
```

**Response:**
```json
{
  "original": "profissional b2b com time comercial",
  "enhanced": "CMO ou Diretor Comercial de empresas B2B (SaaS, Tecnologia ou Serviços Corporativos) com faturamento R$500k-5M/ano, possui equipe comercial/marketing de 3-10 pessoas...",
  "suggested_industry": "SaaS B2B / Tecnologia",
  "suggested_context": "Ciclo de vendas médio/longo (30-90 dias) com processo consultivo",
  "improvements": {
    "added_specificity": true,
    "character_count": {"before": 32, "after": 456},
    "estimated_quality_boost": "high"
  },
  "confidence": 0.85
}
```

**Tempo:** ~3-5 segundos

---

### DELETE /api/personas/:id

Deleta uma persona.

**Response:**
```json
{
  "success": true
}
```

---

## Conversations API

### POST /api/council/conversations

Cria uma conversa em grupo com o conselho.

**Request Body:**
```json
{
  "problem": "Problema que foi analisado...",
  "personaId": "persona-uuid",
  "expertIds": ["philip-kotler", "seth-godin"],
  "analysisId": "analysis-uuid"  // opcional
}
```

**Response:**
```json
{
  "id": "conversation-uuid",
  "problem": "...",
  "personaId": "persona-uuid",
  "expertIds": [...],
  "created_at": "2025-11-03T20:00:00Z"
}
```

---

### GET /api/council/conversations/:id

Busca uma conversa específica.

**Response:**
```json
{
  "id": "conversation-uuid",
  "problem": "...",
  "personaId": "persona-uuid",
  "expertIds": [...],
  "created_at": "..."
}
```

---

### GET /api/council/conversations/:id/messages

Lista mensagens de uma conversa.

**Response:**
```json
[
  {
    "id": "message-uuid",
    "conversationId": "conversation-uuid",
    "role": "user",
    "content": "Minha pergunta...",
    "timestamp": "2025-11-03T20:05:00Z"
  },
  {
    "id": "message-uuid-2",
    "conversationId": "conversation-uuid",
    "role": "assistant",
    "content": "Resposta do conselho...",
    "expertContributions": {
      "philip-kotler": "Contribuição do Kotler...",
      "seth-godin": "Contribuição do Godin..."
    },
    "timestamp": "2025-11-03T20:05:15Z"
  }
]
```

---

### POST /api/council/conversations/:id/messages

Envia mensagem em conversa de grupo.

**Request Body:**
```json
{
  "message": "Minha pergunta de follow-up..."
}
```

**Response:**
```json
{
  "id": "message-uuid",
  "role": "assistant",
  "content": "Resposta colaborativa...",
  "expertContributions": {...}
}
```

**Tempo:** ~10-20 segundos (depende do número de experts)

---

## Models e Schemas

### Expert
```typescript
interface Expert {
  id: string;
  name: string;
  title: string;
  expertise: string[];
  bio: string;
  systemPrompt: string;
  category?: string;
  avatar?: string;
}
```

---

### PersonaModern
```typescript
interface PersonaModern {
  id: string;
  userId: string;
  name: string;
  researchMode: "quick" | "strategic";
  
  // JTBD Framework
  job_statement: string;
  functional_jobs: string[];
  emotional_jobs: string[];
  social_jobs: string[];
  situational_contexts: string[];
  
  // BAG Framework
  behaviors: {
    online: string[];
    purchasing: string[];
    content_consumption: string[];
  };
  aspirations: string[];
  goals: string[];
  
  // Quantified Data
  pain_points_quantified: Array<{
    description: string;
    impact: string;
    cost: string;
    frequency: string;
  }>;
  
  // Decision Making
  decision_criteria: {
    must_have?: string[];
    nice_to_have?: string[];
    deal_breakers?: string[];
  };
  
  // Demographics
  demographics: {
    age: string;
    location: string;
    occupation: string;
    education: string;
    income: string;
  };
  
  // Values and Preferences
  values: string[];
  touchpoints: Array<{
    channel: string;
    stage: string;
    importance: number;
    preferred_content: string[];
  }>;
  content_preferences: {
    formats: string[];
    topics: string[];
    channels: string[];
    influencers: string[];
  };
  
  // Research Metadata
  communities: string[];
  research_data: {
    sources: string[];
    confidence_level: "low" | "medium" | "high";
    timestamp: string;
    perplexity_calls?: number;
    research_depth?: string;
  };
  
  created_at: string;
  updated_at: string;
}
```

---

### CouncilAnalysis
```typescript
interface CouncilAnalysis {
  id: string;
  problem: string;
  personaId: string;
  
  contributions: Array<{
    expertId: string;
    expertName: string;
    analysis: string;
    keyInsights: string[];
    recommendations: string[];
  }>;
  
  consensus: string;
  
  actionPlan: {
    phases: Array<{
      phaseNumber: number;
      name: string;
      duration: string;
      objectives: string[];
      actions: Array<{
        id: string;
        title: string;
        description: string;
        responsible: string;
        priority: "alta" | "média" | "baixa";
        estimatedTime: string;
        tools: string[];
        steps: string[];
      }>;
      dependencies: string[];
      deliverables: string[];
    }>;
    totalDuration: string;
    estimatedBudget?: string;
    successMetrics: string[];
  };
}
```

---

## Rate Limits

### Por Endpoint

| Endpoint | Limite | Window |
|----------|--------|--------|
| POST /api/experts/auto-clone | 5 | 1 hora |
| POST /api/personas | 10 | 1 hora |
| POST /api/personas/enhance | 30 | 1 hora |
| POST /api/council/analyze* | 10 | 1 hora |
| POST /api/experts/chat | 60 | 1 hora |
| POST /api/experts | 10 | 1 hora |
| GET * | Sem limite | - |

### Headers de Rate Limit

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1699045200
```

### Response quando excedido:

```json
{
  "detail": "Rate limit exceeded: 10 per hour"
}
```

**Status Code:** `429 Too Many Requests`

---

## Error Handling

### Status Codes Padrão

| Code | Significado | Ação |
|------|-------------|------|
| 200 | OK | Sucesso |
| 400 | Bad Request | Corrigir dados enviados |
| 401 | Unauthorized | Autenticar (futuro) |
| 404 | Not Found | Recurso não existe |
| 429 | Too Many Requests | Aguardar e tentar novamente |
| 500 | Internal Server Error | Tentar novamente ou reportar |
| 503 | Service Unavailable | Aguardar e tentar novamente |

### Estrutura de Erro

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Erros Comuns

#### Timeout
```json
{
  "detail": "Requisição expirou após 30000ms. Tente novamente."
}
```
**Solução:** Operação demorada, tente novamente

#### Persona Obrigatória
```json
{
  "detail": "personaId é obrigatória para análise do conselho"
}
```
**Solução:** Crie uma persona primeiro

#### Rate Limit
```json
{
  "detail": "Rate limit exceeded: 10 per hour"
}
```
**Solução:** Aguarde 1 hora ou use outro endpoint

#### API Key Missing
```json
{
  "detail": "ANTHROPIC_API_KEY environment variable not set"
}
```
**Solução:** Configure API key no `.env`

---

## Webhooks (Futuro - v2.2)

### POST /api/webhooks/council-completed

**Payload:**
```json
{
  "event": "council.analysis.completed",
  "data": {
    "analysisId": "uuid",
    "userId": "user-id",
    "timestamp": "2025-11-03T20:00:00Z"
  }
}
```

---

## Versionamento da API

**Versão Atual:** v1 (implícita em todas as rotas)

**Futuro:** Versões explícitas
```
/api/v1/experts
/api/v2/experts (breaking changes)
```

---

## Limites Técnicos

### Payload Size
- Request body: 10 MB max
- File uploads: Não suportado ainda

### Timeouts
- Default: 90 segundos
- Personas: 120 segundos
- Auto-clone: 180 segundos
- Council: 180 segundos

### Concorrência
- Conexões simultâneas: 100
- Background tasks: 50 simultâneas

---

## Referências

### Documentação Relacionada
- [Architecture](ARCHITECTURE.md) - Estrutura do sistema
- [Development Guide](DEVELOPMENT.md) - Para desenvolvedores
- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) - Solução de problemas

### APIs Externas
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Perplexity API Docs](https://docs.perplexity.ai/)

---

**Mantido por:** Time AdvisorIA Elite  
**Última revisão:** 3 de Novembro de 2025

