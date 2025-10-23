"""
CrewAI Integration for Marketing Legends Cognitive Clones
"""
import os
from typing import List
from anthropic import AsyncAnthropic

class MarketingLegendAgent:
    """
    Wrapper for CrewAI Agent representing a marketing legend
    Uses Async Anthropic Claude to avoid blocking the event loop
    """
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        # Use AsyncAnthropic to avoid blocking FastAPI's event loop
        self.anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def chat(self, conversation_history: List[dict], user_message: str) -> str:
        """
        Process a chat message using the legend's cognitive clone
        
        Args:
            conversation_history: List of {role: str, content: str} messages
            user_message: New user message to process
        
        Returns:
            str: Assistant response from the cognitive clone
        """
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
            "content": user_message
        })
        
        # Call Claude with the legend's system prompt (async to avoid blocking event loop)
        response = await self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=self.system_prompt,
            messages=messages
        )
        
        # Extract text from response - handle different content block types
        for block in response.content:
            if hasattr(block, 'text'):
                return block.text
        
        # Fallback to string representation if no text attribute found
        return str(response.content[0])

class LegendAgentFactory:
    """Factory to create agents for different marketing legends"""
    
    @staticmethod
    def create_agent(expert_name: str, system_prompt: str) -> MarketingLegendAgent:
        """Create a cognitive clone agent for a marketing legend"""
        return MarketingLegendAgent(
            name=expert_name,
            system_prompt=system_prompt
        )
