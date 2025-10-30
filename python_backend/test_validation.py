"""
Test script for persona validation system
"""
import json
from validation import persona_validator

# Sample persona data with varying levels of completeness
test_personas = [
    # High quality persona
    {
        "job_statement": "Encontrar soluções eficientes para gerenciar o estoque e logística a fim de reduzir custos operacionais",
        "situational_contexts": ["Quando o estoque está baixo", "Quando há atrasos na entrega"],
        "demographics": {
            "age": "28-45 anos",
            "location": "Capitais e grandes centros urbanos",
            "occupation": "Empreendedores de e-commerce",
            "education": "Ensino superior completo",
            "income": "R$5.000-15.000 mensais"
        },
        "behaviors": {
            "online": ["Pesquisa extensivamente antes de comprar", "Compara preços em múltiplos sites"],
            "purchasing": ["Valoriza custo-benefício", "Prefere soluções completas"],
            "decision_making": ["Baseia decisões em ROI", "Consulta outros empreendedores"]
        },
        "aspirations": [
            "Escalar o negócio para faturamento de 7 dígitos",
            "Automatizar processos operacionais",
            "Alcançar equilíbrio entre vida pessoal e profissional"
        ],
        "goals": [
            {
                "description": "Aumentar a taxa de conversão do site em 30%",
                "timeframe": "short",
                "success_metrics": ["Taxa de conversão de 3% para 4%", "Redução de 20% na taxa de abandono"],
                "obstacles": ["Orçamento limitado", "Conhecimento técnico insuficiente"]
            },
            {
                "description": "Expandir para novos nichos de mercado",
                "timeframe": "medium",
                "success_metrics": ["Lançar 2 novas categorias de produtos", "Aumentar base de clientes em 40%"],
                "obstacles": ["Concorrência estabelecida", "Desconhecimento do novo mercado"]
            }
        ],
        "functional_jobs": [
            "Gerenciar estoque eficientemente",
            "Otimizar processos de entrega",
            "Reduzir custos operacionais"
        ],
        "emotional_jobs": [
            "Sentir-se no controle do negócio",
            "Reduzir estresse com problemas logísticos",
            "Ter confiança nas decisões de estoque"
        ],
        "social_jobs": [
            "Ser visto como empreendedor bem-sucedido",
            "Ser reconhecido pela qualidade do serviço"
        ],
        "pain_points_quantified": [
            {
                "description": "Dificuldade em prever demanda",
                "impact": "Perda de 15% em vendas potenciais",
                "cost": "R$5.000/mês em oportunidades perdidas",
                "frequency": "mensalmente"
            },
            {
                "description": "Problemas logísticos",
                "impact": "20 horas semanais gastas em resolução",
                "cost": "R$3.000/mês em custos extras",
                "frequency": "semanalmente"
            },
            {
                "description": "Alto custo de aquisição de clientes",
                "impact": "30% do faturamento gasto em marketing",
                "cost": "R$150 por cliente adquirido",
                "frequency": "constantemente"
            }
        ]
    },
    
    # Medium quality persona
    {
        "job_statement": "Melhorar as vendas online",
        "situational_contexts": ["Quando as vendas estão baixas"],
        "demographics": {
            "age": "30-50 anos",
            "location": "Brasil",
            "occupation": "Empreendedores"
        },
        "behaviors": {
            "online": ["Pesquisa antes de comprar"],
            "purchasing": ["Valoriza preço baixo"]
        },
        "aspirations": [
            "Crescer o negócio",
            "Ter mais tempo livre"
        ],
        "goals": [
            {
                "description": "Aumentar vendas",
                "timeframe": "short"
            }
        ],
        "functional_jobs": [
            "Vender produtos online",
            "Gerenciar estoque"
        ],
        "emotional_jobs": [
            "Sentir-se realizado"
        ],
        "social_jobs": [
            "Ser visto como empreendedor"
        ],
        "pain_points_quantified": [
            {
                "description": "Dificuldade em vender",
                "impact": "Menos vendas"
            }
        ]
    },
    
    # Low quality persona
    {
        "job_statement": "Vender mais",
        "demographics": {
            "age": "Adultos"
        },
        "behaviors": {
            "online": ["Usa internet"]
        },
        "aspirations": [
            "Sucesso"
        ],
        "goals": [
            {
                "description": "Crescer"
            }
        ],
        "functional_jobs": [
            "Vender produtos"
        ],
        "emotional_jobs": [
            "Sentir-se bem"
        ],
        "social_jobs": [
            "Ser respeitado"
        ],
        "pain_points_quantified": [
            {
                "description": "Problemas de vendas"
            }
        ]
    }
]

def test_validation():
    """Test the persona validation system"""
    print("🧪 TESTANDO SISTEMA DE VALIDAÇÃO DE PERSONAS")
    print("="*60)
    
    for i, persona_data in enumerate(test_personas):
        print(f"\n📋 Testando Persona {i+1}:")
        
        # Validate persona
        is_valid, errors, enhanced_data = persona_validator.validate_persona(persona_data)
        
        # Print validation results
        print(f"   Válida: {'✅ Sim' if is_valid else '❌ Não'}")
        
        if errors:
            print(f"   Erros: {len(errors)}")
            for error in errors:
                print(f"   - {error}")
        
        # Print confidence levels
        if "research_data" in enhanced_data and "confidence_metadata" in enhanced_data["research_data"]:
            confidence = enhanced_data["research_data"]["confidence_metadata"]
            print("\n   📊 Níveis de Confiança:")
            
            for field, level in confidence.items():
                emoji = "🟢" if level == "high" else "🟡" if level == "medium" else "🔴"
                print(f"   {emoji} {field}: {level}")
            
            if "confidence_level" in enhanced_data["research_data"]:
                overall = enhanced_data["research_data"]["confidence_level"]
                emoji = "🟢" if overall == "high" else "🟡" if overall == "medium" else "🔴"
                print(f"\n   📈 Confiança Geral: {emoji} {overall}")
        
        print("\n" + "-"*60)
    
    print("\n✅ TESTE DE VALIDAÇÃO CONCLUÍDO")

if __name__ == "__main__":
    test_validation()
