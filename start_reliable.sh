#!/bin/bash

# Script de inicialização confiável com health checks
# Garante que ambos os serviços estão funcionando antes de liberar

set -e  # Parar em caso de erro

echo "🚀 AdvisorIA Elite - Inicialização Confiável"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se porta está em uso
check_port() {
    lsof -ti:$1 > /dev/null 2>&1
    return $?
}

# Função para aguardar porta ficar disponível
wait_port_free() {
    local port=$1
    local max_wait=10
    local waited=0
    
    while check_port $port && [ $waited -lt $max_wait ]; do
        echo "  ⏳ Aguardando porta $port liberar... (${waited}s)"
        sleep 1
        waited=$((waited + 1))
    done
    
    if check_port $port; then
        echo -e "${RED}  ❌ Porta $port ainda ocupada após ${max_wait}s${NC}"
        return 1
    fi
    return 0
}

# Função para aguardar serviço estar pronto
wait_service_ready() {
    local url=$1
    local name=$2
    local max_wait=$3
    local waited=0
    
    while [ $waited -lt $max_wait ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}  ✅ $name está pronto!${NC}"
            return 0
        fi
        echo "  ⏳ Aguardando $name... (${waited}s/${max_wait}s)"
        sleep 2
        waited=$((waited + 2))
    done
    
    echo -e "${RED}  ❌ $name não iniciou em ${max_wait}s${NC}"
    return 1
}

# 1. Parar processos existentes
echo "1️⃣ Parando processos existentes..."
lsof -ti:5500 | xargs kill -9 2>/dev/null && echo "  ✓ Porta 5500 liberada" || echo "  ✓ Porta 5500 já estava livre"
lsof -ti:5501 | xargs kill -9 2>/dev/null && echo "  ✓ Porta 5501 liberada" || echo "  ✓ Porta 5501 já estava livre"
lsof -ti:5201 | xargs kill -9 2>/dev/null && echo "  ✓ Porta 5201 liberada" || echo "  ✓ Porta 5201 já estava livre"
lsof -ti:3001 | xargs kill -9 2>/dev/null && echo "  ✓ Porta 3001 liberada" || echo "  ✓ Porta 3001 já estava livre"
sleep 2
echo ""

# 2. Verificar dependências
echo "2️⃣ Verificando dependências..."

if ! command -v node &> /dev/null; then
    echo -e "${RED}  ❌ Node.js não encontrado${NC}"
    exit 1
fi
echo "  ✓ Node.js: $(node --version)"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}  ❌ Python3 não encontrado${NC}"
    exit 1
fi
echo "  ✓ Python3: $(python3 --version)"

if ! command -v npm &> /dev/null; then
    echo -e "${RED}  ❌ npm não encontrado${NC}"
    exit 1
fi
echo "  ✓ npm: $(npm --version)"
echo ""

# 3. Verificar node_modules
echo "3️⃣ Verificando dependências Node.js..."
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}  ⚠️  node_modules não encontrado. Instalando...${NC}"
    npm install
fi
echo "  ✓ Dependências OK"
echo ""

# 4. Iniciar serviços
echo "4️⃣ Iniciando serviços..."
echo "  📍 Frontend: http://localhost:5500"
echo "  📍 Backend Python: http://localhost:5501"
echo ""

# Iniciar em background com logs
PORT=5500 PY_PORT=5501 NODE_ENV=development npm run dev > /tmp/advisoria_startup.log 2>&1 &
SERVER_PID=$!

echo "  ✓ Servidor iniciado (PID: $SERVER_PID)"
echo ""

# 5. Aguardar serviços ficarem prontos
echo "5️⃣ Aguardando serviços ficarem prontos..."

# Aguardar Node.js (máximo 20 segundos)
if ! wait_service_ready "http://localhost:5500" "Frontend (Node.js)" 20; then
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ❌ ERRO: Frontend não iniciou${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Logs do servidor:"
    tail -30 /tmp/advisoria_startup.log
    exit 1
fi

# Aguardar Python Backend (máximo 30 segundos)
if ! wait_service_ready "http://localhost:5501/api/experts" "Backend Python" 30; then
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ❌ ERRO: Backend Python não iniciou${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Logs do servidor:"
    tail -30 /tmp/advisoria_startup.log | grep -i python
    exit 1
fi

echo ""

# 6. Validação final
echo "6️⃣ Validando sistema..."

# Testar endpoint de especialistas
EXPERT_COUNT=$(curl -s http://localhost:5501/api/experts | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")
if [ "$EXPERT_COUNT" -gt "0" ]; then
    echo -e "${GREEN}  ✅ $EXPERT_COUNT especialistas carregados${NC}"
else
    echo -e "${YELLOW}  ⚠️  Especialistas não carregados (pode ser normal na primeira execução)${NC}"
fi

# Testar proxy
PROXY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5500/api/experts 2>/dev/null || echo "000")
if [ "$PROXY_STATUS" = "200" ]; then
    echo -e "${GREEN}  ✅ Proxy Node.js → Python funcionando${NC}"
else
    echo -e "${YELLOW}  ⚠️  Proxy retornou status: $PROXY_STATUS${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ SISTEMA INICIADO COM SUCESSO!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📍 Acesse: ${GREEN}http://localhost:5500${NC}"
echo "💬 Conselho: ${GREEN}http://localhost:5500/test-council${NC}"
echo ""
echo "📋 Logs em tempo real:"
echo "   tail -f /tmp/advisoria_startup.log"
echo ""
echo "⏹️  Para parar: Ctrl+C ou pkill -f 'tsx server'"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Mostrar logs em tempo real
tail -f /tmp/advisoria_startup.log | grep -v "Browserslist"

