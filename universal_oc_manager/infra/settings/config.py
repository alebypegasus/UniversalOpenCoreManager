from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    data_dir: Path = Path.home() / ".uocm"
    db_path: Path = (Path.home() / ".uocm" / "uocm.sqlite3")
    cache_dir: Path = Path.home() / ".uocm" / "cache"
    locale: str = "pt-BR"


CONFIG = AppConfig()
