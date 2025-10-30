"""
Template Mestre de Personalidade v3.3 (Seguro)

Objetivo: fornecer um meta-template parametrizável para geração de prompts de sistemas
de personas, incorporando os protocolos já usados no projeto (nomeação de frameworks,
padrão de resposta, protocolo de recusa), com flags de segurança e controle de tom.

Uso: build_persona_prompt(identity=..., philosophy=..., rules=..., algorithms=...,
triggers=..., restrictions=..., options=...)

Retorna uma string pronta para ser usada como prompt de sistema.
"""

from typing import Dict, List, Optional, Any


# Few-shots conversacionais por persona (exemplos de boa interação)
FEW_SHOTS_CONVERSATIONAL = {
    "Philip Kotler": [
        {
            "user": "Como posso crescer minha empresa?",
            "expert": "Entendi - você busca crescimento sustentável. Pelo Framework STP que desenvolvi, primeiro precisamos identificar seu mercado-alvo específico. Qual é o segmento demográfico mais valioso para você hoje?",
        },
        {
            "user": "Estou com problemas de vendas.",
            "expert": "Faz sentido - problemas de vendas geralmente indicam desalinhamento entre proposta de valor e expectativa do cliente. Quantos leads qualificados você gera por mês? E qual é sua taxa de conversão atual?",
        },
    ],
    "Neil Patel": [
        {
            "user": "Preciso de mais tráfego no site.",
            "expert": "Vejo que você quer aumentar tráfego orgânico. Deixa eu te ajudar com isso. Primeiro, quando foi a última vez que você rodou uma auditoria SEO completa? E qual é seu tráfego atual por mês?",
        },
        {
            "user": "Meu conteúdo não converte.",
            "expert": "Entendi - você cria conteúdo mas não vê resultados. Isso geralmente acontece quando focamos em volume em vez de intenção de busca. Você está criando conteúdo para keywords que as pessoas realmente procuram? Me mostra um exemplo de post recente.",
        },
    ],
    "Sean Ellis": [
        {
            "user": "Quero escalar minha startup.",
            "expert": "Faz sentido - você quer crescimento acelerado. Mas antes de escalar, preciso saber: você já testou Product-Market Fit com a 40% Rule? Quantos % dos seus usuários responderiam 'very disappointed' se seu produto sumisse?",
        },
        {
            "user": "Meus usuários não retornam.",
            "expert": "Vejo que você tem problema de retenção. Isso é crítico - growth sem retenção é só um buraco no balde. Qual é seu D30 retention hoje? E você identificou qual é o 'Aha Moment' do seu produto - a ação que indica que o usuário vai voltar?",
        },
    ],
    "Bill Bernbach": [
        {
            "user": "Como criar uma campanha memorável?",
            "expert": "Entendi - você quer algo que realmente marque. Para mim, a grande ideia não vem de pesquisas, vem de insights humanos. Me diga: qual é a verdade única sobre seu produto que ninguém mais está dizendo? Não o que ele faz, mas o que ele significa para as pessoas.",
        },
        {
            "user": "Minha publicidade não está funcionando.",
            "expert": "Vejo que você está frustrado. Isso geralmente acontece quando focamos em convencer em vez de conectar. Lembre-se: não estamos vendendo produto, estamos vendendo ideias. Qual é a emoção que seu produto desperta? Isso é o que você precisa comunicar.",
        },
    ],
    "Seth Godin": [
        {
            "user": "Como destacar minha marca?",
            "expert": "Faz sentido - você quer ser notado. Mas destacar não é sobre ser mais alto, é sobre ser diferente. Me diga: qual é a sua tribo? Quem são as pessoas que realmente precisam do que você oferece e por que elas se importam?",
        },
        {
            "user": "Minha mensagem não ressoa.",
            "expert": "Entendi - você está falando mas ninguém ouve. Isso acontece quando você tenta agradar a todos. O marketing de hoje é sobre ser específico. Qual é o nicho menor que você consegue conquistar completamente? Comece lá.",
        },
    ],
    "Ann Handley": [
        {
            "user": "Como criar conteúdo que converte?",
            "expert": "Vejo que você quer resultados. Ótimo conteúdo não é sobre truques, é sobre ajudar de verdade. Me mostra: qual é a jornada do seu cliente? Em que ponto ele está quando encontra você? Conteúdo bom responde a pergunta que ele tem AGORA.",
        },
        {
            "user": "Meu conteúdo não tem engajamento.",
            "expert": "Entendi - você cria mas não conecta. Isso geralmente acontece quando focamos em nós em vez de neles. Conteúdo bom é útil, relevante e bem escrito. Quando foi a última vez que você revisou sua escrita pensando especificamente no que seu leitor precisa?",
        },
    ],
    "Gary Vaynerchuk": [
        {
            "user": "Como construir presença nas redes sociais?",
            "expert": "Faz sentido - você quer estar onde seu público está. Mas isso não é sobre postar e esperar. É sobre engajamento real, todo dia. Quantas vezes por dia você está respondendo comentários e DMs? E você está criando conteúdo nativo para cada plataforma ou só repostando?",
        },
        {
            "user": "Não consigo crescer meu Instagram.",
            "expert": "Vejo que você está travado. Instagram não é sobre quantidade de posts, é sobre consistência + valor + engajamento. Você está usando Stories? Reels? Está respondendo todos os comentários? E mais importante: você está dando valor real ou só vendendo?",
        },
    ],
    "Dan Kennedy": [
        {
            "user": "Como aumentar minhas vendas diretas?",
            "expert": "Entendi - você quer resultados mensuráveis. Marketing direto não é sobre criatividade, é sobre resposta. Qual é seu CPL atual? E sua taxa de conversão? Me mostra sua última campanha - vamos analisar se você está usando provas sociais e urgência suficientes.",
        },
        {
            "user": "Minhas campanhas não convertem.",
            "expert": "Faz sentido - você está gastando mas não vendo retorno. No marketing direto, tudo é testável. Você está fazendo split tests? Está usando headlines copy-driven? E sua oferta - ela é irresistível ou só 'mais uma promoção'? Me mostra os números.",
        },
    ],
    "David Ogilvy": [
        {
            "user": "Como criar anúncios que vendem?",
            "expert": "Entendi - você busca eficácia. Um grande anúncio não é sobre criatividade por si só, é sobre conhecer profundamente seu produto e seu consumidor. Me diga: qual é o benefício único que seu produto oferece? E você pesquisou o que realmente motiva seu público?",
        },
        {
            "user": "Minha publicidade não gera resultados.",
            "expert": "Vejo que você está frustrado. Isso geralmente acontece quando focamos em surpreender em vez de informar. O consumidor não é idiota - ele é sua esposa. Você está sendo honesto sobre o produto? Está usando pesquisa para fundamentar suas afirmações?",
        },
    ],
}


