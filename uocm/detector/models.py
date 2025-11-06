"""
Modelos de dados para informações de hardware
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class CPUInfo:
    """Informações sobre a CPU"""
    model: str
    vendor: str  # Intel, AMD
    cores: Optional[int] = None
    threads: Optional[int] = None
    frequency: Optional[float] = None
    microarchitecture: Optional[str] = None  # Coffee Lake, Skylake, etc.


@dataclass
class GPUInfo:
    """Informações sobre a GPU"""
    model: str
    vendor: str  # Intel, AMD, NVIDIA
    vram: Optional[int] = None  # VRAM em MB
    device_id: Optional[str] = None
    vendor_id: Optional[str] = None


@dataclass
class AudioInfo:
    """Informações sobre áudio"""
    codec: Optional[str] = None
    vendor_id: Optional[str] = None
    device_id: Optional[str] = None
    layout_id: Optional[int] = None


@dataclass
class NetworkInfo:
    """Informações sobre rede"""
    wifi_model: Optional[str] = None
    wifi_vendor: Optional[str] = None
    bluetooth_model: Optional[str] = None
    bluetooth_vendor: Optional[str] = None
    ethernet_model: Optional[str] = None


@dataclass
class HardwareInfo:
    """Informações completas de hardware detectado"""
    cpu: CPUInfo
    gpu: Optional[GPUInfo] = None
    audio: Optional[AudioInfo] = None
    network: Optional[NetworkInfo] = None
    chipset: Optional[str] = None
    motherboard: Optional[str] = None
    ram_total_gb: Optional[int] = None
    storage: Optional[List[Dict[str, Any]]] = None
    raw_data: Optional[Dict[str, Any]] = None  # Dados brutos do sistema

