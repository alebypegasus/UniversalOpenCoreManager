# UOCM - Universal OpenCore Manager

**Advanced EFI Generator and Manager for Hackintosh**

UOCM is a modern desktop application that unifies and surpasses tools like OC Auxiliary Tools, OpenCore Simplify, and Hackintool. The application automatically detects hardware, generates EFIs, manages kexts/SSDTs/ACPI, validates, debugs, and exports EFIs with an elegant Liquid Glass-style interface inspired by macOS Tahoe.

---

## 🇧🇷 Português

**Gerador e Gerenciador Avançado de EFI para Hackintosh**

UOCM é uma aplicação desktop moderna que unifica e ultrapassa ferramentas como OC Auxiliary Tools, OpenCore Simplify e Hackintool. O aplicativo detecta hardware automaticamente, gera EFIs, gerencia kexts/SSDTs/ACPI, valida, depura e exporta EFIs com uma interface elegante estilo Liquid Glass inspirada no macOS Tahoe.

---

## ✨ Features / Características

- 🎯 **Automatic Hardware Detection**: Detects CPU, GPU, chipset, Wi-Fi/Bluetooth, and audio automatically (macOS only)
- ⚡ **Automatic EFI Generation**: Generates complete EFI structures with one click (Conservative/Standard/Aggressive modes)
- 📝 **Visual config.plist Editor**: Complete tree editor inspired by ProperTree with drag & drop, copy/paste, find/replace, OC Snapshot, value converter, and real-time validation
- 📦 **Kext Manager**: Catalog with versions, checksums, download, update, and duplicate verification
- 🔧 **SSDT/ACPI Builder**: Templates and SSDT generation with iasl integration
- 🐛 **Debug and Validation**: Validates schema, detects duplicates, missing drivers, and incompatible versions
- 📊 **Comparator and Versioning**: Visual diff between EFIs, snapshots, and rollback
- 📤 **Exporter/Installer**: Exports .zip, creates .dmg and .pkg with automatic backup
- 🗄️ **Robust Database**: SQLite with SMBIOS profiles, heuristics, and hardware mappings
- 🔌 **Plugin System**: Extensible API to add heuristics, templates, and validators
- 🎨 **Liquid Glass Interface**: Modern visual inspired by macOS Tahoe with blur and translucency
- 🌍 **Multilingual**: Supports PT-BR and EN (US) with automatic language detection
- 🖥️ **Cross-platform**: Works on macOS and Windows (hardware detection macOS only)

- 🎯 **Detecção Automática de Hardware**: Detecta CPU, GPU, chipset, Wi-Fi/Bluetooth e áudio automaticamente (apenas macOS)
- ⚡ **Geração Automática de EFI**: Gera estruturas EFI completas com um clique (modos Conservador/Padrão/Agressivo)
- 📝 **Editor Visual de config.plist**: Editor árvore completo inspirado no ProperTree com drag & drop, copy/paste, find/replace, OC Snapshot, conversor de valores e validação em tempo real
- 📦 **Gerenciador de Kexts**: Catálogo com versões, checksums, download, atualização e verificação de duplicações
- 🔧 **Builder SSDT/ACPI**: Templates e geração de SSDTs com integração iasl
- 🐛 **Debug e Validação**: Valida schema, detecta duplicações, drivers faltando e versões incompatíveis
- 📊 **Comparador e Versionamento**: Diff visual entre EFIs, snapshots e reversão
- 📤 **Exportador/Instalador**: Exporta .zip, cria .dmg e .pkg com backup automático
- 🗄️ **Banco de Dados Robusto**: SQLite com perfis SMBIOS, heurísticas e mapeamentos de hardware
- 🔌 **Sistema de Plugins**: API extensível para adicionar heurísticas, templates e validadores
- 🎨 **Interface Liquid Glass**: Visual moderno inspirado no macOS Tahoe com blur e translucência
- 🌍 **Multilíngue**: Suporte a PT-BR e EN (US) com detecção automática de idioma
- 🖥️ **Multiplataforma**: Funciona no macOS e Windows (detecção de hardware apenas macOS)

## 📋 Requirements / Requisitos

### macOS
- macOS 11.0+ (Big Sur or higher)
- Python 3.11+
- Xcode Command Line Tools

- macOS 11.0+ (Big Sur ou superior)
- Python 3.11+
- Xcode Command Line Tools

### Windows
- Windows 10/11
- Python 3.11+
- Visual C++ Redistributable (for PyQt6)

- Windows 10/11
- Python 3.11+
- Visual C++ Redistributable (para PyQt6)

## 🚀 Installation / Instalação

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/seu-usuario/uocm.git
cd uocm
```

2. Run the setup script:
```bash
# macOS/Linux
chmod +x scripts/setup.sh
./scripts/setup.sh --dev

# Windows
scripts\setup.bat
```

3. Activate the virtual environment:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Run the application:
```bash
python -m uocm.main
```

### Setup de Desenvolvimento

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/uocm.git
cd uocm
```

2. Execute o script de setup:
```bash
# macOS/Linux
chmod +x scripts/setup.sh
./scripts/setup.sh --dev

# Windows
scripts\setup.bat
```

3. Ative o ambiente virtual:
```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. Execute a aplicação:
```bash
python -m uocm.main
```

### Installation via pip

```bash
pip install uocm
uocm
```

## 🔨 Build and Compilation

### Test and Build

Run the test and build script:

```bash
# macOS/Linux
chmod +x scripts/test_build.sh
./scripts/test_build.sh --build

