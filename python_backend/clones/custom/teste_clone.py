"""
Clone Cognitivo: Teste
Auto-gerado via sistema de Auto-Clone
Framework EXTRACT completo de 20 pontos
"""
from python_backend.clones.base import ExpertCloneBase

class TesteClone(ExpertCloneBase):
    """
    Especialista Teste
    
    Bio: Teste de salvamento...
    
    Expertise: Marketing
    
    Framework EXTRACT: 20 pontos de fidelidade cognitiva
    Quality Score: 20/20
    """
    
    def __init__(self):
        super().__init__()
        
        # Identity Core
        self.name = "Teste"
        self.title = "Especialista Teste"
        self.expertise = ['Marketing']
        self.bio = """Teste de salvamento"""
        
        # System prompt EXTRACT completo
        self._system_prompt = """System prompt teste"""
    
    def get_system_prompt(self, context: dict = None) -> str:
        """
        Retorna o system prompt EXTRACT completo
        
        Este clone foi gerado automaticamente via Auto-Clone e contém
        Framework EXTRACT de 20 pontos com máxima fidelidade cognitiva.
        
        Args:
            context: Contexto opcional para personalização
            
        Returns:
            System prompt completo
        """
        return self._system_prompt
    
    def apply_signature_framework(self, problem: str, context: dict = None) -> str:
        """
        Aplica framework característico do especialista
        
        Este é um clone auto-gerado, então usa o system prompt completo
        como base para qualquer análise.
        
        Args:
            problem: Problema ou questão a analisar
            context: Contexto adicional
            
        Returns:
            Análise usando framework do especialista
        """
        # Para clones auto-gerados, delega para process_input
        return self.process_input(problem, context)
    
    def process_input(self, user_input: str, context: dict = None) -> str:
        """
        Processa input do usuário usando personalidade do clone
        
        Args:
            user_input: Input do usuário
            context: Contexto adicional
            
        Returns:
            Resposta processada (deve ser enviada para LLM com system_prompt)
        """
        # Clone auto-gerado: retorna instrução para usar com LLM
        return f"[Use o system prompt deste clone com o LLM para responder: {user_input}]"
