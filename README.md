# Universal OpenCore Manager (Python – macOS first)

Desktop application in Python (PyQt6 + Qt Quick/QML) to generate, edit, validate, update and export OpenCore EFIs with macOS 26 (Tahoe, Liquid Glass) style UX. This is the base app for macOS; later it will be adapted for Windows (Python) and rebuilt natively in Swift/SwiftUI.

## 📋 Blueprint & Standards

**See [BLUEPRINT.md](./BLUEPRINT.md) for complete project documentation**, including:
- Detailed architecture (Phase 1: macOS Python, Phase 2: Windows Python, Phase 3: macOS Swift)
- Module structure and functionalities
- Roadmap and milestones
- Technical references and acceptance criteria

**See [CODING_STANDARDS.md](./CODING_STANDARDS.md) for development guidelines**:
- **English is the PRIMARY language** for all code, comments, and documentation
- Secondary language: Portuguese (Brazil) - `pt-BR` (translations only)
- All UI strings use translation files (`i18n/`)

## Requirements
- Python 3.11+
- macOS 13+ (optimized for macOS 26 – Tahoe)
- Xcode Command Line Tools (for system utilities)

## Installation (dev)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python app.py
```

## Build (.app)
```bash
bash scripts/build_mac.sh
```

## Sign and Notarize (skeleton)
```bash
bash scripts/sign_and_notarize.sh "Universal OpenCore Manager.app"
```

## Structure
- `universal_oc_manager/ui/qml`: QML screens (Liquid Glass)
- `universal_oc_manager/core/*`: services (detector, EFI engine, plist, kexts, acpi, validator, comparer, exporter, updater)
- `universal_oc_manager/infra/*`: db, http, logging, settings, schemas, templates
- `tests`: pytest

**Mandatory technical references**: Dortania (Install/ACPI/Post-Install/Multiboot), Acidanthera, VoodooI2C, OC-Little, ChefKiss, Hackintool.
