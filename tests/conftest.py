"""
Fixtures pytest para testes
"""

import pytest
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from uocm.db.models import Base
from uocm.db.database import Database
from uocm.core.config import Config


@pytest.fixture
def temp_db():
    """Cria banco de dados temporário para testes"""
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = Path(db_file.name)
    db_file.close()
    
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session, db_path
    
    session.close()
    db_path.unlink()


@pytest.fixture
def temp_dir():
    """Cria diretório temporário para testes"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_hardware_info():
    """Retorna informações de hardware de exemplo"""
    from uocm.detector.models import HardwareInfo, CPUInfo, GPUInfo
    
    return HardwareInfo(
        cpu=CPUInfo(
            model="Intel Core i7-8700K",
            vendor="Intel",
            cores=6,
            threads=12,
            microarchitecture="Coffee Lake",
        ),
        gpu=GPUInfo(
            model="Intel UHD Graphics 630",
            vendor="Intel",
        ),
    )


@pytest.fixture(autouse=True)
def setup_config(temp_dir):
    """Configura Config para testes"""
    Config.set_app_path(temp_dir)
    yield
    # Cleanup se necessário

