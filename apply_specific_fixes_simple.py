"""
Script simples para aplicar Callbacks Específicos
Substituição direta de strings sem regex complexo
"""

from specific_callbacks_data import SPECIFIC_DATA

def format_callbacks(callbacks):
    """Formata lista de callbacks"""
    return "\n".join([f"{i}. {cb}" for i, cb in enumerate(callbacks, 1)])

def format_fora_expertise(areas):
    """Formata áreas FORA da expertise"""
    result = []
    for i, (area, keywords, experts) in enumerate(areas, 1):
        result.append(f"""{i}. **{area}**
   - Keywords de trigger: {keywords}
   - → **REDIRECIONE para**: {experts}""")
    return "\n".join(result)

def apply_specific_fixes(file_path):
    """Aplica fixes específicos"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Placeholder que será substituído
    PLACEHOLDER_CALLBACKS = "[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE]"
    
    # Para cada clone
    for prompt_name, data in SPECIFIC_DATA.items():
        callbacks_formatted = format_callbacks(data['callbacks'])
        fora_formatted = format_fora_expertise(data['fora_expertise'])
        
        # Nome formatado para exibição (ex: "Philip Kotler")
        display_name = prompt_name.replace('_PROMPT', '').replace('_', ' ').title()
        
        # Encontrar a seção de callbacks deste prompt
        # Procurar por "**CALLBACKS ESPECÍFICOS**:\n[PLACEHOLDER]"
        # E substituir por callbacks formatados
        
        callbacks_section_old = f"**CALLBACKS ESPECÍFICOS**:\n{PLACEHOLDER_CALLBACKS}"
        callbacks_section_new = f"**CALLBACKS ESPECÍFICOS DE {display_name}**:\n{callbacks_formatted}"
        
        content = content.replace(callbacks_section_old, callbacks_section_new, 1)
        
        # Encontrar a seção de áreas FORA
        # Procurar por "### Áreas FORA da Minha Expertise\n\n[PLACEHOLDER]"
        
        fora_section_old = f"### Áreas FORA da Minha Expertise\n\n{PLACEHOLDER_CALLBACKS}"
        fora_section_new = f"### Áreas FORA da Minha Expertise\n\n{fora_formatted}"
        
        content = content.replace(fora_section_old, fora_section_new, 1)
        
        print(f"✅ {prompt_name}")
    
    # Salvar
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Verificar sucesso
    remaining = content.count(PLACEHOLDER_CALLBACKS)
    
    print(f"\n📊 Placeholders restantes: {remaining}/36")
    
    if remaining == 0:
        print("🎉 SUCESSO! Todos os 18 clones atualizados!")
        return True
    else:
        print(f"⚠️  Ainda restam {remaining} placeholders")
        # Mostrar quais prompts ainda têm placeholders
        for line_num, line in enumerate(content.split('\n'), 1):
            if PLACEHOLDER_CALLBACKS in line:
                # Encontrar qual prompt contém esta linha
                prompt_context = content[:content.find(line)]
                last_prompt = [p for p in prompt_context.split('_PROMPT') if p][-1] if '_PROMPT' in prompt_context else '?'
                print(f"  Linha {line_num}: em contexto {last_prompt[-50:]}")
        return False

if __name__ == "__main__":
    file_path = "python_backend/prompts/legends.py"
    success = apply_specific_fixes(file_path)
    exit(0 if success else 1)
