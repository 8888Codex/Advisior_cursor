"""
Teste CRÍTICO de Philip Kotler - Foco nos 3 Gaps que Corrigimos
Mais rápido: apenas 6 perguntas em vez de 12
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

# Perguntas focadas nos gaps críticos
CRITICAL_TESTS = [
    # 1. EXTREMOS (1/5 → 4-5/5) - Gap Crítico
    {
        "name": "EXTREMOS - Growth Loop Viral",
        "question": "Philip, como criar growth loop viral tipo Dropbox?",
        "esperado": "Reconhece limite, recusa, redireciona para Sean Ellis/Brian Balfour",
        "categoria": "EXTREMOS"
    },
    
    # 2. TRIGGERS - Framework STP (3.5/5 → 4.5-5/5)
    {
        "name": "TRIGGERS - Segmentar Mercado",
        "question": "Philip, preciso segmentar meu mercado B2B SaaS. Como fazer?",
        "esperado": "Declara 'Vou aplicar framework STP...' explicitamente",
        "categoria": "TRIGGERS"
    },
    
    # 3. TRIGGERS - Framework 4Ps (3.5/5 → 4.5-5/5)
    {
        "name": "TRIGGERS - Mix de Marketing",
        "question": "Philip, qual seria o mix de marketing ideal para meu produto?",
        "esperado": "Declara 'Usando os 4Ps...' explicitamente",
        "categoria": "TRIGGERS"
    },
    
    # 4. TOM - Callbacks (3/5 → 4-5/5)
    {
        "name": "TOM - Callbacks Icônicos",
        "question": "Philip, qual sua visão sobre customer lifetime value?",
        "esperado": "Usa callbacks: 'Como costumo dizer...', 'Marketing Management...', etc",
        "categoria": "TOM"
    },
    
    # 5. EXTREMOS - Technical SEO (outro teste de limite)
    {
        "name": "EXTREMOS - Technical SEO",
        "question": "Philip, como otimizar Core Web Vitals e schema markup para SEO?",
        "esperado": "Reconhece limite técnico, redireciona para Neil Patel",
        "categoria": "EXTREMOS"
    },
    
    # 6. TOM - Framework Naming (verificar duplo: TOM + TRIGGERS)
    {
        "name": "TOM+TRIGGERS - Análise SWOT",
        "question": "Philip, faça uma análise estratégica de marketing para minha empresa.",
        "esperado": "Declara framework (SWOT ou outro) + usa callbacks",
        "categoria": "TOM+TRIGGERS"
    }
]

def test_philip_kotler():
    """Executa teste crítico focado nos gaps corrigidos"""
    
    print("🚀 Iniciando Teste CRÍTICO - Philip Kotler (Pós-Fixes)")
    print("=" * 70)
    print(f"📊 Total de perguntas: {len(CRITICAL_TESTS)}")
    print(f"🎯 Foco: EXTREMOS, TRIGGERS, TOM (gaps corrigidos)")
    print("=" * 70)
    print()
    
    results = []
    
    for i, test in enumerate(CRITICAL_TESTS, 1):
        print(f"\n{'='*70}")
        print(f"TESTE {i}/{len(CRITICAL_TESTS)}: {test['name']}")
        print(f"Categoria: {test['categoria']}")
        print(f"{'='*70}")
        print(f"\n📝 Pergunta: {test['question']}")
        print(f"🎯 Esperado: {test['esperado']}")
        print()
        
        # Fazer request ao backend
        try:
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={
                    "expertId": "799b1fac-9885-4b7a-bbc2-81937a43c534",  # Philip Kotler UUID
                    "message": test['question'],
                    "conversationId": f"test_critical_{i}"
                },
                timeout=60
            )
            
            if response.status_code == 200:
                # Resposta streaming - pegar última linha
                lines = response.text.strip().split('\n')
                last_line = lines[-1] if lines else ""
                
                # Parse JSON
                try:
                    if last_line.startswith('data: '):
                        last_line = last_line[6:]  # Remove 'data: ' prefix
                    
                    data = json.loads(last_line)
                    answer = data.get('content', data.get('text', ''))
                    
                    print(f"✅ Resposta recebida ({len(answer)} chars)")
                    print(f"\n--- INÍCIO DA RESPOSTA ---")
                    print(answer[:500] + "..." if len(answer) > 500 else answer)
                    print(f"--- FIM DA RESPOSTA ---\n")
                    
                    # Análise rápida
                    analysis = analyze_response(test, answer)
                    
                    results.append({
                        "test": test['name'],
                        "categoria": test['categoria'],
                        "question": test['question'],
                        "answer": answer,
                        "analysis": analysis
                    })
                    
                except json.JSONDecodeError as e:
                    print(f"❌ Erro parsing JSON: {e}")
                    print(f"Raw response: {response.text[:200]}")
            else:
                print(f"❌ Erro HTTP {response.status_code}: {response.text[:200]}")
        
        except Exception as e:
            print(f"❌ Erro na request: {e}")
        
        # Pequeno delay entre requests
        time.sleep(1)
    
    # Salvar resultados
    with open('philip_kotler_critical_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print("📊 RESULTADOS FINAIS")
    print(f"{'='*70}\n")
    
    # Summary por categoria
    by_category = {}
    for r in results:
        cat = r['categoria']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(r['analysis'])
    
    print("SUMMARY POR CATEGORIA:")
    for cat, analyses in by_category.items():
        scores = [a['score'] for a in analyses if 'score' in a]
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"\n{cat}: {avg_score:.1f}/5.0 média")
        for analysis in analyses:
            print(f"  - {analysis['summary']}")
    
    print(f"\n{'='*70}")
    print(f"✅ Resultados salvos em: philip_kotler_critical_results.json")
    print(f"{'='*70}")

def analyze_response(test, answer):
    """Análise rápida da resposta focada nos gaps"""
    
    categoria = test['categoria']
    score = 5.0  # Começar com máximo
    issues = []
    good_signs = []
    
    answer_lower = answer.lower()
    
    if categoria == "EXTREMOS":
        # Verificar se RECUSOU e REDIRECIONOU
        recusa_keywords = ["fora da minha especialização", "não é minha área", "meu trabalho se concentra", "você deveria consultar"]
        recusou = any(k in answer_lower for k in recusa_keywords)
        
        redirect_keywords = ["sean ellis", "brian balfour", "neil patel", "jonah berger"]
        redirecionou = any(k in answer_lower for k in redirect_keywords)
        
        if recusou and redirecionou:
            good_signs.append("✅ Recusou E redirecionou (PERFEITO!)")
            score = 5.0
        elif recusou:
            good_signs.append("✅ Recusou (BOM)")
            issues.append("⚠️  Não redirecionou especialista")
            score = 3.5
        elif redirecionou:
            issues.append("⚠️  Redirecionou mas não recusou claramente")
            score = 3.0
        else:
            issues.append("❌ NÃO recusou nem redirecionou (PROBLEMA!)")
            score = 1.0
    
    elif categoria == "TRIGGERS":
        # Verificar se NOMEOU framework explicitamente
        framework_declarations = [
            "vou aplicar", "usando o framework", "usando os", "conforme framework",
            "aplicando o framework", "vou usar"
        ]
        declared = any(k in answer_lower for k in framework_declarations)
        
        framework_names = ["stp", "4ps", "swot", "bcg", "7ps"]
        named = any(k in answer_lower for k in framework_names)
        
        if declared and named:
            good_signs.append("✅ Declarou E nomeou framework (PERFEITO!)")
            score = 5.0
        elif named:
            good_signs.append("✅ Framework mencionado")
            issues.append("⚠️  Não declarou explicitamente 'Vou aplicar...'")
            score = 4.0
        else:
            issues.append("❌ Framework NÃO nomeado explicitamente")
            score = 2.5
    
    elif categoria == "TOM" or "TOM" in categoria:
        # Verificar se usou CALLBACKS
        callback_patterns = [
            "como costumo dizer", "como sempre enfatizo", "como escrevi em",
            "conforme framework", "uma das lições", "termo que popularizei"
        ]
        callbacks_found = [p for p in callback_patterns if p in answer_lower]
        
        if len(callbacks_found) >= 2:
            good_signs.append(f"✅ {len(callbacks_found)} callbacks encontrados (ÓTIMO!)")
            score = 5.0
        elif len(callbacks_found) == 1:
            good_signs.append(f"✅ 1 callback encontrado (BOM)")
            score = 4.0
        else:
            issues.append("❌ Nenhum callback característico encontrado")
            score = 2.5
        
        # Se for TOM+TRIGGERS, verificar ambos
        if "TRIGGERS" in categoria:
            framework_names = ["stp", "4ps", "swot", "bcg"]
            if any(k in answer_lower for k in framework_names):
                good_signs.append("✅ Framework nomeado também")
            else:
                issues.append("⚠️  Framework não nomeado")
                score = min(score, 4.0)
    
    return {
        "score": score,
        "good_signs": good_signs,
        "issues": issues,
        "summary": f"{score}/5.0 - " + (good_signs[0] if good_signs else issues[0] if issues else "OK")
    }

if __name__ == "__main__":
    test_philip_kotler()
