#!/bin/bash
# Script de code signing e notarization para macOS

set -e

APP_PATH="$1"
IDENTITY="${2:-Developer ID Application: Your Name (TEAM_ID)}"
ENTITLEMENTS="entitlements.plist"

if [ -z "$APP_PATH" ]; then
    echo "Uso: $0 <caminho_para_app> [identity]"
    echo "Exemplo: $0 dist/UOCM.app"
    exit 1
fi

if [ ! -d "$APP_PATH" ]; then
    echo "Erro: $APP_PATH não encontrado"
    exit 1
fi

echo "=== Code Signing e Notarization ==="
echo "App: $APP_PATH"
echo "Identity: $IDENTITY"

# Criar entitlements.plist se não existir
if [ ! -f "$ENTITLEMENTS" ]; then
    cat > "$ENTITLEMENTS" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
EOF
fi

# Sign frameworks
echo "Assinando frameworks..."
find "$APP_PATH" -name "*.framework" -exec codesign --force --deep --sign "$IDENTITY" --entitlements "$ENTITLEMENTS" {} \;

# Sign app
echo "Assinando aplicação..."
codesign --force --deep --sign "$IDENTITY" --entitlements "$ENTITLEMENTS" "$APP_PATH"

# Verificar assinatura
echo "Verificando assinatura..."
codesign --verify --verbose "$APP_PATH"
spctl --assess --verbose "$APP_PATH"

# Criar .dmg
DMG_NAME="UOCM-v1.0.0.dmg"
DMG_PATH="dist/$DMG_NAME"
echo "Criando DMG..."
hdiutil create -volname "UOCM" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_PATH"

# Assinar DMG
echo "Assinando DMG..."
codesign --sign "$IDENTITY" "$DMG_PATH"

# Notarizar (requer Apple ID e app-specific password)
echo ""
echo "=== Notarization ==="
echo "Para notarizar, execute manualmente:"
echo "  xcrun notarytool submit $DMG_PATH --apple-id YOUR_APPLE_ID --team-id YOUR_TEAM_ID --password APP_SPECIFIC_PASSWORD --wait"
echo ""
echo "Ou usando altool (deprecated):"
echo "  xcrun altool --notarize-app \\"
echo "    --primary-bundle-id dev.mestre.efi.uocm \\"
echo "    --username YOUR_APPLE_ID \\"
echo "    --password APP_SPECIFIC_PASSWORD \\"
echo "    --file $DMG_PATH"

echo ""
echo "=== Signing concluído! ==="
echo "DMG criado: $DMG_PATH"

