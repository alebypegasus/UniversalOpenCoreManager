# Instruções para Adicionar o Ícone do App

## Passo 1: Salvar a Imagem do Ícone

1. Salve a imagem do ícone que você mostrou como `assets/icon.png`
2. A imagem deve ser **PNG com fundo transparente**
3. Tamanho recomendado: **1024x1024 pixels** (ou maior, com múltiplos de 16)

## Passo 2: Criar os Ícones

### macOS

Execute o script automático:

```bash
./scripts/create_icons.sh
```

Isso criará automaticamente:
- `assets/icon.icns` - Ícone para macOS

### Windows

Se você tem ImageMagick instalado:

```bash
# macOS/Linux com ImageMagick
convert assets/icon.png -define icon:auto-resize=256,128,64,48,32,16 assets/icon.ico
```

Ou use uma ferramenta online:
1. Acesse https://convertio.co/png-ico/
2. Faça upload de `assets/icon.png`
3. Baixe o arquivo como `assets/icon.ico`

Ou use uma ferramenta desktop:
- [IcoFX](https://icofx.ro/) (Windows)
- [IconGenerator](https://iconGenerator.app) (macOS)

## Passo 3: Verificar

Após criar os ícones, verifique:

```bash
# macOS
ls -lh assets/icon.icns

# Windows
dir assets\icon.ico
```

## Passo 4: Build

Agora você pode compilar o app e os ícones serão incluídos automaticamente:

```bash
# macOS
./scripts/build_mac.sh

# Windows
scripts\build_windows.bat
```

## Estrutura Final

```
assets/
├── icon.png   # Imagem fonte (1024x1024 PNG)
├── icon.icns  # Ícone macOS (gerado)
└── icon.ico   # Ícone Windows (gerado)
```

## Notas

- O ícone aparecerá no Finder (macOS) e no Explorer (Windows)
- O ícone aparecerá na Dock (macOS) e na barra de tarefas (Windows)
- O ícone aparecerá nos diálogos de arquivo
- Certifique-se de que a imagem fonte tenha boa qualidade (alta resolução)

