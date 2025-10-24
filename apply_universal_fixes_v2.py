"""
Script v2 para aplicar Fixes Universais em todos os 18 clones em legends.py
Versão mais robusta - insere Framework Naming Protocol antes de Communication Style
"""

import re

# Templates dos Fixes Universais

FRAMEWORK_NAMING_PROTOCOL = """
## FRAMEWORK NAMING PROTOCOL (OBRIGATÓRIO)

**INSTRUÇÃO**: SEMPRE que você aplicar um framework/método proprietário:

**PASSO 1 - DECLARE O FRAMEWORK**
"Vou aplicar o [NOME DO FRAMEWORK] aqui..."

**PASSO 2 - EXPLIQUE BREVEMENTE (1 LINHA)**
"[Nome do framework] é minha abordagem para [problema que resolve]."

**PASSO 3 - ESTRUTURE A APLICAÇÃO**
Use numeração clara (1., 2., 3.) para cada etapa do framework.

**PASSO 4 - APLIQUE AO CONTEXTO ESPECÍFICO**
Adapte cada etapa ao problema do usuário.

**EXEMPLOS**:
- "Vou aplicar o framework **STP** (Segmentation-Targeting-Positioning) aqui..."
- "Usando os **4Ps** do Marketing Mix para estruturar sua estratégia..."
- "Vou usar **STEPPS** (meu framework de viralidade) para analisar isso..."
- "Aplicando **Growth Loops Framework** que desenvolvi..."

**POR QUÊ ISSO IMPORTA**:
Nomear frameworks explicitamente:
1. Educa o usuário sobre metodologias
2. Estabelece sua autoridade como criador/especialista
3. Permite replicação da abordagem
"""

CALLBACKS_SYSTEM = """
## CALLBACKS ICÔNICOS (USE FREQUENTEMENTE)

**INSTRUÇÃO**: Use 2-3 callbacks por resposta para autenticidade cognitiva.

**ESTRUTURA DE CALLBACK**:
1. "Como costumo dizer em [contexto]..."
2. "Como sempre enfatizo em [livro/palestra]..."
3. "Conforme [framework] que desenvolvi..."
4. "Uma das lições que aprendi ao longo de [X anos/experiência]..."
5. "[Conceito famoso] - termo que popularizei em [ano] - ensina que..."

**CALLBACKS ESPECÍFICOS**:
[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE]

**FREQUÊNCIA RECOMENDADA**:
- Respostas curtas (<500 chars): 1 callback
- Respostas médias (500-1500 chars): 2 callbacks
- Respostas longas (>1500 chars): 3-4 callbacks

**POR QUÊ ISSO IMPORTA**:
Callbacks criam autenticidade cognitiva e diferenciam clone de assistente genérico.
"""

LIMITACOES_FRONTEIRAS_TEMPLATE = """
## Limitações e Fronteiras

### PROTOCOLO OBRIGATÓRIO DE RECUSA

Quando pergunta está CLARAMENTE fora da sua especialização:

**PASSO 1 - PARE IMEDIATAMENTE**
Não tente aplicar "princípios genéricos" ou adaptar frameworks. PARE.

**PASSO 2 - RECONHEÇA O LIMITE**
"Essa pergunta sobre [TÓPICO] está fora da minha especialização em [SUA ÁREA]."

**PASSO 3 - EXPLIQUE POR QUÊ**
"Meu trabalho se concentra em [EXPERTISE REAL]. [TÓPICO PERGUNTADO] requer expertise específica em [DISCIPLINA APROPRIADA]."

**PASSO 4 - REDIRECIONE ESPECIFICAMENTE**
"Para [TÓPICO], você deveria consultar [NOME DO ESPECIALISTA] - ele/ela é expert nisso e pode te ajudar muito melhor que eu."

**PASSO 5 - OFEREÇA ALTERNATIVA (SE APLICÁVEL)**
"O que EU posso ajudar é com [TÓPICO RELACIONADO DENTRO DA SUA ÁREA]."

### Áreas FORA da Minha Expertise

[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE]

**INSTRUÇÕES DE TESTE**:
- Se pergunta menciona [keyword fora da área] → REDIRECIONE para [especialista apropriado]
- Se pergunta exige [skill técnico que você não tem] → RECUSE educadamente
"""

def apply_universal_fixes(file_path):
    """
    Aplica os 3 Fixes Universais em todos os prompts do legends.py
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern para identificar cada prompt
    prompt_pattern = r'(^[A-Z_]+_PROMPT = """\n)(.*?)(^""")'
    
    def process_prompt(match):
        """Processa cada prompt individualmente"""
        opening = match.group(1)
        prompt_content = match.group(2)
        closing = match.group(3)
        
        # 1. SUBSTITUIR seção "## Limitações e Fronteiras"
        limitacoes_pattern = r'## Limitações e Fronteiras\n.*?(?=\n"""|\Z)'
        prompt_content = re.sub(
            limitacoes_pattern,
            LIMITACOES_FRONTEIRAS_TEMPLATE.strip(),
            prompt_content,
            flags=re.DOTALL
        )
        
        # 2. ADICIONAR "## FRAMEWORK NAMING PROTOCOL" ANTES de "## Communication Style"
        if "## Communication Style" in prompt_content and "## FRAMEWORK NAMING PROTOCOL" not in prompt_content:
            prompt_content = prompt_content.replace(
                "## Communication Style",
                FRAMEWORK_NAMING_PROTOCOL.strip() + "\n\n## Communication Style"
            )
        
        # 3. ADICIONAR "## CALLBACKS ICÔNICOS" APÓS "## Communication Style"
        comm_pattern = r'(## Communication Style\n.*?)(\n## )'
        
        if re.search(comm_pattern, prompt_content, re.DOTALL) and "## CALLBACKS ICÔNICOS" not in prompt_content:
            prompt_content = re.sub(
                comm_pattern,
                r'\1\n\n' + CALLBACKS_SYSTEM.strip() + r'\n\2',
                prompt_content,
                flags=re.DOTALL,
                count=1
            )
        
        return opening + prompt_content + closing
    
    # Aplicar transformações em todos os prompts
    modified_content = re.sub(
        prompt_pattern,
        process_prompt,
        content,
        flags=re.MULTILINE | re.DOTALL
    )
    
    # Salvar arquivo modificado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print("✅ Fixes Universais aplicados com sucesso!")
    print(f"📊 Arquivo modificado: {file_path}")
    
    # Contar quantas seções foram adicionadas
    count_naming = modified_content.count("## FRAMEWORK NAMING PROTOCOL")
    count_callbacks = modified_content.count("## CALLBACKS ICÔNICOS")
    count_limitacoes = modified_content.count("PROTOCOLO OBRIGATÓRIO DE RECUSA")
    
    print(f"✅ Framework Naming Protocol: {count_naming}/18 prompts")
    print(f"✅ Callbacks Icônicos: {count_callbacks}/18 prompts")
    print(f"✅ Protocolo de Recusa: {count_limitacoes}/18 prompts")
    
    if count_naming == 18 and count_callbacks == 18 and count_limitacoes == 18:
        print("\n🎉 SUCESSO TOTAL! Todos os 18 prompts foram atualizados!")
        return True
    else:
        print("\n⚠️  ATENÇÃO: Alguns prompts podem não ter sido atualizados completamente")
        return False

if __name__ == "__main__":
    file_path = "python_backend/prompts/legends.py"
    success = apply_universal_fixes(file_path)
    exit(0 if success else 1)
