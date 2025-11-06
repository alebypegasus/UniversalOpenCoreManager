"""
Configurações globais da aplicação
"""

import os
from pathlib import Path
from typing import Optional

from uocm.core.platform import Platform


class Config:
    """Configurações centralizadas da aplicação"""
    
    _app_path: Optional[Path] = None
    _data_path: Optional[Path] = None
    _config_path: Optional[Path] = None
    _db_path: Optional[Path] = None
    
    @classmethod
    def set_app_path(cls, path: Path) -> None:
        """Define o caminho base da aplicação"""
        cls._app_path = path
        cls._data_path = path / "data"
        cls._config_path = path / "config"
        cls._db_path = cls._data_path / "uocm.db"
        
        # Criar diretórios necessários
        cls._data_path.mkdir(parents=True, exist_ok=True)
        cls._config_path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_app_path(cls) -> Path:
        """Retorna o caminho base da aplicação"""
        if cls._app_path is None:
            raise RuntimeError("App path not set. Call set_app_path() first.")
        return cls._app_path
    
    @classmethod
    def get_data_path(cls) -> Path:
        """Retorna o caminho para dados da aplicação"""
        # Se não estiver configurado, usar caminho padrão do sistema
        if cls._data_path is None:
            return Platform.get_app_data_path()
        return cls._data_path
    
    @classmethod
    def get_config_path(cls) -> Path:
        """Retorna o caminho para configurações"""
        if cls._config_path is None:
            raise RuntimeError("App path not set. Call set_app_path() first.")
        return cls._config_path
    
    @classmethod
    def get_db_path(cls) -> Path:
        """Retorna o caminho para o banco de dados"""
        if cls._db_path is None:
            raise RuntimeError("App path not set. Call set_app_path() first.")
        return cls._db_path
    
    @classmethod
    def get_efi_backups_path(cls) -> Path:
        """Retorna o caminho para backups de EFI"""
        path = cls.get_data_path() / "efi_backups"
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @classmethod
    def get_exports_path(cls) -> Path:
        """Retorna o caminho para exports"""
        path = cls.get_data_path() / "exports"
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @classmethod
    def get_plugins_path(cls) -> Path:
        """Retorna o caminho para plugins"""
        path = cls.get_app_path() / "plugins"
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @classmethod
    def get_templates_path(cls) -> Path:
        """Retorna o caminho para templates"""
        path = cls.get_app_path() / "templates"
        path.mkdir(parents=True, exist_ok=True)
        return path

