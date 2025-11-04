#!/bin/bash

# Script de Teste de Produção - AdvisorIA
# Execute após Render estar online

echo "🧪 TESTE DE PRODUÇÃO - ADVISORIA"
echo "================================="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

RENDER_URL="https://advisior-cursor.onrender.com"
VERCEL_URL="https://advisior-cursor.vercel.app"

# Função para testar endpoint
test_endpoint() {
    local url=$1
    local name=$2
    local expected=$3
    
    echo -n "Testando $name... "
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>&1)
    
    if [ "$STATUS" = "$expected" ]; then
        echo -e "${GREEN}✅ OK (${STATUS})${NC}"
        return 0
    else
        echo -e "${RED}❌ ERRO (${STATUS})${NC}"
        return 1
    fi
}

# Contador de sucessos/falhas
PASSED=0
FAILED=0

echo "📊 FASE 1: INFRAESTRUTURA"
echo "-------------------------"

# Teste 1: Vercel Frontend
test_endpoint "$VERCEL_URL" "Vercel Frontend" "200" && ((PASSED++)) || ((FAILED++))

# Teste 2: Render Backend
test_endpoint "$RENDER_URL" "Render Backend" "200" && ((PASSED++)) || ((FAILED++))

# Teste 3: Render API Experts
test_endpoint "$RENDER_URL/api/experts" "Render API Especialistas" "200" && ((PASSED++)) || ((FAILED++))

# Teste 4: Vercel Proxy
test_endpoint "$VERCEL_URL/api/experts" "Vercel Proxy → Render" "200" && ((PASSED++)) || ((FAILED++))

echo ""
echo "📊 FASE 2: DADOS"
echo "----------------"

# Teste 5: Contar especialistas Render
echo -n "Contando especialistas Render... "
EXPERTS_COUNT=$(curl -s "$RENDER_URL/api/experts" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ "$EXPERTS_COUNT" = "18" ]; then
    echo -e "${GREEN}✅ 18 especialistas${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ $EXPERTS_COUNT especialistas (esperado: 18)${NC}"
    ((FAILED++))
fi

# Teste 6: Contar especialistas Vercel
echo -n "Contando especialistas Vercel... "
EXPERTS_COUNT_V=$(curl -s "$VERCEL_URL/api/experts" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ "$EXPERTS_COUNT_V" = "18" ]; then
    echo -e "${GREEN}✅ 18 especialistas${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ $EXPERTS_COUNT_V especialistas (esperado: 18)${NC}"
    ((FAILED++))
fi

echo ""
echo "📊 FASE 3: FUNCIONALIDADES"
echo "--------------------------"

# Teste 7: Criar conversa
echo -n "Criando conversa... "
EXPERT_ID=$(curl -s "$RENDER_URL/api/experts" | python3 -c "import sys, json; print(json.load(sys.stdin)[0]['id'])" 2>/dev/null)
CONV_RESPONSE=$(curl -s -X POST "$RENDER_URL/api/conversations" \
    -H "Content-Type: application/json" \
    -d "{\"expertId\":\"$EXPERT_ID\",\"title\":\"Production Test\"}")
CONV_ID=$(echo "$CONV_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))" 2>/dev/null)

if [ -n "$CONV_ID" ] && [ "$CONV_ID" != "None" ]; then
    echo -e "${GREEN}✅ Conversa criada ($CONV_ID)${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ Falha ao criar conversa${NC}"
    ((FAILED++))
fi

echo ""
echo "📊 RESUMO"
echo "==========="
echo -e "Passou: ${GREEN}$PASSED${NC}"
echo -e "Falhou: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo "Sistema está 100% funcional em produção."
    exit 0
else
    echo -e "${YELLOW}⚠️ Alguns testes falharam.${NC}"
    echo "Verifique os erros acima e corrija antes de declarar produção."
    exit 1
fi

