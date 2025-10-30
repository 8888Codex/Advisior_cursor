#!/bin/bash

# Script para iniciar o AdvisorIA Elite
# Mata processos antigos e inicia o servidor limpo

echo "🚀 Iniciando AdvisorIA Elite..."
echo ""

# Matar processos nas portas 5000 e 5001
echo "🔍 Verificando portas..."
if lsof -ti:5000 > /dev/null 2>&1; then
    echo "⚠️  Porta 5000 ocupada, liberando..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    sleep 1
fi

if lsof -ti:5001 > /dev/null 2>&1; then
    echo "⚠️  Porta 5001 ocupada, liberando..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "✅ Portas livres!"
echo ""
echo "🎯 Iniciando servidor..."
echo "📍 Acesse: http://localhost:5000"
echo ""
echo "⌨️  Para parar: Pressione Ctrl + C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Iniciar o projeto
npm run dev

