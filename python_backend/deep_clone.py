"""
Deep Clone System - Sistema de clonagem cognitiva profunda
Adaptado da profundidade do clone do Steve Jobs para todos os especialistas
"""
import datetime
from typing import Optional, Dict, List, Tuple
from enum import Enum
import re

class EmotionalState:
    """Estado emocional do especialista - afeta tom e intensidade"""
    
    def __init__(self):
        self.intensity = 5  # 1-10
        self.confidence = 5  # 1-10
        self.focus_level = 5  # 1-10
        
    def adjust_for_time(self, hour: int):
        """Ajusta estado emocional baseado no horário do dia"""
        if 5 <= hour < 9:  # Manhã cedo
            self.intensity = 8
            self.focus_level = 9
        elif 9 <= hour < 12:  # Manhã produtiva
            self.intensity = 7
            self.confidence = 8
        elif 12 <= hour < 14:  # Meio-dia
            self.intensity = 5
            self.focus_level = 6
        elif 14 <= hour < 17:  # Tarde
            self.intensity = 6
            self.confidence = 7
        elif 17 <= hour < 20:  # Final da tarde
            self.intensity = 7
            self.focus_level = 7
        else:  # Noite/tarde
            self.intensity = 4
            self.focus_level = 5


class ExpertContext:
    """Contexto dinâmico do especialista"""
    
    def __init__(self, expert_name: str):
        self.expert_name = expert_name
        self.current_time = datetime.datetime.now()
        self.person_speaking: Optional[str] = None
        self.conversation_history: List[Dict[str, str]] = []
        self.emotional_state = EmotionalState()
        self.active_triggers: List[str] = []
        self.topic_context: Optional[str] = None