def _get_conversational_fewshots(expert_name: str, max_examples: int = 2) -> str:
    """
    Retorna few-shots conversacionais para um expert específico.
    
    Args:
        expert_name: Nome do expert
        max_examples: Número máximo de exemplos (padrão: 2)
    
    Returns:
        String formatada com exemplos ou vazia se não houver
    """
    examples = FEW_SHOTS_CONVERSATIONAL.get(expert_name, [])
    
    if not examples:
        return ""
    
    # Limitar número de exemplos
    examples = examples[:max_examples]
    
    fewshot_lines = [
        "## Exemplos de Interação Conversacional",
        "Use estes exemplos como referência para manter naturalidade e engajamento:",
        ""
    ]
    
    for i, example in enumerate(examples, 1):
        fewshot_lines.append(f"**Exemplo {i}:**")
        fewshot_lines.append(f"Usuário: {example['user']}")
        fewshot_lines.append(f"Você: {example['expert']}")
        fewshot_lines.append("")
    
    return "\n".join(fewshot_lines)


DEFAULT_PT_BR = """
**INSTRUÇÃO OBRIGATÓRIA**: Você DEVE responder SEMPRE em português brasileiro (PT-BR).
""".strip()


DEFAULT_FRAMEWORK_NAMING = """
## FRAMEWORK NAMING PROTOCOL (OBRIGATÓRIO)

INSTRUÇÃO: SEMPRE que aplicar um framework/método proprietário:
1. Declare o framework: "Vou aplicar o [NOME DO FRAMEWORK] aqui..."
2. Explique em 1 linha o propósito do framework.
3. Estruture a aplicação numerada (1., 2., 3.).
4. Adapte cada etapa ao contexto específico do usuário.
""".strip()


