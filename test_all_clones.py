#!/usr/bin/env python3
"""
Script para testar TODOS os 18 clones com protocolo T.E.S.T.E.
Captura dados REAIS via API e salva scores medidos.
"""

import httpx
import json
import asyncio
from typing import Dict, List

# Base URL da API - usar backend Python direto (port 5001), não proxy Express (5000)
BASE_URL = "http://localhost:5001"

# Expert IDs (18 clones)
EXPERT_IDS = [
    "philip_kotler",
    "david_ogilvy",
    "claude_hopkins",
    "seth_godin",
    "gary_vaynerchuk",
    "leo_burnett",
    "mary_wells_lawrence",
    "john_wanamaker",
    "al_ries",
    "bill_bernbach",
    "dan_kennedy",
    "ann_handley",
    "neil_patel",
    "sean_ellis",
    "brian_balfour",
    "andrew_chen",
    "jonah_berger",
    "nir_eyal"
]

# Perguntas de teste T.E.S.T.E.
TEST_QUESTIONS = {
    "philip_kotler": {
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
    },
    "david_ogilvy": {
        "tom": [
            "Como criar propaganda que vende?",
            "Devo fazer campanha criativa ou focada em vendas?",
            "Headlines longas funcionam?",
            "Como medir sucesso de propaganda?",
            "Devo investir em branding ou performance?"
        ],
        "expertise": "Tenho R$ 100K para lançar campanha de produto premium (relógio R$ 5K). Público: homens 35-50 anos, executivos. Como estruturar campanha que constrói brand E vende?",
        "situacional": {
            "iniciante": "O que é Big Idea em propaganda?",
            "expert": "David, rodei A/B test de headlines. Headline A: 3.2% CTR, Headline B: 2.8% CTR. Sample size: 10K impressions cada. Devo escalar A ou continuar testando variações?",
            "cetico": "Propaganda criativa é só ego de agência. O que importa é preço baixo. Prove que estou errado."
        },
        "triggers": [
            "Como desenvolver campanha criativa que se destaque?",
            "Como construir imagem de marca forte?"
        ],
        "extremos": "David, meu site está lento (LCP 4.5s). Como otimizar Core Web Vitals?"
    },
    # [Adicionar outros 16 especialistas aqui - formato similar]
}