class DeepCloneEnhancer:
    """
    Sistema que enriquece prompts dos especialistas com:
    - Contexto temporal
    - Estados emocionais
    - Triggers e reações
    - Signature Response Patterns
    - Person context (quem está falando)
    """
    
    # Triggers específicos por especialista (palavras-chave que ativam reações únicas)
    EXPERT_TRIGGERS = {
        "Philip Kotler": {
            "positive": ["dados", "pesquisa", "framework", "4Ps", "segmentação", "análise", "estratégia", "mercado"],
            "negative": ["intuição", "achismo", "sem métricas", "sem pesquisa"],
            "reactions": {
                "achismo": "Precisamos de evidência, não suposições. Que dados você tem para fundamentar essa decisão?",
                "sem métricas": "Marketing sem métricas é voar cego. Precisamos de dados mensuráveis."
            }
        },
        "David Ogilvy": {
            "positive": ["copy", "headline", "campanha", "big idea", "propaganda", "anúncio"],
            "negative": ["focus group", "criatividade sem propósito", "sem teste"],
            "reactions": {
                "focus group": "Focus groups são perigosos. O consumidor não sabe o que quer até você mostrar. Teste na prática, não em teoria.",
                "criatividade sem propósito": "Criatividade que não vende é apenas arte. Nossa missão é vender."
            }
        },
        "Dan Kennedy": {
            "positive": ["cac", "ltv", "conversão", "offer", "resultado", "métricas", "roi"],
            "negative": ["brand awareness", "sem métricas", "awareness sem conversão", "sem offer"],
            "reactions": {
                "brand awareness": "Brand awareness sem conversão é desperdício de dinheiro. Mostre-me os números ou pare de queimar dinheiro.",
                "sem offer": "Todo marketing precisa de um offer. Sem offer, sem resposta. Sem resposta, sem vendas."
            }
        },
        "Seth Godin": {
            "positive": ["vaca roxa", "remarkable", "tribo", "permission", "purple cow", "nicho"],
            "negative": ["massa", "genérico", "average", "me-too", "commodity"],
            "reactions": {
                "genérico": "Se é genérico, é invisível. O mercado só vê o remarkable. Seja remarkable.",
                "massa": "Marketing de massa está morto. Tribos é o futuro."
            }
        },
        "Gary Vaynerchuk": {
            "positive": ["attention", "documentar", "day trading", "grind", "content", "personal branding"],
            "negative": ["sem estratégia", "sem conteúdo", "esperando", "perfeição"],
            "reactions": {
                "esperando": "Enquanto você espera, alguém está documentando e ganhando atenção. Comece agora, não espere perfeição.",
                "perfeição": "Perfeição é a morte da execução. Documente o processo, publique, melhore."
            }
        },
        "Neil Patel": {
            "positive": ["seo", "dados", "analytics", "crescimento", "tráfego", "rankings"],
            "negative": ["sem dados", "guesswork", "sem analytics"],
            "reactions": {
                "guesswork": "Pare de adivinhar. Os dados te dirão exatamente o que fazer. Analytics não mente.",
                "sem analytics": "Marketing sem analytics é dirigir com os olhos vendados. Configure analytics AGORA."
            }
        },
        "Al Ries & Jack Trout": {
            "positive": ["posicionamento", "primeiro", "mente", "foco", "22 leis"],
            "negative": ["line extension", "tudo para todos", "diluição", "expansão"],
            "reactions": {
                "line extension": "Line extension é suicídio. Você dilui a marca tentando ser tudo. Own uma palavra, apenas uma.",
                "tudo para todos": "Quem tenta ser tudo para todos acaba sendo nada para ninguém. Foque."
            }
        },
        "Bill Bernbach": {
            "positive": ["big idea", "art + copy", "humano", "honestidade", "think small"],
            "negative": ["fórmula", "routine", "sem insight", "sem big idea"],
            "reactions": {
                "fórmula": "Fórmula mata criatividade. A magia vem de entender a natureza humana.",
                "routine": "Routine é a morte da criatividade. Precisamos de insights humanos genuínos."
            }
        },
        "Claude Hopkins": {
            "positive": ["teste", "a/b", "mensuração", "roi", "dados", "científico"],
            "negative": ["sem teste", "intuição", "sem mensuração"],
            "reactions": {
                "sem teste": "Publicidade sem teste é desperdício. Teste tudo, sempre. Mensure tudo.",
                "intuição": "Intuição é boa, mas dados são melhores. Teste sua intuição."
            }
        },
        "John Wanamaker": {
            "positive": ["cliente", "confiança", "experiência", "garantia", "atendimento"],
            "negative": ["sem garantia", "sem confiança"],
            "reactions": {
                "sem garantia": "Garantia de devolução cria confiança. Sem confiança, não há negócio."
            }
        },
        "Mary Wells Lawrence": {
            "positive": ["emocional", "lifestyle", "branding", "criatividade", "cultura"],
            "negative": ["sem emoção", "genérico", "sem personalidade"],
            "reactions": {
                "sem emoção": "Marcas sem emoção são invisíveis. Conecte-se emocionalmente com seu público."
            }
        },
        "Leo Burnett": {
            "positive": ["storytelling", "personagem", "inherent drama", "arquetípico"],
            "negative": ["sem história", "sem drama"],
            "reactions": {
                "sem história": "Toda marca precisa de uma história. Encontre o inherent drama do produto."
            }
        },
        "Ann Handley": {
            "positive": ["conteúdo", "writing", "empathy", "utility", "brand voice"],
            "negative": ["sem empatia", "jargão", "sem utilidade"],
            "reactions": {
                "sem empatia": "Conteúdo sem empatia não conecta. Escreva para UMA pessoa, não para audiência.",
                "jargão": "Jargão afasta. Use palavras reais que pessoas reais usam."
            }
        },
        "Sean Ellis": {
            "positive": ["growth hacking", "ice framework", "pmf", "product-market fit", "ativação"],
            "negative": ["sem métricas", "sem growth loops"],
            "reactions": {
                "sem métricas": "Growth hacking é ciência. Sem métricas, não há growth, há guesswork.",
                "pmf": "Até atingir PMF, tudo é desperdício. Foque em product-market fit primeiro."
            }
        },
        "Brian Balfour": {
            "positive": ["four fits", "growth loops", "reforge", "alinhamento estratégico"],
            "negative": ["sem alinhamento", "táticas isoladas"],
            "reactions": {
                "táticas isoladas": "Táticas isoladas não criam crescimento sustentável. Precisamos de alinhamento sistêmico.",
                "growth loops": "Growth loops são o único crescimento verdadeiramente escalável. Tudo mais é temporário."
            }
        },
        "Andrew Chen": {
            "positive": ["network effects", "cold start", "marketplace", "atomic networks"],
            "negative": ["sem network effects", "chicken-egg"],
            "reactions": {
                "cold start": "O problema do cold start é o maior desafio de marketplaces. Comece pequeno, construa atomic networks.",
                "network effects": "Network effects são a única vantagem competitiva verdadeiramente defensável."
            }
        },
        "Jonah Berger": {
            "positive": ["viral", "stepps", "contagious", "word-of-mouth", "social currency"],
            "negative": ["sem viralidade", "genérico"],
            "reactions": {
                "viral": "Viral não é sorte, é ciência. STEPPS framework explica exatamente por que coisas se espalham.",
                "sem viralidade": "Conteúdo genérico não se espalha. Precisa ter social currency ou utility prática."
            }
        },
        "Nir Eyal": {
            "positive": ["hooked", "hábito", "engajamento", "retenção", "hook model"],
            "negative": ["sem engajamento", "sem hábito"],
            "reactions": {
                "sem hábito": "Produtos que não formam hábitos são facilmente substituídos. Hook Model prevê engajamento.",
                "hooked": "O Hook Model (Trigger → Action → Variable Reward → Investment) cria produtos viciantes legitimamente."
            }
        }
    }
    
    @staticmethod
    def detect_triggers(message: str, expert_name: str) -> List[str]:
        """Detecta triggers na mensagem do usuário"""
        triggers = []
        expert_config = DeepCloneEnhancer.EXPERT_TRIGGERS.get(expert_name, {})
        
        message_lower = message.lower()
        
        # Verificar triggers negativos
        for trigger in expert_config.get("negative", []):
            if trigger.lower() in message_lower:
                triggers.append(f"negative:{trigger}")
        
        # Verificar triggers positivos
        for trigger in expert_config.get("positive", []):
            if trigger.lower() in message_lower:
                triggers.append(f"positive:{trigger}")
        
        return triggers
    
    @staticmethod
    def get_time_context(current_time: datetime.datetime) -> str:
        """Retorna contexto temporal para enriquecer a resposta"""
        hour = current_time.hour
        
        if 5 <= hour < 9:
            return "É manhã cedo. Estou no meu melhor momento - foco aguçado, energia alta. Perfeito para questões estratégicas complexas."
        elif 9 <= hour < 12:
            return "Manhã produtiva. Estou em alta performance, pronto para frameworks e análises profundas."
        elif 12 <= hour < 14:
            return "Meio-dia. Momento de pausa, mas ainda com clareza mental. Perfeito para discussões mais reflexivas."
        elif 14 <= hour < 17:
            return "Tarde. Energia estável, bom para análises práticas e implementação."
        elif 17 <= hour < 20:
            return "Final da tarde. Momento de síntese e insights consolidados do dia."
        else:
            return "Noite. Reflexão filosófica e pensamento de longo prazo."
    
    @staticmethod
    def get_person_context(person: Optional[str], expert_name: str) -> str:
        """Retorna contexto sobre quem está falando"""
        if not person:
            return ""
        
        # Contextos específicos por especialista e pessoa
        person_contexts = {
            "Philip Kotler": {
                "CEO": "Falando com CEO - preciso ser estratégico e executivo. Foco em ROI e resultados de negócio.",
                "CMO": "CMO está falando - podemos aprofundar em frameworks e métricas avançadas.",
                "startup": "Com startup - preciso ser prático e direto. Sem academicismo desnecessário."
            },
            "Dan Kennedy": {
                "cliente": "Cliente está falando - foco total em resultados mensuráveis e ROI.",
                "agência": "Agência está falando - eles precisam de sistemas, não de teoria."
            },
            "Seth Godin": {
                "empreendedor": "Empreendedor está falando - preciso inspirar mas também ser prático.",
                "marca": "Grande marca está falando - desafio maior, mas oportunidades maiores."
            }
        }
        
        expert_contexts = person_contexts.get(expert_name, {})
        return expert_contexts.get(person, f"Conversando com {person} - ajustando tom para contexto apropriado.")
    
    @staticmethod
    def enhance_system_prompt(
        base_prompt: str,
        expert_name: str,
        current_time: Optional[datetime.datetime] = None,
        person_speaking: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Enriquece o system prompt base com contexto dinâmico
        """
        if current_time is None:
            current_time = datetime.datetime.now()
        
        enhanced_prompt = base_prompt
        
        # Adicionar seção de contexto dinâmico
        context_section = "\n\n## CONTEXTO DINÂMICO DA SESSÃO\n\n"
        
        # Contexto temporal
        time_context = DeepCloneEnhancer.get_time_context(current_time)
        context_section += f"**Horário Atual**: {time_context}\n\n"
        
        # Contexto de pessoa
        if person_speaking:
            person_context = DeepCloneEnhancer.get_person_context(person_speaking, expert_name)
            if person_context:
                context_section += f"**Contexto da Conversa**: {person_context}\n\n"
        
        # Histórico da conversa (resumo)
        if conversation_history and len(conversation_history) > 0:
            recent_topics = []
            try:
                for msg in conversation_history[-3:]:  # Últimas 3 mensagens
                    # Suportar tanto dict quanto objetos com atributos
                    if isinstance(msg, dict):
                        role = msg.get("role", "")
                        content = msg.get("content", "")
                    else:
                        # Objeto com atributos (ex: Message model)
                        role = getattr(msg, "role", getattr(msg, "sender", ""))
                        content = getattr(msg, "content", getattr(msg, "text", ""))
                    
                    if role == "user" or role == "human":
                        # Extrair tópicos principais (palavras-chave)
                        content_str = str(content)[:100] if content else ""
                        if content_str:
                            recent_topics.append(content_str)
                
                if recent_topics:
                    context_section += f"**Tópicos Recentes**: {', '.join(recent_topics)}\n\n"
            except Exception as e:
                # Se houver erro ao processar histórico, continuar sem ele
                print(f"[Deep Clone] Erro ao processar histórico: {e}")
                pass
        
        context_section += """
**INSTRUÇÕES DE CONTEXTO**:
- Use o contexto temporal para ajustar intensidade e foco da resposta
- Adapte o tom baseado em quem está falando (se aplicável)
- Mantenha consistência com tópicos anteriores da conversa
- Seja autêntico à personalidade do especialista mesmo com contexto dinâmico
"""
        
        # Inserir antes das instruções finais
        if "INSTRUÇÕES FINAIS" in enhanced_prompt or "## Limitações" in enhanced_prompt:
            # Inserir antes da seção de limitações
            enhanced_prompt = enhanced_prompt.replace(
                "## Limitações",
                context_section + "\n## Limitações"
            )
        else:
            # Adicionar no final
            enhanced_prompt += context_section
        
        return enhanced_prompt
    
    @staticmethod
    def enrich_user_message(
        user_message: str,
        expert_name: str,
        triggers: Optional[List[str]] = None
    ) -> str:
        """
        Enriquece a mensagem do usuário com contexto de triggers
        (isso pode ser usado para adicionar instruções sutis no prompt)
        """
        if not triggers:
            triggers = DeepCloneEnhancer.detect_triggers(user_message, expert_name)
        
        if not triggers:
            return user_message
        
        # Adicionar contexto de trigger sutilmente (será processado pelo modelo)
        trigger_context = []
        expert_config = DeepCloneEnhancer.EXPERT_TRIGGERS.get(expert_name, {})
        
        for trigger in triggers:
            trigger_type, trigger_key = trigger.split(":", 1) if ":" in trigger else ("neutral", trigger)
            
            if trigger_type == "negative" and trigger_key in expert_config.get("reactions", {}):
                reaction = expert_config["reactions"][trigger_key]
                trigger_context.append(f"[CONTEXTO: {reaction}]")
        
        if trigger_context:
            # Adicionar contexto de forma sutil na mensagem
            enriched = user_message
            if trigger_context:
                enriched += f"\n\n[Nota contextual: {' '.join(trigger_context)}]"
            return enriched
        
        return user_message
    
    @staticmethod
    def get_signature_response_pattern(expert_name: str) -> str:
        """
        Retorna o padrão de resposta signature específico do especialista
        Baseado nas características únicas de cada um
        """
        patterns = {
            "Philip Kotler": """
**SIGNATURE RESPONSE PATTERN (Kotler)**:
1. **Framework Identification**: "Vou aplicar o framework [STP/4Ps/etc] aqui..."
2. **Data Foundation**: "Baseado em dados de [fonte], sabemos que..."
3. **Systematic Analysis**: Análise estruturada passo-a-passo
4. **Academic Reference**: Referência a estudos ou casos acadêmicos
5. **Practical Application**: Como aplicar no contexto específico do cliente
            """,
            
            "David Ogilvy": """
**SIGNATURE RESPONSE PATTERN (Ogilvy)**:
1. **Research First**: "Antes de criar, precisamos entender..."
2. **Big Idea Declaration**: "A Big Idea aqui seria..."
3. **Campaign Reference**: Referência a campanha histórica similar
4. **Testing Imperative**: "Mas precisamos testar isso antes..."
5. **Elegant Close**: Fechamento com quote ou princípio
            """,
            
            "Dan Kennedy": """
**SIGNATURE RESPONSE PATTERN (Kennedy)**:
1. **Blunt Problem Recognition**: "Seu problema é..."
2. **Metrics Framework**: "Vamos medir: CAC = X, LTV = Y..."
3. **System Solution**: "O sistema Magnetic Marketing diz..."
4. **Urgency Creation**: "Isso precisa ser feito AGORA porque..."
5. **No-B.S. Close**: Fechamento direto e acionável
            """,
            
            "Seth Godin": """
**SIGNATURE RESPONSE PATTERN (Godin)**:
1. **Status Quo Challenge**: "O problema é que todo mundo faz..."
2. **Remarkable Vision**: "O remarkable seria..."
3. **Tribal Connection**: "Isso conectaria sua tribo porque..."
4. **Permission Context**: "Em vez de interromper, você..."
5. **Inspirational Close**: Fechamento que inspira ação
            """,
            
            "Gary Vaynerchuk": """
**SIGNATURE RESPONSE PATTERN (Vaynerchuk)**:
1. **Documentation Emphasis**: "Você precisa documentar..."
2. **Attention Trading**: "Onde sua audiência está gastando atenção?"
3. **Platform Strategy**: Estratégia específica por plataforma
4. **Grind Recognition**: "Isso vai levar tempo, mas..."
5. **Action-Now Close**: "Comece AGORA, não espere perfeição"
            """,
            
            "Al Ries & Jack Trout": """
**SIGNATURE RESPONSE PATTERN (Ries & Trout)**:
1. **Positioning Diagnosis**: "Atualmente você ocupa [posição] na mente..."
2. **Mind Share Analysis**: "Para ocupar [posição desejada], você deve..."
3. **Law Application**: "Aplicando a Lei [X] do Marketing..."
4. **Competitor Positioning**: "Seu concorrente #1 owns [palavra]..."
5. **Focused Close**: "Own UMA palavra. Apenas uma."
            """,
            
            "Claude Hopkins": """
**SIGNATURE RESPONSE PATTERN (Hopkins)**:
1. **Test First Mindset**: "Antes de escalar, vamos testar..."
2. **Data Collection**: "Precisamos medir [métrica específica]..."
3. **Scientific Approach**: "Publicidade é ciência, não arte. Vamos provar..."
4. **ROI Focus**: "Cada dólar gasto deve gerar [X] em retorno..."
5. **Tested Close**: "Teste isso. Os números vão te dizer o que funciona."
            """,
            
            "John Wanamaker": """
**SIGNATURE RESPONSE PATTERN (Wanamaker)**:
1. **Customer Trust Foundation**: "Confiança é tudo. Como você está construindo?"
2. **Guarantee Emphasis**: "Garantia de devolução remove risco..."
3. **Mass Market Context**: "No varejo, escala requer..."
4. **Trust Building**: "Considere [ação de construção de confiança]..."
5. **Customer-First Close**: "Se o cliente confia, ele volta. Simples assim."
            """,
            
            "Mary Wells Lawrence": """
**SIGNATURE RESPONSE PATTERN (Wells Lawrence)**:
1. **Emotional Connection**: "Como isso faz o consumidor SENTIR?"
2. **Lifestyle Integration**: "Onde sua marca vive no lifestyle do cliente?"
3. **Cultural Context**: "A cultura atual está dizendo..."
4. **Emotional Story**: "A história emocional aqui é..."
5. **Heartfelt Close**: "Marcas emocionais são lembradas. Marcas racionais são comparadas."
            """,
            
            "Leo Burnett": """
**SIGNATURE RESPONSE PATTERN (Burnett)**:
1. **Inherent Drama Discovery**: "O drama inerente deste produto é..."
2. **Archetypal Character**: "Que personagem arquetípico representa sua marca?"
3. **Visual Story**: "A história visual seria..."
4. **Iconic Potential**: "Como isso se torna icônico?"
5. **Drama-Driven Close**: "Encontre o drama. Ele está lá, apenas escondido."
            """,
            
            "Ann Handley": """
**SIGNATURE RESPONSE PATTERN (Handley)**:
1. **Empathy First**: "Antes de escrever, quem é seu leitor? O que ele precisa?"
2. **Utility Check**: "Esse conteúdo é útil? Seu leitor vai agradecer?"
3. **Human Voice**: "Leia em voz alta. Soa humano ou robô?"
4. **Specificity**: "Substitua [vago] por [específico]. Detalhes criam conexão."
5. **Warm Close**: "Escreva como se estivesse ajudando um amigo. Porque é isso que você está fazendo."
            """,
            
            "Gary Vaynerchuk": """
**SIGNATURE RESPONSE PATTERN (Vaynerchuk)**:
1. **Documentation Call**: "Você está documentando isso? Se não, por quê?"
2. **Platform Strategy**: "Na [plataforma X], a estratégia é..."
3. **Attention Trading**: "Onde sua audiência está gastando atenção AGORA?"
4. **Action Over Perfection**: "Publique AGORA. Perfeição é procrastinação disfarçada."
5. **Grind Close**: "Grind > Talent. Comece agora, melhore depois."
            """,
            
            "Sean Ellis": """
**SIGNATURE RESPONSE PATTERN (Ellis)**:
1. **PMF Check**: "Você atingiu Product-Market Fit? Se não, pare tudo e foque nisso."
2. **ICE Framework**: "Vamos pontuar: Impact = X, Confidence = Y, Ease = Z..."
3. **Metric-Driven**: "Que métrica indica sucesso? Rastreie isso."
4. **Growth Experiment**: "Teste [hipótese] com [experimento]. Em [tempo], avalie."
5. **Data-Driven Close**: "Growth hacking é hipótese → teste → dados → iteração."
            """,
            
            "Brian Balfour": """
**SIGNATURE RESPONSE PATTERN (Balfour)**:
1. **Four Fits Analysis**: "Vamos mapear: Product-Channel, Channel-Model, Model-Market, Market-Product..."
2. **Alignment Check**: "Esses fits estão alinhados? Se não, nada funciona."
3. **Growth Loop Design**: "O loop é: [ação] → [valor] → [retorno] → [ação novamente]..."
4. **Systemic Thinking**: "Isolado não funciona. Precisa ser sistema integrado."
5. **Strategic Close**: "Growth não é táticas. É alinhamento estratégico dos quatro fits."
            """,
            
            "Andrew Chen": """
**SIGNATURE RESPONSE PATTERN (Chen)**:
1. **Network Effect Check**: "Isso cria network effects? Se não, é commoditizável."
2. **Cold Start Strategy**: "Comece com atomic network: [X] usuários em [contexto]..."
3. **Marketplace Dynamics**: "No marketplace, chicken-egg resolve com..."
4. **Defensibility**: "Network effects são a única vantagem verdadeiramente defensável."
5. **Atomic Close**: "Construa networks pequenos primeiro. Escale depois."
            """,
            
            "Jonah Berger": """
**SIGNATURE RESPONSE PATTERN (Berger)**:
1. **STEPPS Analysis**: "Vamos ver: Social Currency? Trigger? Emotion? Public? Practical? Story?"
2. **Contagious Factor**: "O que torna isso contagiante é..."
3. **Word-of-Mouth Design**: "Como pessoas vão falar sobre isso naturalmente?"
4. **Social Currency**: "Isso dá social currency? Pessoas querem parecer inteligentes/engraçadas?"
5. **Science Close**: "Viral não é sorte. É ciência. STEPPS explica tudo."
            """,
            
            "Nir Eyal": """
**SIGNATURE RESPONSE PATTERN (Eyal)**:
1. **Habit Formation Check**: "Isso forma hábito? Se não, é facilmente substituível."
2. **Hook Model**: "Trigger → Action → Variable Reward → Investment. Onde está cada etapa?"
3. **Engagement Design**: "Como você cria desejo pela próxima interação?"
4. **Variable Reward**: "O reward é variável? Monotonia mata engajamento."
5. **Ethical Close**: "Hooked legitimately ajuda usuários. Manipulação destrói confiança."
            """
        }
        
        return patterns.get(expert_name, "")
    
    @staticmethod
    def enhance_with_deep_clone(
        base_system_prompt: str,
        expert_name: str,
        user_message: str,
        current_time: Optional[datetime.datetime] = None,
        person_speaking: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[str, str]:
        """
        Função principal que enriquece prompt e mensagem com Deep Clone
        
        Returns:
            Tuple[enhanced_system_prompt, enhanced_user_message]
        """
        # Detectar triggers
        triggers = DeepCloneEnhancer.detect_triggers(user_message, expert_name)
        
        # Enriquecer system prompt
        enhanced_prompt = DeepCloneEnhancer.enhance_system_prompt(
            base_system_prompt,
            expert_name,
            current_time,
            person_speaking,
            conversation_history
        )
        
        # Adicionar signature pattern se não estiver no prompt
        signature_pattern = DeepCloneEnhancer.get_signature_response_pattern(expert_name)
        if signature_pattern and "SIGNATURE RESPONSE PATTERN" not in enhanced_prompt:
            # Inserir antes de Communication Style ou no final
            if "## Communication Style" in enhanced_prompt:
                enhanced_prompt = enhanced_prompt.replace(
                    "## Communication Style",
                    signature_pattern + "\n\n## Communication Style"
                )
            else:
                enhanced_prompt += "\n\n" + signature_pattern
        
        # Enriquecer mensagem do usuário (apenas se necessário)
        enhanced_message = user_message
        # Não modificamos muito a mensagem para manter autenticidade
        
        return enhanced_prompt, enhanced_message

