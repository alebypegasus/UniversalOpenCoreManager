#!/bin/zsh
set -euo pipefail
APP_PATH=${1:?"Passe o caminho do .app"}
IDENTITY=${CODESIGN_IDENTITY:-"Developer ID Application: YOUR NAME (TEAMID)"}
BUNDLE_ID=${BUNDLE_ID:-"com.example.uocm"}

codesign --deep --force --options runtime --sign "$IDENTITY" "$APP_PATH"

# Notarize (placeholder):
# xcrun notarytool submit "$APP_PATH" --apple-id YOUR_ID --team-id YOUR_TEAM --password YOUR_PASS --wait
# xcrun stapler staple "$APP_PATH"

echo "Assinatura concluída (placeholder notarize)."
