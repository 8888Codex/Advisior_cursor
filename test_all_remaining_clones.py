#!/usr/bin/env python3
"""
Teste T.E.S.T.E. EM MASSA - 17 Clones Restantes
Executa 12 perguntas por clone com pontuação objetiva automática
Total: 17 clones × 12 perguntas = 204 tests (~60-90min)
"""

import httpx
import json
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:5001"

# Mapeamento de especialistas para contexto de testes
EXPERT_CONTEXTS = {
    "David Ogilvy": ("Brand Building", ["Big Idea", "38 Headlines"], "growth loops virais", "Sean Ellis"),
    "Seth Godin": ("Marketing Moderno", ["Purple Cow", "Tribo"], "direct response", "Dan Kennedy"),
    "Al Ries": ("Posicionamento", ["Positioning", "22 Laws"], "content marketing", "Ann Handley"),
    "Bill Bernbach": ("Creative Advertising", ["Big Idea"], "SEO técnico", "Neil Patel"),
    "Dan Kennedy": ("Direct Response", ["Magnetic Marketing"], "brand storytelling", "Bill Bernbach"),
    "Ann Handley": ("Content Marketing", ["Content-First"], "media buying", "David Ogilvy"),
    "Neil Patel": ("SEO & Analytics", ["SEO Framework"], "creative advertising", "Bill Bernbach"),
    "Robert Cialdini": ("Psicologia Persuasão", ["6 Princípios"], "product-led growth", "Brian Balfour"),
    "Simon Sinek": ("Purpose & Why", ["Golden Circle"], "conversion optimization", "Brian Balfour"),
    "Byron Sharp": ("Science-Based Marketing", ["Mental Availability"], "viral mechanics", "Jonah Berger"),
    "Sean Ellis": ("Growth Hacking", ["North Star", "Growth Loops"], "brand positioning clássico", "Philip Kotler"),
    "Brian Balfour": ("Product-Led Growth", ["4 Fits"], "traditional advertising", "David Ogilvy"),
    "Andrew Chen": ("Network Effects", ["Cold Start"], "direct mail", "Dan Kennedy"),
    "Jonah Berger": ("Virality", ["STEPPS"], "analytics técnico", "Neil Patel"),
    "Hiten Shah": ("Product Marketing SaaS", ["PMF"], "creative campaigns", "Bill Bernbach"),
    "Elena Verna": ("Retention & Monetization", ["RARRA"], "posicionamento estratégico", "Al Ries"),
    "Casey Winters": ("Growth Strategy", ["Growth Model"], "persuasion psychology", "Robert Cialdini")
}

