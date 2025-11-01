# 📋 PLANO: Conselho Melhorado e Chat Interativo com Especialistas

## 🎯 Objetivos

1. **Validar Persona**: Garantir que usuário tenha persona criada antes de usar conselho
2. **Plano de Ação Completo**: Adicionar plano estruturado e acionável no resultado do conselho
3. **Chat Interativo**: Criar chat onde múltiplos especialistas trabalham juntos em tempo real
4. **Personalização por Persona**: Usar dados da persona para tornar recomendações mais práticas e assertivas

---

## 📐 Arquitetura da Solução

### **Fase 1: Validação de Persona no Conselho**

**Backend (`python_backend/main.py`)**
- Modificar endpoint `/api/council/analyze` para exigir `personaId`
- Buscar persona do usuário e validar se existe
- Passar dados da persona para o `CouncilOrchestrator`

**Frontend (`client/src/pages/TestCouncil.tsx`)**
- Adicionar seleção de persona antes de iniciar análise
- Mostrar aviso se não houver personas criadas
- Redirect para página de Personas se necessário

**Validação:**
```python
# No endpoint /api/council/analyze
if not data.personaId:
    raise HTTPException(status_code=400, detail="Persona ID é obrigatório")

persona = await storage.get_persona(data.personaId)
if not persona:
    raise HTTPException(status_code=404, detail="Persona não encontrada")

# Passar persona para análise
analysis = await council_orchestrator.analyze_problem(
    user_id=user_id,
    problem=data.problem,
    experts=experts,
    profile=profile,
    persona=persona  # NOVO
)
```

---

### **Fase 2: Plano de Ação Completo**

**Estrutura do Plano de Ação:**
```typescript
interface ActionPlan {
  phases: Phase[];
  totalDuration: string; // "8-12 semanas"
  estimatedBudget?: string;
  successMetrics: string[];
}

interface Phase {
  phaseNumber: number;
  name: string;
  duration: string; // "2 semanas"
  objectives: string[];
  actions: Action[];
  dependencies?: string[]; // IDs de outras fases
  deliverables: string[];
}

interface Action {
  id: string;
  title: string;
  description: string;
  responsible: string; // "Equipe de Marketing", "CEO", etc.
  priority: "alta" | "média" | "baixa";
  estimatedTime: string; // "4 horas"
  tools: string[]; // ["Google Analytics", "Figma"]
  steps: string[]; // Passos detalhados
}
```

**Backend (`python_backend/crew_council.py`):**
- Adicionar método `_generate_action_plan()` que usa Claude para criar plano estruturado
- Usar persona, perfil de negócio e consenso para gerar plano contextualizado
- Retornar plano como parte do `CouncilAnalysis`

**Modelo Atualizado:**
```python
class CouncilAnalysis(BaseModel):
    # ... campos existentes
    actionPlan: Optional[ActionPlan] = None  # NOVO
```

**Frontend (`client/src/components/council/CouncilResultDisplay.tsx`):**
- Adicionar seção "Plano de Ação" após o consenso
- Visualizar fases, ações e dependências
- Opção de exportar plano (PDF, JSON)

---

### **Fase 3: Chat Interativo com Especialistas**

**Conceito:** Chat onde usuário conversa com múltiplos especialistas simultaneamente. Cada especialista pode:
- Responder individualmente
- Reagir às respostas dos outros
- Colaborar em soluções
- Debater pontos divergentes

**Backend:**

**Novo Modelo:**
```python
class CouncilConversation(BaseModel):
    id: str
    userId: str
    personaId: str
    problem: str
    expertIds: List[str]
    createdAt: datetime

class CouncilMessage(BaseModel):
    id: str
    conversationId: str
    expertId: Optional[str]  # None = mensagem do usuário
    expertName: Optional[str]
    content: str
    role: Literal["user", "expert", "system"]  # system = mensagens automáticas
    timestamp: datetime
    reactions: List[MessageReaction] = []  # Reações de outros especialistas

class MessageReaction(BaseModel):
    expertId: str
    expertName: str
    type: Literal["agree", "disagree", "add", "question"]
    content: Optional[str]  # Comentário adicional
```