class CloneTester:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=60.0)
        self.results = {}
        self.expert_ids = {}  # name → UUID mapping
    
    async def load_expert_ids(self):
        """Carrega mapping de nomes para UUIDs"""
        response = await self.client.get(f"{self.base_url}/api/experts")
        response.raise_for_status()
        experts = response.json()
        
        # Criar mapping simplificado: nome normalizado → UUID
        for expert in experts:
            # Normalizar nome para snake_case
            normalized = expert["name"].lower().replace(" ", "_").replace("&", "").replace(".", "").strip()
            self.expert_ids[normalized] = expert["id"]
        
        print(f"  ✓ Carregados {len(self.expert_ids)} expert IDs")
    
    async def create_conversation(self, expert_id: str) -> str:
        """Cria conversa com expert e retorna conversation_id"""
        response = await self.client.post(
            f"{self.base_url}/api/conversations",
            json={
                "expertId": expert_id,
                "title": f"Teste T.E.S.T.E. - {expert_id}"
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["id"]
    
    async def send_message(self, conversation_id: str, message: str) -> str:
        """Envia mensagem e retorna resposta do clone"""
        response = await self.client.post(
            f"{self.base_url}/api/conversations/{conversation_id}/messages",
            json={"content": message}
        )
        response.raise_for_status()
        data = response.json()
        return data["assistantMessage"]["content"]
    
    def score_tom(self, responses: List[str], expert_id: str) -> Dict:
        """Pontua Tom (personalidade) baseado em 5 respostas"""
        score = 0
        details = []
        
        # Critérios de avaliação (manual - será refinado)
        # TODO: Implementar scoring automático baseado em keywords
        
        return {
            "score": score,
            "max": 5,
            "details": details
        }
    
    def score_expertise(self, response: str, expert_id: str) -> Dict:
        """Pontua Expertise baseado em 1 pergunta complexa"""
        score = 0
        details = []
        
        # Critérios:
        # 1. Framework mencionado? (+1)
        # 2. Diagnóstico correto? (+1)
        # 3. Solução estruturada? (+1)
        # 4. Números/métricas? (+1)
        # 5. Ação clara? (+1)
        
        return {
            "score": score,
            "max": 5,
            "details": details
        }
    
    async def test_clone(self, expert_name_key: str):
        """Testa um clone com protocolo T.E.S.T.E. completo"""
        print(f"\n{'='*60}")
        print(f"Testando: {expert_name_key.replace('_', ' ').title()}")
        print(f"{'='*60}")
        
        if expert_name_key not in TEST_QUESTIONS:
            print(f"  ⚠️  Perguntas não definidas para {expert_name_key}")
            return
        
        # Resolver UUID real do expert
        if expert_name_key not in self.expert_ids:
            print(f"  ❌ Expert ID não encontrado para {expert_name_key}")
            return
        
        expert_uuid = self.expert_ids[expert_name_key]
        
        questions = TEST_QUESTIONS[expert_name_key]
        results = {
            "expert_name": expert_name_key,
            "expert_uuid": expert_uuid,
            "tom": {},
            "expertise": {},
            "situacional": {},
            "triggers": {},
            "extremos": {}
        }
        
        # Criar conversa
        conversation_id = await self.create_conversation(expert_uuid)
        print(f"  ✓ Conversa criada: {conversation_id}")
        
        # T - Tom (5 perguntas simples)
        print(f"\n  [T] Tom - 5 perguntas simples...")
        tom_responses = []
        for i, question in enumerate(questions["tom"], 1):
            print(f"    Pergunta {i}/5: {question[:60]}...")
            response = await self.send_message(conversation_id, question)
            tom_responses.append(response)
            print(f"      ✓ Resposta: {len(response)} chars")
            await asyncio.sleep(0.5)  # Rate limiting
        
        results["tom"] = {
            "questions": questions["tom"],
            "responses": tom_responses,
            "score": self.score_tom(tom_responses, expert_name_key)
        }
        
        # E - Expertise (1 pergunta complexa)
        print(f"\n  [E] Expertise - Pergunta complexa...")
        print(f"    Pergunta: {questions['expertise'][:60]}...")
        expertise_response = await self.send_message(conversation_id, questions["expertise"])
        print(f"      ✓ Resposta: {len(expertise_response)} chars")
        results["expertise"] = {
            "question": questions["expertise"],
            "response": expertise_response,
            "score": self.score_expertise(expertise_response, expert_name_key)
        }
        
        # S - Situacional (3 contextos)
        print(f"\n  [S] Situacional - 3 contextos...")
        situacional_responses = {}
        for context in ["iniciante", "expert", "cetico"]:
            print(f"    Contexto: {context}")
            question = questions["situacional"][context]
            print(f"      Pergunta: {question[:60]}...")
            response = await self.send_message(conversation_id, question)
            situacional_responses[context] = response
            print(f"      ✓ Resposta: {len(response)} chars")
            await asyncio.sleep(0.5)
        
        results["situacional"] = {
            "questions": questions["situacional"],
            "responses": situacional_responses
        }
        
        # T - Triggers (2-3 keywords)
        print(f"\n  [T] Triggers - Keywords...")
        trigger_responses = []
        for i, question in enumerate(questions["triggers"], 1):
            print(f"    Trigger {i}/{len(questions['triggers'])}: {question[:60]}...")
            response = await self.send_message(conversation_id, question)
            trigger_responses.append(response)
            print(f"      ✓ Resposta: {len(response)} chars")
            await asyncio.sleep(0.5)
        
        results["triggers"] = {
            "questions": questions["triggers"],
            "responses": trigger_responses
        }
        
        # E - Extremos (1 pergunta fora da área)
        print(f"\n  [E] Extremos - Pergunta fora da área...")
        print(f"    Pergunta: {questions['extremos'][:60]}...")
        extremos_response = await self.send_message(conversation_id, questions["extremos"])
        print(f"      ✓ Resposta: {len(extremos_response)} chars")
        results["extremos"] = {
            "question": questions["extremos"],
            "response": extremos_response
        }
        
        # Salvar resultados
        self.results[expert_name_key] = results
        
        print(f"\n  ✅ Teste completo para {expert_name_key}")
        return results
    
    async def test_all_clones(self):
        """Testa TODOS os 18 clones"""
        print(f"\n{'#'*60}")
        print(f"# TESTE T.E.S.T.E. - 18 CLONES COGNITIVOS")
        print(f"{'#'*60}")
        
        # Carregar IDs reais dos experts
        await self.load_expert_ids()
        
        # Testar apenas clones com perguntas definidas
        experts_to_test = [eid for eid in EXPERT_IDS if eid in TEST_QUESTIONS]
        print(f"\nClones com perguntas definidas: {len(experts_to_test)}/{len(EXPERT_IDS)}")
        print(f"Clones a testar: {', '.join(experts_to_test)}\n")
        
        for expert_id in experts_to_test:
            try:
                await self.test_clone(expert_id)
            except Exception as e:
                print(f"  ❌ Erro testando {expert_id}: {str(e)}")
                continue
        
        # Salvar resultados em JSON
        output_file = "test_results_18_clones.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✅ TESTES COMPLETOS")
        print(f"   Resultados salvos em: {output_file}")
        print(f"   Clones testados: {len(self.results)}")
        print(f"{'='*60}\n")
    
    async def close(self):
        await self.client.aclose()

async def main():
    tester = CloneTester()
    try:
        await tester.test_all_clones()
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main())
