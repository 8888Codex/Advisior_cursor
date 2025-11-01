"""
CrewAI Integration for Marketing Legends Cognitive Clones
Com sistema Deep Clone para profundidade e contexto
"""
import os
import datetime
from typing import List, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv, find_dotenv
from python_backend.deep_clone import DeepCloneEnhancer

# Carregar .env quando o módulo é importado
_env_file = find_dotenv(usecwd=True)
if _env_file:
    load_dotenv(_env_file)

class MarketingLegendAgent:
    """
    Wrapper for CrewAI Agent representing a marketing legend
    Uses Async Anthropic Claude to avoid blocking the event loop
    Enhanced with Deep Clone system for contextual depth
    """
    
    def __init__(self, name: str, system_prompt: str, enable_deep_clone: bool = False):
        self.name = name
        self.base_system_prompt = system_prompt
        self.enable_deep_clone = enable_deep_clone
        # Carregar .env novamente para garantir (pode ter mudado)
        _env_file = find_dotenv(usecwd=True)
        if _env_file:
            load_dotenv(_env_file)
        
        # Use AsyncAnthropic to avoid blocking FastAPI's event loop
        anthropic_key = os.getenv("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not anthropic_key:
            raise ValueError(
                "ANTHROPIC_API_KEY não encontrada. "
                "Verifique se o arquivo .env existe e contém ANTHROPIC_API_KEY=sk-ant-..."
            )
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)
    
    async def chat(
        self, 
        conversation_history: List[dict], 
        user_message: str,
        current_time: Optional[datetime.datetime] = None,
        person_speaking: Optional[str] = None
    ) -> str:
        """
        Process a chat message using the legend's cognitive clone
        Enhanced with Deep Clone system for contextual depth
        
        Args:
            conversation_history: List of {role: str, content: str} messages
            user_message: New user message to process
            current_time: Optional datetime for temporal context
            person_speaking: Optional person context (who is speaking)
        
        Returns:
            str: Assistant response from the cognitive clone
        """
        # Apply Deep Clone enhancement if enabled
        if self.enable_deep_clone:
            try:
                enhanced_prompt, enhanced_message = DeepCloneEnhancer.enhance_with_deep_clone(
                    self.base_system_prompt,
                    self.name,
                    user_message,
                    current_time or datetime.datetime.now(),
                    person_speaking,
                    conversation_history
                )
                system_prompt_to_use = enhanced_prompt
                message_to_use = enhanced_message
            except Exception as e:
                # Se Deep Clone falhar, usar prompt original (fail-safe)
                print(f"[MarketingLegendAgent] Erro no Deep Clone, usando prompt original: {e}")
                import traceback
                traceback.print_exc()
                system_prompt_to_use = self.base_system_prompt
                message_to_use = user_message
        else:
            system_prompt_to_use = self.base_system_prompt
            message_to_use = user_message
        
        # Build full message history for Claude
        messages = []
        
        # Add conversation history (excluding the current user message)
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add new user message
        messages.append({
            "role": "user",
            "content": message_to_use
        })
        
        # Call Claude with the enhanced system prompt (async to avoid blocking event loop)
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                system=system_prompt_to_use,
                messages=messages
            )
            
            # Extract text from response - handle different content block types
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
                elif block.type == 'text':
                    return block.text
            
            # Fallback to string representation if no text attribute found
            if response.content and len(response.content) > 0:
                return str(response.content[0])
            return "Erro: Resposta vazia da API"
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                raise ValueError(
                    f"Erro de autenticação com Anthropic API: {error_msg}. "
                    "Verifique se ANTHROPIC_API_KEY está configurada corretamente no .env"
                )
            raise

class LegendAgentFactory:
    """
    Factory to create agents for different marketing legends
    
    Suporta duas abordagens (backward compatible):
    1. Classes Python completas (novo) - se disponível
    2. Prompt-based (antigo) - fallback
    """
    
    @staticmethod
    def create_agent(expert_name: str, system_prompt: str, enable_deep_clone: bool = True) -> MarketingLegendAgent:
        """
        Create a cognitive clone agent for a marketing legend
        
        Args:
            expert_name: Nome do especialista
            system_prompt: System prompt (usado se clone Python não existir)
            enable_deep_clone: Se True, tenta usar classe Python; se False, usa prompt
            
        Returns:
            MarketingLegendAgent configurado (prompt-based ou class-based)
        """
        # Tentar usar classe Python se disponível (novo sistema)
        if enable_deep_clone:
            try:
                from python_backend.clones.registry import CloneRegistry
                
                clone_class = CloneRegistry.get_clone(expert_name)
                
                if clone_class:
                    # ✅ CLONE PYTHON DISPONÍVEL - Usar sistema novo!
                    print(f"[LegendAgentFactory] ✨ Usando clone Python para {expert_name}")
                    
                    # Criar instância do clone
                    clone_instance = clone_class()
                    
                    # Gerar system prompt dinâmico da classe
                    dynamic_prompt = clone_instance.get_system_prompt()
                    
                    # Criar agent com prompt dinâmico
                    agent = MarketingLegendAgent(
                        name=expert_name,
                        system_prompt=dynamic_prompt,
                        enable_deep_clone=True
                    )
                    
                    # Anexar instância do clone para uso posterior
                    agent._clone_instance = clone_instance
                    
                    return agent
            
            except Exception as e:
                # Se falhar, continua com fallback
                print(f"[LegendAgentFactory] ⚠️  Erro ao carregar clone Python para {expert_name}: {e}")
                print(f"[LegendAgentFactory] 🔄 Usando fallback (prompt-based)")
        
        # ✅ FALLBACK - Usar sistema antigo (prompt-based)
        # Isso garante que nada quebra durante a migração!
        return MarketingLegendAgent(
            name=expert_name,
            system_prompt=system_prompt,
            enable_deep_clone=enable_deep_clone
        )