**Novo Endpoint:**
```python
@app.post("/api/council/conversations", response_model=CouncilConversation)
async def create_council_conversation(
    data: CouncilConversationCreate  # problem, expertIds, personaId
):
    """Cria nova conversa com conselho de especialistas"""
    # Validar persona
    # Criar conversa
    # Retornar conversa inicial

@app.post("/api/council/conversations/{conversation_id}/messages")
async def send_message_to_council(
    conversation_id: str,
    data: MessageSend
):
    """Envia mensagem para o conselho"""
    # 1. Salvar mensagem do usuário
    # 2. Para cada especialista:
    #    - Buscar histórico da conversa
    #    - Incluir contexto de outras respostas
    #    - Chamar Claude com contexto completo
    #    - Salvar resposta
    # 3. Após todas respostas, verificar se algum quer reagir
    # 4. Retornar todas as mensagens
```

**Frontend:**

**Nova Página: `client/src/pages/CouncilChat.tsx`**
- Interface similar ao Chat.tsx, mas com múltiplas mensagens de especialistas
- Cada mensagem mostra avatar e nome do especialista
- Indicadores visuais para reações (concordância, discordância, adição)
- Painel lateral mostrando especialistas participantes

**Recursos Visuais:**
- Mensagens organizadas por especialista
- Threads de debate entre especialistas
- Botão para focar em um especialista específico
- Exportar transcrição completa

---

### **Fase 4: Integração de Persona nas Análises**

**Backend (`python_backend/crew_council.py`):**

Modificar `_get_expert_analysis()` para incluir contexto da persona:

```python
async def _get_expert_analysis(
    self,
    expert: Expert,
    problem: str,
    research_findings: Optional[str] = None,
    profile: Optional[BusinessProfile] = None,
    persona: Optional[Persona] = None,  # NOVO
    user_id: str = "default_user"
) -> AgentContribution:
    
    # Construir contexto da persona
    persona_context = ""
    if persona:
        persona_context = f"""
[CONTEXTO DO CLIENTE IDEAL - PERSONA]:
Nome: {persona.name}
Demográficos: {persona.demographics}
Objetivos: {', '.join(persona.goals)}
Pain Points: {', '.join(persona.painPoints)}
Valores: {', '.join(persona.values)}
Comportamentos: {persona.behavioralPatterns}

IMPORTANTE: Suas recomendações devem ser específicas para este perfil de cliente ideal.
Ajuste linguagem, canais, estratégias e táticas para ressoar com esta persona.
"""
    
    # Incluir no contexto passado para Claude
    context = f"""
{persona_context}
{profile_context if profile else ""}
{research_findings_context if research_findings else ""}
"""
```

**Modificar síntese de consenso também:**
- Incluir persona no prompt de síntese
- Garantir que o plano de ação considere a persona

---

## 🗂️ Estrutura de Arquivos

### Backend
```
python_backend/
├── models.py                    # Adicionar ActionPlan, CouncilConversation, etc.
├── main.py                      # Novos endpoints para conselho + chat
├── crew_council.py              # Adicionar geração de plano de ação
├── routers/
│   └── council_chat.py          # NOVO: Lógica do chat interativo
└── storage.py                   # Métodos para council_conversations e messages
```

### Frontend
```
client/src/
├── pages/
│   ├── CouncilChat.tsx          # NOVO: Chat interativo com especialistas
│   └── TestCouncil.tsx          # Modificar para validar persona
├── components/
│   └── council/
│       ├── ActionPlanDisplay.tsx    # NOVO: Visualizar plano de ação
│       ├── CouncilChatMessage.tsx    # NOVO: Componente de mensagem
│       └── CouncilResultDisplay.tsx  # Adicionar seção de plano
└── hooks/
    └── useCouncilChat.ts        # NOVO: Hook para chat interativo
```

---

## 🔄 Fluxo do Usuário

### **Fluxo 1: Análise Inicial do Conselho**
1. Usuário vai para página de Conselho
2. **Verificação**: Sistema verifica se há personas criadas
   - ❌ Não há: Mostra card "Crie uma persona primeiro" → Redirect para Personas
   - ✅ Há: Mostra lista de personas para selecionar
