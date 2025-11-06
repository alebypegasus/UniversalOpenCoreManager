# Build and Compilation Guide - UOCM

## Prerequisites / Pré-requisitos

### macOS
- Python 3.11+
- Xcode Command Line Tools
- py2app (installed automatically by script)

### Windows
- Python 3.11+
- Visual C++ Redistributable
- PyInstaller (installed automatically by script)

## Build for macOS

### 1. Prepare environment

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -e ".[dev]"
```

### 2. Build

```bash
chmod +x scripts/build_mac_pyinstaller.sh
./scripts/build_mac_pyinstaller.sh
```

The `.app` file will be created in `dist/UOCM.app`.

### 3. Test

```bash
open dist/UOCM.app
```

### 4. Code Signing (Optional)

```bash
chmod +x scripts/sign_and_notarize.sh
./scripts/sign_and_notarize.sh dist/UOCM.app "Developer ID Application: Your Name (TEAM_ID)"
```

## Build for Windows

### 1. Prepare environment

```batch
REM Install dependencies
pip install -r requirements.txt
```

### 2. Build

```batch
scripts\build_windows.bat
```

The `.exe` file will be created in `dist/UOCM.exe`.

### 3. Test

```batch
dist\UOCM.exe
```

## Complete Test and Build

### macOS/Linux

```bash
chmod +x scripts/test_build.sh
./scripts/test_build.sh --build
```

### Windows

```batch
scripts\test_build.bat --build
```

This script:
1. Runs tests
2. Checks lint
3. Checks types (mypy)
4. Compiles the application (if `--build` is specified)

Este script:
1. Executa testes
2. Verifica lint
3. Verifica tipos (mypy)
4. Compila a aplicação (se `--build` for especificado)

## Generated File Structure

### macOS
```
dist/
└── UOCM.app/
    ├── Contents/
    │   ├── MacOS/
    │   │   └── uocm (executable)
    │   ├── Resources/
    │   │   ├── translations/
    │   │   ├── templates/
    │   │   └── plugins/
    │   └── Info.plist
```

### Windows
```
dist/
└── UOCM.exe (standalone executable)
```

## Internationalization

UOCM supports multiple languages through JSON files in `translations/`:

- `pt_BR.json` - Portuguese (Brazil)
- `en_US.json` - English (US)

The language is automatically detected based on the operating system.

O idioma é detectado automaticamente com base no sistema operacional.

## Troubleshooting

### Error: "Python 3.11+ is required"
- Install Python 3.11 or higher
- Check with `python3 --version`

### Error: "ModuleNotFoundError: No module named 'tkinter'"
- macOS: Install Xcode Command Line Tools
- Linux: `sudo apt-get install python3-tk`
- Windows: Usually included

### Error: "PyInstaller not found"
- Run: `pip install PyInstaller`

### Error: "py2app not found"
- Run: `pip install py2app`

## Distribution

### macOS
- Create a `.dmg` for distribution
- Use `hdiutil` to create DMG
- Sign and notarize for distribution outside App Store

### Windows
- The `.exe` can be distributed directly
- Consider creating an installer with Inno Setup or NSIS

## Important Notes

1. **Hardware Detection**: Works only on macOS
2. **Resources**: Files in `translations/`, `templates/`, and `plugins/` are included in the build
3. **Database**: SQLite will be created in `~/Library/Application Support/UOCM/` (macOS) or `%APPDATA%/UOCM/` (Windows)

## Notas Importantes

1. **Detecção de Hardware**: Funciona apenas no macOS
2. **Recursos**: Arquivos em `translations/`, `templates/` e `plugins/` são incluídos no build
3. **Banco de Dados**: SQLite será criado em `~/Library/Application Support/UOCM/` (macOS) ou `%APPDATA%/UOCM/` (Windows)
