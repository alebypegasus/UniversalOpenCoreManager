# Assets do UOCM

Esta pasta contém os assets visuais da aplicação.

## Ícones

### macOS
- `icon.icns` - Ícone para macOS (.app bundle)

### Windows
- `icon.ico` - Ícone para Windows (.exe)

### Desenvolvimento
- `icon.png` - Ícone PNG de alta resolução (1024x1024)
- `icon.svg` - Ícone vetorial (opcional)

## Como criar os ícones

### macOS (.icns)

1. Tenha uma imagem PNG de 1024x1024 pixels
2. Use `iconutil` ou uma ferramenta como:
   - [IconGenerator](https://iconGenerator.app)
   - [Image2icon](http://www.img2icnsapp.com/)
   - Ou manualmente crie um `.iconset`:

```bash
# Criar estrutura .iconset
mkdir icon.iconset

# Copiar imagens em diferentes tamanhos
# icon_16x16.png, icon_32x32.png, icon_128x128.png, etc.

# Converter para .icns
iconutil -c icns icon.iconset -o icon.icns
```

### Windows (.ico)

1. Tenha uma imagem PNG de 1024x1024 pixels
2. Use uma ferramenta online ou:
   - [IcoFX](https://icofx.ro/)
   - [Online ICO Converter](https://convertio.co/png-ico/)
   - Ou use ImageMagick:

```bash
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

## Notas

- O ícone deve ter fundo transparente (PNG com alpha)
- Tamanhos recomendados: 16x16 até 1024x1024
- Para macOS, incluir múltiplos tamanhos no .icns
- Para Windows, incluir múltiplos tamanhos no .ico

