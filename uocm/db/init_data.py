"""
Inicialização do banco de dados com dados iniciais
"""

from uocm.db.database import get_database
from uocm.db.models import SMBIOSProfile, HardwareProfile, KextInfo, SSDTTemplate


def init_database() -> None:
    """Inicializa banco de dados com dados iniciais"""
    db = get_database()
    session = db.get_session()
    
    try:
        # Perfis SMBIOS comuns
        smbios_profiles = [
            SMBIOSProfile(
                name="MacBookPro15,1",
                product_name="MacBookPro15,1",
                serial_number_prefix="C02",
                description="MacBook Pro 15\" 2018-2019 (Coffee Lake)",
                recommended_cpu="Intel Core i7/i9 8th/9th Gen",
                recommended_ram_min=16,
            ),
            SMBIOSProfile(
                name="MacBookPro15,2",
                product_name="MacBookPro15,2",
                serial_number_prefix="C02",
                description="MacBook Pro 13\" 2018-2019 (Coffee Lake)",
                recommended_cpu="Intel Core i5/i7 8th Gen",
                recommended_ram_min=8,
            ),
            SMBIOSProfile(
                name="iMac20,1",
                product_name="iMac20,1",
                serial_number_prefix="C02",
                description="iMac 27\" 2020 (Comet Lake)",
                recommended_cpu="Intel Core i5/i7/i9 10th Gen",
                recommended_ram_min=8,
            ),
            SMBIOSProfile(
                name="iMacPro1,1",
                product_name="iMacPro1,1",
                serial_number_prefix="C02",
                description="iMac Pro 2017 (Xeon)",
                recommended_cpu="Intel Xeon",
                recommended_ram_min=32,
            ),
            SMBIOSProfile(
                name="Mac14,2",
                product_name="Mac14,2",
                serial_number_prefix="C02",
                description="Mac Studio 2022 (M1 Ultra)",
                recommended_cpu="Apple Silicon / Intel 12th+ Gen",
                recommended_ram_min=16,
            ),
        ]
        
        for profile in smbios_profiles:
            existing = session.query(SMBIOSProfile).filter(
                SMBIOSProfile.name == profile.name
            ).first()
            if not existing:
                session.add(profile)
        
        # Kexts principais
        kexts = [
            KextInfo(
                name="Lilu",
                display_name="Lilu",
                version="1.6.0",
                author="Acidanthera",
                github_repo="acidanthera/Lilu",
                description="Kext patcher base necessário para muitos outros kexts",
                required=True,
                category="System",
            ),
            KextInfo(
                name="VirtualSMC",
                display_name="VirtualSMC",
                version="1.3.0",
                author="Acidanthera",
                github_repo="acidanthera/VirtualSMC",
                description="Emulador SMC para Hackintosh",
                required=True,
                category="System",
            ),
            KextInfo(
                name="WhateverGreen",
                display_name="WhateverGreen",
                version="1.6.0",
                author="Acidanthera",
                github_repo="acidanthera/WhateverGreen",
                description="Driver unificado para GPUs",
                required=True,
                category="Graphics",
            ),
            KextInfo(
                name="AppleALC",
                display_name="AppleALC",
                version="1.8.0",
                author="Acidanthera",
                github_repo="acidanthera/AppleALC",
                description="Driver de áudio",
                required=False,
                category="Audio",
            ),
            KextInfo(
                name="AirportItlwm",
                display_name="AirportItlwm",
                version="2.3.0",
                author="OpenIntelWireless",
                github_repo="OpenIntelWireless/itlwm",
                description="Driver Wi-Fi para Intel",
                required=False,
                category="Network",
            ),
            KextInfo(
                name="AirportBrcmFixup",
                display_name="AirportBrcmFixup",
                version="2.1.0",
                author="Acidanthera",
                github_repo="acidanthera/AirportBrcmFixup",
                description="Fix para chips Broadcom Wi-Fi/Bluetooth",
                required=False,
                category="Network",
            ),
            KextInfo(
                name="CPUFriend",
                display_name="CPUFriend",
                version="1.2.0",
                author="Acidanthera",
                github_repo="acidanthera/CPUFriend",
                description="Gerenciamento de energia da CPU",
                required=False,
                category="Power",
            ),
        ]
        
        for kext in kexts:
            existing = session.query(KextInfo).filter(
                KextInfo.name == kext.name
            ).first()
            if not existing:
                session.add(kext)
        
        # Templates SSDT
        ssdt_templates = [
            SSDTTemplate(
                name="SSDT-PLUG",
                display_name="SSDT-PLUG",
                description="Habilita gerenciamento de energia nativo (XCPM)",
                category="CPU",
                required_kexts=["Lilu", "CPUFriend"],
                source_url="https://dortania.github.io/Getting-Started-With-ACPI/",
            ),
            SSDTTemplate(
                name="SSDT-PMC",
                display_name="SSDT-PMC",
                description="Habilita NVRAM nativo (300-series)",
                category="System",
                compatible_hardware=["Coffee Lake"],
                source_url="https://dortania.github.io/Getting-Started-With-ACPI/",
            ),
            SSDTTemplate(
                name="SSDT-USB-Reset",
                display_name="SSDT-USB-Reset",
                description="Reset USB para sistemas 300-series",
                category="USB",
                source_url="https://dortania.github.io/OpenCore-Post-Install/usb/",
            ),
        ]
        
        for template in ssdt_templates:
            existing = session.query(SSDTTemplate).filter(
                SSDTTemplate.name == template.name
            ).first()
            if not existing:
                session.add(template)
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    init_database()
    print("Banco de dados inicializado com dados iniciais!")

