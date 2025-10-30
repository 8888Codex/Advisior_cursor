"""
Script para testar a API do Perplexity isoladamente
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv, find_dotenv

async def test_perplexity_api():
    """Teste simples da API do Perplexity"""
    # Carregar variáveis de ambiente
    env_file = find_dotenv(usecwd=True)
    if env_file:
        load_dotenv(env_file)
        print(f"[ENV] Carregado .env de: {env_file}")
    else:
        print("[ENV] Arquivo .env não encontrado!")
        return
    
    # Obter chave de API
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("[ERRO] PERPLEXITY_API_KEY não encontrada no ambiente!")
        return
    
    print(f"[INFO] Usando chave de API Perplexity: {api_key[:10]}...")
    
    # Lista de modelos para testar
    models_to_test = [
        "sonar",               # lightweight search
        "sonar-pro",           # advanced search
        "sonar-deep-research", # exhaustive research
        "sonar-reasoning",     # fast reasoning
        "sonar-reasoning-pro"  # premier reasoning
    ]
    
    # Testar cada modelo
    for model in models_to_test:
        print(f"\n[TESTE] Testando modelo: {model}")
        
        # Preparar payload
        request_payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": "Olá, como você está?"}
            ],
            "temperature": 0.2,
            "max_tokens": 100
        }
        
        # Fazer chamada à API
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_payload
                )
                
                # Verificar resposta
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    print(f"[SUCESSO] Modelo {model} respondeu: {content[:50]}...")
                    print(f"[INFO] Modelo {model} é válido!")
                else:
                    print(f"[ERRO] Modelo {model} falhou com status {response.status_code}")
                    print(f"[ERRO] Resposta: {response.text}")
        except Exception as e:
            print(f"[ERRO] Exceção ao testar modelo {model}: {str(e)}")
    
    print("\n[INFO] Teste concluído!")

if __name__ == "__main__":
    asyncio.run(test_perplexity_api())