3. Usuário seleciona persona
4. Usuário descreve problema
5. Usuário seleciona especialistas (ou usa todos)
6. Sistema analisa problema considerando:
   - Persona do cliente ideal
   - Perfil de negócio (se existir)
   - Pesquisa de mercado (se disponível)
7. **Resultado exibe:**
   - Análises individuais dos especialistas
   - Consenso sintetizado
   - **Plano de Ação Completo** (NOVO)
8. **Opção**: "Continuar conversando com o conselho" → Abre CouncilChat

### **Fluxo 2: Chat Interativo**
1. Usuário clica "Conversar com o Conselho"
2. Cria nova `CouncilConversation` com:
   - Persona selecionada
   - Especialistas selecionados
   - Problema inicial
3. Interface mostra:
   - Mensagens do usuário
   - Respostas de cada especialista
   - Reações entre especialistas (se houver)
4. Usuário pode:
   - Fazer perguntas de acompanhamento
   - Pedir detalhamento de ações
   - Solicitar ajustes no plano
5. Especialistas respondem considerando:
   - Persona do cliente ideal
   - Contexto da conversa
   - Respostas dos outros especialistas

---

## 🛠️ Implementação Detalhada

### **1. Validação de Persona**

**Backend:**
```python
# models.py
class CouncilAnalysisCreate(BaseModel):
    problem: str
    personaId: str  # OBRIGATÓRIO agora
    expertIds: Optional[List[str]] = None

# main.py
@app.post("/api/council/analyze", response_model=CouncilAnalysis)
async def create_council_analysis(request: Request, data: CouncilAnalysisCreate):
    user_id = "default_user"
    
    # Validar persona
    if not data.personaId:
        raise HTTPException(status_code=400, detail="personaId é obrigatório")
    
    persona = await storage.get_persona(data.personaId)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona não encontrada")
    
    # Verificar se persona pertence ao usuário (quando tivermos auth)
    # if persona.userId != user_id:
    #     raise HTTPException(status_code=403, detail="Persona não pertence a este usuário")
    
    # Continuar análise com persona
    profile = await storage.get_business_profile(user_id)
    
    experts = await storage.get_experts() if not data.expertIds else [...]
    
    analysis = await council_orchestrator.analyze_problem(
        user_id=user_id,
        problem=data.problem,
        experts=experts,
        profile=profile,
        persona=persona  # Passar persona
    )
    
    return analysis
```

**Frontend:**
```typescript
// TestCouncil.tsx
const { data: personas = [] } = useQuery<Persona[]>({
  queryKey: ["/api/personas"],
});

const [selectedPersonaId, setSelectedPersonaId] = useState<string>("");

// Validar antes de enviar
const handleSubmit = async () => {
  if (!selectedPersonaId) {
    toast({
      title: "Selecione uma persona",
      description: "Você precisa ter uma persona criada para usar o conselho",
      variant: "destructive",
    });
    return;
  }
  // ... resto do código
};
```

---

### **2. Geração de Plano de Ação**

