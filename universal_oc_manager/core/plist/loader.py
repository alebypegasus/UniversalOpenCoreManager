from __future__ import annotations
import plistlib
from typing import Any
from pathlib import Path


def load_plist(path: Path) -> dict[str, Any]:
    with path.open("rb") as fp:
        return plistlib.load(fp)


def save_plist(path: Path, data: dict[str, Any]) -> None:
    with path.open("wb") as fp:
        plistlib.dump(data, fp)
