#!/bin/bash
# Render Build Script - Frontend + Backend

echo "🔨 RENDER BUILD - Frontend + Backend"
echo "====================================="
echo ""

echo "📦 PASSO 1: Instalar dependências Node.js..."
npm install --include=dev
echo "✅ Node.js dependencies instaladas"
echo ""

echo "🎨 PASSO 2: Build do frontend (Vite)..."
npm run build
echo "✅ Frontend buildado em dist/public/"
echo ""

echo "🐍 PASSO 3: Instalar dependências Python..."
pip install -r python_backend/requirements.txt
echo "✅ Python dependencies instaladas"
echo ""

echo "📊 Verificando build..."
ls -lh dist/public/ | head -10
echo ""

echo "✅ BUILD COMPLETO!"

