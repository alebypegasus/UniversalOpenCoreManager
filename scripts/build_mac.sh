#!/bin/zsh
set -euo pipefail
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --noconfirm \
  --name "Universal OpenCore Manager" \
  --windowed \
  --add-data "universal_oc_manager/ui/qml:universal_oc_manager/ui/qml" \
  app.py
