#!/bin/bash

# Script para iniciar o AdvisorIA Elite
# Mata processos antigos e inicia o servidor limpo

echo "🚀 Iniciando AdvisorIA Elite..."
echo ""

# Matar processos nas portas 5500 e 5501
echo "🔍 Verificando portas..."
if lsof -ti:5500 > /dev/null 2>&1; then
    echo "⚠️  Porta 5500 ocupada, liberando..."
    lsof -ti:5500 | xargs kill -9 2>/dev/null
    sleep 1
fi

if lsof -ti:5501 > /dev/null 2>&1; then
    echo "⚠️  Porta 5501 ocupada, liberando..."
    lsof -ti:5501 | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "✅ Portas livres!"
echo ""
echo "🎯 Iniciando servidor..."
echo "📍 Acesse: http://localhost:5500"
echo ""
echo "⌨️  Para parar: Pressione Ctrl + C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Iniciar o projeto
npm run dev

