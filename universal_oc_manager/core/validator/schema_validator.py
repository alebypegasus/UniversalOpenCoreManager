from __future__ import annotations
from jsonschema import Draft202012Validator
from typing import Any
from dataclasses import dataclass
from ...infra.schemas.schema_manager import get_schema


@dataclass
class ValidationErrorInfo:
    """Detailed information about a validation error."""
    message: str
    path: str
    validator: str
    value: Any = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "path": self.path,
            "validator": self.validator,
            "value": str(self.value) if self.value is not None else None,
        }


def validate_config(
    config: dict[str, Any], schema: dict[str, Any] | None = None
) -> list[ValidationErrorInfo]:
    """Validate a config.plist against OpenCore schema.
    
    Returns list of detailed errors (path, message, validator).
    """
    if schema is None:
        schema = get_schema()

    validator = Draft202012Validator(schema)
    errors: list[ValidationErrorInfo] = []

    for error in validator.iter_errors(config):
        path = ".".join(str(x) for x in error.path) if error.path else "root"
        errors.append(
            ValidationErrorInfo(
                message=error.message,
                path=path,
                validator=error.validator,
                value=error.instance,
            )
        )

    return errors


def validate_config_simple(config: dict[str, Any]) -> list[str]:
    """Simplified version: returns only error messages."""
    return [e.message for e in validate_config(config)]
