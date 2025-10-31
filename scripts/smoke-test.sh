#!/bin/bash
# Smoke tests básicos para validação local e CI

set -e

echo "🧪 Running smoke tests..."

# Test 1: Type check
echo "✓ Type checking..."
npm run check

# Test 2: Build
echo "✓ Building..."
npm run build

# Test 3: Health endpoints (se servidor estiver rodando)
if curl -s http://localhost:3000 > /dev/null 2>&1; then
  echo "✓ UI endpoint responding"
else
  echo "⚠ UI endpoint not available (server may not be running)"
fi

if curl -s http://localhost:5200/api/health > /dev/null 2>&1; then
  echo "✓ API health endpoint responding"
  curl -s http://localhost:5200/api/health | grep -q '"status":"ok"' && echo "✓ Health check valid"
else
  echo "⚠ API endpoint not available (server may not be running)"
fi

echo "✅ Smoke tests completed!"


