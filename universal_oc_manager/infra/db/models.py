from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    pass


class Kext(Base):
    __tablename__ = "kexts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    repo: Mapped[str] = mapped_column(String(256))
    latest_version: Mapped[str] = mapped_column(String(64), default="")
