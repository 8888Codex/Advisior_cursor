from typing import List, Dict, Any
import os

class CouncilConsensusAgent:
    """
    Agente para síntese de consenso entre especialistas de marketing.
    Usa Anthropic Claude através da variável de ambiente ANTHROPIC_API_KEY.
    """

    def __init__(self, model: str = "claude-3-haiku-20240307", temperature: float = 0.3, max_tokens: int = 4000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY não definida no ambiente")

    @property
    def system_prompt(self) -> str:
        return (
            "Você é um orquestrador de conselho de especialistas em marketing. "
            "Sua função é sintetizar diversas contribuições em um consenso coeso, claro e acionável, "
            "escrito em português do Brasil, usando Markdown com negritos e listas para clareza. "
            "Priorize recomendações praticáveis e objetivas."
        )

    def render_instruction(self, problem: str, contributions: List[Dict[str, str]], research_findings: str = "") -> str:
        lines: List[str] = []
        lines.append("[CONTEXTO]")
        lines.append("Problema do usuário:")
        lines.append(problem)
        lines.append("")
        lines.append("Contribuições dos especialistas (nomes e conteúdos):")
        for c in contributions:
            lines.append(f"- {c.get('expert','Expert')}: {c.get('content','')}")
        lines.append("")
        if research_findings:
            lines.append("Achados de pesquisa (opcional):")
            lines.append(research_findings)
            lines.append("")
        lines.append("[OBJETIVO]")
        lines.append("Produza um relatório de consenso estruturado contendo:")
        lines.append("1. **Síntese Geral** (2-3 parágrafos)")
        lines.append("2. **5 Insights-Chave do Consenso**")
        lines.append("3. **5 Recomendações Prioritárias** (claras e acionáveis)")
        lines.append("4. **Perspectivas Divergentes** (se houver)")
        lines.append("5. **Próximos 15 minutos** (ação imediata)")
        lines.append("6. **Risco Principal**")
        lines.append("7. **Pergunta de Avanço**")
        lines.append("")
        lines.append("Regras: português do Brasil; use Markdown; seja específico e prático; não invente fontes.")
        return "\n".join(lines)

    async def run_async(self, problem: str, contributions: List[Dict[str, str]], research_findings: str = "") -> str:
        """Executa a síntese chamando a API da Anthropic de forma assíncrona."""
        from anthropic import AsyncAnthropic

        client = AsyncAnthropic(api_key=self.api_key)
        user_message = self.render_instruction(problem, contributions, research_findings)
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

    def run(self, problem: str, contributions: List[Dict[str, str]], research_findings: str = "") -> str:
        """Executa de forma síncrona (útil onde async não é prático)."""
        import asyncio
        return asyncio.get_event_loop().run_until_complete(
            self.run_async(problem, contributions, research_findings)
        )

# Exemplo de uso:
# agent = CouncilConsensusAgent()
# result = agent.run(
#     problem="Quero aumentar a conversão do meu e-commerce de 1,2% para 2,5%",
#     contributions=[{"expert": "Ann Handley", "content": "Foque em copy clara e prova social."}],
# )
# print(result)
