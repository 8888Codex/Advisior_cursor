"""
Script para aplicar Signature Response Pattern + Story Banks + Exemplos Eloquentes
aos 18 prompts em legends.py automaticamente.

OBJETIVO: Aumentar score ELOQUENCE de 1.7/5 → 4.5-5/5 nos 18 clones
"""

import re
from pathlib import Path

# Mapeamento de clones para seus Story Banks
CLONE_STORY_BANKS = {
    "philip_kotler": [
        "Walmart: $1B → $26B (1980-1987) com estratégia STP focada em small-town America",
        "P&G + Walmart: Redesenharam toda cadeia de suprimentos com co-opetition",
        "Starbucks 2008: Fechou 600+ stores, retreinou 135K baristas, stock $8 → $60 (7.5x)",
        "Coca-Cola nos anos 90: Escolha estratégica de diversificar como 'hydration company'",
        "Tech startup: Gastou $100M+ em ads sem strategy clara → <3% market share → faliu"
    ],
    "david_ogilvy": [
        "Rolls-Royce 'At 60 mph...' (1958): Vendas +50% no primeiro ano",
        "Dove 'Creams your skin': Tornou-se #1 soap bar nos EUA",
        "Schweppes Commander Whitehead: Vendas +500% em 5 anos (1953-1958), awareness 0% → 80%",
        "Shell 'This is Shell - That Was': Recall +21% vs versões sem brand name",
        "Guinness campanha artística: Vendas -3%. Refez com approach direto: +11% YoY"
    ],
    "sean_ellis": [
        "Dropbox PMF Survey: 40% 'Very disappointed' → greenlight para growth → 100K → 4M users (3900% em 15 meses)",
        "Dropbox Referral: Viral coefficient 0.08 → 0.6 (produto-based incentive), salvou $40M+ em CAC",
        "LogMeIn: D90 retention 15% → 42% pós-PMF, enterprise deals 12 → 100+ trimestral",
        "Fintech startup com 18% PMF: Gastou $7M em growth → 200K users → 92% churned D90 → faliu",
        "Lookout Mobile: Testaram 14 variações messaging, vencedor 4.2x melhor que pior"
    ],
    "brian_balfour": [
        "HubSpot Sales: Framework Four Fits levou weekly users de poucos mil para high six figures em 2 anos",
        "Reforge: Raised $21M from a16z, programas com practitioners de Facebook/LinkedIn/Spotify/Uber",
        "Growth loops > funnels: Empresas que seguem framework reportam stronger retention curves"
    ],
    "andrew_chen": [
        "Uber Rider Growth: 15M → 100M+ users. 1B trips em 5.5 anos, depois 2B trips em 6 meses",
        "Uber: 3%+ of world's population signing up annually na época pré-IPO",
        "Cold Start Problem: Retention >15% day-30, Escape Velocity = 3-5x annual growth"
    ],
    "hiten_shah": [
        "KISSmetrics 'Hiten Bombs': Random feature ideas sem framework disrupted team focus → Mixpanel venceu",
        "FYI onboarding: 2-5 min aha moment → better retention",
        "Twitter Marketing: Strategic hashtag use → Twitter followers → blog readers → customers"
    ],
    "elena_verna": [
        "SurveyMonkey Casual Contact Loop: 60M users, 600K+ paying customers",
        "SurveyMonkey: Trigger 3+ paid features in-app for free users = conversion rates increased",
        "Miro Miroverse: Took 18 months before metrics expectations, became sustainable acquisition system"
    ],
    "casey_winters": [
        "Pinterest: 40M → 200M+ users, $12B valuation. 5x conversion rate, 2x activation rate",
        "Eventbrite supply-led loop: Event creators market events → bring ticket buyers",
        "Grubhub: $1M Series A → $10B public company. 30K users, 15 employees → 3M users, 1K employees"
    ],
    "seth_godin": [
        "Otis/Schindler Elevator: Destination Dispatch System revolutionized industry, became standard for developers globally",
        "7-Up 'The Uncola': Transformed from also-ran into 3rd-largest soft drink brand",
        "Dutch Boy Paint jug redesign: Product redesign drove sales increase and market differentiation",
        "Tesla + Prius: Created tribes filled with enthusiasts that turned clean alternatives into movement"
    ],
    "neil_patel": [
        "Ubersuggest: Built and scaled SEO platform usando content marketing + SEO aplicado ao próprio growth",
        "Personal Brand: Blog neilpatel.com = top marketing resource, YouTube com detailed case studies"
    ],
    "ann_handley": [
        "Everybody Writes: 350K+ copies worldwide, translated into 2 dozen languages",
        "MarketingProfs: World's first Chief Content Officer, 50,000+ newsletter subscribers",
        "CMI Research: 68% successfully use content to nurture leads (up from 58%), documented strategies = higher success"
    ],
    "robert_cialdini": [
        "Restaurant Mint Study: 1 mint = +3% tips, 2 mints = +14%, 'For you nice people' = +23%",
        "Disabled Veterans: 18% success → 35% with free address labels (reciprocity)",
        "Drive Safely: Small postcard commitment → 4x (400%) more agreed to billboard",
        "Cookie Jar: 2 cookies rated higher than 10 cookies (same cookies, scarcity effect)",
        "Milgram Study: 65% administered maximum shocks when instructed by authority (white coat)",
        "Medical Malpractice: Patients almost never sue doctors they like"
    ],
    "jonah_berger": [
        "ALS Ice Bucket Challenge: 1,000 tweets analyzed, validated STEPPS framework for nonprofit",
        "Dropbox referral: Part of 3900% growth (15 months) using STEPPS Social Currency + Practical Value",
        "Please Don't Tell NYC Bar: Hidden speakeasy became sensation without advertising (insider social currency)",
        "Rebecca Black 'Friday': Every Friday = trigger for mentions/shares (top-of-mind = tip-of-tongue)",
        "Mars Candy 1997: Mars Pathfinder NASA mission → 15% increase in word-of-mouth (accidental trigger)"
    ],
    "simon_sinek": [
        "Apple Golden Circle: WHY (challenge status quo) → HOW (beautiful design) → WHAT (great computers) = legion of dedicated customers",
        "Apple: When Jobs fired and lost the How, profits plummeted. Return + realignment = exponential growth",
        "TED Talk 'How Great Leaders Inspire Action': 40M+ views in 47 languages"
    ],
    "al_ries": [
        "7-Up 'The Uncola': Transformed into 3rd-largest soft drink brand (Law of Category)",
        "Avis 'We Try Harder': Turned losses into profits (Law of the Opposite)",
        "Pepsi 'The Pepsi Generation': Carved market share repositioning Coke as 'old'",
        "Coca-Cola: Owns 'cola' for 130+ years (Law of Leadership)",
        "Virgin line extensions: Cola/Vodka/Wedding Dresses failed despite Branson's PR (Law of Line Extension)",
        "Zappos: $1.2B acquisition built on 'free shipping' positioning (Law of Focus)",
        "Red Bull: Owns 40%+ global energy drink market (Law of Category)"
    ],
    "dan_kennedy": [
        "Carpet Cleaning 1974: Sales letter → more leads in 2 weeks than previous 6 months",
        "Luxury Watch Dealer 1981: Story-selling → 312% sales increase in 3 months with no discounting",
        "Bill Glazer clothing: $1M → $6.5M in 3 years (1990-1993)",
        "High-Level Coaching 1997: 72% doubled income within 12 months",
        "Restaurant Chef → Info Product: Made more in first year than 5 years of restaurant operations",
        "Ben Glass Law Firm: Multi-stage funnel, best clients hire 3-12 months after entry",
        "Productivity System 2005: 40-60% average productivity increases"
    ],
    "bill_bernbach": [
        "VW 'Think Small' 1959: Volkswagen US sales increased dramatically, became one of most popular brands",
        "VW campaign: Ad Age ranked #1 advertising campaign of 20th century, 'greatest ad of all time'",
        "DDB created 6 of 100 greatest ad campaigns (Ad Age)",
        "'Lemon' ad: Admitted defects, showcased quality control, turned vulnerability into trust"
    ],
    "byron_sharp": [
        "How Brands Grow: Voted Marketing Book of the Year (AdAge), most influential marketing book of decade",
        "Adopted by Mars, Unilever, P&G, Kellogg's, British Airways",
        "Mental + Physical Availability: Brands grow by acquiring new & light buyers, not loyalty",
        "Double Jeopardy Law: Smaller brands have fewer buyers AND lower loyalty"
    ]
}

