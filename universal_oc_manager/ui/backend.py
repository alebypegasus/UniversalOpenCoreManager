from __future__ import annotations
from PyQt6.QtCore import QObject, pyqtSlot, pyqtSignal, QUrl
from pathlib import Path
from typing import Any
import json
from ..core.detector.detect import detect_hardware
from ..core.engine.generator import generate_efi
from ..core.plist.loader import load_plist, save_plist
from ..core.validator.schema_validator import validate_config, ValidationErrorInfo
from ..infra.logging.logger import get_logger


class AppController(QObject):
    # Signals for QML
    # Note: QML doesn't accept list directly, so we use "QVariantList" or emit as list of objects
    validationErrorsChanged = pyqtSignal("QVariantList")  # List of errors (dicts)
    hardwareDetected = pyqtSignal("QVariantMap")  # Detected hardware profile
    efiGenerated = pyqtSignal(str)  # Path of generated EFI

    def __init__(self) -> None:
        super().__init__()
        self._logger = get_logger("uocm.ui")
        self._last_profile: dict[str, Any] | None = None
        self._current_config: dict[str, Any] | None = None
        self._current_config_path: Path | None = None

    @pyqtSlot()
    def detectHardware(self) -> None:
        self._logger.info("Detecting hardware...")
        profile = detect_hardware().to_dict()
        self._last_profile = profile
        self.hardwareDetected.emit(profile)
        self._logger.info(f"Hardware detected: {profile}")

    @pyqtSlot()
    def generateEFI(self) -> None:
        out = Path.home() / "Desktop" / "UOCM-EFI"
        out.mkdir(parents=True, exist_ok=True)
        profile = self._last_profile or {}
        self._logger.info("Generating EFI...")
        efi_path = generate_efi(out, profile)
        self.efiGenerated.emit(str(efi_path))
        self._logger.info(f"EFI generated at: {efi_path}")

    @pyqtSlot(str, result="QVariantList")
    def validateConfigFile(self, file_path: str) -> list[dict[str, Any]]:
        """Validate a config.plist file and return list of errors (as dicts)."""
        try:
            path = Path(file_path)
            if not path.exists():
                return [{"message": f"File not found: {file_path}", "path": "", "validator": ""}]
            config = load_plist(path)
            self._current_config = config
            self._current_config_path = path
            errors = validate_config(config)
            errors_dict = [e.to_dict() for e in errors]
            self.validationErrorsChanged.emit(errors_dict)
            return errors_dict
        except Exception as e:
            self._logger.error(f"Error validating config: {e}")
            return [{"message": f"Validation error: {str(e)}", "path": "", "validator": ""}]

    @pyqtSlot(result="QVariantList")
    def validateCurrentConfig(self) -> list[dict[str, Any]]:
        """Validate the current config.plist in memory."""
        if self._current_config is None:
            return []
        errors = validate_config(self._current_config)
        errors_dict = [e.to_dict() for e in errors]
        self.validationErrorsChanged.emit(errors_dict)
        return errors_dict

    @pyqtSlot(str, result="QVariantList")
    def validateConfigJSON(self, config_json: str) -> list[dict[str, Any]]:
        """Validate a config.plist passed as JSON string."""
        try:
            config = json.loads(config_json)
            errors = validate_config(config)
            errors_dict = [e.to_dict() for e in errors]
            self.validationErrorsChanged.emit(errors_dict)
            return errors_dict
        except json.JSONDecodeError as e:
            return [{"message": f"Invalid JSON: {str(e)}", "path": "", "validator": ""}]
        except Exception as e:
            return [{"message": f"Error: {str(e)}", "path": "", "validator": ""}]

    @pyqtSlot(str)
    def loadConfig(self, file_path: str) -> None:
        """Load a config.plist file for editing."""
        try:
            path = Path(file_path)
            config = load_plist(path)
            self._current_config = config
            self._current_config_path = path
            # Automatically validate after loading
            self.validateCurrentConfig()
        except Exception as e:
            self._logger.error(f"Error loading config: {e}")

    @pyqtSlot(str, str, result=bool)
    def saveConfig(self, file_path: str | None = None, config_json: str | None = None) -> bool:
        """Save the current config.plist."""
        try:
            if config_json:
                config = json.loads(config_json)
            elif self._current_config:
                config = self._current_config
            else:
                return False

            path = Path(file_path) if file_path else self._current_config_path
            if not path:
                return False

            save_plist(path, config)
            self._current_config = config
            self._current_config_path = path
            return True
        except Exception as e:
            self._logger.error(f"Erro ao salvar config: {e}")
            return False

