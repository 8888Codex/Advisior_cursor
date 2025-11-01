#!/usr/bin/env python3
"""
Script para verificar se as variáveis de ambiente estão sendo carregadas corretamente
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

print("🔍 Verificando variáveis de ambiente...\n")

# Tentar encontrar .env
env_file = find_dotenv(usecwd=True)
if env_file:
    print(f"✅ Arquivo .env encontrado: {env_file}")
    load_dotenv(env_file)
else:
    print("⚠️  Arquivo .env não encontrado")
    print("   Procurando em:", Path.cwd())

print("\n📋 Variáveis de ambiente:")
print(f"   ANTHROPIC_API_KEY: {'✅ Configurada' if os.getenv('ANTHROPIC_API_KEY') else '❌ NÃO configurada'}")
if os.getenv('ANTHROPIC_API_KEY'):
    key = os.getenv('ANTHROPIC_API_KEY')
    print(f"   Primeiros 15 chars: {key[:15]}...")
    print(f"   Últimos 5 chars: ...{key[-5:] if len(key) > 5 else key}")
    print(f"   Tamanho: {len(key)} caracteres")

print(f"   PERPLEXITY_API_KEY: {'✅ Configurada' if os.getenv('PERPLEXITY_API_KEY') else '⚠️  Opcional (não configurada)'}")

# Testar importação do módulo
print("\n🧪 Testando importação do crew_agent...")
try:
    sys.path.insert(0, str(Path.cwd()))
    from python_backend.crew_agent import MarketingLegendAgent
    print("✅ Módulo crew_agent importado com sucesso")
    
    # Tentar criar uma instância (vai falhar se não tiver API key)
    try:
        test_agent = MarketingLegendAgent("Test", "You are a test assistant")
        print("✅ MarketingLegendAgent criado com sucesso")
        print("   ✅ ANTHROPIC_API_KEY foi carregada corretamente!")
    except ValueError as ve:
        print(f"❌ Erro ao criar agente: {ve}")
        print("\n💡 SOLUÇÃO:")
        print("   1. Crie/edite o arquivo .env na raiz do projeto")
        print("   2. Adicione: ANTHROPIC_API_KEY=sk-ant-sua_chave_aqui")
        print("   3. Reinicie o servidor Python")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")

print("\n" + "="*50)
print("Verificação concluída!")

