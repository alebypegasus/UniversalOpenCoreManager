# Guia de Build e Compilação - UOCM

## Pré-requisitos

### macOS
- Python 3.11+
- Xcode Command Line Tools
- py2app (instalado automaticamente pelo script)

### Windows
- Python 3.11+
- Visual C++ Redistributable
- PyInstaller (instalado automaticamente pelo script)

## Build para macOS

### 1. Preparar ambiente

```bash
# Instalar dependências
pip install -r requirements.txt

# Instalar dependências de desenvolvimento (opcional)
pip install -e ".[dev]"
```

### 2. Build

```bash
chmod +x scripts/build_mac.sh
./scripts/build_mac.sh
```

O arquivo `.app` será criado em `dist/UOCM.app`.

### 3. Testar

```bash
open dist/UOCM.app
```

### 4. Code Signing (Opcional)

```bash
chmod +x scripts/sign_and_notarize.sh
./scripts/sign_and_notarize.sh dist/UOCM.app "Developer ID Application: Your Name (TEAM_ID)"
```

## Build para Windows

### 1. Preparar ambiente

```batch
REM Instalar dependências
pip install -r requirements.txt
```

### 2. Build

```batch
scripts\build_windows.bat
```

O arquivo `.exe` será criado em `dist/UOCM.exe`.

### 3. Testar

```batch
dist\UOCM.exe
```

## Teste e Build Completo

### macOS/Linux

```bash
chmod +x scripts/test_build.sh
./scripts/test_build.sh --build
```

### Windows

```batch
scripts\test_build.bat --build
```

Este script:
1. Executa testes
2. Verifica lint
3. Verifica tipos (mypy)
4. Compila a aplicação (se `--build` for especificado)

## Estrutura de Arquivos Gerados

### macOS
```
dist/
└── UOCM.app/
    ├── Contents/
    │   ├── MacOS/
    │   │   └── uocm (executável)
    │   ├── Resources/
    │   │   ├── translations/
    │   │   ├── templates/
    │   │   └── plugins/
    │   └── Info.plist
```

### Windows
```
dist/
└── UOCM.exe (executável standalone)
```

## Internacionalização

O UOCM suporta múltiplos idiomas através de arquivos JSON em `translations/`:

- `pt_BR.json` - Português (Brasil)
- `en_US.json` - Inglês (EUA)

O idioma é detectado automaticamente baseado no sistema operacional.

## Troubleshooting

### Erro: "Python 3.11+ é necessário"
- Instale Python 3.11 ou superior
- Verifique com `python3 --version`

### Erro: "ModuleNotFoundError: No module named 'tkinter'"
- macOS: Instale Xcode Command Line Tools
- Linux: `sudo apt-get install python3-tk`
- Windows: Normalmente incluído

### Erro: "PyInstaller não encontrado"
- Execute: `pip install PyInstaller`

### Erro: "py2app não encontrado"
- Execute: `pip install py2app`

## Distribuição

### macOS
- Crie um `.dmg` para distribuição
- Use `hdiutil` para criar DMG
- Assine e notarize para distribuição fora da App Store

### Windows
- O `.exe` pode ser distribuído diretamente
- Considere criar um instalador com Inno Setup ou NSIS

## Notas Importantes

1. **Detecção de Hardware**: Funciona apenas no macOS
2. **Recursos**: Arquivos em `translations/`, `templates/` e `plugins/` são incluídos no build
3. **Banco de Dados**: SQLite será criado em `~/Library/Application Support/UOCM/` (macOS) ou `%APPDATA%/UOCM/` (Windows)

