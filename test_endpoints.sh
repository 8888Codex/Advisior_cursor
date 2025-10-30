#!/bin/bash

echo "🧪 AUDITORIA DE ENDPOINTS - AdvisorIA Elite"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo -n "Testing $description... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" -H "Content-Type: application/json" -d "$data")
    fi
    
    if [ "$response" = "200" ] || [ "$response" = "201" ]; then
        echo -e "${GREEN}✓ $response${NC}"
        return 0
    elif [ "$response" = "404" ]; then
        echo -e "${RED}✗ 404 NOT FOUND${NC}"
        return 1
    else
        echo -e "${YELLOW}⚠ $response${NC}"
        return 2
    fi
}

echo "📍 ENDPOINTS CRÍTICOS"
echo "===================="
echo ""

# Experts endpoints
test_endpoint "GET" "http://localhost:5001/api/experts" "" "GET /api/experts (Python)"
test_endpoint "GET" "http://localhost:5001/api/categories" "" "GET /api/categories (Python)"

# Conversations endpoints  
test_endpoint "GET" "http://localhost:5001/api/conversations" "" "GET /api/conversations (Python)"

# Profile endpoints
test_endpoint "GET" "http://localhost:5001/api/profile" "" "GET /api/profile (Python)"
test_endpoint "GET" "http://localhost:5001/api/insights" "" "GET /api/insights (Python)"

echo ""
echo "📍 ENDPOINTS FALTANDO (Esperado 404)"
echo "====================================="
echo ""

test_endpoint "POST" "http://localhost:5001/api/experts/auto-clone" '{"targetName":"Test"}' "POST /api/experts/auto-clone"
test_endpoint "POST" "http://localhost:5001/api/experts/test-chat" '{"message":"test"}' "POST /api/experts/test-chat"
test_endpoint "GET" "http://localhost:5001/api/experts/test-id/suggested-questions" "" "GET /api/experts/:id/suggested-questions"

echo ""
echo "📍 ENDPOINTS AVANÇADOS"
echo "====================="
echo ""

test_endpoint "POST" "http://localhost:5001/api/recommend-experts" '{"problem":"Como aumentar vendas?"}' "POST /api/recommend-experts"
test_endpoint "POST" "http://localhost:5001/api/council/analyze" '{"problem":"Test"}' "POST /api/council/analyze"

echo ""
echo "📍 PERSONAS ENDPOINTS"
echo "===================="
echo ""

test_endpoint "GET" "http://localhost:5001/api/personas" "" "GET /api/personas"
test_endpoint "POST" "http://localhost:5001/api/personas/create" '{"mode":"quick","targetDescription":"Test"}' "POST /api/personas/create"

echo ""
echo "✅ Auditoria completa!"
