# Solução para Background Tasks

## Problema
Quando o usuário muda de página, as tarefas (análise do conselho, respostas do chat) são canceladas porque a requisição HTTP é interrompida.

## Solução Implementada

### 1. Backend - Processamento Assíncrono Não-Bloqueante
- Endpoints retornam imediatamente (202 Accepted)
- Processamento acontece em background usando `asyncio.create_task`
- Resultados salvos no banco de dados
- Status pode ser consultado via polling

### 2. Frontend - Polling Persistent
- Quando usuário muda de página, salvar task IDs no localStorage
- Service Worker ou polling em background verifica status
- Notificações quando task completa

## Implementação Rápida (Simplificada)

Para começar rápido, vamos fazer:
1. Modificar `send_message_to_council` para processar em background
2. Retornar imediatamente com status "processing"
3. Frontend faz polling para verificar novas mensagens

## Próximos Passos (Completo)

1. ✅ Criar modelo BackgroundTask
2. ⏳ Adicionar storage methods para tasks
3. ⏳ Modificar endpoints para criar tasks
4. ⏳ Endpoint de status de task
5. ⏳ Frontend polling service
6. ⏳ Notificações quando completo