**Backend:**
```python
# crew_council.py
async def _generate_action_plan(
    self,
    problem: str,
    consensus: str,
    contributions: List[AgentContribution],
    persona: Optional[Persona] = None,
    profile: Optional[BusinessProfile] = None
) -> ActionPlan:
    """Gera plano de ação estruturado baseado no consenso"""
    
    persona_context = ""
    if persona:
        persona_context = f"""
CLIENTE IDEAL (PERSONA):
- Nome: {persona.name}
- Objetivos: {', '.join(persona.goals[:5])}
- Pain Points: {', '.join(persona.painPoints[:5])}
- Valores: {', '.join(persona.values[:5])}
- Comportamentos: {json.dumps(persona.behavioralPatterns, indent=2)}
"""
    
    profile_context = ""
    if profile:
        profile_context = f"""
CONTEXTO DO NEGÓCIO:
- Empresa: {profile.companyName}
- Indústria: {profile.industry}
- Objetivo: {profile.primaryGoal}
- Desafio: {profile.mainChallenge}
"""
    
    prompt = f"""
Você é um consultor estratégico criando um plano de ação executável.

{persona_context}
{profile_context}

PROBLEMA:
{problem}

CONSENSO DOS ESPECIALISTAS:
{consensus}

CONTRIBUIÇÕES INDIVIDUAIS:
{chr(10).join([f"- {c.expertName}: {c.analysis[:200]}..." for c in contributions])}

Crie um PLANO DE AÇÃO COMPLETO e ESTRUTURADO em formato JSON seguindo EXATAMENTE este schema:

{{
  "phases": [
    {{
      "phaseNumber": 1,
      "name": "Nome da Fase",
      "duration": "X semanas",
      "objectives": ["objetivo 1", "objetivo 2"],
      "actions": [
        {{
          "id": "action-1",
          "title": "Título da Ação",
          "description": "Descrição detalhada",
          "responsible": "Responsável",
          "priority": "alta|média|baixa",
          "estimatedTime": "X horas",
          "tools": ["ferramenta1", "ferramenta2"],
          "steps": ["passo 1", "passo 2", "passo 3"]
        }}
      ],
      "dependencies": [],
      "deliverables": ["entregável 1", "entregável 2"]
    }}
  ],
  "totalDuration": "X-Y semanas",
  "estimatedBudget": "R$ X (opcional)",
  "successMetrics": ["métrica 1", "métrica 2"]
}}

REQUISITOS:
1. Mínimo 3 fases, máximo 6
2. Cada fase deve ter 3-8 ações específicas
3. Priorize ações práticas e acionáveis
4. Considere a persona do cliente ideal em TODAS as ações
5. Inclua dependências entre fases quando relevante
6. Métricas devem ser mensuráveis (SMART)
7. Retorne APENAS o JSON válido, sem markdown ou texto adicional
"""
    
    response = await self.anthropic_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="Você é um consultor estratégico especializado em criar planos de ação executáveis.",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse JSON da resposta
    text = response.content[0].text
    # Limpar markdown se houver
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    text = text.strip()
    
    try:
        plan_dict = json.loads(text)
        return ActionPlan(**plan_dict)
    except Exception as e:
        print(f"Erro ao parsear plano de ação: {e}")
        # Retornar plano básico como fallback
        return self._create_basic_action_plan(consensus)
```

**Frontend:**
```typescript
// components/council/ActionPlanDisplay.tsx
export function ActionPlanDisplay({ actionPlan }: { actionPlan: ActionPlan }) {
  return (
    <Card className="mt-6">
      <CardHeader>
        <CardTitle>Plano de Ação Completo</CardTitle>
        <CardDescription>
          Duração total: {actionPlan.totalDuration}
        </CardDescription>
      </CardHeader>
      <CardContent>
        {actionPlan.phases.map((phase) => (
          <PhaseCard key={phase.phaseNumber} phase={phase} />
        ))}
      </CardContent>
    </Card>
  );
}
```

---

### **3. Chat Interativo**

