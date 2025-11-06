"""
Funcionalidade OC Snapshot inspirada no ProperTree
Referência: https://github.com/corpnewt/ProperTree
"""

import plistlib
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class OCSnapshot:
    """Gerenciador de OC Snapshot"""
    
    def __init__(self, oc_path: Path):
        self.oc_path = oc_path
        self.acpi_path = oc_path / "ACPI"
        self.kexts_path = oc_path / "Kexts"
        self.drivers_path = oc_path / "Drivers"
        self.tools_path = oc_path / "Tools"
    
    def get_opencore_version(self) -> Optional[str]:
        """Obtém versão do OpenCore.efi via MD5 hash"""
        opencore_efi = self.oc_path / "OpenCore.efi"
        
        if not opencore_efi.exists():
            return None
        
        # Calcular MD5
        md5_hash = self._calculate_md5(opencore_efi)
        
        # Mapeamento conhecido de hashes (exemplo - expandir com hashes reais)
        known_hashes = {
            # Adicionar hashes conhecidos do OpenCore
        }
        
        return known_hashes.get(md5_hash, None)
    
    def _calculate_md5(self, file_path: Path) -> str:
        """Calcula MD5 de um arquivo"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def snapshot_acpi(self, clean: bool = False, existing_add: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """Snapshot de arquivos ACPI"""
        if not self.acpi_path.exists():
            return []
        
        entries = [] if clean else (existing_add or [])
        aml_files = sorted(self.acpi_path.glob("*.aml"))
        
        for aml_file in aml_files:
            # Verificar se já existe
            existing = None
            if not clean:
                existing = next(
                    (e for e in entries if e.get("Path") == aml_file.name),
                    None
                )
            
            if existing:
                entry = existing
            else:
                entry = {
                    "Enabled": True,
                    "Path": aml_file.name,
                    "Comment": f"{aml_file.stem} - Auto-snapshot",
                }
                entries.append(entry)
        
        # Remover entradas de arquivos que não existem mais
        if not clean:
            existing_paths = {e.get("Path") for e in entries}
            current_paths = {f.name for f in aml_files}
            entries = [e for e in entries if e.get("Path") in current_paths]
        
        return entries
    
    def snapshot_kexts(
        self,
        clean: bool = False,
        existing_add: Optional[List[Dict]] = None,
    ) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Snapshot de kexts com ordenação por dependências"""
        if not self.kexts_path.exists():
            return [], []
        
        entries = [] if clean else (existing_add or [])
        kext_dirs = sorted([
            d for d in self.kexts_path.iterdir()
            if d.is_dir() and d.suffix == ".kext"
        ], key=lambda x: x.name)
        
        kext_info_map = {}
        warnings = []
        
        # Carregar informações de todos os kexts
        for kext_dir in kext_dirs:
            info_plist = kext_dir / "Contents" / "Info.plist"
            if not info_plist.exists():
                continue
            
            try:
                with open(info_plist, "rb") as f:
                    kext_info = plistlib.load(f)
                
                bundle_id = kext_info.get("CFBundleIdentifier", "")
                executable = kext_info.get("CFBundleExecutable", kext_dir.stem)
                os_bundle_libraries = kext_info.get("OSBundleLibraries", {})
                
                kext_info_map[kext_dir.name] = {
                    "bundle_id": bundle_id,
                    "executable": executable,
                    "libraries": os_bundle_libraries,
                    "path": kext_dir,
                }
            except Exception as e:
                warnings.append(f"Erro ao ler Info.plist de {kext_dir.name}: {e}")
        
        # Verificar duplicações de CFBundleIdentifier
        bundle_ids = {}
        for name, info in kext_info_map.items():
            bundle_id = info["bundle_id"]
            if bundle_id:
                if bundle_id in bundle_ids:
                    warnings.append(
                        f"CFBundleIdentifier duplicado: {bundle_id} "
                        f"({bundle_ids[bundle_id]} e {name})"
                    )
                bundle_ids[bundle_id] = name
        
        # Ordenar kexts por dependências
        sorted_kexts = self._sort_kexts_by_dependencies(kext_info_map)
        
        # Criar/atualizar entradas
        for kext_name in sorted_kexts:
            info = kext_info_map[kext_name]
            
            # Verificar se já existe
            existing = None
            if not clean:
                existing = next(
                    (e for e in entries if e.get("BundlePath") == kext_name),
                    None
                )
            
            if existing:
                # Atualizar entrada existente
                entry = existing
            else:
                # Criar nova entrada
                entry = {
                    "Arch": "Any",
                    "BundlePath": kext_name,
                    "Enabled": True,
                    "ExecutablePath": f"Contents/MacOS/{info['executable']}",
                    "PlistPath": "Contents/Info.plist",
                    "Comment": f"{Path(kext_name).stem} - Auto-snapshot",
                    "MinKernel": "",
                    "MaxKernel": "",
                }
                entries.append(entry)
        
        # Remover entradas de kexts que não existem mais
        if not clean:
            existing_paths = {e.get("BundlePath") for e in entries}
            current_paths = set(kext_info_map.keys())
            entries = [e for e in entries if e.get("BundlePath") in current_paths]
        
        return entries, warnings
    
    def _sort_kexts_by_dependencies(self, kext_info_map: Dict[str, Dict]) -> List[str]:
        """Ordena kexts por dependências (topological sort)"""
        sorted_kexts = []
        visited = set()
        temp_visited = set()
        
        def visit(kext_name: str):
            if kext_name in temp_visited:
                # Dependência circular detectada
                return
            if kext_name in visited:
                return
            
            temp_visited.add(kext_name)
            
            # Visitar dependências primeiro
            info = kext_info_map.get(kext_name, {})
            libraries = info.get("libraries", {})
            
            for lib_bundle_id in libraries.keys():
                # Encontrar kext que fornece esta biblioteca
                for other_name, other_info in kext_info_map.items():
                    if other_info.get("bundle_id") == lib_bundle_id:
                        visit(other_name)
                        break
            
            temp_visited.remove(kext_name)
            visited.add(kext_name)
            sorted_kexts.append(kext_name)
        
        for kext_name in kext_info_map.keys():
            if kext_name not in visited:
                visit(kext_name)
        
        return sorted_kexts
    
    def snapshot_drivers(self, clean: bool = False, existing_drivers: Optional[List[str]] = None) -> List[str]:
        """Snapshot de drivers UEFI"""
        if not self.drivers_path.exists():
            return []
        
        drivers = [] if clean else (existing_drivers or [])
        driver_files = sorted(self.drivers_path.glob("*.efi"))
        
        current_drivers = {f.name for f in driver_files}
        
        # Adicionar drivers novos
        for driver_file in driver_files:
            if driver_file.name not in drivers:
                drivers.append(driver_file.name)
        
        # Remover drivers que não existem mais
        if not clean:
            drivers = [d for d in drivers if d in current_drivers]
        
        return drivers
    
    def snapshot_tools(
        self,
        clean: bool = False,
        existing_tools: Optional[List[Dict]] = None,
    ) -> List[Dict[str, Any]]:
        """Snapshot de tools"""
        if not self.tools_path.exists():
            return []
        
        tools = [] if clean else (existing_tools or [])
        tool_files = sorted(self.tools_path.glob("*.efi"))
        
        for tool_file in tool_files:
            # Verificar se já existe
            existing = None
            if not clean:
                existing = next(
                    (e for e in tools if e.get("Path") == tool_file.name),
                    None
                )
            
            if existing:
                entry = existing
            else:
                entry = {
                    "Arguments": "",
                    "Auxiliary": False,
                    "Comment": f"{tool_file.stem} - Auto-snapshot",
                    "Enabled": True,
                    "Name": tool_file.stem,
                    "Path": tool_file.name,
                }
                tools.append(entry)
        
        # Remover entradas de tools que não existem mais
        if not clean:
            existing_paths = {e.get("Path") for e in tools}
            current_paths = {f.name for f in tool_files}
            tools = [e for e in tools if e.get("Path") in current_paths]
        
        return tools
    
    def perform_snapshot(
        self,
        config_data: Dict[str, Any],
        clean: bool = False,
    ) -> Tuple[Dict[str, Any], List[str]]:
        """
        Executa snapshot completo do OpenCore
        
        Returns:
            Tuple de (config_data_updated, warnings)
        """
        warnings = []
        
        # ACPI
        existing_acpi = config_data.get("ACPI", {}).get("Add", []) if not clean else []
        acpi_entries = self.snapshot_acpi(clean, existing_acpi)
        if "ACPI" not in config_data:
            config_data["ACPI"] = {}
        config_data["ACPI"]["Add"] = acpi_entries
        
        # Kexts
        existing_kexts = config_data.get("Kernel", {}).get("Add", []) if not clean else []
        kext_entries, kext_warnings = self.snapshot_kexts(clean, existing_kexts)
        if "Kernel" not in config_data:
            config_data["Kernel"] = {}
        config_data["Kernel"]["Add"] = kext_entries
        warnings.extend(kext_warnings)
        
        # Drivers
        existing_drivers = config_data.get("UEFI", {}).get("Drivers", []) if not clean else []
        drivers = self.snapshot_drivers(clean, existing_drivers)
        if "UEFI" not in config_data:
            config_data["UEFI"] = {}
        config_data["UEFI"]["Drivers"] = drivers
        
        # Tools
        existing_tools = config_data.get("Misc", {}).get("Tools", []) if not clean else []
        tools = self.snapshot_tools(clean, existing_tools)
        if "Misc" not in config_data:
            config_data["Misc"] = {}
        config_data["Misc"]["Tools"] = tools
        
        return config_data, warnings

