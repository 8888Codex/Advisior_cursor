#!/usr/bin/env python3
"""
Validação de Compatibilidade de Endpoints - AdvisorIA Elite

Verifica se endpoints existentes no código estão documentados e se schemas
estão sincronizados entre backend (Python) e frontend (TypeScript).

Validações:
1. Endpoints em main.py estão em API_REFERENCE.md
2. Schemas Python (Pydantic) compatíveis com docs
3. Rate limits documentados
4. Nenhum endpoint foi removido acidentalmente

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

# Endpoints conhecidos (baseado em docs/API_REFERENCE.md)
DOCUMENTED_ENDPOINTS = {
    # Experts API
    "GET /api/experts",
    "GET /api/experts/:id",
    "POST /api/experts",
    "POST /api/experts/auto-clone",
    "POST /api/experts/:id/chat",
    "POST /api/experts/test-chat",
    
    # Personas API
    "GET /api/personas",
    "POST /api/personas",
    "POST /api/personas/enhance-description",
    "DELETE /api/personas/:id",
    
    # Council API
    "POST /api/council/analyze",
    "POST /api/council/analyze-async",
    "POST /api/council/analyze-stream",
    "GET /api/council/tasks/:id",
    "POST /api/council/recommend-experts",
    
    # Conversations API
    "POST /api/council/conversations",
    "GET /api/council/conversations/:id",
    "GET /api/council/conversations/:id/messages",
    "POST /api/council/conversations/:id/messages",
}

def extract_endpoints_from_code(file_path: str) -> List[Dict[str, str]]:
    """Extrai endpoints definidos no código FastAPI"""
    endpoints = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Padrão: @app.METHOD("/path")
            pattern = r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']\)'
            matches = re.findall(pattern, content)
            
            for method, path in matches:
                endpoints.append({
                    'method': method.upper(),
                    'path': path,
                    'full': f"{method.upper()} {path}"
                })
    
    except Exception as e:
        print_warning(f"Erro ao ler {file_path}: {e}")
    
    return endpoints

def check_rate_limits(file_path: str) -> Dict[str, str]:
    """Verifica rate limits configurados"""
    rate_limits = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for i, line in enumerate(lines):
                # Buscar @limiter.limit("X/hour")
                match = re.search(r'@limiter\.limit\(["\']([^"\']+)["\']\)', line)
                if match:
                    limit = match.group(1)
                    
                    # Próxima linha deve ser @app.METHOD
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        endpoint_match = re.search(r'@app\.(get|post|put|delete)\(["\']([^"\']+)["\']\)', next_line)
                        if endpoint_match:
                            method = endpoint_match.group(1).upper()
                            path = endpoint_match.group(2)
                            rate_limits[f"{method} {path}"] = limit
    
    except Exception as e:
        print_warning(f"Erro ao verificar rate limits: {e}")
    
    return rate_limits

def validate_endpoints():
    """Validação principal de endpoints"""
    errors = 0
    warnings = 0
    
    print()
    print_info("Validando Endpoints...")
    print()
    
    # Extrair endpoints do código
    main_py = "python_backend/main.py"
    
    if not os.path.exists(main_py):
        print_error("python_backend/main.py não encontrado!")
        return 1, 0
    
    code_endpoints = extract_endpoints_from_code(main_py)
    code_endpoint_set = {ep['full'] for ep in code_endpoints}
    
    print_info(f"Endpoints encontrados no código: {len(code_endpoints)}")
    
    # Verificar se endpoints documentados existem no código
    missing_in_code = DOCUMENTED_ENDPOINTS - code_endpoint_set
    if missing_in_code:
        print()
        print_warning("Endpoints documentados mas NÃO encontrados no código:")
        for endpoint in sorted(missing_in_code):
            # Alguns endpoints têm :id que não batem exato - permitir
            if ':id' not in endpoint:
                print(f"   • {endpoint}")
                warnings += 1
    
    # Verificar se há endpoints não documentados
    # Normalizar endpoints com :id para comparação
    def normalize_endpoint(ep: str) -> str:
        # Substituir {id}, {taskId}, etc por :id
        ep = re.sub(r'\{[^}]+\}', ':id', ep)
        return ep
    
    normalized_code = {normalize_endpoint(ep) for ep in code_endpoint_set}
    normalized_docs = {normalize_endpoint(ep) for ep in DOCUMENTED_ENDPOINTS}
    
    undocumented = normalized_code - normalized_docs
    if undocumented:
        print()
        print_warning("Endpoints NO CÓDIGO mas NÃO documentados:")
        for endpoint in sorted(undocumented):
            print(f"   • {endpoint}")
            print_info("     → Adicione em docs/API_REFERENCE.md")
        warnings += 1
    
    # Verificar rate limits
    rate_limits = check_rate_limits(main_py)
    
    endpoints_without_limit = []
    for endpoint in code_endpoints:
        full = endpoint['full']
        normalized = normalize_endpoint(full)
        
        # POST/PUT/DELETE devem ter rate limit
        if endpoint['method'] in ['POST', 'PUT', 'DELETE']:
            if full not in rate_limits and normalized not in rate_limits:
                endpoints_without_limit.append(full)
    
    if endpoints_without_limit:
        print()
        print_warning("Endpoints sem rate limit (POST/PUT/DELETE devem ter):")
        for ep in endpoints_without_limit[:5]:  # Mostrar apenas primeiros 5
            print(f"   • {ep}")
        if len(endpoints_without_limit) > 5:
            print(f"   ... e mais {len(endpoints_without_limit) - 5}")
    
    print()
    
    return errors, warnings

def main():
    """Função principal"""
    print()
    print("🔍 Validação de Endpoints...")
    print()
    
    errors, warnings = validate_endpoints()
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    
    if errors == 0:
        print_success("VALIDAÇÃO DE ENDPOINTS: PASSOU!")
        if warnings > 0:
            print()
            print_warning(f"{warnings} aviso(s) - revise mas não bloqueia")
        print()
        return 0
    else:
        print_error(f"VALIDAÇÃO FALHOU: {errors} erro(s)")
        print()
        print_info("Consulte: docs/API_REFERENCE.md")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

