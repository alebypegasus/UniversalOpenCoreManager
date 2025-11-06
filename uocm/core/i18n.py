"""
Internationalization (i18n) system
Sistema de internacionalização (i18n)
"""

import json
from pathlib import Path
from typing import Dict, Optional
import locale

from uocm.core.config import Config


class Translator:
    """
    Translation manager
    Gerenciador de traduções
    """
    
    _instance: Optional['Translator'] = None
    _translations: Dict[str, Dict[str, str]] = {}
    _current_language: str = "en_US"  # English is primary
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_translations()
        return cls._instance
    
    def _load_translations(self) -> None:
        """
        Loads translations from JSON files
        Carrega traduções dos arquivos JSON
        """
        try:
            translations_dir = Config.get_app_path() / "translations"
        except RuntimeError:
            # If Config not initialized, use relative path
            # Se Config não estiver inicializado, usar caminho relativo
            from pathlib import Path
            translations_dir = Path(__file__).parent.parent.parent / "translations"
        
        translations_dir.mkdir(parents=True, exist_ok=True)
        
        # Detect system language
        # Detectar idioma do sistema
        self._current_language = self._detect_system_language()
        
        # Load translations
        # Carregar traduções
        for lang_file in translations_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    self._translations[lang_code] = json.load(f)
            except Exception:
                pass
        
        # If no translation for detected language, use en_US (English is primary)
        if self._current_language not in self._translations:
            self._current_language = "en_US"
    
    def _detect_system_language(self) -> str:
        """
        Detects system language automatically
        Detects language from system locale
        Returns 'en_US' as default (English is primary)
        """
        try:
            # Try to get system locale
            sys_lang, _ = locale.getdefaultlocale()
            if sys_lang:
                lang_lower = sys_lang.lower()
                if lang_lower.startswith("pt"):
                    return "pt_BR"
                elif lang_lower.startswith("en"):
                    return "en_US"
            
            # Try alternative method
            import os
            lang_env = os.environ.get("LANG", "")
            if lang_env:
                if "pt" in lang_env.lower():
                    return "pt_BR"
                elif "en" in lang_env.lower():
                    return "en_US"
        except Exception:
            pass
        
        # Default to English (primary language)
        return "en_US"
    
    def set_language(self, language: str) -> None:
        """
        Sets current language
        Define idioma atual
        """
        if language in self._translations:
            self._current_language = language
    
    def get_language(self) -> str:
        """
        Returns current language
        Retorna idioma atual
        """
        return self._current_language
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """
        Translates a key
        Traduz uma chave
        
        Args:
            key: Translation key (e.g., "app.title")
            default: Default value if translation not found
        
        Returns:
            Translated text
            Texto traduzido
        """
        translations = self._translations.get(self._current_language, {})
        
        # Search translation with support for nested keys (e.g., "app.title")
        # Buscar tradução com suporte a chaves aninhadas (ex: "app.title")
        keys = key.split(".")
        value = translations
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                break
        
        if value and isinstance(value, str):
            return value
        
        # If not found, try English as fallback
        # Se não encontrou, tentar inglês como fallback
        if self._current_language != "en_US":
            en_translations = self._translations.get("en_US", {})
            value = en_translations
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    break
            if value and isinstance(value, str):
                return value
        
        return default or key
    
    def get_available_languages(self) -> list[str]:
        """
        Returns list of available languages
        Retorna lista de idiomas disponíveis
        """
        return list(self._translations.keys())


# Global instance
# Instância global
_translator = Translator()


def tr(key: str, default: Optional[str] = None) -> str:
    """
    Helper function for translation
    Função auxiliar para tradução
    """
    return _translator.translate(key, default)


def set_language(language: str) -> None:
    """
    Sets language
    Define idioma
    """
    _translator.set_language(language)


def get_language() -> str:
    """
    Returns current language
    Retorna idioma atual
    """
    return _translator.get_language()


def get_available_languages() -> list[str]:
    """
    Returns available languages
    Retorna idiomas disponíveis
    """
    return _translator.get_available_languages()

