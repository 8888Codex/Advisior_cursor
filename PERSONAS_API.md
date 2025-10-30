# 📊 API de Personas Modernas - AdvisorIA Elite

## 📋 Visão Geral

A API de Personas Modernas permite criar, gerenciar e visualizar personas baseadas nos frameworks modernos de 2025:

1. **Framework Híbrido: Personas + Jobs to Be Done (JTBD)**
2. **Framework BAG: Behaviors, Aspirations, Goals**
3. **Elementos Quantitativos** (pontos de dor mensuráveis, impacto financeiro)

## 🚀 Endpoints

### 1. Criar Persona Moderna

```
POST /api/personas-modern
```

**Corpo da Requisição:**
```json
{
  "targetDescription": "Descrição do público-alvo",
  "industry": "Indústria ou setor",
  "mode": "quick ou strategic",
  "additionalContext": "Informações adicionais (opcional)",
  "framework": "hybrid"
}
```

**Parâmetros:**
- `targetDescription`: Descrição do público-alvo (ex: "Empreendedor de e-commerce")
- `industry`: Indústria ou setor (ex: "Varejo online")
- `mode`: Modo de pesquisa
  - `quick`: Análise básica (mais rápida)
  - `strategic`: Análise detalhada (mais completa)
- `additionalContext`: Informações adicionais para refinar a pesquisa (opcional)
- `framework`: Tipo de framework a ser usado (hybrid, jtbd, bag)

**Resposta:**
```json
{
  "id": "uuid",
  "userId": "user_id",
  "name": "Nome da Persona",
  "researchMode": "strategic",
  
  "job_statement": "Declaração principal do trabalho a ser feito",
  "situational_contexts": ["Contexto 1", "Contexto 2"],
  
  "demographics": {
    "age": "28-45 anos",
    "location": "Capitais e grandes centros urbanos",
    "occupation": "Empreendedores de e-commerce",
    "education": "Ensino superior completo",
    "income": "R$5.000-15.000 mensais"
  },
  
  "behaviors": {
    "online": ["Comportamento 1", "Comportamento 2"],
    "purchasing": ["Comportamento 1", "Comportamento 2"],
    "decision_making": ["Comportamento 1", "Comportamento 2"]
  },
  
  "aspirations": [
    "Aspiração 1",
    "Aspiração 2"
  ],
  
  "goals": [
    {
      "description": "Descrição do objetivo",
      "timeframe": "short|medium|long",
      "success_metrics": ["Métrica 1", "Métrica 2"],
      "obstacles": ["Obstáculo 1", "Obstáculo 2"]
    }
  ],
  
  "functional_jobs": [
    "Trabalho funcional 1",
    "Trabalho funcional 2"
  ],
  
  "emotional_jobs": [
    "Trabalho emocional 1",
    "Trabalho emocional 2"
  ],
  
  "social_jobs": [
    "Trabalho social 1",
    "Trabalho social 2"
  ],
  
  "pain_points_quantified": [
    {
      "description": "Descrição do ponto de dor",
      "impact": "Impacto mensurável",
      "cost": "Custo financeiro",
      "frequency": "Frequência"
    }
  ],
  
  "values": [
    "Valor 1",
    "Valor 2"
  ],
  
  "research_data": {
    "confidence_level": "high|medium|low",
    "confidence_metadata": {
      "job_statement": "high|medium|low",
      "demographics": "high|medium|low",
      "goals": "high|medium|low",
      "pain_points_quantified": "high|medium|low",
      "behaviors": "high|medium|low"
    },
    "validated_at": "2025-10-27T12:00:00Z",
    "generated_at": "2025-10-27T12:00:00Z"
  },
  
  "created_at": "2025-10-27T12:00:00Z",
  "updated_at": "2025-10-27T12:00:00Z"
}
```

### 2. Listar Personas Modernas

```
GET /api/personas-modern
```

**Resposta:**
```json
[
  {
    "id": "uuid",
    "userId": "user_id",
    "name": "Nome da Persona",
    ...
  },
  {
    "id": "uuid",
    "userId": "user_id",
    "name": "Nome da Persona",
    ...
  }
]
```

