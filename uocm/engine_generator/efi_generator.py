"""
Gerador automático de EFI/OpenCore
"""

import json
import plistlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

from uocm.detector.models import HardwareInfo
from uocm.engine_generator.modes import GenerationMode
from uocm.core.config import Config
from uocm.db.database import get_db_session
from uocm.db.models import SMBIOSProfile, HardwareProfile, KextInfo, SSDTTemplate


class EFIGenerator:
    """Gerador automático de EFI baseado em hardware detectado"""
    
    def __init__(self):
        self.templates_path = Config.get_templates_path()
    
    def generate_efi(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode = GenerationMode.STANDARD,
        output_path: Optional[Path] = None,
        smbios_override: Optional[str] = None,
    ) -> Path:
        """
        Gera uma estrutura EFI completa baseada no hardware detectado
        
        Args:
            hardware: Informações de hardware detectadas
            mode: Modo de geração (conservative/standard/aggressive)
            output_path: Caminho de saída (opcional)
            smbios_override: SMBIOS manual para usar (opcional)
        
        Returns:
            Caminho para o EFI gerado
        """
        if output_path is None:
            output_path = Config.get_exports_path() / f"EFI_{hardware.cpu.model.replace(' ', '_')}"
        
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Criar estrutura de diretórios
        oc_path = output_path / "EFI" / "OC"
        for subdir in ["ACPI", "Kexts", "Drivers", "Tools", "Resources"]:
            (oc_path / subdir).mkdir(parents=True, exist_ok=True)
        
        # Gerar config.plist
        config_plist = self._generate_config_plist(hardware, mode, smbios_override)
        config_path = oc_path / "config.plist"
        with open(config_path, "wb") as f:
            plistlib.dump(config_plist, f)
        
        # Copiar kexts necessários
        kexts = self._get_recommended_kexts(hardware, mode)
        self._install_kexts(kexts, oc_path / "Kexts")
        
        # Copiar drivers necessários
        drivers = self._get_recommended_drivers(hardware, mode)
        self._install_drivers(drivers, oc_path / "Drivers")
        
        # Gerar SSDTs necessários
        ssdts = self._get_recommended_ssdts(hardware, mode)
        self._generate_ssdts(ssdts, oc_path / "ACPI", hardware)
        
        return output_path
    
    def _generate_config_plist(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
        smbios_override: Optional[str],
    ) -> Dict[str, Any]:
        """Gera o config.plist baseado no hardware"""
        # Carregar template base
        base_template = self._load_base_template()
        
        # Determinar SMBIOS
        smbios = self._determine_smbios(hardware, smbios_override)
        
        # Configurar SMBIOS
        base_template["PlatformInfo"]["Generic"] = {
            "AdviseFeatures": False,
            "MLB": self._generate_mlb(),
            "ROM": self._generate_rom(),
            "SystemProductName": smbios["product_name"],
            "SystemSerialNumber": self._generate_serial(smbios.get("serial_prefix", "")),
            "SystemUUID": self._generate_uuid(),
        }
        
        # Configurar ACPI
        base_template["ACPI"]["Add"] = self._get_acpi_add_entries(hardware, mode)
        base_template["ACPI"]["Patch"] = self._get_acpi_patches(hardware, mode)
        base_template["ACPI"]["Quirks"] = self._get_acpi_quirks(hardware, mode)
        
        # Configurar Boot
        base_template["Boot"]["Quirks"] = self._get_boot_quirks(hardware, mode)
        
        # Configurar Kernel
        base_template["Kernel"]["Add"] = self._get_kernel_add_entries(hardware, mode)
        base_template["Kernel"]["Quirks"] = self._get_kernel_quirks(hardware, mode)
        
        # Configurar UEFI
        base_template["UEFI"]["Drivers"] = self._get_uefi_drivers(hardware, mode)
        base_template["UEFI"]["Quirks"] = self._get_uefi_quirks(hardware, mode)
        
        return base_template
    
    def _load_base_template(self) -> Dict[str, Any]:
        """Carrega template base do config.plist"""
        template_path = self.templates_path / "config_base.plist"
        
        if template_path.exists():
            with open(template_path, "rb") as f:
                return plistlib.load(f)
        
        # Template mínimo se não existir arquivo
        return self._get_minimal_config()
    
    def _get_minimal_config(self) -> Dict[str, Any]:
        """Retorna configuração mínima válida do OpenCore"""
        return {
            "ACPI": {
                "Add": [],
                "Delete": [],
                "Patch": [],
                "Quirks": {},
            },
            "Booter": {
                "MmioWhitelist": [],
                "Quirks": {},
            },
            "Boot": {
                "Arguments": "",
                "ConsoleAttributes": 0,
                "HibernateMode": "None",
                "LauncherOption": "Disabled",
                "LauncherPath": "Default",
                "MiscDebug": False,
                "PickerMode": "Builtin",
                "PickerVariant": "Auto",
                "PollAppleHotKeys": False,
                "Quirks": {},
                "Security": "Vault",
                "Timeout": 5,
            },
            "DeviceProperties": {
                "Add": {},
                "Delete": {},
            },
            "Kernel": {
                "Add": [],
                "Block": [],
                "Emulate": {},
                "Force": [],
                "Patch": [],
                "Quirks": {},
                "Scheme": {},
            },
            "Misc": {
                "Boot": {},
                "Debug": {},
                "Entries": [],
                "Security": {},
                "Tools": [],
            },
            "NVRAM": {
                "Add": {},
                "Delete": {},
                "LegacyEnable": False,
                "LegacyOverwrite": False,
                "LegacySchema": {},
            },
            "PlatformInfo": {
                "DataHub": {},
                "Generic": {},
                "PlatformNVRAM": {},
                "SMBIOS": {},
                "UpdateDataHub": False,
                "UpdateNVRAM": False,
                "UpdateSMBIOS": False,
            },
            "UEFI": {
                "Audio": {},
                "ConnectDrivers": True,
                "Drivers": [],
                "Input": {},
                "Output": {},
                "ProtocolOverrides": {},
                "Quirks": {},
                "ReservedMemory": [],
            },
        }
    
    def _determine_smbios(
        self,
        hardware: HardwareInfo,
        smbios_override: Optional[str],
    ) -> Dict[str, str]:
        """Determina o SMBIOS recomendado baseado no hardware"""
        session = get_db_session()
        try:
            if smbios_override:
                profile = session.query(SMBIOSProfile).filter(
                    SMBIOSProfile.name == smbios_override
                ).first()
                if profile:
                    return {
                        "product_name": profile.product_name,
                        "serial_prefix": profile.serial_number_prefix or "",
                    }
            
            # Buscar perfil de hardware no banco
            profile = session.query(HardwareProfile).filter(
                HardwareProfile.cpu_model.like(f"%{hardware.cpu.model}%")
            ).first()
            
            if profile and profile.recommended_smbios_id:
                smbios = session.query(SMBIOSProfile).filter(
                    SMBIOSProfile.id == profile.recommended_smbios_id
                ).first()
                if smbios:
                    return {
                        "product_name": smbios.product_name,
                        "serial_prefix": smbios.serial_number_prefix or "",
                    }
            
            # Fallback: recomendar baseado em CPU
            if hardware.cpu.vendor == "Intel":
                if "Coffee Lake" in (hardware.cpu.microarchitecture or ""):
                    return {"product_name": "MacBookPro15,1", "serial_prefix": "C02"}
                elif "Comet Lake" in (hardware.cpu.microarchitecture or ""):
                    return {"product_name": "iMac20,1", "serial_prefix": "C02"}
                elif "Alder Lake" in (hardware.cpu.microarchitecture or ""):
                    return {"product_name": "Mac14,2", "serial_prefix": "C02"}
            
            # Default seguro
            return {"product_name": "iMacPro1,1", "serial_prefix": "C02"}
        finally:
            session.close()
    
    def _get_recommended_kexts(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[str]:
        """Retorna lista de kexts recomendados"""
        session = get_db_session()
        try:
            kexts = []
            
            # Kexts essenciais sempre
            kexts.extend(["Lilu", "VirtualSMC", "WhateverGreen"])
            
            # Kexts baseados em GPU
            if hardware.gpu:
                if hardware.gpu.vendor == "AMD":
                    kexts.append("WhateverGreen")
                elif hardware.gpu.vendor == "NVIDIA":
                    # NVIDIA não suportado em versões recentes
                    pass
            
            # Kexts de áudio
            if hardware.audio:
                kexts.append("AppleALC")
            
            # Kexts de rede
            if hardware.network:
                if hardware.network.wifi_model:
                    # Detectar tipo de Wi-Fi e adicionar kext apropriado
                    if "Intel" in (hardware.network.wifi_model or ""):
                        kexts.append("AirportItlwm")
                    elif "Broadcom" in (hardware.network.wifi_model or ""):
                        kexts.append("AirportBrcmFixup")
            
            # Kexts baseados em CPU
            if hardware.cpu.vendor == "Intel":
                if "Coffee Lake" in (hardware.cpu.microarchitecture or ""):
                    kexts.append("CPUFriend")
            
            # Modo agressivo adiciona mais kexts
            if mode == GenerationMode.AGGRESSIVE:
                kexts.extend(["USBInjectAll", "VoodooI2C"])
            
            return kexts
        finally:
            session.close()
    
    def _get_recommended_drivers(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[str]:
        """Retorna lista de drivers UEFI recomendados"""
        drivers = ["OpenRuntime.efi", "OpenCanopy.efi"]
        
        if mode != GenerationMode.CONSERVATIVE:
            drivers.append("HfsPlus.efi")
        
        return drivers
    
    def _get_recommended_ssdts(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[str]:
        """Retorna lista de SSDTs recomendados"""
        ssdts = []
        
        if hardware.cpu.vendor == "Intel":
            ssdts.append("SSDT-PLUG")
            if "Coffee Lake" in (hardware.cpu.microarchitecture or ""):
                ssdts.append("SSDT-PMC")
        
        if mode != GenerationMode.CONSERVATIVE:
            ssdts.append("SSDT-USB-Reset")
        
        return ssdts
    
    def _install_kexts(self, kext_names: List[str], kexts_dir: Path) -> None:
        """Instala kexts no diretório"""
        session = get_db_session()
        try:
            for kext_name in kext_names:
                kext = session.query(KextInfo).filter(
                    KextInfo.name == kext_name
                ).first()
                
                if kext and kext.local_path:
                    kext_path = Path(kext.local_path)
                    if kext_path.exists():
                        # Copiar kext
                        import shutil
                        dest = kexts_dir / kext_path.name
                        if kext_path.is_dir():
                            shutil.copytree(kext_path, dest, dirs_exist_ok=True)
                        else:
                            shutil.copy2(kext_path, dest)
        finally:
            session.close()
    
    def _install_drivers(self, driver_names: List[str], drivers_dir: Path) -> None:
        """Instala drivers UEFI no diretório"""
        # Implementar busca e cópia de drivers
        pass
    
    def _generate_ssdts(
        self,
        ssdt_names: List[str],
        acpi_dir: Path,
        hardware: HardwareInfo,
    ) -> None:
        """Gera SSDTs necessários"""
        # Implementar geração de SSDTs a partir de templates
        pass
    
    def _get_acpi_add_entries(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[Dict[str, Any]]:
        """Retorna entradas ACPI Add"""
        entries = []
        ssdts = self._get_recommended_ssdts(hardware, mode)
        
        for ssdt in ssdts:
            entries.append({
                "Enabled": True,
                "Path": f"{ssdt}.aml",
                "Comment": f"{ssdt} - Auto-generated",
            })
        
        return entries
    
    def _get_acpi_patches(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[Dict[str, Any]]:
        """Retorna patches ACPI"""
        return []
    
    def _get_acpi_quirks(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> Dict[str, bool]:
        """Retorna quirks ACPI"""
        return {
            "FadtEnableReset": True,
            "NormalizeHeaders": True,
            "RebaseRegions": True,
            "ResetHpet": False,
            "ResetLogoStatus": False,
        }
    
    def _get_boot_quirks(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> Dict[str, bool]:
        """Retorna quirks de boot"""
        return {
            "AllowNvramReset": True,
            "AvoidRuntimeDefrag": True,
            "DevirtualiseMmio": False,
            "DisableSingleUser": False,
            "DisableVariableWrite": False,
            "DiscardHibernateMap": False,
            "EnableSafeModeSlide": True,
            "EnableWriteUnprotector": True,
            "ForceBooterSignature": False,
            "ForceExitBootServices": False,
            "ProtectCsmRegion": False,
            "ProtectSecureBoot": False,
            "ProtectUefiServices": False,
            "ProvideCustomSlide": True,
            "RebuildAppleMemoryMap": True,
            "SetupVirtualMap": True,
            "SignalAppleOS": False,
            "SyncRuntimePermissions": True,
        }
    
    def _get_kernel_add_entries(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[Dict[str, Any]]:
        """Retorna entradas Kernel Add"""
        entries = []
        kexts = self._get_recommended_kexts(hardware, mode)
        
        for kext in kexts:
            entries.append({
                "Arch": "Any",
                "BundlePath": f"{kext}.kext",
                "Enabled": True,
                "ExecutablePath": "Contents/MacOS/" + kext,
                "MinKernel": "",
                "MaxKernel": "",
                "Comment": f"{kext} - Auto-generated",
                "PlistPath": "Contents/Info.plist",
            })
        
        return entries
    
    def _get_kernel_quirks(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> Dict[str, bool]:
        """Retorna quirks de kernel"""
        return {
            "AppleCpuPmCfgLock": False,
            "AppleXcpmCfgLock": False,
            "AppleXcpmExtraMsrs": False,
            "AppleXcpmForceBoost": False,
            "CustomSMBIOSGuid": False,
            "DisableIoMapper": False,
            "DisableLinkeditJettison": True,
            "DisableRtcChecksum": False,
            "ExtendBTFeatureFlags": False,
            "ExternalDiskIcons": True,
            "ForceSecureBootScheme": False,
            "IncreasePciBarSize": False,
            "LapicKernelPanic": False,
            "LegacyCommpage": False,
            "PanicNoKextDump": True,
            "PowerTimeoutKernelPanic": True,
            "SetApfsTrimTimeout": 0,
            "ThirdPartyDrives": True,
            "XhciPortLimit": mode != GenerationMode.CONSERVATIVE,
        }
    
    def _get_uefi_drivers(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> List[str]:
        """Retorna lista de drivers UEFI"""
        return self._get_recommended_drivers(hardware, mode)
    
    def _get_uefi_quirks(
        self,
        hardware: HardwareInfo,
        mode: GenerationMode,
    ) -> Dict[str, bool]:
        """Retorna quirks UEFI"""
        return {
            "AvoidHighAlloc": False,
            "DisableSecurityPolicy": False,
            "EnableAudioSupport": False,
            "ExitBootServicesDelay": 0,
            "IgnoreInvalidFlexRatio": False,
            "ReleaseUsbOwnership": True,
            "RequestBootVarRouting": True,
            "TscSyncTimeout": 0,
            "UnblockFsConnect": False,
        }
    
    def _generate_mlb(self) -> str:
        """Gera MLB (Main Logic Board)"""
        import random
        import string
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=17))
    
    def _generate_rom(self) -> str:
        """Gera ROM"""
        import random
        return "".join([f"{random.randint(0, 255):02X}" for _ in range(6)])
    
    def _generate_serial(self, prefix: str = "C02") -> str:
        """Gera número de série"""
        import random
        import string
        if prefix:
            return prefix + "".join(random.choices(string.ascii_uppercase + string.digits, k=9))
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    
    def _generate_uuid(self) -> str:
        """Gera UUID"""
        import uuid
        return str(uuid.uuid4()).upper()

