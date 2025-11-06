#!/bin/bash
# Script de teste e build

set -e

echo "=== UOCM - Teste e Build ==="
echo ""

# Verificar Python
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python: $python_version"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Erro: Python 3.11+ é necessário"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Instalar dependências
echo "Instalando dependências..."
pip install -q -r requirements.txt

# Executar testes
echo ""
echo "=== Executando Testes ==="
python3 -m pytest tests/ -v || echo "Alguns testes falharam (continuando...)"

# Verificar lint
echo ""
echo "=== Verificando Lint ==="
if command -v ruff &> /dev/null; then
    ruff check uocm/ || echo "Lint encontrou problemas (continuando...)"
else
    echo "ruff não instalado, pulando lint"
fi

# Verificar tipo
echo ""
echo "=== Verificando Tipos ==="
if command -v mypy &> /dev/null; then
    mypy uocm/ || echo "Type checking encontrou problemas (continuando...)"
else
    echo "mypy não instalado, pulando type checking"
fi

# Build se solicitado
if [ "$1" == "--build" ]; then
    echo ""
    echo "=== Build ==="
    if [[ "$OSTYPE" == "darwin"* ]]; then
        bash scripts/build_mac.sh
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        bash scripts/build_windows.bat
    else
        echo "Plataforma não suportada para build automático"
    fi
fi

echo ""
echo "=== Concluído! ==="

