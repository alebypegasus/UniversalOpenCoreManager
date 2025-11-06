from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from ..settings.config import CONFIG
from ..http.github_client import GitHubClient
from ..logging.logger import get_logger


class SchemaManager:
    """Manages OpenCore schema: fetch, cache, and loading."""

    def __init__(self) -> None:
        self._logger = get_logger("uocm.schema")
        self._cache_dir = CONFIG.cache_dir / "schemas"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._github = GitHubClient()
        self._schema_path = self._cache_dir / "opencore_schema.json"

    def _fetch_official_schema(self) -> dict[str, Any] | None:
        """Try to fetch official schema from OpenCorePkg (if available)."""
        try:
            # Try to fetch schema from OpenCorePkg repository
            # Note: OpenCore may not have an official JSON schema, so we use a fallback
            schema_content = self._github.get_raw_file(
                "acidanthera", "OpenCorePkg", "Docs/Sample.plist", branch="master"
            )
            # For now, return None and use our local schema
            # TODO: Parse Sample.plist and generate schema based on it
            self._logger.info("Official schema not available as JSON, using local schema")
            return None
        except Exception as e:
            self._logger.warning(f"Failed to fetch official schema: {e}")
            return None

    def get_schema(self, force_refresh: bool = False) -> dict[str, Any]:
        """Return OpenCore schema (local cache or remote fetch)."""
        if not force_refresh and self._schema_path.exists():
            try:
                with self._schema_path.open("r", encoding="utf-8") as fp:
                    return json.load(fp)
            except Exception as e:
                self._logger.warning(f"Error loading schema from cache: {e}")

        # Try to fetch official schema
        official = self._fetch_official_schema()
        if official:
            with self._schema_path.open("w", encoding="utf-8") as fp:
                json.dump(official, fp, indent=2)
            return official

        # Fallback: use local minimal schema
        fallback_path = Path(__file__).parent / "opencore_schema.json"
        if fallback_path.exists():
            with fallback_path.open("r", encoding="utf-8") as fp:
                schema = json.load(fp)
                # Save to cache
                with self._schema_path.open("w", encoding="utf-8") as fp:
                    json.dump(schema, fp, indent=2)
                return schema

        # Last resort: minimal inline schema
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "ACPI": {"type": "object"},
                "Booter": {"type": "object"},
                "DeviceProperties": {"type": "object"},
                "Kernel": {"type": "object"},
                "Misc": {"type": "object"},
                "NVRAM": {"type": "object"},
                "PlatformInfo": {"type": "object"},
                "UEFI": {"type": "object"},
            },
            "required": [
                "ACPI",
                "Booter",
                "DeviceProperties",
                "Kernel",
                "Misc",
                "NVRAM",
                "PlatformInfo",
                "UEFI",
            ],
        }


_SCHEMA_MANAGER = SchemaManager()


def get_schema(force_refresh: bool = False) -> dict[str, Any]:
    """Helper function to get the schema."""
    return _SCHEMA_MANAGER.get_schema(force_refresh=force_refresh)