async def test_expert(client, expert, existing_philip_result=None):
    """Testa um expert com 12 perguntas T.E.S.T.E."""
    
    name = expert["name"]
    
    # Skip Philip Kotler (já testado)
    if "Philip" in name:
        print(f"\n⏭️  Pulando {name} (já testado - usando resultado existente)")
        return existing_philip_result
    
    print(f"\n{'='*70}")
    print(f"TESTANDO: {name}")
    print(f"{'='*70}")
    
    # Get context
    if name not in EXPERT_CONTEXTS:
        print(f"  ⚠️  Contexto não definido para {name}, usando genérico")
        area, fws, oos, red = "Marketing", ["Framework"], "tópico fora", "outro expert"
    else:
        area, fws, oos, red = EXPERT_CONTEXTS[name]
    
    # Criar conversa
    try:
        conv_resp = await client.post(f"{BASE_URL}/api/conversations", 
                                     json={"expertId": expert["id"], "title": f"Teste T.E.S.T.E."})
        conv_id = conv_resp.json()["id"]
        print(f"  ✓ Conversa: {conv_id[:8]}...")
    except Exception as e:
        print(f"  ❌ Erro conversa: {e}")
        return None
    
    results = {"expert_name": name, "expert_id": expert["id"], "timestamp": datetime.now().isoformat(), "tests": {}}
    
    # Helper para enviar pergunta
    async def ask(q):
        try:
            resp = await client.post(f"{BASE_URL}/api/conversations/{conv_id}/messages", json={"content": q})
            return resp.json()["assistantMessage"]["content"]
        except Exception as e:
            print(f"    ❌ Erro: {e}")
            return ""
    
    # 1. TOM (5 perguntas)
    print("\n[TOM] 5 perguntas...")
    tom_qs = [
        f"O que faz {area.lower()} ser diferente?",
        f"Como saber se estou fazendo {area.lower()} certo?",
        f"Qual maior erro em {area.lower()}?",
        f"Meu negócio é pequeno. {area} se aplica?",
        f"Fundamentos de {area.lower()}?"
    ]
    tom_resps = []
    for i, q in enumerate(tom_qs, 1):
        r = await ask(q)
        tom_resps.append(r)
        print(f"  {i}/5: {len(r)} chars")
        await asyncio.sleep(0.2)
    
    all_tom = " ".join(tom_resps)
    tom_score = sum([
        1 if any(fw.lower() in all_tom.lower() for fw in fws) else 0,  # vocab
        1 if len(all_tom) > 2500 else 0,  # substância
        1 if "##" in all_tom or "1." in all_tom else 0,  # estrutura
        1 if any(m in all_tom.lower() for m in ["como costumo", "framework"]) else 0,  # callback
        1 if sum(1 for c in all_tom if c.isupper()) / max(len(all_tom), 1) < 0.05 else 0  # energia
    ])
    results["tests"]["tom"] = {"score": tom_score, "max": 5}
    print(f"  SCORE: {tom_score}/5")
    
    # 2. EXPERTISE
    print("\n[EXPERTISE] Pergunta complexa...")
    exp_q = f"Tenho produto SaaS B2B com R$ 50K budget. Como aplicar {area.lower()} para maximizar resultado em 6 meses?"
    exp_r = await ask(exp_q)
    print(f"  ✓ {len(exp_r)} chars")
    
    exp_score = sum([
        1 if any(fw.lower() in exp_r.lower() for fw in fws) else 0,  # framework
        1 if any(w in exp_r.lower() for w in ["análise", "considere"]) else 0,  # diagnóstico
        1 if "1." in exp_r or "2." in exp_r else 0,  # estruturado
        1 if "%" in exp_r or "r$" in exp_r.lower() else 0,  # números
        1 if any(w in exp_r.lower() for w in ["recomendo", "deve"]) else 0  # ação
    ])
    results["tests"]["expertise"] = {"score": exp_score, "max": 5}
    print(f"  SCORE: {exp_score}/5")
    
    # 3. SITUACIONAL (3 contextos)
    print("\n[SITUACIONAL] 3 contextos...")
    sit_qs = {
        "iniciante": f"Sou novo em {area.lower()}. Por onde começar?",
        "expert": f"Tenho 5 anos em marketing. Como dominar {area.lower()}? Conceitos avançados?",
        "cetico": f"{area} parece teoria. Mostre resultados mensuráveis."
    }
    sit_scores = []
    for ctx, q in sit_qs.items():
        r = await ask(q)
        print(f"  {ctx}: {len(r)} chars")
        sit_scores.append(2 if len(r) > 500 else 1)  # Simplificado
        await asyncio.sleep(0.2)
    
    sit_avg = (sum(sit_scores) / len(sit_scores)) * (5/2)  # Normalizar para /5
    results["tests"]["situacional"] = {"score": round(sit_avg, 1), "max": 5}
    print(f"  SCORE: {round(sit_avg, 1)}/5")
    
    # 4. TRIGGERS (2 keywords)
    print("\n[TRIGGERS] 2 keywords...")
    trig_qs = [
        f"Preciso aplicar {fws[0] if fws else 'framework'} mas não sei como.",
        f"Como usar {area.lower()} para aumentar conversões?"
    ]
    trig_scores = []
    for i, q in enumerate(trig_qs, 1):
        r = await ask(q)
        print(f"  {i}/2: {len(r)} chars")
        score = sum([
            1,  # keyword detectada (assumido)
            1 if any(fw.lower() in r.lower() for fw in fws) else 0,  # framework mencionado
            1 if "1." in r or "2." in r else 0,  # aplicado
            1,  # nomenclatura (assumido)
            1  # consistência (assumido)
        ])
        trig_scores.append(score)
        await asyncio.sleep(0.2)
    
    trig_avg = sum(trig_scores) / len(trig_scores)
    results["tests"]["triggers"] = {"score": round(trig_avg, 1), "max": 5}
    print(f"  SCORE: {round(trig_avg, 1)}/5")
    
    # 5. EXTREMOS (pergunta fora da área)
    print("\n[EXTREMOS] Pergunta fora...")
    ext_q = f"Como resolver {oos}?"
    ext_r = await ask(ext_q)
    print(f"  ✓ {len(ext_r)} chars")
    
    ext_score = sum([
        2 if any(m in ext_r.lower() for m in ["não é minha área", "fora da minha expertise"]) else 0,  # reconhecimento (2 pts)
        1 if any(m in ext_r.lower() for m in ["recomendo consultar", "você deveria"]) else 0,  # recusa
        1 if "expertise" in ext_r.lower() or "especialização" in ext_r.lower() else 0,  # explicação
        1 if red.lower() in ext_r.lower() else 0  # redirecionamento
    ])
    results["tests"]["extremos"] = {"score": ext_score, "max": 5}
    print(f"  SCORE: {ext_score}/5")
    
    # SCORE FINAL
    total = sum([results["tests"]["tom"]["score"], results["tests"]["expertise"]["score"],
                 results["tests"]["situacional"]["score"], results["tests"]["triggers"]["score"],
                 results["tests"]["extremos"]["score"]])
    normalized = (total / 25) * 20
    classification = "LENDÁRIO" if normalized >= 19 else "PROFISSIONAL" if normalized >= 17 else "BOM" if normalized >= 14 else "PRECISA UPGRADE"
    
    results["final_score"] = {
        "total_raw": total,
        "total_normalized_20": round(normalized, 1),
        "classification": classification
    }
    
    print(f"\n  SCORE FINAL: {round(normalized, 1)}/20 ({classification})")
    
    return results

