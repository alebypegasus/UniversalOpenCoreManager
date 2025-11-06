"""
Testes do módulo de detecção de hardware
"""

import pytest
from uocm.detector.models import HardwareInfo, CPUInfo


def test_cpu_info():
    """Testa criação de CPUInfo"""
    cpu = CPUInfo(
        model="Intel Core i7-8700K",
        vendor="Intel",
        cores=6,
        threads=12,
    )
    
    assert cpu.model == "Intel Core i7-8700K"
    assert cpu.vendor == "Intel"
    assert cpu.cores == 6
    assert cpu.threads == 12


def test_hardware_info():
    """Testa criação de HardwareInfo"""
    cpu = CPUInfo(model="Test CPU", vendor="Intel")
    hardware = HardwareInfo(cpu=cpu)
    
    assert hardware.cpu.model == "Test CPU"
    assert hardware.gpu is None


@pytest.mark.skipif(
    pytest.importorskip("platform").system() != "Darwin",
    reason="Detecção de hardware só funciona no macOS"
)
def test_hardware_detection():
    """Testa detecção de hardware"""
    from uocm.detector import HardwareDetector
    
    detector = HardwareDetector()
    hardware = detector.detect_all()
    
    assert hardware is not None
    assert hardware.cpu is not None
    assert hardware.cpu.model is not None

