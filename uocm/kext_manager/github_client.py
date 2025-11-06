"""
Cliente GitHub para buscar informações de kexts
"""

import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime


class GitHubClient:
    """Cliente para API do GitHub"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {}
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    async def get_release(
        self,
        owner: str,
        repo: str,
        tag: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Busca release de um repositório"""
        async with httpx.AsyncClient() as client:
            if tag:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/releases/tags/{tag}"
            else:
                url = f"{self.BASE_URL}/repos/{owner}/{repo}/releases/latest"
            
            try:
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception:
                return None
    
    async def get_releases(
        self,
        owner: str,
        repo: str,
        per_page: int = 30,
    ) -> List[Dict[str, Any]]:
        """Busca todas as releases de um repositório"""
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/releases"
            params = {"per_page": per_page}
            
            try:
                response = await client.get(url, headers=self.headers, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception:
                return []
    
    async def download_asset(
        self,
        owner: str,
        repo: str,
        asset_id: int,
        save_path: str,
    ) -> bool:
        """Faz download de um asset de release"""
        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}/repos/{owner}/{repo}/releases/assets/{asset_id}"
            
            try:
                # Obter URL de download
                response = await client.get(url, headers=self.headers, timeout=30.0)
                response.raise_for_status()
                asset_info = response.json()
                download_url = asset_info.get("browser_download_url")
                
                if not download_url:
                    return False
                
                # Download do arquivo
                download_response = await client.get(
                    download_url,
                    headers={"Accept": "application/octet-stream"},
                    timeout=60.0,
                    follow_redirects=True,
                )
                download_response.raise_for_status()
                
                # Salvar arquivo
                from pathlib import Path
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(download_response.content)
                
                return True
            except Exception:
                return False

