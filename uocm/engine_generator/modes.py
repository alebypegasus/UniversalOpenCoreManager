"""
Modos de geração de EFI
"""

from enum import Enum


class GenerationMode(Enum):
    """Modos de geração de EFI"""
    CONSERVATIVE = "conservative"  # Mais seguro, menos features
    STANDARD = "standard"  # Padrão balanceado
    AGGRESSIVE = "aggressive"  # Mais features, pode ser menos estável

