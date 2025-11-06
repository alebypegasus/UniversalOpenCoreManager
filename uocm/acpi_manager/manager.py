"""
Gerenciador de SSDTs/ACPI com templates e geração
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any
import plistlib

from uocm.db.database import get_db_session
from uocm.db.models import SSDTTemplate
from uocm.core.config import Config


class ACPIManager:
    """Gerenciador de SSDTs/ACPI"""
    
    def __init__(self):
        self.templates_dir = Config.get_templates_path() / "ssdt"
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.acpi_dir = Config.get_data_path() / "acpi"
        self.acpi_dir.mkdir(parents=True, exist_ok=True)
    
    def get_available_templates(self) -> List[SSDTTemplate]:
        """Retorna lista de templates SSDT disponíveis"""
        session = get_db_session()
        try:
            return session.query(SSDTTemplate).all()
        finally:
            session.close()
    
    def generate_ssdt(
        self,
        template_name: str,
        output_path: Path,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Gera SSDT a partir de template"""
        session = get_db_session()
        try:
            template = session.query(SSDTTemplate).filter(
                SSDTTemplate.name == template_name
            ).first()
            
            if not template:
                return False
            
            template_path = Path(template.template_path) if template.template_path else None
            if not template_path or not template_path.exists():
                return False
            
            # Carregar template
            with open(template_path, "r") as f:
                template_content = f.read()
            
            # Substituir parâmetros
            if parameters:
                for key, value in parameters.items():
                    template_content = template_content.replace(f"{{{key}}}", str(value))
            
            # Compilar com iasl se disponível
            if self._has_iasl():
                # Salvar .dsl temporário
                dsl_path = output_path.with_suffix(".dsl")
                with open(dsl_path, "w") as f:
                    f.write(template_content)
                
                # Compilar
                result = subprocess.run(
                    ["iasl", str(dsl_path)],
                    capture_output=True,
                    text=True,
                )
                
                if result.returncode == 0:
                    # .aml deve ter sido gerado
                    aml_path = output_path.with_suffix(".aml")
                    if aml_path.exists():
                        return True
            
            # Fallback: salvar como .dsl
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(template_content)
            
            return True
        except Exception:
            return False
        finally:
            session.close()
    
    def _has_iasl(self) -> bool:
        """Verifica se iasl está disponível"""
        try:
            result = subprocess.run(
                ["iasl", "-v"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def patch_acpi(
        self,
        acpi_path: Path,
        patches: List[Dict[str, Any]],
    ) -> bool:
        """Aplica patches ACPI"""
        # Implementar patching ACPI
        # Referência: https://dortania.github.io/Getting-Started-With-ACPI/
        return False
    
    def validate_aml(self, aml_path: Path) -> bool:
        """Valida arquivo AML usando iasl"""
        if not self._has_iasl():
            return False
        
        try:
            result = subprocess.run(
                ["iasl", "-d", str(aml_path)],
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

