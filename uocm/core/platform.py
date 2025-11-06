"""
Platform detection and utilities
Detecção e utilitários de plataforma
"""

import platform
import sys
import os
from pathlib import Path
from typing import Optional


class Platform:
    """
    Platform utilities
    Utilitários de plataforma
    """
    
    @staticmethod
    def get_system() -> str:
        """
        Returns operating system
        Retorna sistema operacional
        """
        return platform.system()
    
    @staticmethod
    def is_macos() -> bool:
        """
        Checks if running on macOS
        Verifica se é macOS
        """
        return Platform.get_system() == "Darwin"
    
    @staticmethod
    def is_windows() -> bool:
        """
        Checks if running on Windows
        Verifica se é Windows
        """
        return Platform.get_system() == "Windows"
    
    @staticmethod
    def is_linux() -> bool:
        """
        Checks if running on Linux
        Verifica se é Linux
        """
        return Platform.get_system() == "Linux"
    
    @staticmethod
    def get_app_data_path() -> Path:
        """
        Returns application data path
        Retorna caminho para dados da aplicação
        """
        system = Platform.get_system()
        
        if system == "Darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / "UOCM"
        elif system == "Windows":
            return Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming")) / "UOCM"
        else:  # Linux
            return Path.home() / ".config" / "uocm"
    
    @staticmethod
    def get_resource_path() -> Optional[Path]:
        """
        Returns resource path (useful when packaged)
        Retorna caminho para recursos (útil quando empacotado)
        """
        if getattr(sys, 'frozen', False):
            # Packaged application (PyInstaller, py2app, etc.)
            # Aplicação empacotada (PyInstaller, py2app, etc.)
            if Platform.is_macos():
                return Path(sys.executable).parent.parent / "Resources"
            else:
                return Path(sys.executable).parent
        else:
            # Running in development mode
            # Executando em modo desenvolvimento
            return Path(__file__).parent.parent.parent
    
    @staticmethod
    def get_executable_name() -> str:
        """
        Returns executable name
        Retorna nome do executável
        """
        if Platform.is_windows():
            return "uocm.exe"
        else:
            return "uocm"
    
    @staticmethod
    def can_detect_hardware() -> bool:
        """
        Checks if hardware detection is available (macOS only)
        Verifica se pode detectar hardware (apenas macOS)
        """
        return Platform.is_macos()
    
    @staticmethod
    def get_system_profiler_command() -> Optional[str]:
        """
        Returns system_profiler command (macOS only)
        Retorna comando system_profiler (apenas macOS)
        """
        if Platform.is_macos():
            return "system_profiler"
        return None

