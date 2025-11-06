#!/bin/bash
# Script de build para macOS (.app bundle)

set -e

echo "=== UOCM - Build para macOS ==="

# Verificar se estamos no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Erro: Este script só funciona no macOS"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalar py2app se não estiver instalado
if ! python3 -c "import py2app" 2>/dev/null; then
    echo "Instalando py2app..."
    pip install py2app
fi

# Criar diretório de build
BUILD_DIR="build"
DIST_DIR="dist"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Criar setup.py para py2app se não existir
# Verificar se ícone existe
if [ ! -f "assets/icon.icns" ]; then
    echo "⚠ Aviso: assets/icon.icns não encontrado."
    echo "  O app será criado sem ícone personalizado."
    echo "  Para criar o ícone, coloque assets/icon.png e execute:"
    echo "    ./scripts/create_icons.sh"
    echo ""
fi

if [ ! -f "setup.py" ]; then
    cat > setup.py << 'EOF'
from setuptools import setup
from pathlib import Path

APP = ['uocm/main.py']
DATA_FILES = [
    ('translations', ['translations']),
    ('templates', ['templates']),
    ('plugins', ['plugins']),
]

OPTIONS = {
    'argv_emulation': False,
    'packages': ['uocm', 'PyQt6', 'sqlalchemy'],
    'includes': ['uocm.*'],
    'iconfile': 'assets/icon.icns' if Path('assets/icon.icns').exists() else None,
    'plist': {
        'CFBundleName': 'UOCM',
        'CFBundleDisplayName': 'Universal OpenCore Manager',
        'CFBundleIdentifier': 'dev.mestre.efi.uocm',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHighResolutionCapable': True,
        'NSHumanReadableCopyright': 'Copyright © 2024 Mestre EFI',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF
fi

# Build
echo "Construindo aplicação..."
python3 setup.py py2app

echo ""
echo "=== Build concluído! ==="
echo "Aplicação .app está em: $DIST_DIR/UOCM.app"
echo ""
echo "Para testar:"
echo "  open $DIST_DIR/UOCM.app"
