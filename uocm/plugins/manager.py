"""
Gerenciador de plugins
"""

import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Type
import json

from uocm.plugins.base import BasePlugin, PluginManifest, HeuristicPlugin, SSDTPlugin, ValidatorPlugin
from uocm.core.config import Config
from uocm.db.database import get_db_session
from uocm.db.models import Plugin


class PluginManager:
    """Gerenciador de plugins"""
    
    def __init__(self):
        self.plugins_dir = Config.get_plugins_path()
        self.loaded_plugins: Dict[str, BasePlugin] = {}
    
    def discover_plugins(self) -> List[Path]:
        """Descobre plugins na pasta de plugins"""
        plugins = []
        
        if not self.plugins_dir.exists():
            return plugins
        
        for item in self.plugins_dir.iterdir():
            if item.is_dir() and (item / "manifest.json").exists():
                plugins.append(item)
            elif item.is_file() and item.suffix == ".py":
                plugins.append(item)
        
        return plugins
    
    def load_plugin(self, plugin_path: Path) -> Optional[BasePlugin]:
        """Carrega um plugin"""
        try:
            if plugin_path.is_dir():
                return self._load_directory_plugin(plugin_path)
            elif plugin_path.is_file():
                return self._load_file_plugin(plugin_path)
        except Exception as e:
            print(f"Erro ao carregar plugin {plugin_path}: {e}")
            return None
    
    def _load_directory_plugin(self, plugin_path: Path) -> Optional[BasePlugin]:
        """Carrega plugin de diretório"""
        manifest_path = plugin_path / "manifest.json"
        
        if not manifest_path.exists():
            return None
        
        # Carregar manifesto
        with open(manifest_path, "r") as f:
            manifest_data = json.load(f)
        
        manifest = PluginManifest(**manifest_data)
        
        # Carregar módulo
        module_name = plugin_path.name
        sys_path = str(plugin_path.parent)
        
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        
        try:
            if manifest.entry_point == "__init__":
                module = importlib.import_module(module_name)
            else:
                module = importlib.import_module(f"{module_name}.{manifest.entry_point}")
        except ImportError as e:
            print(f"Erro ao importar módulo do plugin: {e}")
            return None
        
        # Encontrar classe do plugin
        plugin_class = None
        for name, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BasePlugin)
                and obj != BasePlugin
            ):
                plugin_class = obj
                break
        
        if not plugin_class:
            return None
        
        # Instanciar plugin
        plugin = plugin_class(manifest)
        
        if plugin.initialize():
            self.loaded_plugins[manifest.name] = plugin
            return plugin
        
        return None
    
    def _load_file_plugin(self, plugin_path: Path) -> Optional[BasePlugin]:
        """Carrega plugin de arquivo único"""
        # Implementar carregamento de plugin de arquivo único
        return None
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Retorna plugin carregado"""
        return self.loaded_plugins.get(name)
    
    def get_heuristic_plugins(self) -> List[HeuristicPlugin]:
        """Retorna plugins de heurística"""
        return [
            p for p in self.loaded_plugins.values()
            if isinstance(p, HeuristicPlugin)
        ]
    
    def get_ssdt_plugins(self) -> List[SSDTPlugin]:
        """Retorna plugins SSDT"""
        return [
            p for p in self.loaded_plugins.values()
            if isinstance(p, SSDTPlugin)
        ]
    
    def get_validator_plugins(self) -> List[ValidatorPlugin]:
        """Retorna plugins validador"""
        return [
            p for p in self.loaded_plugins.values()
            if isinstance(p, ValidatorPlugin)
        ]
    
    def load_all_plugins(self) -> None:
        """Carrega todos os plugins descobertos"""
        plugins = self.discover_plugins()
        for plugin_path in plugins:
            self.load_plugin(plugin_path)
    
    def unload_plugin(self, name: str) -> bool:
        """Descarrega um plugin"""
        if name in self.loaded_plugins:
            plugin = self.loaded_plugins[name]
            plugin.cleanup()
            del self.loaded_plugins[name]
            return True
        return False

