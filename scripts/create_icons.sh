#!/bin/bash
# Script para criar ícones do app a partir de uma imagem PNG

set -e

ICON_SOURCE="assets/icon.png"
ICONSET_DIR="assets/icon.iconset"
ICNS_OUTPUT="assets/icon.icns"

echo "=== Criando Ícones do UOCM ==="

# Verificar se imagem fonte existe
if [ ! -f "$ICON_SOURCE" ]; then
    echo "Erro: $ICON_SOURCE não encontrado!"
    echo "Por favor, coloque uma imagem PNG de 1024x1024 em assets/icon.png"
    exit 1
fi

echo "Imagem fonte encontrada: $ICON_SOURCE"

# Criar diretório iconset
rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

# Criar diferentes tamanhos para macOS
echo "Gerando tamanhos para macOS..."

# macOS requer múltiplos tamanhos
sips -z 16 16 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_16x16.png" > /dev/null 2>&1
sips -z 32 32 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_16x16@2x.png" > /dev/null 2>&1
sips -z 32 32 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_32x32.png" > /dev/null 2>&1
sips -z 64 64 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_32x32@2x.png" > /dev/null 2>&1
sips -z 128 128 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_128x128.png" > /dev/null 2>&1
sips -z 256 256 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_128x128@2x.png" > /dev/null 2>&1
sips -z 256 256 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_256x256.png" > /dev/null 2>&1
sips -z 512 512 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_256x256@2x.png" > /dev/null 2>&1
sips -z 512 512 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_512x512.png" > /dev/null 2>&1
sips -z 1024 1024 "$ICON_SOURCE" --out "${ICONSET_DIR}/icon_512x512@2x.png" > /dev/null 2>&1

# Converter para .icns
echo "Convertendo para .icns..."
iconutil -c icns "$ICONSET_DIR" -o "$ICNS_OUTPUT"

# Limpar diretório temporário
rm -rf "$ICONSET_DIR"

echo ""
echo "✓ Ícone macOS criado: $ICNS_OUTPUT"

# Criar .ico para Windows usando Python/Pillow
echo "Criando .ico para Windows..."
if python3 -c "from PIL import Image" 2>/dev/null; then
    python3 scripts/create_ico.py
elif command -v convert &> /dev/null; then
    convert "$ICON_SOURCE" -define icon:auto-resize=256,128,64,48,32,16 "assets/icon.ico"
    echo "✓ Ícone Windows criado: assets/icon.ico"
else
    echo "⚠ Pillow/ImageMagick não encontrado. Instalando Pillow..."
    pip install -q Pillow
    python3 scripts/create_ico.py
fi

echo ""
echo "=== Concluído! ==="

