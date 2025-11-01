"""
Background Tasks System
========================

Sistema para executar tarefas em segundo plano, permitindo que o usuário
navegue pela aplicação enquanto tarefas longas são executadas.
"""

import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import uuid
from python_backend.models import BackgroundTask, TaskStatus, TaskType
from python_backend.storage import storage

# Task registry - armazena funções de processamento por tipo de task
_task_processors: Dict[TaskType, Callable] = {}


def register_task_processor(task_type: TaskType, processor: Callable):
    """Registra um processador para um tipo de task"""
    _task_processors[task_type] = processor


async def create_task(
    user_id: str,
    task_type: TaskType,
    metadata: Optional[Dict[str, Any]] = None
) -> BackgroundTask:
    """Cria uma nova task em background"""
    task_id = str(uuid.uuid4())
    
    task = BackgroundTask(
        id=task_id,
        userId=user_id,
        taskType=task_type,
        status=TaskStatus.PENDING,
        progress=0,
        metadata=metadata or {},
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    
    # Salvar task no storage
    await storage.create_background_task(task)
    
    # Iniciar processamento em background
    asyncio.create_task(process_task(task_id))
    
    return task


async def process_task(task_id: str):
    """Processa uma task em background"""
    try:
        # Buscar task
        task = await storage.get_background_task(task_id)
        if not task:
            print(f"[Background Task] Task {task_id} não encontrada")
            return
        
        # Atualizar status para RUNNING
        await storage.update_background_task(
            task_id,
            status=TaskStatus.RUNNING,
            progress=0
        )
        
        # Obter processador para este tipo de task
        processor = _task_processors.get(task.taskType)
        if not processor:
            await storage.update_background_task(
                task_id,
                status=TaskStatus.FAILED,
                error=f"Processador não encontrado para tipo {task.taskType}"
            )
            return
        
        # Executar processador
        result = await processor(task.metadata)
        
        # Atualizar task como completada
        await storage.update_background_task(
            task_id,
            status=TaskStatus.COMPLETED,
            progress=100,
            result=result,
            completedAt=datetime.utcnow()
        )
        
        print(f"[Background Task] Task {task_id} completada com sucesso")
        
    except Exception as e:
        print(f"[Background Task] Erro ao processar task {task_id}: {e}")
        import traceback
        traceback.print_exc()
        
        # Atualizar task como falha
        try:
            await storage.update_background_task(
                task_id,
                status=TaskStatus.FAILED,
                error=str(e)
            )
        except:
            pass


async def get_task_status(task_id: str) -> Optional[BackgroundTask]:
    """Obtém o status de uma task"""
    return await storage.get_background_task(task_id)


async def cancel_task(task_id: str) -> bool:
    """Cancela uma task (se ainda estiver pendente ou rodando)"""
    task = await storage.get_background_task(task_id)
    if not task:
        return False
    
    if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
        await storage.update_background_task(
            task_id,
            status=TaskStatus.CANCELLED
        )
        return True
    
    return False

