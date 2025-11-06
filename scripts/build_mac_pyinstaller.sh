#!/bin/bash
# Script de build para macOS usando PyInstaller (alternativa ao py2app)

set -e

echo "=== UOCM - Build para macOS (PyInstaller) ==="

# Verificar se estamos no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Erro: Este script só funciona no macOS"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Instalar PyInstaller se não estiver instalado
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "Instalando PyInstaller..."
    pip install PyInstaller
fi

# Criar diretório de build
BUILD_DIR="build"
DIST_DIR="dist"
mkdir -p "$BUILD_DIR" "$DIST_DIR"

# Verificar se ícone existe
ICON_FLAG=""
if [ -f "assets/icon.icns" ]; then
    ICON_FLAG="--icon=assets/icon.icns"
    echo "✓ Ícone encontrado: assets/icon.icns"
else
    echo "⚠ Aviso: assets/icon.icns não encontrado."
    echo "  O app será criado sem ícone personalizado."
fi

# Criar spec file
echo "Criando spec file..."
python3 -m PyInstaller --name=UOCM \
    --windowed \
    --onedir \
    --add-data "translations:translations" \
    --add-data "templates:templates" \
    --add-data "plugins:plugins" \
    --hidden-import=PyQt6 \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=sqlalchemy \
    --hidden-import=uocm \
    --hidden-import=uocm.core \
    --hidden-import=uocm.ui \
    --hidden-import=uocm.db \
    --hidden-import=uocm.detector \
    --hidden-import=uocm.engine_generator \
    --hidden-import=uocm.plist_editor \
    --hidden-import=uocm.kext_manager \
    --hidden-import=uocm.acpi_manager \
    --hidden-import=uocm.debugger \
    --hidden-import=uocm.plugins \
    $ICON_FLAG \
    --osx-bundle-identifier=dev.mestre.efi.uocm \
    uocm/main.py

echo ""
echo "=== Build concluído! ==="
echo "Aplicação .app está em: $DIST_DIR/UOCM.app"
echo ""
echo "Para testar:"
echo "  open $DIST_DIR/UOCM.app"

