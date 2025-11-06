"""
Gerenciador de Kexts com download, atualização e instalação
"""

import zipfile
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
import hashlib

from uocm.db.database import get_db_session
from uocm.db.models import KextInfo
from uocm.kext_manager.github_client import GitHubClient
from uocm.core.config import Config


class KextManager:
    """Gerenciador de kexts com integração GitHub"""
    
    def __init__(self):
        self.github = GitHubClient()
        self.kexts_dir = Config.get_data_path() / "kexts"
        self.kexts_dir.mkdir(parents=True, exist_ok=True)
    
    async def update_kext_catalog(self) -> bool:
        """Atualiza catálogo de kexts do GitHub"""
        session = get_db_session()
        try:
            # Lista de kexts principais (Acidanthera)
            kexts_repos = [
                ("acidanthera", "Lilu"),
                ("acidanthera", "VirtualSMC"),
                ("acidanthera", "WhateverGreen"),
                ("acidanthera", "AppleALC"),
                ("acidanthera", "AirportBrcmFixup"),
                ("OpenIntelWireless", "itlwm"),
                ("OpenIntelWireless", "AirportItlwm"),
                ("acidanthera", "CPUFriend"),
                ("acidanthera", "HibernationFixup"),
                ("acidanthera", "NVMeFix"),
                ("acidanthera", "RestrictEvents"),
                ("acidanthera", "VoodooI2C"),
            ]
            
            for owner, repo in kexts_repos:
                release = await self.github.get_release(owner, repo)
                if release:
                    await self._update_kext_info(session, owner, repo, release)
            
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False
        finally:
            session.close()
    
    async def _update_kext_info(
        self,
        session: Any,
        owner: str,
        repo: str,
        release: Dict[str, Any],
    ) -> None:
        """Atualiza informações de um kext no banco"""
        kext = session.query(KextInfo).filter(KextInfo.name == repo).first()
        
        if not kext:
            kext = KextInfo(name=repo)
            session.add(kext)
        
        kext.display_name = repo
        kext.version = release.get("tag_name", "").lstrip("v")
        kext.github_repo = f"{owner}/{repo}"
        kext.github_release_tag = release.get("tag_name", "")
        kext.description = release.get("body", "")[:500] if release.get("body") else None
        
        # Buscar asset ZIP
        assets = release.get("assets", [])
        for asset in assets:
            if asset.get("name", "").endswith(".zip"):
                kext.download_url = asset.get("browser_download_url")
                break
        
        session.add(kext)
    
    async def download_kext(self, kext_name: str) -> Optional[Path]:
        """Faz download de um kext"""
        session = get_db_session()
        try:
            kext = session.query(KextInfo).filter(KextInfo.name == kext_name).first()
            if not kext or not kext.download_url:
                return None
            
            # Download
            zip_path = self.kexts_dir / f"{kext_name}.zip"
            
            # Extrair do download_url
            if "/" in kext.github_repo:
                owner, repo = kext.github_repo.split("/", 1)
                # Simplificado - assumir que download_url já está correto
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(kext.download_url, timeout=60.0, follow_redirects=True)
                    response.raise_for_status()
                    with open(zip_path, "wb") as f:
                        f.write(response.content)
            
            # Extrair ZIP
            extract_dir = self.kexts_dir / kext_name
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Encontrar .kext dentro do ZIP extraído
            kext_file = None
            for item in extract_dir.rglob("*.kext"):
                kext_file = item
                break
            
            if kext_file:
                kext.local_path = str(kext_file)
                kext.installed = True
                kext.installed_version = kext.version
                session.commit()
                return kext_file
            
            return None
        except Exception:
            return None
        finally:
            session.close()
    
    def get_installed_kexts(self) -> List[KextInfo]:
        """Retorna lista de kexts instalados"""
        session = get_db_session()
        try:
            return session.query(KextInfo).filter(KextInfo.installed == True).all()
        finally:
            session.close()
    
    def get_available_kexts(self) -> List[KextInfo]:
        """Retorna lista de todos os kexts disponíveis"""
        session = get_db_session()
        try:
            return session.query(KextInfo).all()
        finally:
            session.close()
    
    def verify_kext(self, kext_path: Path) -> bool:
        """Verifica integridade de um kext"""
        if not kext_path.exists():
            return False
        
        # Verificar estrutura básica
        if kext_path.is_dir() and kext_path.suffix == ".kext":
            info_plist = kext_path / "Contents" / "Info.plist"
            return info_plist.exists()
        
        return False
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calcula checksum SHA256 de um arquivo"""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

