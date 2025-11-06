#!/bin/bash
# Script de setup do projeto UOCM

set -e

echo "=== UOCM - Universal OpenCore Manager ==="
echo "Configurando ambiente de desenvolvimento..."

# Verificar Python 3.11+
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Erro: Python 3.11+ é necessário. Versão atual: $python_version"
    exit 1
fi

echo "Python encontrado: $python_version"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Instalar dependências de desenvolvimento
if [ "$1" == "--dev" ]; then
    echo "Instalando dependências de desenvolvimento..."
    pip install -e ".[dev]"
fi

# Inicializar banco de dados
echo "Inicializando banco de dados..."
python3 -c "from uocm.db.database import get_database; get_database().init_db()"

echo ""
echo "=== Setup concluído! ==="
echo "Para ativar o ambiente virtual, execute:"
echo "  source venv/bin/activate"
echo ""
echo "Para executar a aplicação:"
echo "  python -m uocm.main"

