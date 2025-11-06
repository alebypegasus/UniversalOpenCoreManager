from __future__ import annotations
from pathlib import Path
from typing import Mapping, Any
from jinja2 import Template
from ..plist.loader import save_plist
import plistlib


def generate_efi(output_dir: Path, profile: Mapping[str, Any]) -> Path:
    """Generate basic /EFI/OC structure in output_dir and return EFI folder path."""
    efi = output_dir / "EFI" / "OC"
    (efi / "Kexts").mkdir(parents=True, exist_ok=True)
    (efi / "ACPI").mkdir(parents=True, exist_ok=True)
    (efi / "Drivers").mkdir(parents=True, exist_ok=True)
    (efi / "Resources").mkdir(parents=True, exist_ok=True)
    # Create config.plist from template and profile
    template_path = Path(__file__).parents[2] / "infra" / "templates" / "config_default.plist"
    text = template_path.read_text(encoding="utf-8")
    rendered = Template(text).render(SMBIOS_PRODUCT=profile.get("smbios_suggestion", "iMac19,1"))
    config_path = efi / "config.plist"
    with config_path.open("wb") as fp:
        plistlib.dump(plistlib.loads(rendered.encode("utf-8")), fp)
    return efi.parent