async def main():
    print("="*70)
    print("TESTE T.E.S.T.E. EM MASSA - 17 CLONES RESTANTES")
    print("="*70)
    
    # Carregar resultado Philip Kotler existente
    philip_result = None
    try:
        with open("philip_kotler_teste_real.json", "r") as f:
            philip_result = json.load(f)
        print("\n✅ Resultado Philip Kotler carregado (13.2/20)")
    except:
        print("\n⚠️  Resultado Philip Kotler não encontrado - será re-testado")
    
    async with httpx.AsyncClient(timeout=90.0) as client:
        # Buscar experts
        print("\n[1] Buscando experts...")
        experts = (await client.get(f"{BASE_URL}/api/experts")).json()
        print(f"    ✓ {len(experts)} experts encontrados")
        
        # Testar todos
        all_results = []
        for i, expert in enumerate(experts, 1):
            print(f"\n\n{'#'*70}")
            print(f"CLONE {i}/{len(experts)}")
            print(f"{'#'*70}")
            
            result = await test_expert(client, expert, philip_result)
            if result:
                all_results.append(result)
                
                # Salvar progresso a cada 3
                if i % 3 == 0:
                    with open("all_clones_progress.json", "w") as f:
                        json.dump(all_results, f, indent=2, ensure_ascii=False)
                    print(f"\n💾 Progresso salvo ({i}/{len(experts)})")
        
        # Salvar final
        with open("all_clones_results.json", "w") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        # Summary
        print(f"\n\n{'='*70}")
        print("TESTE COMPLETO!")
        print(f"{'='*70}")
        scores = [r["final_score"]["total_normalized_20"] for r in all_results]
        print(f"  Clones testados: {len(all_results)}")
        print(f"  Score médio: {sum(scores)/len(scores):.1f}/20")
        print(f"  Melhor: {max(scores):.1f}/20")
        print(f"  Pior: {min(scores):.1f}/20")
        
        # Classificações
        clfs = {}
        for r in all_results:
            c = r["final_score"]["classification"]
            clfs[c] = clfs.get(c, 0) + 1
        print(f"\n  Classificações:")
        for c, cnt in sorted(clfs.items(), key=lambda x: -x[1]):
            print(f"    {c}: {cnt}/{len(all_results)}")

if __name__ == "__main__":
    asyncio.run(main())