# Windows
scripts\test_build.bat
```

### Build for macOS (.app)

```bash
chmod +x scripts/build_mac_pyinstaller.sh
./scripts/build_mac_pyinstaller.sh
```

The .app will be created in `dist/UOCM.app`.

### Build for Windows (.exe)

```batch
scripts\build_windows.bat
```

The .exe will be created in `dist/UOCM.exe`.

## 📖 Usage / Uso

### Hardware Detection (macOS only)

1. Open the application
2. Navigate to the **Detector** tab
3. Click **Detect Hardware**
4. Wait for automatic system detection

### Detecção de Hardware (apenas macOS)

1. Abra a aplicação
2. Navegue para a aba **Detector**
3. Clique em **Detectar Hardware**
4. Aguarde a detecção automática do sistema

### EFI Generation

1. After detecting hardware, go to the **EFI Generator** tab
2. Select the generation mode:
   - **Conservative**: Safer, fewer features
   - **Standard**: Balanced (recommended)
   - **Aggressive**: More features, may be less stable
3. Click **Generate EFI**
4. The EFI will be automatically generated with all necessary configurations

### Geração de EFI

1. Após detectar o hardware, vá para a aba **Gerador EFI**
2. Selecione o modo de geração:
   - **Conservador**: Mais seguro, menos features
   - **Padrão**: Balanceado (recomendado)
   - **Agressivo**: Mais features, pode ser menos estável
3. Clique em **Gerar EFI**
4. O EFI será gerado automaticamente com todas as configurações necessárias

## 🌍 Language / Idioma

UOCM supports multiple languages:

- **English (US)** - Default / Padrão
- **Portuguese (Brazil)** - Português (Brasil)

The language is automatically detected based on your system settings. The app interface will match your system language.

O idioma é detectado automaticamente com base nas configurações do seu sistema. A interface do app corresponderá ao idioma do seu sistema.

## 🏗️ Architecture

The project follows an MVVM (Model-View-ViewModel) architecture with clear separation of responsibilities:

O projeto segue uma arquitetura MVVM (Model-View-ViewModel) com separação clara de responsabilidades:

```
uocm/
├── core/           # Core configurations and fundamental components
├── db/             # Database models and management
├── detector/       # Hardware detection (macOS)
├── engine_generator/  # Automatic EFI generation
├── plist_editor/   # Visual config.plist editor
├── kext_manager/   # Kext management
├── acpi_manager/   # SSDT/ACPI management
├── debugger/       # Debug and validation
├── ui/             # Graphical interface
└── plugins/        # Plugin system
```

## 📚 References / Referências

UOCM is based on and cites the following sources:

UOCM baseia-se e cita as seguintes fontes:

- [Dortania OpenCore Install Guide](https://dortania.github.io/OpenCore-Install-Guide/)
- [Getting-Started-With-ACPI](https://dortania.github.io/Getting-Started-With-ACPI/)
- [OpenCore Post-Install](https://dortania.github.io/OpenCore-Post-Install/)
- [OC-Little-Translated](https://github.com/5T33Z0/OC-Little-Translated)
- [Acidanthera](https://github.com/acidanthera)
- [OC Auxiliary Tools](https://github.com/ic005k/OCAuxiliaryTools)
- [OpenCore Simplify](https://github.com/lzhoang2801/OpCore-Simplify)
- [ProperTree](https://github.com/corpnewt/ProperTree)
- [Hackintool](https://github.com/headkaze/Hackintool)
- [VoodooI2C](https://voodooi2c.github.io/)
- [ChefKiss](https://chefkiss.dev/guides/hackintosh/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Faça push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Disclaimer

This software is provided "as is", without warranties. Use at your own risk. The developers are not responsible for damages caused by the use of this software.

Este software é fornecido "como está", sem garantias. Use por sua conta e risco. Os desenvolvedores não se responsabilizam por danos causados pelo uso deste software.

## 👨‍💻 Developed by / Desenvolvido por

**Mestre EFI** - Developer specialized in Hackintosh, EFI, and OpenCore

**Mestre EFI** - Desenvolvedor especializado em Hackintosh, EFI e OpenCore

## 📬 Contact & Feedback / Contato e Feedback

Stay connected with me on these platforms and follow my Hackintosh journey!

Mantenha-se conectado comigo nessas plataformas e siga minha jornada Hackintosh!

<table style="width:100%; margin-top: 20px;">
    <thead>
        <tr style="background-color: #f5f5f7;">
            <th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Platform / Plataforma</th>
            <th style="padding: 12px; text-align: left; border-bottom: 1px solid #ddd;">Link</th>
        </tr>
    </thead>
    <tbody>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">Facebook</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://facebook.com/alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">Instagram</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://instagram.com/alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">X (Twitter)</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://x.com/alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">LinkedIn</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://linkedin.com/in/alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">TikTok</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://tiktok.com/@alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">Reddit</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://reddit.com/u/alebypegasus">alebypegasus</a></td></tr>
        <tr><td style="padding: 12px; border-bottom: 1px solid #ddd;">Telegram</td><td style="padding: 12px; border-bottom: 1px solid #ddd;"><a href="https://telegram.me/alebypegasus">alebypegasus</a></td></tr>
    </tbody>
</table>

---

**Version**: 0.1.0  
**Last update**: 2025  
**Platforms**: macOS, Windows
