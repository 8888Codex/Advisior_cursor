#!/bin/bash

# Script de Monitoramento do Render
# Execute APÓS aplicar as correções no dashboard

echo "🔍 MONITORANDO RENDER"
echo "====================="
echo ""

RENDER_URL="https://advisior-cursor.onrender.com"
MAX_ATTEMPTS=30
SLEEP_TIME=20

echo "URL: $RENDER_URL"
echo "Tentativas máximas: $MAX_ATTEMPTS"
echo "Intervalo: ${SLEEP_TIME}s"
echo ""
echo "⏳ Aguardando Render ficar online..."
echo ""

for i in $(seq 1 $MAX_ATTEMPTS); do
    echo -n "Tentativa $i/$MAX_ATTEMPTS: "
    
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$RENDER_URL" 2>&1)
    
    if [ "$STATUS" = "200" ]; then
        echo "✅ ONLINE!"
        echo ""
        echo "🎉 RENDER ESTÁ FUNCIONANDO!"
        echo ""
        echo "Executando testes completos..."
        ./test_producao.sh
        exit 0
    else
        echo "Status $STATUS (aguardando...)"
        sleep $SLEEP_TIME
    fi
done

echo ""
echo "❌ Timeout após $((MAX_ATTEMPTS * SLEEP_TIME / 60)) minutos"
echo ""
echo "Possíveis causas:"
echo "  1. Deploy ainda em andamento"
echo "  2. Erro na configuração"
echo "  3. Serviço travado"
echo ""
echo "Ações:"
echo "  1. Verifique logs no dashboard Render"
echo "  2. Confirme que Build Command está correto"
echo "  3. Confirme que Start Command está correto"
echo "  4. Verifique Environment Variables"
echo ""
exit 1