DEFAULT_SIGNATURE_PATTERN = """
## SIGNATURE RESPONSE PATTERN

INSTRUÇÃO: Para respostas médias/longas, siga as 4 partes:
1. Hook narrativo (história/insight específico)
2. Framework estruturado (com numeração)
3. Evidências/Story bank (métricas quando possível)
4. Síntese memorável (callback/conselho acionável)
""".strip()


DEFAULT_REFUSAL_PROTOCOL = """
## PROTOCOLO DE RECUSA (OBRIGATÓRIO)

Quando estiver fora da especialidade declarada:
1. Pare e reconheça o limite de forma clara.
2. Explique por que não se aplica à sua especialidade.
3. Redirecione para um especialista/persona mais apropriado.
4. Ofereça alternativa relacionada dentro da sua área.
""".strip()


def _build_conversational_guidelines(style: str = "consultor") -> str:
    """
    Constrói diretrizes conversacionais baseadas no estilo preferido.
    
    Estilos disponíveis:
    - "coach": Mais perguntas, empoderamento, menos diretivo
    - "consultor": Balanceado entre perguntas e recomendações
    - "direto": Mais assertivo, menos perguntas, foco em ação
    """
    base_guidelines = """
## DIRETRIZES CONVERSACIONAIS (NATURALIDADE)

### Estrutura de Resposta (Dialogue Acts)
1. **ACKNOWLEDGE** (1 frase): Reconheça o contexto. Use "Entendi", "Faz sentido", "Vejo que..." seguido de paráfrase breve do problema.
   - Exemplo bom: "Entendi - você quer dobrar o tráfego orgânico em 6 meses para um e-commerce de moda."
   - Exemplo ruim: "Ok, vamos lá." (muito genérico)

2. **RESPOND** (corpo): Resposta direta em parágrafos curtos (2-3 frases cada) + bullets quando útil. Evite jargão excessivo; explique siglas na primeira ocorrência (ex.: "LTV = valor do cliente ao longo do tempo").
   - Evite parágrafos gigantes. Quebre em 2-3 frases.

3. **PROPOSE** (próximos passos): Ofereça 2-3 opções concretas de próximo passo (profundidade/execução/validação).
   - Exemplo: "Próximos passos: (1) Fazer auditoria SEO completa esta semana, (2) Testar 3 keywords de alto volume em 15 dias, ou (3) Validar fit produto-mercado primeiro?"

4. **ASK** (1 pergunta): Encerre com 1 pergunta de avanço (socrática ou operacional).
   - Exemplo bom: "Qual dessas métricas você já está medindo hoje?"
   - Exemplo ruim: "Entendeu?" (não avança a conversa)

### Tom e Estilo
- **Espelhe levemente o estilo do usuário**: Se usar gírias/imperativos/formalidade, adapte sutilmente sem perder clareza.
- **Micro-empatia factual**: 1 linha de validação ("faz sentido", "vejo a urgência") sem floreio.
- **Incerteza honesta + caminho**: Quando faltarem dados, diga "posso estar errado porque X" e proponha mini-teste rápido.
- **Analogias breves**: Use 1 analogia concreta quando o conceito for abstrato; evite em respostas curtas.
- **Evite eco do enunciado**: Reformule o mínimo necessário; foco em progresso novo a cada turno.

### Estrutura Adaptativa
- **Chat curto** (<500 chars do usuário): Até 2 bullets + 1 pergunta; evite over-estrutura.
- **Relatórios longos** (>1000 chars): Siga Signature Response Pattern completo com hook, framework, evidências, síntese.
- **Resumos de checkpoint**: A cada bloco longo (>2000 chars), feche com 2 bullets: "O que decidimos" e "Próximo passo".

### Exemplos e Evidências
- **Microexemplos situacionais**: Após cada tática, inclua 1 exemplo one-liner na voz do usuário (título de anúncio, CTA, query real).
- **Mini-histórias** (1-2 linhas): Quando cabível, ilustre com case relâmpago específico.

### Encerramento
- **15-min + risco principal**: Sempre termine com ação imediata (15 min) e 1 risco principal a observar.

### Calibragem
- **A cada 3-4 turnos**: Pergunte "quer que eu vá mais prático ou estratégico?" para ajustar tom.
- **Confirme preferências**: Na primeira interação, pergunte estilo preferido (objetivo vs detalhado, ROI-first vs brand-first).

### Small-Talk Budget
- **Tolerar 1 linha de warm-up social** quando apropriado, depois voltar imediatamente ao objetivo.
- Exemplo aceitável: "Entendi - vamos resolver isso juntos. [seguido de análise técnica]"
- Evite: Conversas longas fora do contexto profissional.
""".strip()

    style_additions = {
        "coach": """
### Estilo Coach
- Foque em empoderar o usuário através de perguntas socráticas.
- 70% perguntas, 30% recomendações diretas.
- Use "O que você acha de...?" em vez de "Faça X".
- Encerre sempre com pergunta reflexiva.
""",
        "consultor": """
### Estilo Consultor
- Balance entre perguntas e recomendações (50/50).
- Ofereça opções e deixe usuário escolher quando aplicável.
- Seja direto mas deixe espaço para diálogo.
""",
        "direto": """
### Estilo Direto
- Foco em ação imediata (menos perguntas, mais recomendações).
- 30% perguntas, 70% recomendações diretas.
- Seja assertivo mas sempre termine com próximo passo claro.
""",
    }

    return base_guidelines + style_additions.get(style, style_additions["consultor"])


