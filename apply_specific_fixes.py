"""
Script para aplicar Callbacks Específicos e Áreas FORA da Expertise
em todos os 18 clones em legends.py
"""

import re
from specific_callbacks_data import SPECIFIC_DATA

def format_callbacks(callbacks):
    """Formata lista de callbacks para inserção no prompt"""
    formatted = []
    for i, callback in enumerate(callbacks, 1):
        formatted.append(f"{i}. {callback}")
    return "\n".join(formatted)

def format_fora_expertise(areas):
    """Formata áreas FORA da expertise para inserção no prompt"""
    formatted = []
    for i, (area, keywords, experts) in enumerate(areas, 1):
        formatted.append(f"""
{i}. **{area}**
   - Keywords de trigger: {keywords}
   - → **REDIRECIONE para**: {experts}""")
    return "\n".join(formatted)

def apply_specific_fixes(file_path):
    """Aplica callbacks específicos e áreas FORA da expertise"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Para cada clone, substituir placeholders
    for prompt_name, data in SPECIFIC_DATA.items():
        # Encontrar o prompt específico
        prompt_pattern = rf'({prompt_name}_PROMPT = """.*?)(\[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE\])(.*?""")'
        
        matches = list(re.finditer(prompt_pattern, content, re.DOTALL))
        
        if len(matches) >= 2:
            # Primeiro placeholder: CALLBACKS ESPECÍFICOS
            callbacks_text = format_callbacks(data['callbacks'])
            
            # Segundo placeholder: Áreas FORA da Expertise
            fora_text = format_fora_expertise(data['fora_expertise'])
            
            # Substituir placeholders
            # Estratégia: substituir um de cada vez de trás para frente (para não quebrar índices)
            
            # Encontrar todos os placeholders neste prompt
            prompt_start = content.find(f'{prompt_name}_PROMPT = """')
            prompt_end = content.find('"""', content.find('"""', prompt_start) + 3) + 3
            prompt_content = content[prompt_start:prompt_end]
            
            # Substituir placeholders
            modified_prompt = prompt_content
            
            # Substituir na seção CALLBACKS ESPECÍFICOS
            modified_prompt = modified_prompt.replace(
                "**CALLBACKS ESPECÍFICOS**:\n[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE]",
                f"**CALLBACKS ESPECÍFICOS DE {prompt_name.replace('_', ' ').title()}**:\n{callbacks_text}"
            )
            
            # Substituir na seção Áreas FORA da Expertise
            modified_prompt = re.sub(
                r'### Áreas FORA da Minha Expertise\n+\[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE\]',
                f"### Áreas FORA da Minha Expertise\n{fora_text}",
                modified_prompt
            )
            
            # Substituir no conteúdo completo
            content = content[:prompt_start] + modified_prompt + content[prompt_end:]
            
            print(f"✅ {prompt_name}: Callbacks e áreas FORA aplicados")
        else:
            print(f"⚠️  {prompt_name}: Não encontrado ou estrutura inesperada ({len(matches)} matches)")
    
    # Salvar arquivo modificado
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ Fixes Específicos aplicados com sucesso!")
    print(f"📊 Arquivo modificado: {file_path}")
    
    # Verificar se todos os placeholders foram substituídos
    remaining_placeholders = content.count("[SERÁ PREENCHIDO NA PRÓXIMA TASK - ESPECÍFICO POR CLONE]")
    
    if remaining_placeholders == 0:
        print("🎉 Todos os placeholders foram substituídos!")
        return True
    else:
        print(f"⚠️  Ainda restam {remaining_placeholders} placeholders não substituídos")
        return False

if __name__ == "__main__":
    file_path = "python_backend/prompts/legends.py"
    success = apply_specific_fixes(file_path)
    exit(0 if success else 1)
