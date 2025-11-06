"""
Validador de config.plist baseado em schema OpenCore
"""

import plistlib
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple as TupleType

import jsonschema


class PlistValidator:
    """Validador de config.plist usando schema OpenCore"""
    
    def __init__(self):
        self.schema = self._load_opencore_schema()
    
    def validate(self, plist_path: Path) -> TupleType[bool, List[str]]:
        """
        Valida um config.plist
        
        Returns:
            Tuple de (is_valid, list_of_errors)
        """
        try:
            with open(plist_path, "rb") as f:
                plist_data = plistlib.load(f)
            
            # Converter para JSON para validação
            json_data = self._plist_to_json(plist_data)
            
            # Validar schema
            validator = jsonschema.Draft7Validator(self.schema)
            errors = list(validator.iter_errors(json_data))
            
            if errors:
                error_messages = [self._format_error(e) for e in errors]
                return False, error_messages
            
            return True, []
        except Exception as e:
            return False, [f"Erro ao validar: {str(e)}"]
    
    def validate_dict(self, plist_dict: Dict[str, Any]) -> TupleType[bool, List[str]]:
        """Valida um dicionário de config.plist"""
        try:
            json_data = self._plist_to_json(plist_dict)
            validator = jsonschema.Draft7Validator(self.schema)
            errors = list(validator.iter_errors(json_data))
            
            if errors:
                error_messages = [self._format_error(e) for e in errors]
                return False, error_messages
            
            return True, []
        except Exception as e:
            return False, [f"Erro ao validar: {str(e)}"]
    
    def _load_opencore_schema(self) -> Dict[str, Any]:
        """Carrega schema OpenCore"""
        # Schema básico - deve ser expandido com schema completo do OpenCore
        # Referência: https://github.com/acidanthera/OpenCorePkg/tree/master/Utilities/ocvalidate
        return {
            "type": "object",
            "properties": {
                "ACPI": {"type": "object"},
                "Booter": {"type": "object"},
                "Boot": {"type": "object"},
                "DeviceProperties": {"type": "object"},
                "Kernel": {"type": "object"},
                "Misc": {"type": "object"},
                "NVRAM": {"type": "object"},
                "PlatformInfo": {"type": "object"},
                "UEFI": {"type": "object"},
            },
            "additionalProperties": False,
        }
    
    def _plist_to_json(self, data: Any) -> Any:
        """Converte dados PLIST para JSON compatível"""
        if isinstance(data, dict):
            return {k: self._plist_to_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._plist_to_json(item) for item in data]
        elif isinstance(data, bytes):
            return data.hex()
        else:
            return data
    
    def _format_error(self, error: jsonschema.ValidationError) -> str:
        """Formata mensagem de erro"""
        path = " -> ".join(str(p) for p in error.path)
        return f"{path}: {error.message}"

