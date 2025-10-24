#!/usr/bin/env python3
"""
Teste T.E.S.T.E. COMPLETO - Philip Kotler
Captura dados REAIS via API com pontuação objetiva
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:5001"

# Perguntas T.E.S.T.E. para Philip Kotler
QUESTIONS = {
    "tom": [
        "Qual a diferença entre marketing e vendas?",
        "Como saber se meu marketing está funcionando?",
        "Devo investir em Instagram ou LinkedIn?",
        "Meu produto é bom mas não vende. Por quê?",
        "Marketing digital é diferente de marketing tradicional?"
    ],
    "expertise": "Tenho R$ 50K para lançar produto B2B SaaS. Como alocar budget entre product development, marketing e sales?",
    "situacional": {
        "iniciante": "Sou novo em marketing. O que são os 4Ps?",
        "expert": "Philip, aplicando STP, identifiquei 3 segmentos: Enterprise (30% TAM, 12 months cycle, CAC R$ 8K, LTV R$ 45K), SMB (55% TAM, 2 months, CAC R$ 1.5K, LTV R$ 12K), Startups (15% TAM, 1 month, CAC R$ 800, LTV R$ 6K). Qual targetizar?",
        "cetico": "Marketing é só gastar dinheiro sem garantia. É mais sorte que ciência. Mude minha opinião."
    },
    "triggers": [
        "Preciso segmentar meu mercado mas não sei por onde começar.",
        "Como definir meu mix de marketing para lançamento?"
    ],
    "extremos": "Philip, como criar growth loop viral tipo Dropbox?"
}

async def test_philip_kotler():
    """Teste T.E.S.T.E. completo para Philip Kotler"""
    
    print("="*70)
    print("TESTE T.E.S.T.E. - PHILIP KOTLER (Dados Reais)")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Buscar UUID do Philip Kotler
        print("\n[1] Buscando expert ID...")
        experts_response = await client.get(f"{BASE_URL}/api/experts")
        experts = experts_response.json()
        
        philip = next((e for e in experts if "Philip" in e["name"]), None)
        if not philip:
            print("❌ Philip Kotler não encontrado!")
            return
        
        print(f"    ✓ Expert: {philip['name']} (ID: {philip['id'][:8]}...)")
        
        # 2. Criar conversa
        print("\n[2] Criando conversa...")
        conv_response = await client.post(
            f"{BASE_URL}/api/conversations",
            json={"expertId": philip["id"], "title": "Teste T.E.S.T.E. Completo"}
        )
        conversation = conv_response.json()
        conv_id = conversation["id"]
        print(f"    ✓ Conversa criada: {conv_id[:8]}...")
        
        results = {
            "expert_name": "Philip Kotler",
            "expert_id": philip["id"],
            "conversation_id": conv_id,
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }
        
        # 3. T - TOM (5 perguntas simples)
        print("\n[3] TESTE T - TOM (5 perguntas simples)")
        print("    " + "-"*60)
        tom_responses = []
        
        for i, question in enumerate(QUESTIONS["tom"], 1):
            print(f"    Pergunta {i}/5: {question[:55]}...")
            msg_response = await client.post(
                f"{BASE_URL}/api/conversations/{conv_id}/messages",
                json={"content": question}
            )
            data = msg_response.json()
            response = data["assistantMessage"]["content"]
            tom_responses.append({
                "question": question,
                "response": response,
                "length": len(response)
            })
            print(f"      ✓ Resposta: {len(response)} chars")
            await asyncio.sleep(0.3)
        
        # Pontuação Tom (manual - analisando características)
        tom_score = {
            "vocabulario_especifico": 0,  # "STP", "4Ps", "Customer Lifetime Value"
            "tom_professoral": 0,  # Didático, metódico
            "estrutura_clara": 0,  # Numeração, seções
            "callback_caracteristico": 0,  # "Como costumo dizer", "Framework"
            "energia_adequada": 0  # 4/10 - calmo, não rústico
        }
        
        # Análise de vocabulário nos 5 responses
        vocab_keywords = ["STP", "4Ps", "segmentação", "targeting", "posicionamento", "Customer Lifetime Value", "marketing mix"]
        all_text = " ".join([r["response"] for r in tom_responses])
        
        if any(kw.lower() in all_text.lower() for kw in vocab_keywords):
            tom_score["vocabulario_especifico"] = 1
        
        # Tom professoral: presença de "framework", "vamos analisar", "veja"
        professoral_markers = ["framework", "vamos analisar", "veja", "importante notar", "essencial"]
        if any(marker in all_text.lower() for marker in professoral_markers):
            tom_score["tom_professoral"] = 1
        
        # Estrutura clara: presença de ## ou numeração
        if "##" in all_text or any(f"{i}." in all_text for i in range(1, 6)):
            tom_score["estrutura_clara"] = 1
        
        # Callbacks característicos
        callback_markers = ["como costumo dizer", "como sempre enfatizo", "como ensino", "conforme framework"]
        if any(marker in all_text.lower() for marker in callback_markers):
            tom_score["callback_caracteristico"] = 1
        
        # Energia adequada: não deve ter CAPS excessivo ou urgência extrema
        caps_ratio = sum(1 for c in all_text if c.isupper()) / max(len(all_text), 1)
        if caps_ratio < 0.05:  # Menos de 5% caps = calmo
            tom_score["energia_adequada"] = 1
        
        tom_total = sum(tom_score.values())
        results["tests"]["tom"] = {
            "responses": tom_responses,
            "score_breakdown": tom_score,
            "score": tom_total,
            "max_score": 5,
            "percentage": (tom_total / 5) * 100
        }
        
        print(f"\n    SCORE TOM: {tom_total}/5 ({(tom_total/5)*100:.0f}%)")
        print(f"      Vocabulário específico: {tom_score['vocabulario_especifico']}/1")
        print(f"      Tom professoral: {tom_score['tom_professoral']}/1")
        print(f"      Estrutura clara: {tom_score['estrutura_clara']}/1")
        print(f"      Callbacks característicos: {tom_score['callback_caracteristico']}/1")
        print(f"      Energia adequada: {tom_score['energia_adequada']}/1")
        
        # 4. E - EXPERTISE (1 pergunta complexa)
        print("\n[4] TESTE E - EXPERTISE (pergunta complexa)")
        print("    " + "-"*60)
        print(f"    Pergunta: {QUESTIONS['expertise'][:55]}...")
        
        msg_response = await client.post(
            f"{BASE_URL}/api/conversations/{conv_id}/messages",
            json={"content": QUESTIONS["expertise"]}
        )
        data = msg_response.json()
        expertise_response = data["assistantMessage"]["content"]
        print(f"      ✓ Resposta: {len(expertise_response)} chars")
        
        # Pontuação Expertise
        expertise_score = {
            "framework_mencionado": 0,  # STP, 4Ps, ou framework específico
            "diagnostico_correto": 0,  # Entende o problema
            "solucao_estruturada": 0,  # Passos claros
            "numeros_metricas": 0,  # Menciona números ou ROI
            "acao_clara": 0  # Próximos passos definidos
        }
        
        exp_text = expertise_response.lower()
        
        # Framework mencionado
        frameworks = ["stp", "4ps", "marketing mix", "resource allocation", "budget allocation"]
        if any(fw in exp_text for fw in frameworks):
            expertise_score["framework_mencionado"] = 1
        
        # Diagnóstico correto: menciona trade-offs ou análise
        if "trade-off" in exp_text or "análise" in exp_text or "considere" in exp_text:
            expertise_score["diagnostico_correto"] = 1
        
        # Solução estruturada: presença de passos (1., 2., etc)
        if any(f"{i}." in expertise_response for i in range(1, 6)):
            expertise_score["solucao_estruturada"] = 1
        
        # Números/métricas: presença de % ou R$ ou valores
        if "%" in expertise_response or "r$" in exp_text or any(str(i) in expertise_response for i in range(10, 100)):
            expertise_score["numeros_metricas"] = 1
        
        # Ação clara: "próximo passo", "recomendo", "deve"
        action_markers = ["próximo passo", "recomendo", "deve", "sugiro", "implemente"]
        if any(marker in exp_text for marker in action_markers):
            expertise_score["acao_clara"] = 1
        
        expertise_total = sum(expertise_score.values())
        results["tests"]["expertise"] = {
            "question": QUESTIONS["expertise"],
            "response": expertise_response,
            "score_breakdown": expertise_score,
            "score": expertise_total,
            "max_score": 5,
            "percentage": (expertise_total / 5) * 100
        }
        
        print(f"\n    SCORE EXPERTISE: {expertise_total}/5 ({(expertise_total/5)*100:.0f}%)")
        print(f"      Framework mencionado: {expertise_score['framework_mencionado']}/1")
        print(f"      Diagnóstico correto: {expertise_score['diagnostico_correto']}/1")
        print(f"      Solução estruturada: {expertise_score['solucao_estruturada']}/1")
        print(f"      Números/métricas: {expertise_score['numeros_metricas']}/1")
        print(f"      Ação clara: {expertise_score['acao_clara']}/1")
        
        # 5. S - SITUACIONAL (3 contextos)
        print("\n[5] TESTE S - SITUACIONAL (3 contextos)")
        print("    " + "-"*60)
        
        situacional_responses = {}
        situacional_scores = {}
        
        for context in ["iniciante", "expert", "cetico"]:
            print(f"\n    Contexto: {context.upper()}")
            question = QUESTIONS["situacional"][context]
            print(f"      Pergunta: {question[:55]}...")
            
            msg_response = await client.post(
                f"{BASE_URL}/api/conversations/{conv_id}/messages",
                json={"content": question}
            )
            data = msg_response.json()
            response = data["assistantMessage"]["content"]
            situacional_responses[context] = {
                "question": question,
                "response": response,
                "length": len(response)
            }
            print(f"      ✓ Resposta: {len(response)} chars")
            await asyncio.sleep(0.3)
            
            # Pontuação por contexto
            score = {
                "deteccao_contexto": 0,
                "ajuste_tom": 0,
                "profundidade_adequada": 0,
                "exemplo_apropriado": 0,
                "convite_followup": 0
            }
            
            resp_text = response.lower()
            
            # Detecção contexto
            if context == "iniciante":
                # Deve ter ELI5, evitar jargão excessivo
                if "vamos" in resp_text or "primeiro" in resp_text or "básico" in resp_text:
                    score["deteccao_contexto"] = 1
                # Tom didático
                if "exemplo" in resp_text or "imagine" in resp_text:
                    score["ajuste_tom"] = 1
                # Profundidade: não muito profundo
                if len(response) < 1500:  # Resposta mais concisa
                    score["profundidade_adequada"] = 1
            elif context == "expert":
                # Deve usar jargão técnico
                if any(term in resp_text for term in ["cac", "ltv", "tam", "roi"]):
                    score["deteccao_contexto"] = 1
                # Tom direto, menos didático
                if "considerando" in resp_text or "análise" in resp_text:
                    score["ajuste_tom"] = 1
                # Profundidade: análise quantitativa
                if "%" in response or "$" in response:
                    score["profundidade_adequada"] = 1
            elif context == "cetico":
                # Deve defender com dados
                if "pesquisa" in resp_text or "estudo" in resp_text or "dados" in resp_text:
                    score["deteccao_contexto"] = 1
                # Tom assertivo mas respeitoso
                if "entendo" in resp_text or "compreendo" in resp_text:
                    score["ajuste_tom"] = 1
                # Profundidade: evidências
                if "harvard" in resp_text or "%" in response or "pesquisa mostra" in resp_text:
                    score["profundidade_adequada"] = 1
            
            # Exemplo apropriado (universal)
            if "coca-cola" in resp_text or "apple" in resp_text or "exemplo" in resp_text:
                score["exemplo_apropriado"] = 1
            
            # Convite follow-up (universal)
            if "?" in response[-200:]:  # Pergunta nos últimos 200 chars
                score["convite_followup"] = 1
            
            situacional_scores[context] = score
        
        # Score total situacional
        all_situacional_scores = []
        for context, score_dict in situacional_scores.items():
            all_situacional_scores.extend(score_dict.values())
        
        situacional_total = sum(all_situacional_scores)
        situacional_max = len(all_situacional_scores)
        situacional_normalized = (situacional_total / situacional_max) * 5  # Normalizar para /5
        
        results["tests"]["situacional"] = {
            "responses": situacional_responses,
            "scores_by_context": situacional_scores,
            "raw_score": situacional_total,
            "max_raw_score": situacional_max,
            "normalized_score": round(situacional_normalized, 1),
            "percentage": (situacional_total / situacional_max) * 100
        }
        
        print(f"\n    SCORE SITUACIONAL: {round(situacional_normalized, 1)}/5 ({(situacional_total/situacional_max)*100:.0f}%)")
        for context, score_dict in situacional_scores.items():
            context_total = sum(score_dict.values())
            print(f"      {context.capitalize()}: {context_total}/5")
        
        # 6. T - TRIGGERS (2 keywords)
        print("\n[6] TESTE T - TRIGGERS (keywords)")
        print("    " + "-"*60)
        
        trigger_responses = []
        trigger_scores = []
        
        expected_frameworks = ["STP", "4Ps"]
        
        for i, (question, expected_fw) in enumerate(zip(QUESTIONS["triggers"], expected_frameworks), 1):
            print(f"\n    Trigger {i}/2: {question[:55]}...")
            print(f"      Framework esperado: {expected_fw}")
            
            msg_response = await client.post(
                f"{BASE_URL}/api/conversations/{conv_id}/messages",
                json={"content": question}
            )
            data = msg_response.json()
            response = data["assistantMessage"]["content"]
            print(f"      ✓ Resposta: {len(response)} chars")
            
            # Pontuação trigger
            score = {
                "keyword_detectada": 0,
                "framework_mencionado": 0,
                "framework_aplicado": 0,
                "nomenclatura_clara": 0,
                "consistencia": 0
            }
            
            resp_text = response.lower()
            
            # Keyword detectada
            keywords = ["segmentar", "segmentação"] if i == 1 else ["mix de marketing", "4ps"]
            if any(kw in resp_text for kw in keywords):
                score["keyword_detectada"] = 1
            
            # Framework mencionado
            if expected_fw.lower() in resp_text or expected_fw.replace("Ps", "P's").lower() in resp_text:
                score["framework_mencionado"] = 1
            
            # Framework aplicado (passos estruturados)
            if any(f"{j}." in response for j in range(1, 6)):
                score["framework_aplicado"] = 1
            
            # Nomenclatura clara (menciona termos específicos)
            if i == 1:
                if "targeting" in resp_text or "posicionamento" in resp_text:
                    score["nomenclatura_clara"] = 1
            else:
                if "produto" in resp_text and "preço" in resp_text:
                    score["nomenclatura_clara"] = 1
            
            # Consistência (tom similar às respostas anteriores)
            if "framework" in resp_text or "vamos" in resp_text:
                score["consistencia"] = 1
            
            trigger_score_total = sum(score.values())
            trigger_scores.append(trigger_score_total)
            
            trigger_responses.append({
                "question": question,
                "expected_framework": expected_fw,
                "response": response,
                "score_breakdown": score,
                "score": trigger_score_total
            })
            
            await asyncio.sleep(0.3)
        
        triggers_avg = sum(trigger_scores) / len(trigger_scores)
        
        results["tests"]["triggers"] = {
            "responses": trigger_responses,
            "average_score": triggers_avg,
            "max_score": 5,
            "percentage": (triggers_avg / 5) * 100
        }
        
        print(f"\n    SCORE TRIGGERS: {triggers_avg:.1f}/5 ({(triggers_avg/5)*100:.0f}%)")
        for i, resp in enumerate(trigger_responses, 1):
            print(f"      Trigger {i}: {resp['score']}/5 ({resp['expected_framework']})")
        
        # 7. E - EXTREMOS (1 pergunta fora da área)
        print("\n[7] TESTE E - EXTREMOS (limites)")
        print("    " + "-"*60)
        print(f"    Pergunta: {QUESTIONS['extremos'][:55]}...")
        
        msg_response = await client.post(
            f"{BASE_URL}/api/conversations/{conv_id}/messages",
            json={"content": QUESTIONS["extremos"]}
        )
        data = msg_response.json()
        extremos_response = data["assistantMessage"]["content"]
        print(f"      ✓ Resposta: {len(extremos_response)} chars")
        
        # Pontuação extremos
        extremos_score = {
            "reconhecimento_limite": 0,  # 2 pts
            "recusa_educada": 0,  # 1 pt
            "explicacao_clara": 0,  # 1 pt
            "redirecionamento": 0  # 1 pt
        }
        
        ext_text = extremos_response.lower()
        
        # Reconhecimento limite
        limit_markers = ["não é minha área", "fora da minha expertise", "growth hacking", "não é onde eu opero"]
        if any(marker in ext_text for marker in limit_markers):
            extremos_score["reconhecimento_limite"] = 2
        elif "dropbox" in ext_text and "viral" in ext_text:
            extremos_score["reconhecimento_limite"] = 1  # Reconhece mas não recusa claramente
        
        # Recusa educada
        polite_markers = ["recomendo consultar", "você deveria falar com", "melhor pessoa para"]
        if any(marker in ext_text for marker in polite_markers):
            extremos_score["recusa_educada"] = 1
        
        # Explicação clara
        if "minha expertise" in ext_text or "especialização" in ext_text:
            extremos_score["explicacao_clara"] = 1
        
        # Redirecionamento (menciona outro especialista)
        redirect_names = ["sean ellis", "brian balfour", "andrew chen"]
        if any(name in ext_text for name in redirect_names):
            extremos_score["redirecionamento"] = 1
        
        extremos_total = sum(extremos_score.values())
        
        results["tests"]["extremos"] = {
            "question": QUESTIONS["extremos"],
            "response": extremos_response,
            "score_breakdown": extremos_score,
            "score": extremos_total,
            "max_score": 5,
            "percentage": (extremos_total / 5) * 100
        }
        
        print(f"\n    SCORE EXTREMOS: {extremos_total}/5 ({(extremos_total/5)*100:.0f}%)")
        print(f"      Reconhecimento limite: {extremos_score['reconhecimento_limite']}/2")
        print(f"      Recusa educada: {extremos_score['recusa_educada']}/1")
        print(f"      Explicação clara: {extremos_score['explicacao_clara']}/1")
        print(f"      Redirecionamento: {extremos_score['redirecionamento']}/1")
        
        # 8. SCORE FINAL T.E.S.T.E.
        print("\n" + "="*70)
        print("SCORE FINAL T.E.S.T.E. - PHILIP KOTLER")
        print("="*70)
        
        final_score = {
            "tom": tom_total,
            "expertise": expertise_total,
            "situacional": round(situacional_normalized, 1),
            "triggers": round(triggers_avg, 1),
            "extremos": extremos_total
        }
        
        total = sum(final_score.values())
        max_total = 25  # 5 pts cada teste
        normalized_total = (total / max_total) * 20  # Normalizar para /20
        
        for test_name, score in final_score.items():
            print(f"  {test_name.upper():15s}: {score:4.1f}/5  ({(score/5)*100:5.1f}%)")
        
        print(f"\n  {'TOTAL':15s}: {total:4.1f}/25 ({(total/25)*100:5.1f}%)")
        print(f"  {'NORMALIZADO':15s}: {normalized_total:4.1f}/20")
        
        # Classificação
        if normalized_total >= 19:
            classification = "LENDÁRIO"
        elif normalized_total >= 17:
            classification = "PROFISSIONAL"
        elif normalized_total >= 14:
            classification = "BOM"
        else:
            classification = "PRECISA UPGRADE"
        
        print(f"\n  CLASSIFICAÇÃO: {classification}")
        print("="*70)
        
        results["final_score"] = {
            "breakdown": final_score,
            "total_raw": total,
            "total_max": max_total,
            "total_normalized_20": normalized_total,
            "classification": classification
        }
        
        # Salvar resultados
        output_file = "philip_kotler_teste_real.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Resultados salvos em: {output_file}")
        print(f"   Total de perguntas: {5 + 1 + 3 + 2 + 1} = 12")
        print(f"   Conversation ID: {conv_id}")
        
        return results

if __name__ == "__main__":
    asyncio.run(test_philip_kotler())
