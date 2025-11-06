"""
Modelos SQLAlchemy para o banco de dados
"""

from datetime import datetime
from typing import Optional
from pathlib import Path

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    Float, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum


Base = declarative_base()


class SMBIOSProfile(Base):
    """Perfis SMBIOS recomendados para diferentes configurações"""
    
    __tablename__ = "smbios_profiles"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    product_name = Column(String(100), nullable=False)
    system_uuid = Column(String(100))
    board_product = Column(String(100))
    serial_number_prefix = Column(String(10))
    description = Column(Text)
    recommended_cpu = Column(String(100))  # CPU recomendado para este SMBIOS
    recommended_ram_min = Column(Integer)  # RAM mínima em GB
    features = Column(JSON)  # Features específicas (Thunderbolt, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HardwareProfile(Base):
    """Perfis de hardware detectados e suas recomendações"""
    
    __tablename__ = "hardware_profiles"
    
    id = Column(Integer, primary_key=True)
    cpu_model = Column(String(100), nullable=False)
    cpu_vendor = Column(String(50))  # Intel, AMD
    gpu_model = Column(String(100))
    gpu_vendor = Column(String(50))  # Intel, AMD, NVIDIA
    chipset = Column(String(100))
    wifi_model = Column(String(100))
    bluetooth_model = Column(String(100))
    audio_codec = Column(String(100))
    motherboard_model = Column(String(100))
    recommended_smbios_id = Column(Integer, ForeignKey("smbios_profiles.id"))
    recommended_kexts = Column(JSON)  # Lista de IDs de kexts recomendados
    recommended_ssdts = Column(JSON)  # Lista de IDs de SSDTs recomendados
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    recommended_smbios = relationship("SMBIOSProfile", foreign_keys=[recommended_smbios_id])


class KextInfo(Base):
    """Informações sobre kexts disponíveis"""
    
    __tablename__ = "kexts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200))
    version = Column(String(50))
    author = Column(String(100))
    github_repo = Column(String(200))  # Formato: owner/repo
    github_release_tag = Column(String(100))
    download_url = Column(String(500))
    checksum_sha256 = Column(String(64))
    description = Column(Text)
    required = Column(Boolean, default=False)
    category = Column(String(50))  # Audio, Network, Graphics, etc.
    compatible_macos = Column(JSON)  # Lista de versões do macOS compatíveis
    dependencies = Column(JSON)  # Lista de nomes de kexts dependentes
    conflicts = Column(JSON)  # Lista de nomes de kexts conflitantes
    local_path = Column(String(500))  # Caminho local do kext
    installed = Column(Boolean, default=False)
    installed_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SSDTTemplate(Base):
    """Templates de SSDT/ACPI"""
    
    __tablename__ = "ssdt_templates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200))
    description = Column(Text)
    template_path = Column(String(500))  # Caminho para o template
    category = Column(String(50))  # CPU, USB, Power, etc.
    required_kexts = Column(JSON)  # Lista de kexts necessários
    parameters = Column(JSON)  # Parâmetros configuráveis do template
    compatible_hardware = Column(JSON)  # Hardware compatível
    source_url = Column(String(500))  # URL de referência
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EFISnapshot(Base):
    """Snapshots de configurações EFI para versionamento"""
    
    __tablename__ = "efi_snapshots"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    efi_path = Column(String(500))  # Caminho para o EFI
    config_plist = Column(Text)  # Conteúdo do config.plist em JSON
    kexts = Column(JSON)  # Lista de kexts usados
    ssdts = Column(JSON)  # Lista de SSDTs usados
    drivers = Column(JSON)  # Lista de drivers usados
    hardware_profile_id = Column(Integer, ForeignKey("hardware_profiles.id"))
    tags = Column(JSON)  # Tags para organização
    created_at = Column(DateTime, default=datetime.utcnow)
    
    hardware_profile = relationship("HardwareProfile")


class Plugin(Base):
    """Plugins instalados"""
    
    __tablename__ = "plugins"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200))
    version = Column(String(50))
    author = Column(String(100))
    description = Column(Text)
    entry_point = Column(String(200))  # Função/classe de entrada
    plugin_path = Column(String(500))
    manifest = Column(JSON)  # Manifesto do plugin
    permissions = Column(JSON)  # Permissões solicitadas
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

