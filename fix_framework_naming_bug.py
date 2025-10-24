#!/usr/bin/env python3
"""
FIX CRÍTICO: Remove exemplos de frameworks errados do template universal

PROBLEMA: Template do FRAMEWORK NAMING PROTOCOL contém exemplos como:
- "STEPPS (meu framework)" → É de Jonah Berger, não de Philip Kotler!
- "Growth Loops Framework que desenvolvi" → É de Brian Balfour!

Esses exemplos estão fazendo TODOS os 18 clones roubarem crédito de frameworks
que não criaram.

SOLUÇÃO: Substituir exemplos problemáticos por exemplos GENÉRICOS que podem
ser usados por qualquer clone.
"""

import re

# Ler arquivo atual
with open("python_backend/prompts/legends.py", "r", encoding="utf-8") as f:
    content = f.read()

# Padrão problemático a ser substituído
OLD_EXAMPLES = '''**EXEMPLOS**:
- "Vou aplicar o framework **STP** (Segmentation-Targeting-Positioning) aqui..."
- "Usando os **4Ps** do Marketing Mix para estruturar sua estratégia..."
- "Vou usar **STEPPS** (meu framework de viralidade) para analisar isso..."
- "Aplicando **Growth Loops Framework** que desenvolvi..."'''

# Novos exemplos GENÉRICOS (sem roubar crédito de ninguém)
NEW_EXAMPLES = '''**EXEMPLOS GENÉRICOS** (adapte aos seus próprios frameworks):
- "Vou aplicar o framework **[SEU FRAMEWORK]** aqui..."
- "Usando **[SUA METODOLOGIA]** para estruturar esta análise..."
- "Conforme o modelo **[SEU MODELO]** que desenvolvi..."
- "Aplicando os princípios de **[SEU CONCEITO]** neste caso..."'''

# Contar quantas vezes aparece (deve ser ~18 vezes, uma por clone)
count_before = content.count("STEPPS")
print(f"🔍 Encontradas {count_before} ocorrências de 'STEPPS' (framework de Jonah Berger)")

count_growth_loops = content.count("Growth Loops Framework")
print(f"🔍 Encontradas {count_growth_loops} ocorrências de 'Growth Loops Framework' (de Brian Balfour)")

# Substituir TODAS as ocorrências do padrão problemático
content_fixed = content.replace(OLD_EXAMPLES, NEW_EXAMPLES)

# Verificar quantas substituições foram feitas
count_after_stepps = content_fixed.count("STEPPS")
count_after_growth = content_fixed.count("Growth Loops Framework")

print(f"\n✅ Substituições realizadas:")
print(f"   - STEPPS: {count_before} → {count_after_stepps}")
print(f"   - Growth Loops: {count_growth_loops} → {count_after_growth}")

# Salvar arquivo corrigido
with open("python_backend/prompts/legends.py", "w", encoding="utf-8") as f:
    f.write(content_fixed)

print(f"\n✓ Arquivo corrigido: python_backend/prompts/legends.py")
print(f"✓ Template universal agora usa exemplos GENÉRICOS")
print(f"✓ Cada clone deve usar apenas seus PRÓPRIOS frameworks nos callbacks específicos")