### 3. Obter Persona Moderna por ID

```
GET /api/personas-modern/{persona_id}
```

**Resposta:**
```json
{
  "id": "uuid",
  "userId": "user_id",
  "name": "Nome da Persona",
  ...
}
```

### 4. Excluir Persona Moderna

```
DELETE /api/personas-modern/{persona_id}
```

**Resposta:**
```
204 No Content
```

## 🧠 Frameworks Implementados

### Framework Híbrido: Personas + JTBD

O framework híbrido combina o melhor dos dois mundos:

1. **Job Statement**: Declaração clara do trabalho principal que o usuário precisa realizar
2. **Situational Contexts**: Gatilhos que ativam a necessidade do trabalho
3. **Functional Jobs**: Tarefas práticas que o usuário precisa realizar
4. **Emotional Jobs**: Como o usuário quer se sentir
5. **Social Jobs**: Como o usuário quer ser percebido pelos outros

### Framework BAG: Behaviors, Aspirations, Goals

O framework BAG enfatiza três dimensões principais:

1. **Behaviors**: O que os usuários fazem (comportamentos observáveis)
2. **Aspirations**: Sonhos e desejos de longo prazo
3. **Goals**: Metas específicas de curto prazo com métricas de sucesso

### Elementos Quantitativos

As personas modernas incluem elementos quantitativos para torná-las mais acionáveis:

1. **Pain Points Quantified**: Pontos de dor com impacto mensurável
   - Impacto: "10 horas semanais perdidas"
   - Custo: "R$30K anualmente"
   - Frequência: "diariamente"

2. **Decision Criteria**: Critérios de decisão com pesos relativos
   - Preço: 8/10
   - Facilidade de uso: 6/10
   - Suporte: 9/10

## 🔍 Sistema de Validação e Confiança

Cada persona gerada passa por um sistema de validação que:

1. **Valida campos obrigatórios**: Verifica se todos os campos essenciais estão presentes
2. **Verifica consistência interna**: Garante que os dados são consistentes entre si
3. **Classifica confiança**: Atribui níveis de confiança (alto, médio, baixo) para cada seção
4. **Calcula confiança geral**: Determina a qualidade geral da persona

Os níveis de confiança ajudam a identificar quais aspectos da persona podem precisar de mais refinamento.

## 🗄️ Armazenamento

O sistema suporta dois modos de armazenamento:

1. **In-Memory**: Armazenamento em memória com cache TTL (padrão)
2. **PostgreSQL**: Armazenamento em banco de dados quando DATABASE_URL está configurado

O sistema detecta automaticamente a disponibilidade do PostgreSQL e alterna entre os modos.

## 🔌 Integração com Frontend

Para integrar com o frontend, você pode usar o seguinte código:

```typescript
// Criar persona
async function createPersona(data) {
  const response = await fetch('/api/personas-modern', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

// Listar personas
async function getPersonas() {
  const response = await fetch('/api/personas-modern');
  return response.json();
}

// Obter persona por ID
async function getPersona(id) {
  const response = await fetch(`/api/personas-modern/${id}`);
  return response.json();
}

// Excluir persona
async function deletePersona(id) {
  await fetch(`/api/personas-modern/${id}`, {
    method: 'DELETE',
  });
}
```

## 📈 Próximos Passos

1. **Interface de Usuário**: Desenvolver componentes para criação e visualização de personas
2. **Feedback do Usuário**: Adicionar sistema para coletar feedback sobre a precisão das personas
3. **Exportação**: Implementar recursos para exportar personas em diferentes formatos
4. **Integração com Ferramentas**: Conectar com ferramentas de design e marketing

## 🔧 Considerações Técnicas

- **Rate Limiting**: 5 personas por hora para evitar custos excessivos de API
- **Cache**: Resultados em cache por 1 hora para melhorar performance
- **Validação**: Sistema de validação para garantir qualidade dos dados
- **Armazenamento Híbrido**: Suporte a in-memory e PostgreSQL