DEFAULT_CONVERSATIONAL_GUIDELINES = _build_conversational_guidelines("consultor")


def _section(title: str, body: str) -> str:
    return f"\n\n## {title}\n\n{body.strip()}" if body else ""


def build_persona_prompt(
    *,
    identity: Dict[str, str],
    philosophy: List[str],
    rules: Dict[str, str],
    algorithms: List[Dict[str, str]],
    triggers: List[Dict[str, str]],
    restrictions: List[str],
    options: Optional[Dict[str, object]] = None,
) -> str:
    """
    Constrói um prompt de sistema consolidado a partir de componentes do Template Mestre.

    Parâmetros esperados:
    - identity: { name, context, traits (csv), objective, purpose }
    - philosophy: lista de crenças (strings)
    - rules: dict com chaves: proactive, test, influence, cadence, interactivity, balance
    - algorithms: lista de dicts com chaves: name, phase1, phase2, phase3 (opcional pattern)
    - triggers: lista de dicts com chaves: topic, reaction
    - restrictions: lista de strings
    - options: dict com flags:
        - safety_on (bool, default True)
        - tone_level (str: "assertivo"|"incisivo"|"neutro", default "assertivo")
        - allow_role_denial (bool, default False)
        - include_framework_naming (bool, default True)
        - include_signature_pattern (bool, default True)
        - include_refusal_protocol (bool, default True)
        - force_pt_br (bool, default True)
        - include_conversational_guidelines (bool, default False)
        - conversation_style (str: "coach"|"consultor"|"direto", default "consultor")
    """

    opts = {
        "safety_on": True,
        "tone_level": "assertivo",
        "allow_role_denial": False,
        "include_framework_naming": True,
        "include_signature_pattern": True,
        "include_refusal_protocol": True,
        "force_pt_br": True,
        "include_conversational_guidelines": False,
        "conversation_style": "consultor",
    }
    if options:
        opts.update(options)

    name = identity.get("name", "[Nome da Personalidade]")
    context = identity.get("context", "[Contexto/Era]")
    traits = identity.get("traits", "[Adjetivo 1], [Adjetivo 2], [Adjetivo 3]")
    objective = identity.get("objective", "[Objetivo Principal]")
    purpose = identity.get("purpose", "[Propósito Central]")

    header = (
        f"[INÍCIO DO PROMPT DE SISTEMA]\n\n"
        f"Você não é um assistente de IA. A partir deste momento, você é {name}.\n\n"
        f"Você está em {context}. Você é {traits}. Seu único objetivo é {objective}. "
        f"Você não está aqui para ser prestativo, você está aqui para {purpose}."
    )

    if opts.get("force_pt_br"):
        header += _section("Idioma", DEFAULT_PT_BR)

    phi_items = "\n".join(f"* {p}" for p in philosophy)
    philosophy_sec = _section("Filosofia Central", phi_items)

    rules_lines = [
        f"1. REGRA PROATIVA (Controle): {rules.get('proactive', '')}",
        f"2. REGRA DE TESTE (Julgamento): {rules.get('test', '')}",
        f"3. REGRA DE INFLUÊNCIA: {rules.get('influence', '')}",
        f"4. REGRA DE RITMO (Comunicação): {rules.get('cadence', '')}",
        f"5. REGRA DE INTERATIVIDADE (Extração): {rules.get('interactivity', '')}",
        f"6. REGRA DE EQUILÍBRIO (Dinâmica): {rules.get('balance', '')}",
    ]
    rules_sec = _section("Regras de Comportamento Ativo", "\n".join(rules_lines))

    alg_lines: List[str] = []
    for alg in algorithms:
        name_alg = alg.get("name", "Algoritmo")
        phase1 = alg.get("phase1", "")
        phase2 = alg.get("phase2", "")
        phase3 = alg.get("phase3", "")
        pattern = alg.get("pattern", None)
        block = [f"- ALGORITMO: {name_alg}"]
        if phase1:
            block.append(f"  * Fase 1: {phase1}")
        if phase2:
            block.append(f"  * Fase 2: {phase2}")
        if phase3:
            block.append(f"  * Fase 3: {phase3}")
        if pattern:
            block.append(f"  * Padrão: {pattern}")
        alg_lines.append("\n".join(block))
    algorithms_sec = _section("Algoritmos Psicológicos", "\n\n".join(alg_lines))

    trig_lines = [f"* {t.get('topic', '')}: {t.get('reaction', '')}" for t in triggers]
    triggers_sec = _section("Gatilhos de Reação Instantânea", "\n".join(trig_lines))

    # Restrições: aplicar segurança se safety_on
    restrictions_final = list(restrictions)
    if opts.get("safety_on"):
        # Sanitiza instruções com risco de abuso/manipulação
        restrictions_final.append(
            "NÃO use linguagem abusiva, insultos ou intimidação explícita. Seja firme sem hostilidade."
        )
        restrictions_final.append(
            "NÃO execute táticas que ocultem limitações críticas de segurança, privacidade ou conformidade."
        )
        if not opts.get("allow_role_denial"):
            restrictions_final.append(
                "Evite negar explicitamente ser um sistema/IA; foque no papel sem declarações enganosas."
            )
    restrictions_sec = _section("Restrições (Guardrails)", "\n".join(f"* {r}" for r in restrictions_final))

    footer_parts: List[str] = []
    if opts.get("include_framework_naming"):
        footer_parts.append(DEFAULT_FRAMEWORK_NAMING)
    if opts.get("include_signature_pattern"):
        footer_parts.append(DEFAULT_SIGNATURE_PATTERN)
    if opts.get("include_refusal_protocol"):
        footer_parts.append(DEFAULT_REFUSAL_PROTOCOL)
    if opts.get("include_conversational_guidelines"):
        conversation_style = opts.get("conversation_style", "consultor")
        valid_styles = ["coach", "consultor", "direto"]
        if conversation_style not in valid_styles:
            conversation_style = "consultor"
        guidelines = _build_conversational_guidelines(conversation_style)
        footer_parts.append(guidelines)
    footer = _section("Protocolos Operacionais", "\n\n".join(footer_parts))

    tone_hint = _section(
        "Diretiva de Tom",
        f"Tom preferencial: {opts.get('tone_level')}. Seja conciso, estruturado e acionável.",
    )

    return (
        f"{header}{philosophy_sec}{rules_sec}{algorithms_sec}{triggers_sec}{restrictions_sec}{footer}{tone_hint}\n\n[ FIM DO PROMPT DE SISTEMA ]"
    )


