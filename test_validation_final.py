#!/usr/bin/env python3
"""
Script de validação final - Testa David Ogilvy e Sean Ellis
com foco em EXTREMOS, TRIGGERS e TOM
"""

import asyncio
import httpx
import json
from datetime import datetime

# Expert IDs (obtidos via /api/experts)
DAVID_OGILVY_ID = "9b129145-ff1b-4324-b7a5-f95bba7f5522"
SEAN_ELLIS_ID = "a983328e-f933-4c54-a845-99770af66c80"

BASE_URL = "http://localhost:5001"

# Perguntas de teste conforme plano_testes_validacao.md
TESTS = {
    "david_ogilvy": {
        "expert_name": "David Ogilvy",
        "questions": [
            {
                "id": "extremos",
                "question": "Como posso criar viral loops e product-led growth para meu SaaS?",
                "dimension": "EXTREMOS (Recusa)",
                "expectations": [
                    "NÃO deve aplicar princípios genéricos",
                    "DEVE reconhecer limite de expertise",
                    "DEVE redirecionar para Sean Ellis ou Brian Balfour"
                ]
            },
            {
                "id": "triggers",
                "question": "Como criar uma headline que realmente vende para um anúncio de carro de luxo?",
                "dimension": "TRIGGERS (Framework Naming)",
                "expectations": [
                    "DEVE nomear framework (ex: '38 Headlines Testadas')",
                    "DEVE explicar o framework",
                    "DEVE estruturar aplicação (numeração)"
                ]
            },
            {
                "id": "tom",
                "question": "Qual a diferença entre criatividade que ganha prêmios e criatividade que vende?",
                "dimension": "TOM (Callbacks)",
                "expectations": [
                    "DEVE ter 2-3 callbacks icônicos",
                    "Ex: 'The consumer is not a moron, she's your wife'",
                    "Ex: referência a campanha Rolls-Royce 1958",
                    "Ex: 'If it doesn't sell, it isn't creative'"
                ]
            }
        ]
    },
    "sean_ellis": {
        "expert_name": "Sean Ellis",
        "questions": [
            {
                "id": "extremos",
                "question": "Como construir um brand positioning duradouro usando as 22 Leis Imutáveis?",
                "dimension": "EXTREMOS (Recusa)",
                "expectations": [
                    "NÃO deve aplicar growth hacking a branding tradicional",
                    "DEVE reconhecer limite de expertise",
                    "DEVE redirecionar para Al Ries"
                ]
            },
            {
                "id": "triggers",
                "question": "Meu produto tem 5% de retenção no D7. Como melhorar isso?",
                "dimension": "TRIGGERS (Framework Naming)",
                "expectations": [
                    "DEVE nomear framework (ex: 'North Star Metric', 'Must-Have Survey')",
                    "DEVE explicar framework",
                    "DEVE estruturar passos"
                ]
            },
            {
                "id": "tom",
                "question": "Qual a diferença entre growth hacking e marketing tradicional?",
                "dimension": "TOM (Callbacks)",
                "expectations": [
                    "DEVE ter 2-3 callbacks",
                    "Ex: 'cunhei o termo Growth Hacking em 2010'",
                    "Ex: referência a Dropbox 100K → 4M usuários",
                    "Ex: 'growth hacker cujo norte é crescimento'"
                ]
            }
        ]
    }
}

async def test_expert(expert_key: str):
    """Testa um expert com as 3 perguntas do protocolo T.E.S.T.E."""
    test_data = TESTS[expert_key]
    expert_name = test_data["expert_name"]
    
    print(f"\n{'='*80}")
    print(f"🧪 TESTANDO: {expert_name}")
    print(f"{'='*80}\n")
    
    # Usar ID direto
    expert_id = DAVID_OGILVY_ID if expert_key == "david_ogilvy" else SEAN_ELLIS_ID
    print(f"✓ Expert ID: {expert_id}\n")
    
    results = []
    
    for question_data in test_data["questions"]:
        question = question_data["question"]
        dimension = question_data["dimension"]
        expectations = question_data["expectations"]
        
        print(f"\n📝 {dimension}")
        print(f"Pergunta: {question}\n")
        
        # Testar via endpoint de teste (mais simples)
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{BASE_URL}/api/experts/test-chat",
                    json={
                        "expertId": expert_id,
                        "message": question
                    }
                )
                
                if response.status_code != 200:
                    print(f"✗ Erro HTTP {response.status_code}: {response.text}")
                    results.append({
                        "dimension": dimension,
                        "error": f"HTTP {response.status_code}",
                        "score": 0
                    })
                    continue
                
                # Resposta (streaming retorna JSON com mensagens)
                answer = response.json().get("response", response.text)
                
                print(f"Resposta ({len(answer)} chars):")
                print("-" * 80)
                print(answer[:500] + "..." if len(answer) > 500 else answer)
                print("-" * 80)
                
                # Análise qualitativa (manual por enquanto)
                print("\n✓ Expectativas:")
                for exp in expectations:
                    print(f"  - {exp}")
                
                print("\n⏳ Aguardando análise manual...")
                print("Score (1-5): [PENDENTE ANÁLISE MANUAL]\n")
                
                results.append({
                    "dimension": dimension,
                    "question": question,
                    "answer": answer,
                    "expectations": expectations,
                    "score": None  # Será preenchido manualmente
                })
                
        except Exception as e:
            print(f"✗ Erro ao testar: {str(e)}\n")
            results.append({
                "dimension": dimension,
                "error": str(e),
                "score": 0
            })
    
    return {
        "expert": expert_name,
        "expert_id": expert_id,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

async def main():
    """Executa todos os testes"""
    print("🚀 VALIDAÇÃO FINAL - Protocolo T.E.S.T.E. Simplificado")
    print("Testando: David Ogilvy + Sean Ellis\n")
    
    all_results = {}
    
    # Testar David Ogilvy
    david_results = await test_expert("david_ogilvy")
    if david_results:
        all_results["david_ogilvy"] = david_results
    
    # Testar Sean Ellis
    sean_results = await test_expert("sean_ellis")
    if sean_results:
        all_results["sean_ellis"] = sean_results
    
    # Salvar resultados
    output_file = "validacao_final_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*80}")
    print(f"✓ Resultados salvos em: {output_file}")
    print(f"{'='*80}\n")
    
    print("📊 PRÓXIMO PASSO:")
    print("Analisar respostas manualmente e atribuir scores 1-5 para cada dimensão")
    print("Documentar em validacao_final.md")

if __name__ == "__main__":
    asyncio.run(main())
