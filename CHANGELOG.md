# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2024-12-XX

### Adicionado
- Detecção automática de hardware (CPU, GPU, chipset, Wi-Fi/Bluetooth, áudio) - macOS
- Gerador automático de EFI com modos Conservador/Padrão/Agressivo
- Editor visual de config.plist completo inspirado no ProperTree:
  - Drag & Drop para reordenar itens
  - Copy/Paste
  - Find/Replace
  - Undo/Redo completo
  - Menu contextual com templates OpenCore
  - OC Snapshot e OC Clean Snapshot
  - Conversor de valores (Base64, Hex, ASCII, Decimal)
  - Validação em tempo real
- Gerenciador de kexts com integração GitHub
- Gerenciador de SSDTs/ACPI com templates
- Sistema de debug e validação de EFI
- Banco de dados SQLite com perfis SMBIOS e heurísticas
- Sistema de plugins extensível
- Interface gráfica estilo Liquid Glass (macOS Tahoe)
- **Sistema de internacionalização (i18n)** com suporte a PT-BR e EN
- **Suporte multiplataforma**: macOS e Windows
- **Detecção automática de idioma** baseada no sistema
- Scripts de build para macOS (.app bundle) e Windows (.exe)
- Scripts de code signing e notarization (macOS)
- Testes unitários com pytest
- CI/CD com GitHub Actions
- Documentação completa

### Características Técnicas
- Python 3.11+
- PyQt6 para interface gráfica
- SQLAlchemy para banco de dados
- Integração com GitHub API para kexts
- Validação de PLIST com JSON Schema
- Arquitetura MVVM
- Suporte a plugins com entry points

### Documentação
- README completo com instruções de instalação e uso
- Exemplo de plugin funcional
- Scripts de setup e build automatizados

## [Unreleased]

### Planejado
- Editor QML completo com efeitos Liquid Glass
- Suporte a QML para animações fluidas
- Comparador visual de EFIs
- Exportador para .dmg e .pkg
- Suporte a mais perfis de hardware
- Atualização automática do catálogo de kexts
- Telemetria opt-in
- Suporte a mais idiomas (ES, FR, DE, etc.)
- Suporte a acessibilidade avançado
- Detecção de hardware para Windows (via WMI)

