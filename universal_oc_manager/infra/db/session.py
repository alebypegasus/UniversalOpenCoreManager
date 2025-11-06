from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from ..settings.config import CONFIG
from .models import Base

_engine = create_engine(f"sqlite:///{CONFIG.db_path}", future=True)
SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False, future=True)


def init_db() -> None:
    Path(CONFIG.data_dir).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(_engine)
