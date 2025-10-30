"""
Script de teste A/B simples para validar Conversational Guidelines

Compara respostas de experts com e sem conversational guidelines
para verificar se as diretrizes melhoram a naturalidade e engajamento.
"""

import os
import asyncio
from anthropic import AsyncAnthropic
from python_backend.prompts.template_master import _build_conversational_guidelines
from python_backend.storage import storage


async def test_expert_with_guidelines(expert_name: str, problem: str, with_guidelines: bool = True):
    """
    Testa um expert com ou sem conversational guidelines
    
    Returns:
        Tuple[str, str]: (expert_name, response_text)
    """
    # Buscar expert
    experts = await storage.get_experts()
    expert = next((e for e in experts if e.name == expert_name), None)
    
    if not expert:
        return expert_name, f"Expert {expert_name} não encontrado"
    
    # Preparar system prompt
    if with_guidelines:
        # Adicionar guidelines ao prompt
        base_prompt = expert.systemPrompt
        guidelines = _build_conversational_guidelines("consultor")
        system_prompt = f"{base_prompt}\n\n{guidelines}"
    else:
        system_prompt = expert.systemPrompt
    
    # Preparar mensagem do usuário
    user_message = f"""**Problema/Questão:**
{problem}

**Sua Tarefa:**
Como {expert.name}, forneça sua análise especializada para este problema. Seja natural e conversacional."""

    # Chamar Claude
    anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    try:
        response = await anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": user_message
            }]
        )
        
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text = block.text
                break
        
        return expert_name, response_text
    except Exception as e:
        return expert_name, f"Erro: {str(e)}"


async def run_ab_test():
    """
    Executa teste A/B comparando respostas com e sem guidelines
    """
    test_problem = "Como posso melhorar meu engajamento nas redes sociais para uma empresa B2B?"
    
    test_experts = ["Philip Kotler", "Neil Patel", "Ann Handley"]  # 2-3 experts para teste
    
    print("=" * 80)
    print("TESTE A/B: CONVERSATIONAL GUIDELINES")
    print("=" * 80)
    print(f"\nProblema de teste: {test_problem}\n")
    
    results = []
    
    for expert_name in test_experts:
        print(f"\n{'='*80}")
        print(f"TESTANDO: {expert_name}")
        print(f"{'='*80}\n")
        
        # Teste SEM guidelines
        print(f"[SEM GUIDELINES]")
        print("-" * 80)
        _, response_without = await test_expert_with_guidelines(expert_name, test_problem, with_guidelines=False)
        print(response_without[:500] + "..." if len(response_without) > 500 else response_without)
        print()
        
        # Aguardar um pouco entre chamadas
        await asyncio.sleep(2)
        
        # Teste COM guidelines
        print(f"[COM GUIDELINES]")
        print("-" * 80)
        _, response_with = await test_expert_with_guidelines(expert_name, test_problem, with_guidelines=True)
        print(response_with[:500] + "..." if len(response_with) > 500 else response_with)
        print()
        
        # Análise rápida
        print(f"[ANÁLISE RÁPIDA]")
        print("-" * 80)
        has_acknowledge = any(word in response_with.lower() for word in ["entendi", "faz sentido", "vejo que"])
        has_question = "?" in response_with
        has_next_steps = any(word in response_with.lower() for word in ["próximo", "próximos passos", "próxima ação"])
        
        print(f"✓ Reconhece contexto: {'SIM' if has_acknowledge else 'NÃO'}")
        print(f"✓ Pergunta de avanço: {'SIM' if has_question else 'NÃO'}")
        print(f"✓ Próximos passos: {'SIM' if has_next_steps else 'NÃO'}")
        print()
        
        results.append({
            "expert": expert_name,
            "with_guidelines": {
                "has_acknowledge": has_acknowledge,
                "has_question": has_question,
                "has_next_steps": has_next_steps,
                "length": len(response_with)
            },
            "without_guidelines": {
                "length": len(response_without)
            }
        })
        
        await asyncio.sleep(2)  # Delay entre experts
    
    # Resumo final
    print("\n" + "=" * 80)
    print("RESUMO DO TESTE A/B")
    print("=" * 80)
    print("\nComparação:")
    for result in results:
        print(f"\n{result['expert']}:")
        print(f"  - Com guidelines: {result['with_guidelines']['length']} chars | "
              f"Acknowledge: {result['with_guidelines']['has_acknowledge']} | "
              f"Pergunta: {result['with_guidelines']['has_question']} | "
              f"Next steps: {result['with_guidelines']['has_next_steps']}")
        print(f"  - Sem guidelines: {result['without_guidelines']['length']} chars")
    
    print("\n" + "=" * 80)
    print("CONCLUSÃO:")
    print("=" * 80)
    total_with = sum(1 for r in results if r['with_guidelines']['has_acknowledge'] and 
                     r['with_guidelines']['has_question'] and r['with_guidelines']['has_next_steps'])
    print(f"Experts com todas as melhorias: {total_with}/{len(results)}")
    print("\nSe a maioria dos experts mostrar reconhecimento + pergunta + próximos passos,")
    print("as guidelines conversacionais estão funcionando!")


if __name__ == "__main__":
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv, find_dotenv
    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
    
    asyncio.run(run_ab_test())

