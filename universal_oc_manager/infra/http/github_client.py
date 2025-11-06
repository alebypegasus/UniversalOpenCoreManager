from __future__ import annotations
import httpx
from typing import Any
from pathlib import Path


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._client = httpx.Client(base_url="https://api.github.com", headers=headers, timeout=30)
        self._raw_client = httpx.Client(timeout=30)

    def get_release(self, owner: str, repo: str, tag: str | None = None) -> dict[str, Any]:
        if tag:
            resp = self._client.get(f"/repos/{owner}/{repo}/releases/tags/{tag}")
        else:
            resp = self._client.get(f"/repos/{owner}/{repo}/releases/latest")
        resp.raise_for_status()
        return resp.json()

    def get_raw_file(self, owner: str, repo: str, path: str, branch: str = "master") -> bytes:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        resp = self._raw_client.get(url)
        resp.raise_for_status()
        return resp.content

    def download_asset(self, url: str, dest: Path) -> None:
        resp = self._raw_client.get(url, follow_redirects=True)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