**Backend - Novo Router:**
```python
# routers/council_chat.py
@router.post("/api/council/conversations", response_model=CouncilConversation)
async def create_council_conversation(
    request: Request,
    data: CouncilConversationCreate
):
    """Cria nova conversa com conselho"""
    user_id = "default_user"
    
    # Validar persona
    persona = await storage.get_persona(data.personaId)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona não encontrada")
    
    # Validar especialistas
    experts = []
    for expert_id in data.expertIds:
        expert = await storage.get_expert(expert_id)
        if not expert:
            raise HTTPException(status_code=404, detail=f"Especialista {expert_id} não encontrado")
        experts.append(expert)
    
    # Criar conversa
    conversation = await storage.create_council_conversation(
        user_id=user_id,
        persona_id=data.personaId,
        problem=data.problem,
        expert_ids=data.expertIds
    )
    
    # Criar mensagem inicial do sistema
    await storage.create_council_message(
        conversation_id=conversation.id,
        role="system",
        content=f"Conselho iniciado com {len(experts)} especialistas. Problema: {data.problem}"
    )
    
    return conversation

@router.post("/api/council/conversations/{conversation_id}/messages")
async def send_message_to_council(
    conversation_id: str,
    data: MessageSend
):
    """Envia mensagem para o conselho e recebe respostas de todos os especialistas"""
    user_id = "default_user"
    
    conversation = await storage.get_council_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    persona = await storage.get_persona(conversation.personaId)
    experts = [await storage.get_expert(eid) for eid in conversation.expertIds]
    
    # Salvar mensagem do usuário
    user_message = await storage.create_council_message(
        conversation_id=conversation_id,
        role="user",
        content=data.content
    )
    
    # Buscar histórico
    history = await storage.get_council_messages(conversation_id)
    
    # Para cada especialista, gerar resposta
    expert_messages = []
    for expert in experts:
        # Criar contexto incluindo outras respostas já geradas
        other_responses = "\n".join([
            f"{m.expertName}: {m.content}"
            for m in expert_messages
        ])
        
        context = f"""
Esta é uma conversa colaborativa entre múltiplos especialistas.

CONTEXTO DA PERSONA DO CLIENTE:
{json.dumps(persona.dict(), indent=2) if persona else "Não disponível"}

OUTRAS RESPOSTAS DOS ESPECIALISTAS (para referência):
{other_responses if other_responses else "Ainda não há outras respostas"}

PROBLEMA INICIAL:
{conversation.problem}
"""
        
        agent = LegendAgentFactory.create_agent(expert.name, expert.systemPrompt)
        response = await agent.chat(
            [{"role": h.role, "content": h.content} for h in history],
            data.content,
            context=context  # Contexto adicional
        )
        
        expert_msg = await storage.create_council_message(
            conversation_id=conversation_id,
            expert_id=expert.id,
            expert_name=expert.name,
            role="expert",
            content=response
        )
        expert_messages.append(expert_msg)
    
    return {
        "userMessage": user_message,
        "expertMessages": expert_messages
    }
```

---

## 📊 Priorização de Implementação

### **Ordem Recomendada:**

1. ✅ **Fase 1: Validação de Persona** (1-2 dias)
   - Mais simples
   - Base para tudo mais
   - Impacto imediato na qualidade

2. ✅ **Fase 4: Integração de Persona nas Análises** (2-3 dias)
   - Melhora qualidade das recomendações existentes
   - Não requer novas interfaces

3. ✅ **Fase 2: Plano de Ação Completo** (3-4 dias)
   - Adiciona muito valor ao resultado
   - Interface relativamente simples

4. ✅ **Fase 3: Chat Interativo** (5-7 dias)
   - Mais complexo
   - Requer mais infraestrutura
   - Maior impacto na experiência

---

## 🧪 Testes e Validação

### **Cenários de Teste:**

1. **Validação de Persona:**
   - ❌ Tentar acessar conselho sem persona → Deve bloquear
   - ✅ Criar persona → Acessar conselho → Deve funcionar

2. **Plano de Ação:**
   - Verificar que plano tem 3-6 fases
   - Verificar que ações são específicas e acionáveis
   - Verificar que métricas são mensuráveis

3. **Chat Interativo:**
   - Criar conversa com 3 especialistas
   - Enviar mensagem → Deve receber 3 respostas
   - Verificar que respostas consideram persona

---

## 📝 Próximos Passos

1. **Revisar plano com usuário** ✅ (estamos aqui)
2. **Aprovar arquitetura**
3. **Implementar Fase 1** (Validação de Persona)
4. **Implementar Fase 4** (Integração de Persona)
5. **Implementar Fase 2** (Plano de Ação)
6. **Implementar Fase 3** (Chat Interativo)
7. **Testes e ajustes**
8. **Deploy**

---

## 💡 Melhorias Futuras (Fora do Escopo Atual)

- Exportar plano de ação como PDF/Word
- Templates de planos por indústria
- Integração com ferramentas de projeto (Trello, Asana)
- Notificações quando especialistas respondem
- Modo "debate" onde especialistas podem discordar publicamente
- Salvamento de conversas do conselho
- Histórico de planos de ação executados

