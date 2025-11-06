"""
Sistema de internacionalização (i18n)
"""

import json
from pathlib import Path
from typing import Dict, Optional
import locale

from uocm.core.config import Config


class Translator:
    """Gerenciador de traduções"""
    
    _instance: Optional['Translator'] = None
    _translations: Dict[str, Dict[str, str]] = {}
    _current_language: str = "pt_BR"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_translations()
        return cls._instance
    
    def _load_translations(self) -> None:
        """Carrega traduções dos arquivos JSON"""
        try:
            translations_dir = Config.get_app_path() / "translations"
        except RuntimeError:
            # Se Config não estiver inicializado, usar caminho relativo
            from pathlib import Path
            translations_dir = Path(__file__).parent.parent.parent / "translations"
        
        translations_dir.mkdir(parents=True, exist_ok=True)
        
        # Detectar idioma do sistema
        self._current_language = self._detect_system_language()
        
        # Carregar traduções
        for lang_file in translations_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    self._translations[lang_code] = json.load(f)
            except Exception:
                pass
        
        # Se não houver tradução para o idioma detectado, usar pt_BR
        if self._current_language not in self._translations:
            self._current_language = "pt_BR"
    
    def _detect_system_language(self) -> str:
        """Detecta idioma do sistema"""
        try:
            sys_lang, _ = locale.getdefaultlocale()
            if sys_lang:
                if sys_lang.startswith("pt"):
                    return "pt_BR"
                elif sys_lang.startswith("en"):
                    return "en_US"
        except Exception:
            pass
        return "pt_BR"
    
    def set_language(self, language: str) -> None:
        """Define idioma atual"""
        if language in self._translations:
            self._current_language = language
    
    def get_language(self) -> str:
        """Retorna idioma atual"""
        return self._current_language
    
    def translate(self, key: str, default: Optional[str] = None) -> str:
        """
        Traduz uma chave
        
        Args:
            key: Chave de tradução (ex: "app.title")
            default: Valor padrão se não encontrar tradução
        
        Returns:
            Texto traduzido
        """
        translations = self._translations.get(self._current_language, {})
        
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
        """Retorna lista de idiomas disponíveis"""
        return list(self._translations.keys())


# Instância global
_translator = Translator()


def tr(key: str, default: Optional[str] = None) -> str:
    """Função auxiliar para tradução"""
    return _translator.translate(key, default)


def set_language(language: str) -> None:
    """Define idioma"""
    _translator.set_language(language)


def get_language() -> str:
    """Retorna idioma atual"""
    return _translator.get_language()


def get_available_languages() -> list[str]:
    """Retorna idiomas disponíveis"""
    return _translator.get_available_languages()

