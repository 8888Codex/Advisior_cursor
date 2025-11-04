#!/bin/bash

# ============================================================================
# SCRIPT DE VALIDAÇÃO DE MUDANÇAS - AdvisorIA Elite
# ============================================================================
# 
# Este script valida mudanças de código contra a documentação e padrões
# estabelecidos para prevenir quebras por erros básicos.
#
# Uso: bash scripts/validate-changes.sh
#
# Versão: 1.0
# Data: 3 de Novembro de 2025
# ============================================================================

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
ERRORS=0
WARNINGS=0
CHECKS=0

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🛡️  VALIDAÇÃO DE MUDANÇAS - AdvisorIA Elite v2.0"
echo "═══════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# FUNÇÃO: Print com cor
# ============================================================================
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_check() {
    echo -e "${BLUE}🔍 Verificando: $1${NC}"
    ((CHECKS++))
}

# ============================================================================
# CHECK 1: TypeScript Type Checking
# ============================================================================
print_check "TypeScript Type Checking"

if command -v npm &> /dev/null; then
    if npm run check &> /dev/null; then
        print_success "TypeScript: Sem erros de tipos"
    else
        print_error "TypeScript: Erros de tipos encontrados! Rode 'npm run check' para detalhes"
    fi
else
    print_warning "npm não encontrado - pulando type check"
fi

echo ""

# ============================================================================
# CHECK 2: Python Imports Validation
# ============================================================================
print_check "Python Imports"

if [ -f "scripts/check-imports.py" ]; then
    if python3 scripts/check-imports.py &> /dev/null; then
        print_success "Python: Imports válidos"
    else
        print_error "Python: Erros de import encontrados! Rode 'python3 scripts/check-imports.py'"
    fi
else
    print_warning "scripts/check-imports.py não encontrado - pulando"
fi

echo ""

# ============================================================================
# CHECK 3: Endpoint Compatibility
# ============================================================================
print_check "Compatibilidade de Endpoints"

if [ -f "scripts/check-endpoints.py" ]; then
    if python3 scripts/check-endpoints.py &> /dev/null; then
        print_success "Endpoints: Compatíveis com documentação"
    else
        print_error "Endpoints: Incompatibilidades encontradas! Rode 'python3 scripts/check-endpoints.py'"
    fi
else
    print_warning "scripts/check-endpoints.py não encontrado - pulando"
fi

echo ""

# ============================================================================
# CHECK 4: Naming Conventions
# ============================================================================
print_check "Convenções de Naming"

NAMING_ERRORS=0

# Check Python: snake_case para funções
PYTHON_CAMEL=$(grep -rn "def [a-z][a-zA-Z]*(" python_backend/*.py 2>/dev/null | grep -v "def [a-z_]*(" || true)
if [ -n "$PYTHON_CAMEL" ]; then
    print_warning "Python: Funções devem usar snake_case (encontradas camelCase)"
    ((NAMING_ERRORS++))
fi

# Check TypeScript: PascalCase para componentes
TS_SNAKE=$(find client/src/components -name "*.tsx" -type f 2>/dev/null | grep "_" || true)
if [ -n "$TS_SNAKE" ]; then
    print_warning "React: Componentes devem usar PascalCase (encontrados snake_case)"
    ((NAMING_ERRORS++))
fi

if [ $NAMING_ERRORS -eq 0 ]; then
    print_success "Naming: Convenções seguidas"
fi

echo ""

# ============================================================================
# CHECK 5: Environment Variables
# ============================================================================
print_check "Variáveis de Ambiente"

if [ ! -f ".env" ]; then
    print_error ".env não encontrado! Crie baseado em DEPLOY_ENV_EXAMPLE.txt"
else
    # Verificar variáveis críticas
    if grep -q "ANTHROPIC_API_KEY" .env && grep -q "PERPLEXITY_API_KEY" .env; then
        print_success "Variáveis: API keys configuradas"
    else
        print_error "Variáveis: API keys faltando no .env"
    fi
fi

echo ""

# ============================================================================
# CHECK 6: Documentação Atualizada
# ============================================================================
print_check "Documentação Atualizada"

# Verificar se arquivos essenciais existem
DOCS_MISSING=0

if [ ! -f "docs/ARCHITECTURE.md" ]; then
    print_error "docs/ARCHITECTURE.md não encontrado!"
    ((DOCS_MISSING++))
fi

if [ ! -f "docs/API_REFERENCE.md" ]; then
    print_error "docs/API_REFERENCE.md não encontrado!"
    ((DOCS_MISSING++))
fi

if [ ! -f "docs/DEVELOPMENT.md" ]; then
    print_error "docs/DEVELOPMENT.md não encontrado!"
    ((DOCS_MISSING++))
fi

if [ $DOCS_MISSING -eq 0 ]; then
    print_success "Documentação: Arquivos principais presentes"
fi

echo ""

# ============================================================================
# CHECK 7: Git Status (Warnings)
# ============================================================================
print_check "Git Status"

# Verificar se há mudanças não commitadas em arquivos críticos
if git diff --name-only 2>/dev/null | grep -q "python_backend/main.py\|client/src/App.tsx\|server/index.ts"; then
    print_warning "Mudanças em arquivos críticos detectadas - certifique-se de testar!"
fi

# Verificar se há arquivos não trackeados que deveriam estar no .gitignore
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | grep -E "\.log$|\.pyc$|node_modules|\.env$" || true)
if [ -n "$UNTRACKED" ]; then
    print_warning "Arquivos não trackeados que deveriam estar no .gitignore"
fi

print_success "Git: Status verificado"

echo ""

# ============================================================================
# CHECK 8: Backend Running
# ============================================================================
print_check "Backend Status"

# Verificar se Python backend está rodando
if lsof -i:5501 &> /dev/null; then
    print_success "Backend Python: Rodando na porta 5501"
else
    print_warning "Backend Python: NÃO está rodando na porta 5501"
fi

# Verificar se Node server está rodando
if lsof -i:5500 &> /dev/null; then
    print_success "Backend Node: Rodando na porta 5500"
else
    print_warning "Backend Node: NÃO está rodando na porta 5500"
fi

echo ""

# ============================================================================
# RESUMO FINAL
# ============================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 RESUMO DA VALIDAÇÃO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Verificações realizadas: $CHECKS"
echo -e "${GREEN}Sucessos:${NC} $((CHECKS - ERRORS - WARNINGS))"
echo -e "${YELLOW}Avisos:${NC} $WARNINGS"
echo -e "${RED}Erros:${NC} $ERRORS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}  ✅ VALIDAÇÃO PASSOU!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Você pode commitar suas mudanças com segurança."
    echo ""
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}Avisos encontrados - revise antes de commitar.${NC}"
        echo ""
    fi
    exit 0
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${RED}  ❌ VALIDAÇÃO FALHOU!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${RED}$ERRORS erro(s) crítico(s) encontrado(s).${NC}"
    echo ""
    echo "CORRIJA OS ERROS ANTES DE COMMITAR!"
    echo ""
    echo "Consulte a documentação relevante:"
    echo "  • docs/ARCHITECTURE.md"
    echo "  • docs/API_REFERENCE.md"
    echo "  • docs/DEVELOPMENT.md"
    echo ""
    exit 1
fi

