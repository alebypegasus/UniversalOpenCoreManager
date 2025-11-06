# UOCM - Universal OpenCore Manager

**Gerador e gerenciador avançado de EFI para Hackintosh**

UOCM é uma aplicação desktop moderna que unifica e ultrapassa ferramentas como OC Auxiliary Tools, OpenCore Simplify e Hackintool. O aplicativo faz tudo automaticamente: detecta hardware, gera EFIs, gerencia kexts/SSDTs/ACPI, valida, depura e exporta EFIs com uma interface gráfica elegante estilo Liquid Glass do macOS Tahoe.

## ✨ Características

- 🎯 **Detecção Automática de Hardware**: Detecta CPU, GPU, chipset, Wi-Fi/Bluetooth e áudio automaticamente (macOS)
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
- 🌍 **Multilíngue**: Suporte a PT-BR e EN (inglês) com detecção automática de idioma
- 🖥️ **Multiplataforma**: Funciona no macOS e Windows (detecção de hardware apenas no macOS)

## 📋 Requisitos

### macOS
- macOS 11.0+ (Big Sur ou superior)
- Python 3.11+
- Xcode Command Line Tools

### Windows
- Windows 10/11
- Python 3.11+
- Visual C++ Redistributable (para PyQt6)

## 🚀 Instalação

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

### Instalação via pip

```bash
pip install uocm
uocm
```

## 🔨 Build e Compilação

### Testar e Build

Execute o script de teste e build:

```bash
# macOS/Linux
chmod +x scripts/test_build.sh
./scripts/test_build.sh --build

# Windows
scripts\test_build.bat
```

### Build para macOS (.app)

```bash
chmod +x scripts/build_mac.sh
./scripts/build_mac.sh
```

O .app será criado em `dist/UOCM.app`.

### Build para Windows (.exe)

```batch
scripts\build_windows.bat
```

O .exe será criado em `dist/UOCM.exe`.

### Code Signing e Notarization (macOS)

Para assinar e notarizar a aplicação:

```bash
chmod +x scripts/sign_and_notarize.sh
./scripts/sign_and_notarize.sh dist/UOCM.app "Developer ID Application: Your Name (TEAM_ID)"
```

**Nota**: Você precisará de:
- Apple Developer Account
- Certificado de Developer ID Application
- App-specific password para notarization

## 📖 Uso

### Detecção de Hardware (macOS apenas)

1. Abra a aplicação
2. Navegue para a aba **Detector**
3. Clique em **Detectar Hardware**
4. Aguarde a detecção automática do sistema

### Geração de EFI

1. Após detectar o hardware, vá para a aba **Gerador EFI**
2. Selecione o modo de geração:
   - **Conservador**: Mais seguro, menos features
   - **Padrão**: Balanceado (recomendado)
   - **Agressivo**: Mais features, pode ser menos estável
3. Clique em **Gerar EFI**
4. O EFI será gerado automaticamente com todas as configurações necessárias

### Gerenciamento de Kexts

1. Navegue para **Gerenciador de Kexts**
2. Clique em **Atualizar Catálogo** para buscar kexts do GitHub
3. Selecione os kexts desejados e clique em **Download**
4. Os kexts serão baixados e instalados automaticamente

### Edição de config.plist

1. Abra um EFI existente ou gere um novo
2. Navegue para **Editor PLIST**
3. Edite as configurações visualmente
4. A validação acontece em tempo real
5. Use **Undo/Redo** para desfazer alterações
6. Use **OC Snapshot** para atualizar automaticamente ACPI, Kexts, Drivers e Tools

## 🌍 Idioma / Language

O UOCM suporta múltiplos idiomas:

- **Português (Brasil)** - Padrão
- **English (US)** - Automático se sistema estiver em inglês

Para alterar o idioma, edite as configurações ou aguarde a detecção automática baseada no idioma do sistema.

## 🏗️ Arquitetura

O projeto segue uma arquitetura MVVM (Model-View-ViewModel) com separação clara de responsabilidades:

```
uocm/
├── core/           # Configurações e componentes fundamentais
│   ├── i18n.py    # Sistema de internacionalização
│   └── platform.py # Utilitários de plataforma
├── db/             # Modelos e gerenciamento de banco de dados
├── detector/       # Detecção de hardware (macOS)
├── engine_generator/  # Geração automática de EFI
├── plist_editor/   # Editor visual de config.plist
├── kext_manager/   # Gerenciamento de kexts
├── acpi_manager/   # Gerenciamento de SSDTs/ACPI
├── debugger/       # Debug e validação
├── ui/             # Interface gráfica
└── plugins/        # Sistema de plugins
```

## 🔌 Plugins

UOCM suporta plugins para extensibilidade. Veja o exemplo em `plugins/example_plugin/`.

Para criar um plugin:

1. Crie uma pasta em `plugins/`
2. Crie um `manifest.json` com as informações do plugin
3. Implemente uma classe que herda de `BasePlugin` ou suas subclasses
4. O plugin será carregado automaticamente

## 🧪 Testes

Execute os testes com pytest:

```bash
pytest tests/ -v
```

Ou use o script de teste completo:

```bash
./scripts/test_build.sh
```

## 📚 Referências

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

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Disclaimer

Este software é fornecido "como está", sem garantias. Use por sua conta e risco. Os desenvolvedores não se responsabilizam por danos causados pelo uso deste software.

## 👨‍💻 Desenvolvido por

**Mestre EFI** - Desenvolvedor especializado em Hackintosh, EFI e OpenCore

---

**Versão**: 1.0.0  
**Última atualização**: 2024  
**Plataformas**: macOS, Windows
