"""
Gerenciamento de banco de dados SQLAlchemy
"""

from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.pool import StaticPool

from uocm.core.config import Config
from uocm.db.models import Base


class Database:
    """Gerenciador de banco de dados"""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.get_db_path()
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False,
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
    
    def init_db(self) -> None:
        """Inicializa o banco de dados criando todas as tabelas"""
        Base.metadata.create_all(self.engine)
    
    def drop_db(self) -> None:
        """Remove todas as tabelas do banco de dados"""
        Base.metadata.drop_all(self.engine)
    
    @contextmanager
    def session(self):
        """Context manager para sessões do banco de dados"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão do banco de dados"""
        return self.Session()


# Instância global do banco de dados
_db: Optional[Database] = None


def get_database() -> Database:
    """Retorna a instância global do banco de dados"""
    global _db
    if _db is None:
        _db = Database()
        _db.init_db()
    return _db


def get_db_session() -> Session:
    """Retorna uma sessão do banco de dados"""
    return get_database().get_session()

