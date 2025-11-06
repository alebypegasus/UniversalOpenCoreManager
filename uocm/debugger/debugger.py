"""
Sistema de debug e validação de EFI
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from uocm.plist_editor.validator import PlistValidator
from uocm.kext_manager.manager import KextManager
from uocm.core.config import Config


class EFIDebugger:
    """Debugger e validador de EFI"""
    
    def __init__(self):
        self.validator = PlistValidator()
        self.kext_manager = KextManager()
    
    def validate_efi(self, efi_path: Path) -> Dict[str, Any]:
        """
        Valida uma estrutura EFI completa
        
        Returns:
            Dict com resultados da validação
        """
        results = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": [],
            "timestamp": datetime.now().isoformat(),
        }
        
        # Verificar estrutura de diretórios
        oc_path = efi_path / "EFI" / "OC"
        if not oc_path.exists():
            results["valid"] = False
            results["errors"].append("EFI/OC não encontrado")
            return results
        
        # Validar config.plist
        config_path = oc_path / "config.plist"
        if not config_path.exists():
            results["valid"] = False
            results["errors"].append("config.plist não encontrado")
        else:
            is_valid, errors = self.validator.validate(config_path)
            if not is_valid:
                results["valid"] = False
                results["errors"].extend(errors)
        
        # Verificar kexts
        kexts_dir = oc_path / "Kexts"
        if kexts_dir.exists():
            kext_issues = self._check_kexts(kexts_dir)
            results["warnings"].extend(kext_issues)
        
        # Verificar drivers
        drivers_dir = oc_path / "Drivers"
        if drivers_dir.exists():
            driver_issues = self._check_drivers(drivers_dir)
            results["warnings"].extend(driver_issues)
        
        # Verificar ACPI
        acpi_dir = oc_path / "ACPI"
        if acpi_dir.exists():
            acpi_issues = self._check_acpi(acpi_dir)
            results["warnings"].extend(acpi_issues)
        
        # Verificar duplicações
        duplicates = self._check_duplicates(oc_path)
        if duplicates:
            results["warnings"].extend(duplicates)
        
        return results
    
    def _check_kexts(self, kexts_dir: Path) -> List[str]:
        """Verifica kexts"""
        issues = []
        kexts = list(kexts_dir.glob("*.kext"))
        
        if not kexts:
            issues.append("Nenhum kext encontrado")
        
        for kext in kexts:
            if not self.kext_manager.verify_kext(kext):
                issues.append(f"Kext inválido: {kext.name}")
        
        return issues
    
    def _check_drivers(self, drivers_dir: Path) -> List[str]:
        """Verifica drivers UEFI"""
        issues = []
        drivers = list(drivers_dir.glob("*.efi"))
        
        required_drivers = ["OpenRuntime.efi"]
        for required in required_drivers:
            if not (drivers_dir / required).exists():
                issues.append(f"Driver requerido não encontrado: {required}")
        
        return issues
    
    def _check_acpi(self, acpi_dir: Path) -> List[str]:
        """Verifica arquivos ACPI"""
        issues = []
        aml_files = list(acpi_dir.glob("*.aml"))
        
        if not aml_files:
            issues.append("Nenhum arquivo ACPI encontrado")
        
        return issues
    
    def _check_duplicates(self, oc_path: Path) -> List[str]:
        """Verifica duplicações"""
        issues = []
        
        # Verificar kexts duplicados
        kexts_dir = oc_path / "Kexts"
        if kexts_dir.exists():
            kext_names = {}
            for kext in kexts_dir.glob("*.kext"):
                name = kext.stem
                if name in kext_names:
                    issues.append(f"Kext duplicado: {name}")
                kext_names[name] = kext
        
        return issues
    
    def generate_report(
        self,
        efi_path: Path,
        output_path: Optional[Path] = None,
    ) -> Path:
        """Gera relatório JSON/PDF da validação"""
        validation = self.validate_efi(efi_path)
        
        if output_path is None:
            output_path = Config.get_exports_path() / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w") as f:
            json.dump(validation, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def simulate_boot(self, efi_path: Path) -> Dict[str, Any]:
        """Simula processo de boot sem modificar disco"""
        # Implementar simulação de boot
        # Referência: https://github.com/acidanthera/OpenCorePkg
        return {
            "success": False,
            "message": "Simulação de boot não implementada",
        }