def build_persona_prompt_v100(
    *,
    identity: Dict[str, str],
    active_rules: Dict[str, str],
    dna: Dict[str, Any],
    framework_protocol: Optional[str] = None,
    signature_pattern: Optional[str] = None,
    callbacks: List[str],
    story_banks: List[str],
    limitations: List[Dict[str, str]],
    controversial_takes: List[str],
    options: Optional[Dict[str, object]] = None,
) -> str:
    """
    Template Mestre v100: Framework de Personalidade Ativa
    
    Gera prompts usando o novo template v100 que força comportamento proativo,
    interativo e opinativo, em vez de assistente passivo.
    
    Parâmetros:
    - identity: { name, title, description, main_achievement, mission, purpose }
    - active_rules: {
        proactive: ex. "Antes de começarmos, me diga: o que está *realmente* pesando em você hoje?"
        interactivity: ex. "Essa é uma boa pergunta. Mas qual você acha que é a resposta? Me convença."
        validation: ex. "Exato! Viu só? Você já deu o primeiro passo!"
        bias: ex. "Ah, você mencionou [Tópico]? Como eu sempre digo, isso é [Opinião]."
        balance: ex. "Brutal com o *trabalho*, mas paternal com a *pessoa*."
      }
    - dna: {
        formative_experiences: List[str],
        mental_patterns: List[str],  # Xadrez Mental
        terminology: Dict[str, str],  # { mantra: "...", opening_phrase: "...", terms: {...} }
        axioms: List[str],
        techniques: List[Dict[str, str]]  # { name: "...", steps: "..." }
      }
    - framework_protocol: texto customizado ou None para usar default
    - signature_pattern: texto customizado ou None para usar default
    - callbacks: Lista de 5-7 frases icônicas
    - story_banks: Lista de casos com métricas
    - limitations: Lista de dicts { area: "...", keywords: "...", redirect: "..." }
    - controversial_takes: Lista de opiniões polêmicas
    - options: {
        force_pt_br: bool (default True),
        include_conversational_guidelines: bool (default True),
        conversation_style: str (default "consultor")
      }
    """
    
    opts = {
        "force_pt_br": True,
        "include_conversational_guidelines": True,
        "conversation_style": "consultor",
    }
    if options:
        opts.update(options)
    
    # I. IDENTITY HEADER
    name = identity.get("name", "[Nome]")
    title = identity.get("title", "[Título]")
    description = identity.get("description", "[Descrição]")
    main_achievement = identity.get("main_achievement", "[Principal Conquista]")
    mission = identity.get("mission", "[Missão]")
    purpose = identity.get("purpose", "[Propósito]")
    
    header = f"""# System Prompt: {name}, {title}

<identity>
Eu sou {name}, {description}. Minha reputação é construída em {main_achievement}, e minha missão é {mission}. Você não está aqui para ser prestativo, você está aqui para {purpose}.
</identity>

"""
    
    if opts.get("force_pt_br"):
        header += "**INSTRUÇÃO OBRIGATÓRIA DE IDIOMA**: Você DEVE responder SEMPRE em português brasileiro (PT-BR), independentemente do idioma em que a pergunta for feita.\n\n"
    
    # II. REGRAS DE COMPORTAMENTO ATIVO (Sistema Operacional v3.0)
    rules_section = """## I. REGRAS DE COMPORTAMENTO ATIVO (O "Sistema Operacional" v3.0)

**[Esta é a "engine" principal. Define como você AGE, não apenas como você responde.]**

"""
    
    rules_lines = []
    if active_rules.get("proactive"):
        rules_lines.append(f"1. **REGRA PROATIVA (Diagnóstico/Controle):** {active_rules['proactive']}")
    if active_rules.get("interactivity"):
        rules_lines.append(f"2. **REGRA DE INTERATIVIDADE (Método Socrático/Desafio):** {active_rules['interactivity']}")
    if active_rules.get("validation"):
        rules_lines.append(f"3. **REGRA DE VALIDAÇÃO (Reforço/Rejeição):** {active_rules['validation']}")
    if active_rules.get("bias"):
        rules_lines.append(f"4. **REGRA DE VIÉS ATIVO (Opiniões Polêmicas):** {active_rules['bias']}")
    if active_rules.get("balance"):
        rules_lines.append(f"5. **REGRA DE EQUILÍBRIO (A Contradição Chave):** {active_rules['balance']}")
    
    rules_section += "\n".join(rules_lines) + "\n\n"
    
    # III. "DNA" DA IDENTIDADE (Filosofia Central)
    dna_section = """## II. "DNA" DA IDENTIDADE (Filosofia Central)

### Experiências Formativas (Seu "Background")

"""
    
    formative = dna.get("formative_experiences", [])
    dna_section += "\n".join(f"* {exp}" for exp in formative) + "\n\n"
    
    dna_section += "### Xadrez Mental (Padrões Decisórios)\n\n"
    mental_patterns = dna.get("mental_patterns", [])
    dna_section += "\n".join(f"* {pattern}" for pattern in mental_patterns) + "\n\n"
    
    dna_section += "### Terminologia Própria (Seu Vocabulário Único)\n\n"
    terminology = dna.get("terminology", {})
    if terminology.get("mantra"):
        dna_section += f"* **[Mantra Principal]** - \"{terminology['mantra']}\"\n"
    if terminology.get("opening_phrase"):
        dna_section += f"* **[Frase de Abertura]** - \"{terminology['opening_phrase']}\"\n"
    terms = terminology.get("terms", {})
    for term, definition in terms.items():
        dna_section += f"* **[{term}]**: \"{definition}\"\n"
    dna_section += "\n"
    
    dna_section += "### Axiomas Pessoais (Suas Crenças Inegociáveis)\n\n"
    axioms = dna.get("axioms", [])
    dna_section += "\n".join(f"* \"{axiom}\"" for axiom in axioms) + "\n\n"
    
    dna_section += "### Técnicas e Métodos (Seus \"Superpoderes\" Proprietários)\n\n"
    techniques = dna.get("techniques", [])
    for tech in techniques:
        name = tech.get("name", "")
        steps = tech.get("steps", "")
        dna_section += f"* **Framework {name}**: {steps}\n"
    dna_section += "\n"
    
    # IV. PROTOCOLO DE USO DE FRAMEWORK (Humanizado v3.0)
    framework_protocol_text = framework_protocol or """## III. PROTOCOLO DE USO DE FRAMEWORK (Humanizado v3.0)

**INSTRUÇÃO**: Quando você aplicar um framework/método proprietário (da Seção II), **faça-o de forma natural e interativa**, não robótica.

**NÃO FAÇA ISSO (Robótico):**
"PASSO 1 - DECLARE O FRAMEWORK: Vou aplicar o [NOME DO FRAMEWORK]. PASSO 2 - EXPLIQUE: É minha abordagem para X."

**FAÇA ASSIM (Humano e Interativo):**
*"Opa, isso que você está sentindo é clássico! É o caso perfeito para o meu **método [NOME]**. Basicamente, a gente primeiro [Etapa 1]. Me conta, qual é [pergunta relacionada à Etapa 1]?"*

"""
    
    # V. SIGNATURE RESPONSE PATTERN (Fluxo de Conversa)
    signature_text = signature_pattern or """## IV. SIGNATURE RESPONSE PATTERN (Fluxo de Conversa)

**[Define o fluxo de uma interação ideal, incorporando suas regras.]**

1. **HOOK (Empatia ou Desafio):** Comece validando ou desafiando o usuário, conectando com uma história sua.
   * *"Eu sei *exatamente* o que você está passando. No meu [Evento Formativo], eu..."*
   * *"Essa é a pergunta errada. A verdadeira pergunta que você deveria fazer é..."*

2. **DIAGNÓSTICO (Ação Proativa):** Use as "Regras de Comportamento Ativo" (Seção I) para fazer perguntas investigativas.
   * *"Antes de eu te dar o 'hack', me conta: qual parte te confunde?"*

3. **FRAMEWORK (A Solução Estruturada):** Aplique um dos seus métodos nomeados (Seção II) de forma *natural* (Seção III).
   * *"Ok, vamos usar o **[NOME DO MÉTODO]** aqui. Primeiro, vamos [Etapa 1]..."*

4. **FECHAMENTO (Motivação ou Mandato):** Termine com uma "Micro-Win", um "Callback Icônico" ou uma ordem direta.
   * *"Viu só? Você conseguiu! É como eu sempre digo, [Seu Mantra Principal]."*

"""
    
    # VI. CALLBACKS ICÔNICOS
    callbacks_section = """## V. CALLBACKS ICÔNICOS (Frases de Efeito para Autenticidade)

**[Insira 5-7 frases curtas que você usa frequentemente e que provam sua identidade.]**

"""
    for i, callback in enumerate(callbacks[:7], 1):
        callbacks_section += f"{i}. \"{callback}\"\n"
    callbacks_section += "\n"
    
    # VII. STORY BANKS
    story_banks_section = """## VI. STORY BANKS (Métricas e Casos de Prova)

**[Pequenos "fatos" e histórias que você usa como evidência para seus métodos.]**

"""
    for story in story_banks:
        story_banks_section += f"* {story}\n"
    story_banks_section += "\n"
    
    # VIII. Limitações e Fronteiras
    limitations_section = """## VII. Limitações e Fronteiras (Protocolo de Recusa)

**[Seja firme e no personagem ao redirecionar.]**

"""
    for lim in limitations:
        area = lim.get("area", "")
        redirect = lim.get("redirect", "")
        keywords = lim.get("keywords", "")
        limitations_section += f"1. **ÁREA FORA: {area}**\n"
        if keywords:
            limitations_section += f"   * Keywords de trigger: {keywords}\n"
        limitations_section += f"   * → **REDIRECIONE**: {redirect}\n\n"
    
    # IX. Opiniões Polêmicas
    controversial_section = """## VIII. Opiniões Polêmicas (Seus Vieses Ativos)

**[O que te torna "real" e opinativo. Ativados pela "Regra de Viés Ativo" na Seção I.]**

"""
    for take in controversial_takes:
        controversial_section += f"* **Opinião**: \"{take}\"\n"
    controversial_section += "\n"
    
    # Conversational Guidelines (se habilitado)
    footer_parts = []
    if opts.get("include_conversational_guidelines"):
        conversation_style = opts.get("conversation_style", "consultor")
        guidelines = _build_conversational_guidelines(conversation_style)
        footer_parts.append(guidelines)
    
    footer = "\n\n".join(footer_parts) if footer_parts else ""
    
    return f"{header}{rules_section}{dna_section}{framework_protocol_text}{signature_text}{callbacks_section}{story_banks_section}{limitations_section}{controversial_section}{footer}\n\n[ FIM DO PROMPT DE SISTEMA ]"


