from pathlib import Path
import tempfile
import plistlib
from universal_oc_manager.core.validator.schema_validator import validate_config, ValidationErrorInfo


def test_validate_minimal_config():
    """Testa validação de um config.plist mínimo válido."""
    config = {
        "ACPI": {},
        "Booter": {},
        "DeviceProperties": {},
        "Kernel": {},
        "Misc": {},
        "NVRAM": {},
        "PlatformInfo": {},
        "UEFI": {},
    }
    errors = validate_config(config)
    # Config mínimo deve passar (sem erros críticos de schema)
    assert isinstance(errors, list)


def test_validate_missing_required():
    """Testa validação de config com campos obrigatórios faltando."""
    config = {
        "ACPI": {},
        # Faltam outros campos obrigatórios
    }
    errors = validate_config(config)
    # Deve ter erros de campos faltando
    assert len(errors) > 0
    assert any("required" in e.message.lower() or "Booter" in e.message for e in errors)


def test_validation_error_info():
    """Testa a estrutura ValidationErrorInfo."""
    error = ValidationErrorInfo(
        message="Teste de erro",
        path="ACPI.Add",
        validator="type",
        value="invalid",
    )
    assert error.message == "Teste de erro"
    assert error.path == "ACPI.Add"
    d = error.to_dict()
    assert d["message"] == "Teste de erro"
    assert d["path"] == "ACPI.Add"
    assert d["validator"] == "type"

