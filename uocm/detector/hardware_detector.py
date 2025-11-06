"""
Detector de hardware para macOS
"""

import subprocess
import re
import platform
from typing import Optional, Dict, Any

from uocm.detector.models import HardwareInfo, CPUInfo, GPUInfo, AudioInfo, NetworkInfo
from uocm.core.platform import Platform


class HardwareDetector:
    """Detector de hardware usando system_profiler e IORegistryExplorer"""
    
    def __init__(self):
        self.system = platform.system()
        self.can_detect = Platform.can_detect_hardware()
    
    def detect_all(self) -> HardwareInfo:
        """Detecta todas as informações de hardware"""
        if not self.can_detect:
            # Retornar informações mínimas para outras plataformas
            return HardwareInfo(
                cpu=CPUInfo(
                    model="Unknown",
                    vendor="Unknown",
                ),
                gpu=None,
                audio=None,
                network=None,
                chipset=None,
                motherboard=None,
                ram_total_gb=None,
                raw_data={"platform": self.system, "detection_available": False},
            )
        
        cpu = self._detect_cpu()
        gpu = self._detect_gpu()
        audio = self._detect_audio()
        network = self._detect_network()
        chipset = self._detect_chipset()
        motherboard = self._detect_motherboard()
        ram = self._detect_ram()
        
        raw_data = {
            "cpu": self._get_system_profiler("SPHardwareDataType"),
            "gpu": self._get_system_profiler("SPDisplaysDataType"),
            "audio": self._get_system_profiler("SPAudioDataType"),
            "network": self._get_system_profiler("SPNetworkDataType"),
            "usb": self._get_system_profiler("SPUSBDataType"),
        }
        
        return HardwareInfo(
            cpu=cpu,
            gpu=gpu,
            audio=audio,
            network=network,
            chipset=chipset,
            motherboard=motherboard,
            ram_total_gb=ram,
            raw_data=raw_data,
        )
    
    def _detect_cpu(self) -> CPUInfo:
        """Detecta informações da CPU"""
        try:
            if not self.can_detect:
                return CPUInfo(model="Unknown", vendor="Unknown")
            
            output = self._get_system_profiler("SPHardwareDataType")
            
            cpu_name = output.get("cpu_type", "Unknown")
            cpu_cores = output.get("number_of_cores", 0)
            cpu_threads = output.get("number_of_processors", 1) * cpu_cores
            
            # Determinar vendor
            vendor = "Intel"
            if "AMD" in cpu_name or "Ryzen" in cpu_name:
                vendor = "AMD"
            
            # Detectar microarquitetura Intel
            microarchitecture = None
            if vendor == "Intel":
                if "Core i" in cpu_name:
                    # Tentar detectar geração
                    if "8th" in cpu_name or re.search(r"i[357]-8\d{3}", cpu_name):
                        microarchitecture = "Coffee Lake"
                    elif "9th" in cpu_name or re.search(r"i[357]-9\d{3}", cpu_name):
                        microarchitecture = "Coffee Lake"
                    elif "10th" in cpu_name or re.search(r"i[357]-10\d{3}", cpu_name):
                        microarchitecture = "Comet Lake"
                    elif "11th" in cpu_name or re.search(r"i[357]-11\d{3}", cpu_name):
                        microarchitecture = "Tiger Lake"
                    elif "12th" in cpu_name or re.search(r"i[357]-12\d{3}", cpu_name):
                        microarchitecture = "Alder Lake"
                    elif "13th" in cpu_name or re.search(r"i[357]-13\d{3}", cpu_name):
                        microarchitecture = "Raptor Lake"
            
            return CPUInfo(
                model=cpu_name,
                vendor=vendor,
                cores=cpu_cores,
                threads=cpu_threads,
                microarchitecture=microarchitecture,
            )
        except Exception as e:
            return CPUInfo(model="Unknown", vendor="Intel")
    
    def _detect_gpu(self) -> Optional[GPUInfo]:
        """Detecta informações da GPU"""
        try:
            if not self.can_detect:
                return None
            
            output = self._get_system_profiler("SPDisplaysDataType")
            
            if not output or "displays" not in output:
                return None
            
            displays = output["displays"]
            if not displays:
                return None
            
            # Pegar primeira GPU
            gpu_data = displays[0] if isinstance(displays, list) else displays
            
            gpu_name = gpu_data.get("_name", "Unknown")
            vram = gpu_data.get("spdisplays_vram", 0)
            
            # Determinar vendor
            vendor = "Unknown"
            if "Intel" in gpu_name or "Iris" in gpu_name:
                vendor = "Intel"
            elif "AMD" in gpu_name or "Radeon" in gpu_name:
                vendor = "AMD"
            elif "NVIDIA" in gpu_name or "GeForce" in gpu_name:
                vendor = "NVIDIA"
            
            return GPUInfo(
                model=gpu_name,
                vendor=vendor,
                vram=vram,
            )
        except Exception:
            return None
    
    def _detect_audio(self) -> Optional[AudioInfo]:
        """Detecta informações de áudio"""
        try:
            if not self.can_detect:
                return None
            
            output = self._get_system_profiler("SPAudioDataType")
            # Parsing simplificado - melhorar com IORegistry
            return AudioInfo()
        except Exception:
            return None
    
    def _detect_network(self) -> Optional[NetworkInfo]:
        """Detecta informações de rede"""
        try:
            if not self.can_detect:
                return None
            
            output = self._get_system_profiler("SPNetworkDataType")
            
            wifi_model = None
            bluetooth_model = None
            
            if "interfaces" in output:
                interfaces = output["interfaces"]
                for interface in interfaces:
                    name = interface.get("_name", "")
                    if "Wi-Fi" in name or "AirPort" in name:
                        wifi_model = interface.get("spnetwork_hardware", "Unknown")
                    elif "Bluetooth" in name:
                        bluetooth_model = interface.get("spnetwork_hardware", "Unknown")
            
            return NetworkInfo(
                wifi_model=wifi_model,
                bluetooth_model=bluetooth_model,
            )
        except Exception:
            return None
    
    def _detect_chipset(self) -> Optional[str]:
        """Detecta o chipset"""
        try:
            if not self.can_detect:
                return None
            
            # Tentar detectar via IORegistry
            result = subprocess.run(
                ["ioreg", "-l", "-w0"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            
            # Parsing simplificado - melhorar
            return None
        except Exception:
            return None
    
    def _detect_motherboard(self) -> Optional[str]:
        """Detecta informações da placa-mãe"""
        try:
            if not self.can_detect:
                return None
            
            output = self._get_system_profiler("SPHardwareDataType")
            return output.get("model_identifier", None)
        except Exception:
            return None
    
    def _detect_ram(self) -> Optional[int]:
        """Detecta quantidade de RAM total em GB"""
        try:
            if not self.can_detect:
                return None
            
            output = self._get_system_profiler("SPHardwareDataType")
            ram_str = output.get("physical_memory", "0 GB")
            # Extrair número
            match = re.search(r"(\d+)", ram_str)
            if match:
                return int(match.group(1))
        except Exception:
            pass
        return None
    
    def _get_system_profiler(self, data_type: str) -> Dict[str, Any]:
        """Executa system_profiler e retorna dados parseados"""
        try:
            if not self.can_detect:
                return {}
            
            result = subprocess.run(
                ["system_profiler", "-xml", data_type],
                capture_output=True,
                text=True,
                timeout=10,
            )
            
            if result.returncode != 0:
                return {}
            
            # Parse XML simplificado - usar plistlib para parsing completo
            import plistlib
            data = plistlib.loads(result.stdout.encode())
            
            if data and len(data) > 0:
                return self._parse_sp_xml(data[0])
            
            return {}
        except Exception as e:
            return {}
    
    def _parse_sp_xml(self, node: Any) -> Dict[str, Any]:
        """Parse recursivo de nó do system_profiler"""
        result = {}
        
        if isinstance(node, dict):
            if "_items" in node:
                # Array de items
                items = node["_items"]
                if isinstance(items, list) and len(items) > 0:
                    # Se tem apenas um item, retornar ele diretamente
                    if len(items) == 1:
                        return self._parse_sp_xml(items[0])
                    else:
                        return {"items": [self._parse_sp_xml(item) for item in items]}
            
            # Copiar outras chaves
            for key, value in node.items():
                if key != "_items":
                    if isinstance(value, (dict, list)):
                        result[key] = self._parse_sp_xml(value)
                    else:
                        result[key] = value
        
        elif isinstance(node, list):
            return [self._parse_sp_xml(item) for item in node]
        
        return result
