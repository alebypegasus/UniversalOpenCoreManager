# Instructions for Adding App Icon / Instruções para Adicionar Ícone do App

## Step 1: Save the Icon Image / Passo 1: Salvar a Imagem do Ícone

1. Save the icon image you showed as `assets/icon.png`
2. The image must be **PNG with transparent background**
3. Recommended size: **1024x1024 pixels** (or larger, multiples of 16)

1. Salve a imagem do ícone como `assets/icon.png`
2. A imagem deve ser **PNG com fundo transparente**
3. Tamanho recomendado: **1024x1024 pixels** (ou maior, múltiplos de 16)

## Step 2: Create Icons / Passo 2: Criar os Ícones

### macOS

Run the automatic script:

Execute o script automático:

```bash
./scripts/create_icons.sh
```

This will automatically create:
- `assets/icon.icns` - macOS icon

Isso criará automaticamente:
- `assets/icon.icns` - Ícone para macOS

### Windows

If you have ImageMagick installed:

Se você tem ImageMagick instalado:

```bash
# macOS/Linux with ImageMagick
convert assets/icon.png -define icon:auto-resize=256,128,64,48,32,16 assets/icon.ico
```

Or use Python with Pillow (recommended):

Ou use Python com Pillow (recomendado):

```bash
python scripts/create_ico.py
```

Or use an online tool:
1. Go to https://convertio.co/png-ico/
2. Upload `assets/icon.png`
3. Download the file as `assets/icon.ico`

Ou use uma ferramenta online:
1. Acesse https://convertio.co/png-ico/
2. Faça upload de `assets/icon.png`
3. Baixe o arquivo como `assets/icon.ico`

Or use a desktop tool:
- [IcoFX](https://icofx.ro/) (Windows)
- [IconGenerator](https://iconGenerator.app) (macOS)

Ou use uma ferramenta desktop:
- [IcoFX](https://icofx.ro/) (Windows)
- [IconGenerator](https://iconGenerator.app) (macOS)

## Step 3: Verify / Passo 3: Verificar

After creating the icons, verify:

Após criar os ícones, verifique:

```bash
# macOS
ls -lh assets/icon.icns

# Windows
dir assets\icon.ico
```

## Step 4: Build / Passo 4: Compilar

Now you can compile the app and the icons will be automatically included:

Agora você pode compilar o app e os ícones serão incluídos automaticamente:

```bash
# macOS
./scripts/build_mac_pyinstaller.sh

# Windows
scripts\build_windows.bat
```

## Final Structure / Estrutura Final

```
assets/
├── icon.png   # Source image (1024x1024 PNG)
├── icon.icns  # macOS icon (generated)
└── icon.ico   # Windows icon (generated)
```

## Notes / Notas

- The icon will appear in Finder (macOS) and Explorer (Windows)
- The icon will appear in the Dock (macOS) and taskbar (Windows)
- The icon will appear in file dialogs
- Make sure the source image has good quality (high resolution)

- O ícone aparecerá no Finder (macOS) e no Explorer (Windows)
- O ícone aparecerá na Dock (macOS) e na barra de tarefas (Windows)
- O ícone aparecerá nos diálogos de arquivo
- Certifique-se de que a imagem fonte tenha boa qualidade (alta resolução)
