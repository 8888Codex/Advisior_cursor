"""
Script para testar a criação de personas com tratamento de erros aprimorado
"""
import os
import json
import asyncio
from dotenv import load_dotenv, find_dotenv

# Carregar variáveis de ambiente
env_file = find_dotenv(usecwd=True)
if env_file:
    load_dotenv(env_file)
    print(f"[ENV] Carregado .env de: {env_file}")
else:
    print("[ENV] Arquivo .env não encontrado!")

# Importar módulos necessários
from reddit_research import reddit_research
from models_persona import PersonaModern, PersonaModernCreate

async def test_persona_creation():
    """Teste a criação de personas com tratamento de erros aprimorado"""
    print("\n🧪 TESTANDO CRIAÇÃO DE PERSONAS")
    print("=" * 60)
    
    # Dados de teste
    target_description = "Profissional de marketing digital freelancer"
    industry = "Marketing e Publicidade"
    additional_context = "Especializado em estratégias de conteúdo para pequenas empresas"
    
    try:
        print(f"\n1️⃣ Testando pesquisa rápida para '{target_description}'")
        quick_data = await reddit_research.research_quick(
            target_description=target_description,
            industry=industry
        )
        
        if quick_data:
            print(f"✅ Pesquisa rápida concluída com sucesso!")
            print(f"📊 Dados obtidos:")
            print(f"  • Job Statement: {quick_data.get('job_to_be_done', {}).get('statement', 'N/A')}")
            print(f"  • Comportamentos: {len(quick_data.get('behaviors', {}).get('online', []))} comportamentos online")
            print(f"  • Pontos de dor: {len(quick_data.get('pain_points_quantified', []))} pontos de dor quantificados")
        else:
            print(f"❌ Falha na pesquisa rápida: Nenhum dado retornado")
        
        print(f"\n2️⃣ Testando pesquisa estratégica para '{target_description}'")
        strategic_data = await reddit_research.research_strategic(
            target_description=target_description,
            industry=industry,
            additional_context=additional_context
        )
        
        if strategic_data:
            print(f"✅ Pesquisa estratégica concluída com sucesso!")
            print(f"📊 Dados obtidos:")
            print(f"  • Job Statement: {strategic_data.get('job_to_be_done', {}).get('statement', 'N/A')}")
            print(f"  • Comportamentos: {len(strategic_data.get('behaviors', {}).get('online', []))} comportamentos online")
            print(f"  • Aspirações: {len(strategic_data.get('aspirations', []))} aspirações")
            print(f"  • Objetivos: {len(strategic_data.get('goals', []))} objetivos")
            print(f"  • Pontos de dor: {len(strategic_data.get('pain_points_quantified', []))} pontos de dor quantificados")
            print(f"  • Comunidades: {len(strategic_data.get('communities', []))} comunidades")
        else:
            print(f"❌ Falha na pesquisa estratégica: Nenhum dado retornado")
        
        # Salvar os resultados em um arquivo para inspeção
        with open("test_persona_results.json", "w", encoding="utf-8") as f:
            json.dump({
                "quick": quick_data,
                "strategic": strategic_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 Resultados salvos em test_persona_results.json")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO")

if __name__ == "__main__":
    asyncio.run(test_persona_creation())
