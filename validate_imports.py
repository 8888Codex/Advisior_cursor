#!/usr/bin/env python3
"""
Script de validação de importações e integridade do sistema
Execute antes de commits ou deploys para garantir que não há erros de importação
"""
import sys
import os
import asyncio
from typing import List, Tuple

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{bcolors.HEADER}{bcolors.BOLD}{'=' * 80}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{text.center(80)}{bcolors.ENDC}")
    print(f"{bcolors.HEADER}{bcolors.BOLD}{'=' * 80}{bcolors.ENDC}\n")

def print_success(text: str):
    print(f"{bcolors.OKGREEN}✅ {text}{bcolors.ENDC}")

def print_error(text: str):
    print(f"{bcolors.FAIL}❌ {text}{bcolors.ENDC}")

def print_warning(text: str):
    print(f"{bcolors.WARNING}⚠️  {text}{bcolors.ENDC}")

def print_info(text: str):
    print(f"{bcolors.OKCYAN}ℹ️  {text}{bcolors.ENDC}")

def test_import(module_name: str, description: str) -> Tuple[bool, str]:
    """Testa importação de um módulo"""
    try:
        __import__(module_name)
        return True, f"{description}: OK"
    except ImportError as e:
        return False, f"{description}: FALHA - {str(e)}"
    except Exception as e:
        return False, f"{description}: ERRO - {str(e)}"

async def validate_system():
    """Valida todo o sistema"""
    all_passed = True
    results = []
    
    print_header("VALIDAÇÃO DE IMPORTAÇÕES E INTEGRIDADE DO SISTEMA")
    
    # 1. Módulos Core
    print_info("Validando módulos core...")
    core_modules = [
        ("python_backend.models", "Models (Expert, Message, etc)"),
        ("python_backend.storage", "Storage (MemStorage)"),
        ("python_backend.postgres_storage", "PostgreSQL Storage"),
        ("python_backend.seed", "Seed Functions"),
        ("python_backend.crew_agent", "Agent Factory"),
        ("python_backend.crew_council", "Council Orchestrator"),
    ]
    
    for module, desc in core_modules:
        passed, msg = test_import(module, desc)
        results.append((passed, msg))
        if passed:
            print_success(msg)
        else:
            print_error(msg)
            all_passed = False
    
    # 2. Routers
    print_info("\nValidando routers...")
    router_modules = [
        ("python_backend.routers.experts", "Experts Router"),
        ("python_backend.routers.conversations", "Conversations Router"),
        ("python_backend.routers.council_chat", "Council Chat Router"),
    ]
    
    for module, desc in router_modules:
        passed, msg = test_import(module, desc)
        results.append((passed, msg))
        if passed:
            print_success(msg)
        else:
            print_error(msg)
            all_passed = False
    
    # 3. FastAPI App
    print_info("\nValidando FastAPI App...")
    try:
        from python_backend.main import app
        print_success("FastAPI App: OK")
        results.append((True, "FastAPI App: OK"))
    except Exception as e:
        print_error(f"FastAPI App: FALHA - {str(e)}")
        results.append((False, f"FastAPI App: FALHA - {str(e)}"))
        all_passed = False
    
    # 4. Storage e Seed
    print_info("\nValidando Storage e Seed...")
    try:
        from python_backend.storage import storage
        from python_backend.seed import seed_legends
        print_success("Storage instance: OK")
        print_info(f"   Tipo: {type(storage).__name__}")
        
        # Tentar seed
        if hasattr(storage, 'experts'):
            storage.experts.clear()
        
        await seed_legends(storage)
        experts = await storage.get_experts()
        
        if len(experts) >= 18:
            print_success(f"Seed: OK - {len(experts)} especialistas criados")
            results.append((True, f"Seed: OK - {len(experts)} especialistas"))
        else:
            print_warning(f"Seed: AVISO - Apenas {len(experts)} especialistas (esperado 18+)")
            results.append((False, f"Seed: AVISO - Apenas {len(experts)} especialistas"))
            all_passed = False
            
    except Exception as e:
        print_error(f"Storage/Seed: FALHA - {str(e)}")
        results.append((False, f"Storage/Seed: FALHA - {str(e)}"))
        all_passed = False
    
    # 5. Modelos Pydantic
    print_info("\nValidando modelos Pydantic...")
    try:
        from python_backend.models import (
            Expert, ExpertCreate, Message, MessageSend,
            Conversation, ConversationCreate, CouncilAnalysis,
            Persona, User, UserPreferences, CategoryInfo,
            ExpertContribution, ActionPlan, Phase, Action
        )
        print_success("Todos os modelos principais: OK")
        results.append((True, "Modelos Pydantic: OK"))
    except ImportError as e:
        print_error(f"Modelos Pydantic: FALHA - {str(e)}")
        results.append((False, f"Modelos Pydantic: FALHA - {str(e)}"))
        all_passed = False
    
    # 6. Prompts
    print_info("\nValidando prompts...")
    try:
        from python_backend.prompts.legends import LEGENDS_PROMPTS
        if len(LEGENDS_PROMPTS) >= 18:
            print_success(f"Prompts: OK - {len(LEGENDS_PROMPTS)} prompts disponíveis")
            results.append((True, f"Prompts: OK - {len(LEGENDS_PROMPTS)} prompts"))
        else:
            print_warning(f"Prompts: AVISO - Apenas {len(LEGENDS_PROMPTS)} prompts")
            results.append((False, f"Prompts: AVISO - {len(LEGENDS_PROMPTS)} prompts"))
    except Exception as e:
        print_error(f"Prompts: FALHA - {str(e)}")
        results.append((False, f"Prompts: FALHA - {str(e)}"))
        all_passed = False
    
    # Resumo final
    print_header("RESUMO DA VALIDAÇÃO")
    
    passed_count = sum(1 for passed, _ in results if passed)
    total_count = len(results)
    
    if all_passed:
        print_success(f"TODOS OS TESTES PASSARAM! ({passed_count}/{total_count})")
        print_info("\n✨ Sistema está pronto para uso!")
        return 0
    else:
        print_error(f"ALGUNS TESTES FALHARAM: {passed_count}/{total_count} passaram")
        print_warning("\n⚠️  Corrija os erros acima antes de fazer commit ou deploy!")
        return 1

def main():
    """Função principal"""
    try:
        exit_code = asyncio.run(validate_system())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n❌ Erro crítico durante validação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

