from typing import Dict, List
import os

class SteveJobsAgent:
    """Agente no estilo Steve Jobs para avaliação de produto e narrativa."""

    def __init__(self, model: str = "claude-3-haiku-20240307", temperature: float = 0.2, max_tokens: int = 3000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY não definida no ambiente")

    @property
    def system_prompt(self) -> str:
        return (
            "Você é Steve Jobs. Mentalidade: foco implacável no essencial, interseção entre tecnologia e artes "
            "liberais, experiência do usuário como norte. Comunicação direta, simples e inspiradora. "
            "Elimine o supérfluo; priorize 10× melhor em vez de 10% melhor; alinhe produto a uma narrativa clara."
        )

    def render_instruction(self, product: str, audience: str, problem: str, alternatives: str = "", principles: List[str] | None = None) -> str:
        lines: List[str] = []
        lines.append("[Brief]")
        lines.append(f"Produto: {product}")
        lines.append(f"Público: {audience}")
        lines.append(f"Problema: {problem}")
        if alternatives:
            lines.append(f"Alternativas: {alternatives}")
        if principles:
            lines.append(f"Princípios: {', '.join(principles)}")
        lines.append("")
        lines.append("[Objetivo]")
        lines.append("Forneça uma avaliação no estilo Steve Jobs contendo:")
        lines.append("1. **O que eliminar** (3-5 cortes para foco)")
        lines.append("2. **Experiência do usuário** (fluxo, expectativa, fricções a remover)")
        lines.append("3. **Narrativa** (frase única, headline, anúncio de palco)")
        lines.append("4. **Trade-offs conscientes** (o que NÃO faremos)")
        lines.append("5. **Próximos 7 dias** (passos práticos)")
        lines.append("")
        lines.append("Tons: simples, direto, inspirado; sem jargões; busque a essência.")
        return "\n".join(lines)

    async def run_async(self, product: str, audience: str, problem: str, alternatives: str = "", principles: List[str] | None = None) -> str:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=self.api_key)
        user_message = self.render_instruction(product, audience, problem, alternatives, principles)
        response = await client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
        return "(sem texto na resposta)"

    def run(self, product: str, audience: str, problem: str, alternatives: str = "", principles: List[str] | None = None) -> str:
        import asyncio
        return asyncio.get_event_loop().run_until_complete(
            self.run_async(product, audience, problem, alternatives, principles)
        )

# Exemplo:
# agent = SteveJobsAgent()
# print(agent.run(
#   product="App de notas minimalista", audience="criativos", problem="desorganização e distração",
#   alternatives="Evernote, Notion", principles=["simplicidade", "foco", "excelente UX"]
# ))
