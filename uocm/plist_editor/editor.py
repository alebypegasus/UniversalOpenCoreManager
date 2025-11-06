"""
Editor visual de config.plist com validação em tempo real
"""

import plistlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from uocm.plist_editor.validator import PlistValidator


class PlistEditor:
    """Editor de config.plist com undo/redo e validação"""
    
    def __init__(self, plist_path: Optional[Path] = None):
        self.plist_path = plist_path
        self.validator = PlistValidator()
        self.data: Dict[str, Any] = {}
        self.history: List[Dict[str, Any]] = []
        self.history_index: int = -1
        self.max_history = 50
    
    def load(self, path: Path) -> bool:
        """Carrega um config.plist"""
        try:
            with open(path, "rb") as f:
                self.data = plistlib.load(f)
            self.plist_path = path
            self._save_to_history()
            return True
        except Exception as e:
            return False
    
    def save(self, path: Optional[Path] = None) -> bool:
        """Salva o config.plist"""
        save_path = path or self.plist_path
        if save_path is None:
            return False
        
        try:
            # Validar antes de salvar
            is_valid, errors = self.validator.validate_dict(self.data)
            if not is_valid:
                return False
            
            with open(save_path, "wb") as f:
                plistlib.dump(self.data, f)
            return True
        except Exception:
            return False
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """Obtém valor por caminho de chave (ex: 'ACPI.Add.0.Path')"""
        keys = key_path.split(".")
        value = self.data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif isinstance(value, list):
                try:
                    index = int(key)
                    value = value[index] if 0 <= index < len(value) else None
                except ValueError:
                    return default
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set_value(self, key_path: str, value: Any) -> bool:
        """Define valor por caminho de chave"""
        keys = key_path.split(".")
        target = self.data
        
        # Navegar até o penúltimo nível
        for key in keys[:-1]:
            if isinstance(target, dict):
                if key not in target:
                    target[key] = {}
                target = target[key]
            elif isinstance(target, list):
                try:
                    index = int(key)
                    if index >= len(target):
                        target.extend([{}] * (index - len(target) + 1))
                    target = target[index]
                except ValueError:
                    return False
            else:
                return False
        
        # Definir valor final
        final_key = keys[-1]
        if isinstance(target, dict):
            target[final_key] = value
        elif isinstance(target, list):
            try:
                index = int(final_key)
                if index >= len(target):
                    target.extend([None] * (index - len(target) + 1))
                target[index] = value
            except ValueError:
                return False
        else:
            return False
        
        self._save_to_history()
        return True
    
    def validate(self) -> tuple[bool, List[str]]:
        """Valida o config.plist atual"""
        from typing import Tuple
        return self.validator.validate_dict(self.data)
    
    def undo(self) -> bool:
        """Desfaz última alteração"""
        if self.history_index > 0:
            self.history_index -= 1
            self.data = self._deep_copy(self.history[self.history_index])
            return True
        return False
    
    def redo(self) -> bool:
        """Refaz última alteração desfeita"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.data = self._deep_copy(self.history[self.history_index])
            return True
        return False
    
    def _save_to_history(self) -> None:
        """Salva estado atual no histórico"""
        # Remover estados futuros se houver
        if self.history_index < len(self.history) - 1:
            self.history = self.history[: self.history_index + 1]
        
        # Adicionar novo estado
        self.history.append(self._deep_copy(self.data))
        self.history_index = len(self.history) - 1
        
        # Limitar tamanho do histórico
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
            self.history_index = len(self.history) - 1
    
    def _deep_copy(self, data: Any) -> Any:
        """Cópia profunda de dados"""
        import copy
        return copy.deepcopy(data)

