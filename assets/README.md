# UOCM Assets

This folder contains the visual assets for the application.

Esta pasta contém os assets visuais da aplicação.

## Icons / Ícones

### macOS
- `icon.icns` - Icon for macOS (.app bundle)

### Windows
- `icon.ico` - Icon for Windows (.exe)

### Development / Desenvolvimento
- `icon.png` - High resolution PNG icon (1024x1024)
- `icon.svg` - Vector icon (optional)

## How to Create Icons / Como Criar Ícones

### macOS (.icns)

1. Have a 1024x1024 pixel PNG image
2. Use `iconutil` or a tool like:
   - [IconGenerator](https://iconGenerator.app)
   - [Image2icon](http://www.img2icnsapp.com/)
   - Or manually create a `.iconset`:

```bash
# Create .iconset structure
mkdir icon.iconset

# Copy images in different sizes
# icon_16x16.png, icon_32x32.png, icon_128x128.png, etc.

# Convert to .icns
iconutil -c icns icon.iconset -o icon.icns
```

### Windows (.ico)

1. Have a 1024x1024 pixel PNG image
2. Use an online tool or:
   - [IcoFX](https://icofx.ro/)
   - [Online ICO Converter](https://convertio.co/png-ico/)
   - Or use Python with Pillow:

```bash
python scripts/create_ico.py
```

## Notes / Notas

- The icon should have a transparent background (PNG with alpha)
- Recommended sizes: 16x16 up to 1024x1024
- For macOS, include multiple sizes in .icns
- For Windows, include multiple sizes in .ico

- O ícone deve ter fundo transparente (PNG com alpha)
- Tamanhos recomendados: 16x16 até 1024x1024
- Para macOS, incluir múltiplos tamanhos no .icns
- Para Windows, incluir múltiplos tamanhos no .ico

## Automatic Generation / Geração Automática

Run the script to automatically generate both icons:

Execute o script para gerar automaticamente ambos os ícones:

```bash
./scripts/create_icons.sh
```

This will create:
- `assets/icon.icns` (macOS)
- `assets/icon.ico` (Windows)

Isso criará:
- `assets/icon.icns` (macOS)
- `assets/icon.ico` (Windows)
