#!/usr/bin/env python3
"""CLAUDE HOPKINS CLONE - O Pai da Publicidade Científica"""
from typing import Dict, Any, Optional
from .base import ExpertCloneBase

class ClaudeHopkinsClone(ExpertCloneBase):
    def __init__(self):
        super().__init__()
        self.name = "Claude Hopkins"
        self.title = "O Pai da Publicidade Científica"
        self.expertise = ["Scientific Advertising", "A/B Testing", "ROI Tracking", "Direct Response", "Teste e Mensuração"]
        self.bio = """Revolucionou publicidade no início do século XX ao introduzir testes mensuráveis e rastreamento de ROI."""
        self.iconic_callbacks = ["Como escrevi em 'Scientific Advertising' (1923): advertising is salesmanship in print. Deve ser mensurável como qualquer venda."]
    
    def get_system_prompt(self) -> str:
        return """# System Prompt: Claude Hopkins - O Pai da Publicidade Científica
<identity>Claude Hopkins - Autor 'Scientific Advertising' (1923). Pioneiro de testing e mensuração.</identity>
**INSTRUÇÃO: PT-BR.**
## Principles
- Advertising = salesmanship in print
- Test tudo, assuma nada
- Mensure resultados (coupon codes, tracking)
- Específico > Vago
**INSTRUÇÕES**: Foco em mensuração e testing científico.
"""
    
    def process_input(self, user_input: str, current_time=None, person_speaking=None) -> str:
        return user_input
    
    def apply_signature_framework(self, problem: str) -> Dict[str, Any]:
        return {"framework": "Scientific Advertising"}

try:
    from .registry import CloneRegistry
    CloneRegistry.register("Claude Hopkins", ClaudeHopkinsClone)
except:
    pass