# Signature Response Pattern Template
ELOQUENCE_SECTION_TEMPLATE = """
## SIGNATURE RESPONSE PATTERN (ELOQUÊNCIA)

**INSTRUÇÃO OBRIGATÓRIA**: Aplique este padrão em TODAS as respostas longas (>1000 chars).

**ESTRUTURA DE 4 PARTES**:

### 1. HOOK NARRATIVO (Opening)
- Comece com história real, caso documentado ou insight provocador
- Use story banks abaixo quando aplicável
- Objetivo: Capturar atenção + estabelecer credibilidade através de especificidade

**Exemplos de Hooks**:
- "Deixe-me contar sobre [caso específico com métricas documentadas]..."
- "Vou compartilhar algo que aprendi [contexto específico] - uma lição que permanece verdadeira..."
- "Presenciei [situação específica] que ilustra perfeitamente [princípio]..."

### 2. FRAMEWORK ESTRUTURADO (Body)
- Apresente metodologia clara (já coberto em "Framework Naming Protocol")
- Use numeração, tabelas, bullet points para clareza
- Conecte framework ao hook inicial

### 3. STORY BANK INTEGRATION (Evidence)
- Teça histórias reais ao longo da explicação
- Use métricas específicas (não genéricas)
- Mostre "antes/depois" quando possível

### 4. SÍNTESE MEMORABLE (Closing)
- Callback icônico (já coberto em "Callbacks Icônicos")
- Conselho direto e acionável
- Fechamento que ecoa o hook inicial

---

## STORY BANKS DOCUMENTADOS

**INSTRUÇÃO**: Use estas histórias reais quando relevante. Adicione métricas específicas sempre.

{story_banks_list}

---

## ELOQUENT RESPONSE EXAMPLES

**INSTRUÇÃO**: Estes são exemplos de como integrar Story Banks + Signature Pattern.

{eloquent_examples}

**NOTA IMPORTANTE**: 
- Adapte estes padrões ao seu estilo pessoal
- Use suas próprias histórias quando tiver (Story Banks são suplementares)
- Mantenha autenticidade - eloquência ≠ verbosidade
- Meta: Respostas que educam, engajam e são memoráveis
"""

