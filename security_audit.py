import requests
import json

print("🔒 AUDITORIA DE SEGURANÇA")
print("=========================\n")

print("1. AUTENTICAÇÃO E AUTORIZAÇÃO")
print("------------------------------")
print("❌ Sem sistema de autenticação")
print("   - Não há login/registro")
print("   - Não há proteção de rotas")
print("   - User ID hardcoded como 'default_user'")
print("   - Qualquer pessoa pode acessar TODOS os endpoints\n")

print("2. ROTAS ADMINISTRATIVAS SEM PROTEÇÃO")
print("---------------------------------------")
# Test if we can create experts without auth
try:
    response = requests.post("http://localhost:5001/api/experts", 
        json={
            "name": "Malicious Expert",
            "title": "Hacker",
            "expertise": ["Hacking"],
            "bio": "Test security",
            "systemPrompt": "I am evil",
            "category": "marketing"
        })
    
    if response.status_code in [200, 201]:
        print("   ❌ CRÍTICO: Qualquer um pode criar experts")
        print(f"      Expert malicioso criado: {response.json()['id']}\n")
    else:
        print(f"   Status: {response.status_code}\n")
except Exception as e:
    print(f"   Erro: {e}\n")

print("3. VALIDAÇÃO DE INPUTS")
print("-----------------------")

# Test XSS in expert name
try:
    response = requests.post("http://localhost:5001/api/experts",
        json={
            "name": "<script>alert('XSS')</script>",
            "title": "Test",
            "expertise": ["Test"],
            "bio": "Test",
            "systemPrompt": "Test",
            "category": "marketing"
        })
    
    if response.status_code in [200, 201]:
        print("   ⚠️  Aceita HTML/JavaScript em campos de texto")
        print("      Potencial XSS se não sanitizado no frontend\n")
except Exception as e:
    pass

# Test SQL injection (though using MemStorage, not SQL)
print("   ℹ️  Storage atual: MemStorage (não vulnerável a SQL injection)")
print("      MAS: Se migrar para SQL sem parametrização, será vulnerável\n")

# Test message size limits
print("4. RATE LIMITING E LIMITES")
print("---------------------------")
print("   ❌ Sem rate limiting visível")
print("   ❌ Sem limite de tamanho de mensagens")
print("   ❌ Sem timeout configurado")
print("   ⚠️  Possível abuso: spam de mensagens/criar experts infinitos\n")

print("5. API KEYS E SECRETS")
print("----------------------")
print("   ✅ .env está no .cursorignore (não commitado)")
print("   ❌ Não há .env.example como guia")
print("   ⚠️  API keys são usadas no backend (correto)")
print("   ✅ Frontend não expõe API keys\n")

print("6. CORS E CSP")
print("--------------")
print("   ⚠️  CORS: allow_origins=['*'] (permite qualquer origem)")
print("   ❌ Sem Content Security Policy")
print("   ❌ Sem proteção contra CSRF\n")

print("7. DADOS SENSÍVEIS")
print("-------------------")
print("   ✅ Senhas não são armazenadas (sem auth)")
print("   ⚠️  Perfis de negócio não têm owner (default_user)")
print("   ❌ Qualquer um pode ver/editar qualquer perfil\n")

print("8. HTTPS/TLS")
print("-------------")
print("   ⚠️  Desenvolvimento: HTTP (normal)")
print("   ⚠️  Produção: DEVE usar HTTPS (não configurado)\n")

print("\n📊 SCORE DE SEGURANÇA: 3/10")
print("============================")
print("CRÍTICO:")
print("  • Sem autenticação")
print("  • Sem autorização em rotas admin")
print("  • CORS aberto para todos")
print("  • Sem rate limiting")
print("\nALTO:")
print("  • Sem validação robusta de inputs")
print("  • Sem CSP/CSRF protection")
print("  • User isolation inexistente")
print("\nMÉDIO:")
print("  • Falta .env.example")
print("  • Falta HTTPS config para produção")
