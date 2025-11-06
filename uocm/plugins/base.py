"""
Base classes para plugins
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class PluginManifest:
    """Manifesto de plugin"""
    name: str
    version: str
    author: str
    description: str
    entry_point: str
    permissions: List[str]
    dependencies: Optional[List[str]] = None


class BasePlugin(ABC):
    """Classe base para plugins"""
    
    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
    
    @abstractmethod
    def initialize(self) -> bool:
        """Inicializa o plugin"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Limpa recursos do plugin"""
        pass
    
    def get_manifest(self) -> PluginManifest:
        """Retorna o manifesto do plugin"""
        return self.manifest
    
    def validate_permissions(self, required: List[str]) -> bool:
        """Valida se o plugin tem as permissões necessárias"""
        return all(perm in self.manifest.permissions for perm in required)


class HeuristicPlugin(BasePlugin):
    """Plugin que adiciona heurísticas de detecção/recomendação"""
    
    @abstractmethod
    def recommend_smbios(self, hardware_info: Dict[str, Any]) -> Optional[str]:
        """Recomenda SMBIOS baseado em hardware"""
        pass
    
    @abstractmethod
    def recommend_kexts(self, hardware_info: Dict[str, Any]) -> List[str]:
        """Recomenda kexts baseado em hardware"""
        pass


class SSDTPlugin(BasePlugin):
    """Plugin que adiciona templates SSDT"""
    
    @abstractmethod
    def generate_ssdt(self, parameters: Dict[str, Any]) -> Optional[str]:
        """Gera SSDT baseado em parâmetros"""
        pass


class ValidatorPlugin(BasePlugin):
    """Plugin que adiciona validadores customizados"""
    
    @abstractmethod
    def validate(self, config: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Valida configuração"""
        pass

