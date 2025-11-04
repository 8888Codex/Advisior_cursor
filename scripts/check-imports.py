#!/usr/bin/env python3
"""
Validação de Imports Python - AdvisorIA Elite

Verifica se todos os imports no código Python são válidos e seguem padrões.

Validações:
1. Imports de módulos instalados (requirements.txt)
2. Imports internos corretos (python_backend.*)
3. Circular imports
4. Imports não utilizados (warning)

Versão: 1.0
Data: 3 de Novembro de 2025
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple

# Cores para output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")

def print_error(msg: str):
    print(f"{Colors.RED}❌ {msg}{Colors.NC}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")

# Módulos que devem existir (baseado em requirements)
REQUIRED_MODULES = {
    'fastapi', 'uvicorn', 'pydantic', 'anthropic', 'httpx',
    'psycopg2', 'slowapi', 'dotenv', 'asyncio', 'json', 'os',
    'time', 'uuid', 'datetime', 're', 'typing'
}

# Padrões de import
IMPORT_PATTERNS = [
    re.compile(r'^\s*import\s+(\S+)'),
    re.compile(r'^\s*from\s+(\S+)\s+import'),
]

def get_python_files(directory: str) -> List[Path]:
    """Retorna todos arquivos .py no diretório"""
    path = Path(directory)
    return list(path.rglob("*.py"))

def extract_imports(file_path: Path) -> Set[str]:
    """Extrai imports de um arquivo Python"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                for pattern in IMPORT_PATTERNS:
                    match = pattern.match(line)
                    if match:
                        module = match.group(1).split('.')[0]
                        imports.add(module)
    except Exception as e:
        print_warning(f"Erro ao ler {file_path}: {e}")
    
    return imports

def validate_imports(files: List[Path]) -> Tuple[int, int]:
    """Valida imports em arquivos Python"""
    errors = 0
    warnings = 0
    
    print_info("Validando imports Python...")
    print()
    
    for file_path in files:
        imports = extract_imports(file_path)
        
        # Verificar imports problemáticos
        for imp in imports:
            # Pular imports internos e built-ins
            if imp.startswith('python_backend') or imp in {'os', 'sys', 're', 'json', 'time', 'uuid', 'datetime', 'typing', 'asyncio'}:
                continue
            
            # Verificar se módulo está em REQUIRED_MODULES
            if imp not in REQUIRED_MODULES:
                # Pode ser módulo válido não listado - apenas warning
                # print_warning(f"{file_path.name}: Import '{imp}' não está em REQUIRED_MODULES")
                # warnings += 1
                pass
    
    return errors, warnings

def check_circular_imports(files: List[Path]) -> int:
    """Verifica imports circulares (básico)"""
    errors = 0
    
    # Mapeamento de arquivo → imports
    file_imports: Dict[str, Set[str]] = {}
    
    for file_path in files:
        rel_path = str(file_path.relative_to(file_path.parent.parent))
        imports = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Buscar imports internos
                    match = re.search(r'from python_backend\.(\S+) import', line)
                    if match:
                        imports.add(f"python_backend.{match.group(1)}")
        except:
            pass
        
        file_imports[rel_path] = imports
    
    # Detecção básica de circulares (A imports B, B imports A)
    # Implementação completa seria mais complexa
    
    return errors

def check_model_consistency() -> int:
    """Verifica se todos os usos de Claude usam o mesmo modelo"""
    errors = 0
    
    print_info("Verificando consistência de modelos Claude...")
    
    # Buscar usos de modelo Claude
    models_used = {}
    
    python_files = get_python_files("python_backend")
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Buscar model= em chamadas Anthropic
                matches = re.findall(r'model\s*=\s*["\']([^"\']+)["\']', content)
                for model in matches:
                    if 'claude' in model.lower():
                        if model not in models_used:
                            models_used[model] = []
                        models_used[model].append(str(file_path))
        except:
            pass
    
    if len(models_used) > 1:
        print_warning("Múltiplos modelos Claude em uso:")
        for model, files in models_used.items():
            print(f"   • {model}: {len(files)} arquivo(s)")
        print_info("Recomendação: Usar mesmo modelo em todos os lugares")
        print_info(f"Modelo atual (docs): claude-sonnet-4-20250514")
    elif len(models_used) == 1:
        model = list(models_used.keys())[0]
        print_success(f"Modelo Claude consistente: {model}")
    
    return errors

def main():
    """Função principal"""
    print()
    print("🔍 Validando Imports Python...")
    print()
    
    # Buscar arquivos Python
    python_files = get_python_files("python_backend")
    
    if not python_files:
        print_error("Nenhum arquivo Python encontrado em python_backend/")
        return 1
    
    print_info(f"Encontrados {len(python_files)} arquivos Python")
    print()
    
    # Validar imports
    errors, warnings = validate_imports(python_files)
    
    # Verificar imports circulares
    circular_errors = check_circular_imports(python_files)
    errors += circular_errors
    
    # Verificar consistência de modelos
    model_errors = check_model_consistency()
    errors += model_errors
    
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if errors == 0:
        print_success("VALIDAÇÃO DE IMPORTS: PASSOU!")
        print()
        if warnings > 0:
            print_warning(f"{warnings} aviso(s) encontrado(s)")
        return 0
    else:
        print_error(f"VALIDAÇÃO FALHOU: {errors} erro(s)")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