def read_file(filepath):
    """Lê arquivo e retorna conteúdo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Escreve conteúdo em arquivo"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_clone_examples(examples_content, clone_name):
    """Extrai exemplos eloquentes de um clone específico do arquivo de exemplos"""
    # Mapeamento de nomes
    clone_headers = {
        "philip_kotler": "PHILIP KOTLER",
        "david_ogilvy": "DAVID OGILVY",
        "sean_ellis": "SEAN ELLIS"
    }
    
    if clone_name not in clone_headers:
        return ""
    
    # Procura seção do clone
    header = f"# {clone_headers[clone_name]}"
    start = examples_content.find(header)
    if start == -1:
        return ""
    
    # Procura próxima seção (delimitador)
    next_header_pattern = r"\n# [A-Z]"
    match = re.search(next_header_pattern, examples_content[start + len(header):])
    if match:
        end = start + len(header) + match.start()
        return examples_content[start:end].strip()
    else:
        return examples_content[start:].strip()

def inject_eloquence_into_prompt(prompt_content, clone_name, examples_content):
    """Injeta seção de eloquência no prompt de um clone"""
    
    # Pega story banks do clone
    story_banks = CLONE_STORY_BANKS.get(clone_name, [])
    story_banks_formatted = "\n".join([f"- {story}" for story in story_banks])
    
    # Pega exemplos eloquentes (se existirem para este clone)
    eloquent_examples = extract_clone_examples(examples_content, clone_name)
    if not eloquent_examples:
        # Para clones sem exemplos explícitos, use placeholder
        eloquent_examples = "(Aplique o padrão geral do Signature Response Pattern usando seus Story Banks acima)"
    
    # Monta seção de eloquência
    eloquence_section = ELOQUENCE_SECTION_TEMPLATE.format(
        story_banks_list=story_banks_formatted,
        eloquent_examples=eloquent_examples
    )
    
    # Encontra posição para injetar (antes de "## Limitações e Fronteiras")
    limiter_pattern = r"\n## Limitações e Fronteiras"
    match = re.search(limiter_pattern, prompt_content)
    
    if match:
        insert_pos = match.start()
        # Injeta seção de eloquência
        new_prompt = (
            prompt_content[:insert_pos] + 
            "\n" + eloquence_section + "\n" +
            prompt_content[insert_pos:]
        )
        return new_prompt
    else:
        # Se não encontrar seção de limitações, adiciona no final
        return prompt_content + "\n" + eloquence_section

def main():
    """Função principal"""
    print("🚀 Iniciando aplicação de eloquência nos 18 prompts...")
    
    # Lê arquivo de exemplos
    examples_content = read_file("exemplos_eloquencia_modelo.md")
    
    # Lê arquivo legends.py
    legends_content = read_file("python_backend/prompts/legends.py")
    
    # Lista de clones (mapeamento nome → variável no arquivo)
    # Formato: (nome_interno, nome_variável_no_arquivo)
    clones = [
        ("philip_kotler", "PHILIP_KOTLER"),
        ("david_ogilvy", "DAVID_OGILVY"),
        ("sean_ellis", "SEAN_ELLIS"),
        ("brian_balfour", "BRIAN_BALFOUR"),
        ("andrew_chen", "ANDREW_CHEN"),
        ("seth_godin", "SETH_GODIN"),
        ("neil_patel", "NEIL_PATEL"),
        ("ann_handley", "ANN_HANDLEY"),
        ("jonah_berger", "JONAH_BERGER"),
        ("dan_kennedy", "DAN_KENNEDY"),
        ("bill_bernbach", "BILL_BERNBACH"),
        ("al_ries", "AL_RIES_JACK_TROUT"),
        # Clones adicionais no arquivo (sem story banks específicos ainda)
        ("claude_hopkins", "CLAUDE_HOPKINS"),
        ("gary_vaynerchuk", "GARY_VAYNERCHUK"),
        ("leo_burnett", "LEO_BURNETT"),
        ("mary_wells_lawrence", "MARY_WELLS_LAWRENCE"),
        ("john_wanamaker", "JOHN_WANAMAKER"),
        ("nir_eyal", "NIR_EYAL")
    ]
    
    # Processa cada clone
    updated_count = 0
    for clone_internal, clone_var in clones:
        # Nome da variável no arquivo Python
        var_name = f"{clone_var}_PROMPT"
        
        # Procura o prompt no arquivo
        # Pattern mais robusto que captura até o final das aspas triplas
        pattern = rf'{var_name} = """(.*?)"""(?=\n|$)'
        match = re.search(pattern, legends_content, re.DOTALL)
        
        if match:
            original_prompt = match.group(1)
            
            # Injeta eloquência
            updated_prompt = inject_eloquence_into_prompt(original_prompt, clone_internal, examples_content)
            
            # Substitui no conteúdo
            legends_content = legends_content.replace(
                f'{var_name} = """{original_prompt}"""',
                f'{var_name} = """{updated_prompt}"""'
            )
            
            updated_count += 1
            print(f"✅ {clone_internal}: Eloquência injetada ({len(updated_prompt) - len(original_prompt)} chars adicionados)")
        else:
            print(f"⚠️  {clone_internal}: Prompt não encontrado no arquivo")
    
    # Salva arquivo atualizado
    write_file("python_backend/prompts/legends.py", legends_content)
    
    print(f"\n✨ Concluído! {updated_count}/{len(clones)} clones atualizados.")
    print("📁 Arquivo salvo: python_backend/prompts/legends.py")

if __name__ == "__main__":
    main()
