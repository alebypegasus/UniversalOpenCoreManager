from __future__ import annotations
from dataclasses import dataclass, asdict
import subprocess
import json
from typing import Any


@dataclass
class HardwareProfile:
    cpu: str | None = None
    igpu: str | None = None
    gpu: str | None = None
    chipset: str | None = None
    smbios_suggestion: str | None = "iMac19,1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sp_json(datatype: str) -> dict[str, Any]:
    try:
        out = subprocess.check_output(["/usr/sbin/system_profiler", f"{datatype}", "-json"], text=True)
        return json.loads(out)
    except Exception:
        return {}


def detect_hardware() -> HardwareProfile:
    sp_hw = _sp_json("SPHardwareDataType")
    cpu_name = None
    try:
        items = sp_hw.get("SPHardwareDataType", [])
        if items:
            cpu_name = items[0].get("cpu_type") or items[0].get("machine_model")
    except Exception:
        pass
    return HardwareProfile(cpu=cpu_name)

