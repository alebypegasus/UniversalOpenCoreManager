#!/usr/bin/env python3
"""
Script para criar arquivo .ico a partir de PNG
"""

import sys
from pathlib import Path
from PIL import Image

def create_ico_from_png(png_path: str, ico_path: str) -> None:
    """Cria arquivo .ico a partir de PNG com múltiplos tamanhos"""
    png_file = Path(png_path)
    ico_file = Path(ico_path)
    
    if not png_file.exists():
        print(f"Erro: {png_path} não encontrado!")
        sys.exit(1)
    
    # Abrir imagem PNG
    img = Image.open(png_file)
    
    # Criar lista de tamanhos para .ico (Windows requer múltiplos tamanhos)
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # Redimensionar para cada tamanho
    images = []
    for size in sizes:
        resized = img.resize(size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Salvar como .ico
    images[0].save(
        ico_file,
        format='ICO',
        sizes=[(img.width, img.height) for img in images]
    )
    
    print(f"✓ Ícone Windows criado: {ico_path}")
    print(f"  Tamanhos incluídos: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")

if __name__ == "__main__":
    png_path = "assets/icon.png"
    ico_path = "assets/icon.ico"
    
    create_ico_from_png(png_path, ico_path)

