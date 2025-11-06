# 🔷 Blueprint - Universal OpenCore Manager

**Versão:** 1.0  
**Data:** 2024  
**Status:** Fase 1 (macOS Python) em desenvolvimento

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Fase 1: macOS em Python](#fase-1-macos-em-python)
3. [Fase 2: Windows em Python](#fase-2-windows-em-python)
4. [Fase 3: macOS nativo em Swift/SwiftUI](#fase-3-macos-nativo-em-swiftswiftui)
5. [Arquitetura Geral](#arquitetura-geral)
6. [Roadmap e Marcos](#roadmap-e-marcos)

---

## 🎯 Visão Geral

### Objetivo

Criar um aplicativo unificado que **automatize completamente o fluxo de criação, edição, validação e manutenção de EFIs OpenCore** para Hackintosh, com interface moderna e intuitiva, inspirado em **OC Auxiliary Tools**, **OpenCore Simplify** e **Hackintool**.

### Princípios

- **Automação total**: Detecta hardware, gera EFI, valida, atualiza — tudo automático
- **Sem modo de ensino**: Apenas popups/tooltips curtos explicando o que é cada item
- **Referências técnicas**: Todas as sugestões apontam para fontes oficiais (Dortania, Acidanthera)
- **UX moderna**: Visual "Liquid Glass" estilo macOS Tahoe (macOS 26)
- **Cross-platform**: Funciona em macOS e Windows (Python) e nativo macOS (Swift)

### Fontes Técnicas Obrigatórias

- **Dortania**: OpenCore Install Guide, ACPI Guide, Post-Install, Multiboot
- **Acidanthera**: OpenCorePkg, Lilu, WhateverGreen, VirtualSMC, AppleALC
- **VoodooI2C**: Documentação e drivers
- **OC-Little**: Traduções e patches
- **ChefKiss**: Guias Hackintosh
- **Hackintool**: Referência funcional

---

## 🔵 Fase 1: macOS em Python

### Stack Tecnológica

- **Linguagem**: Python 3.11+
- **GUI**: PyQt6 + Qt Quick (QML) para efeitos Liquid Glass
- **Backend**: asyncio/concurrent.futures para IO pesado
- **DB**: SQLite + SQLAlchemy (migrations com Alembic)
- **Rede**: httpx (assíncrono) + GitHub REST API
- **PLIST**: plistlib + validação JSON Schema
- **Empacotamento**: PyInstaller → .app (com codesign + notarização)
- **Qualidade**: ruff, black, mypy, pytest, coverage

### Arquitetura (MVVM Modular)

```
universal_oc_manager/
├── ui/
│   ├── qml/                    # Telas QML (Liquid Glass)
│   │   ├── Main.qml
│   │   ├── ValidationPanel.qml
│   │   └── EditorWindow.qml
│   ├── backend.py              # AppController (QObject → QML)
│   ├── assets/                 # Ícones, logos
│   ├── themes/                 # Temas Liquid Glass
│   └── i18n/                   # PT-BR, EN
│
├── core/
│   ├── detector/               # Detecção de hardware
│   │   └── detect.py
│   ├── engine/                 # Gerador de EFI
│   │   └── generator.py
│   ├── plist/                  # Editor/carregador plist
│   │   └── loader.py
│   ├── kexts/                  # Gestor de kexts
│   │   └── manager.py
│   ├── acpi/                   # Builder SSDT/ACPI
│   │   └── builder.py
│   ├── validator/              # Validação schema
│   │   └── schema_validator.py
│   ├── comparer/               # Comparação de EFIs
│   │   └── diff.py
│   ├── exporter/               # Export .zip/.dmg/.pkg
│   │   └── packager.py
│   └── updater/                # Atualização de DB/kexts
│       └── updater.py
│
├── infra/
│   ├── db/                     # Models, session, migrations
│   │   ├── models.py
│   │   └── session.py
│   ├── http/                   # Cliente GitHub
│   │   └── github_client.py
│   ├── logging/                # Sistema de logs
│   │   └── logger.py
│   ├── settings/               # Configurações
│   │   └── config.py
│   ├── schemas/                # Schema OpenCore
│   │   ├── schema_manager.py
│   │   └── opencore_schema.json
│   └── templates/              # Templates config.plist
│       └── config_default.plist
│
└── tests/                      # Testes pytest
    ├── test_validator.py
    └── test_generator.py
```

### Funcionalidades Detalhadas

#### 1. Detector de Hardware (`core/detector/detect.py`)

**Objetivo**: Coletar informações do hardware automaticamente

**Métodos**:
- `detect_hardware()` → `HardwareProfile`
  - CPU: tipo, família, modelo (via `system_profiler SPHardwareDataType`)
  - GPU: iGPU/dGPU (via `system_profiler SPDisplaysDataType`)
  - Chipset: modelo (via `ioreg`)
  - Wi-Fi/Bluetooth: chipset (via `system_profiler SPUSBDataType`)
  - Áudio: codec (via `ioreg`)
  - Storage: controladores (via `diskutil`)

**Heurísticas**:
- DB local com mapeamentos CPU → SMBIOS recomendado
- GPU → WhateverGreen flags necessárias
- Wi-Fi → Drivers compatíveis (AirportBrcmFixup, etc.)

**Retorno**:
```python
@dataclass
class HardwareProfile:
    cpu: str | None
    igpu: str | None
    gpu: str | None
    chipset: str | None
    wifi: str | None
    audio: str | None
    smbios_suggestion: str  # Ex: "iMac19,1"
```

#### 2. Gerador Automático de EFI (`core/engine/generator.py`)

**Objetivo**: Criar estrutura `/EFI/OC` completa e funcional

**Fluxo**:
1. Recebe `HardwareProfile`
2. Consulta DB para selecionar kexts/SSDTs compatíveis
3. Cria estrutura de pastas:
   ```
   /EFI/OC/
   ├── ACPI/
   ├── Kexts/
   ├── Drivers/
   ├── Resources/
   └── config.plist
   ```
4. Gera `config.plist` a partir de template Jinja2
5. Inclui kexts necessários (baixa se necessário)
6. Inclui SSDTs base (SSDT-PLUG, SSDT-EC, etc.)
7. Valida com schema OpenCore
8. Retorna caminho da EFI

**Modos**:
- **Conservador**: Configurações mínimas, máxima compatibilidade
- **Padrão**: Balanceado entre recursos e compatibilidade
- **Agressivo**: Máximo de recursos, requer ajustes manuais

**Templates**:
- `config_default.plist`: Template base com todas as seções
- `config_intel.plist`: Específico Intel
- `config_amd.plist`: Específico AMD

#### 3. Editor Visual de config.plist (`core/plist/loader.py` + QML)

**Objetivo**: Editar `config.plist` com interface visual e validação em tempo real

**Funcionalidades**:
- Carregar/salvar arquivo
- Editor tipo árvore (QTreeView/QML TreeView)
- Validação em tempo real (via `validate_config()`)
- Undo/Redo ilimitado
- Busca global
- Histórico de versões (snapshots)
- Tooltips explicando cada chave
- Links para documentação Dortania

**Validação**:
- Schema OpenCore (JSON Schema)
- Regras Dortania (ex: "ACPI.Add não pode ter duplicatas")
- Warnings e erros diferenciados

#### 4. Gestor de Kexts/Drivers/SSDTs (`core/kexts/manager.py`)

**Objetivo**: Download, atualização e gestão de kexts via GitHub

**Catálogo**:
- Repositórios principais:
  - Acidanthera (Lilu, WhateverGreen, VirtualSMC, AppleALC, etc.)
  - VoodooI2C
  - ChefKiss
  - Comunitários (via DB)

**Operações**:
- `list_available()`: Lista kexts disponíveis
- `download(kext_name, version)`: Baixa release específica
- `update(kext_name)`: Atualiza para versão mais recente
- `install(kext_name, efi_path)`: Instala na EFI
- `check_conflicts(kext_list)`: Detecta conflitos
- `verify_signature(kext_path)`: Verifica integridade

**Cache**:
- Armazena releases em `~/.uocm/cache/kexts/`
- Verifica atualizações periodicamente
- Mantém histórico de versões instaladas

#### 5. ACPI/SSDT Builder (`core/acpi/builder.py`)

**Objetivo**: Gerar e aplicar SSDTs/patches ACPI

**Funcionalidades**:
- Importar prebuilts (SSDT-PLUG, SSDT-EC, etc.)
- Gerar SSDTs baseados em templates:
  - SSDT-PLUG (CPU Power Management)
  - SSDT-EC (Embedded Controller)
  - SSDT-USB (USB Map)
  - SSDT-XHC (XHCI Shutdown)
- Editor visual de patches ACPI
- Integração com `iasl` (se instalado)
- Validação de sintaxe ACPI

**Templates SSDT**:
- Baseados em Dortania ACPI Guide
- Adaptáveis por hardware detectado

#### 6. Debug & Validação (`core/validator/schema_validator.py`)

**Objetivo**: Verificar EFI antes de usar

**Checagens**:
- Schema OpenCore (campos obrigatórios, tipos)
- Duplicatas (kexts, drivers, ACPI)
- Arquivos faltando (referências quebradas)
- Conflitos (kexts incompatíveis)
- Versões (kexts desatualizados)
- SMBIOS inconsistente

**Relatório**:
- JSON estruturado com erros/warnings
- PDF exportável
- Links para documentação relevante

#### 7. Comparador & Versionamento (`core/comparer/diff.py`)

**Objetivo**: Comparar EFIs e manter histórico

**Funcionalidades**:
- Snapshots: Salvar estado antes de alterações
- Diff visual: Comparar duas EFIs
  - config.plist: Diff de chaves
  - Kexts: Adicionados/removidos/atualizados
  - ACPI: Mudanças em SSDTs
- Restaurar snapshot: Reverter para versão anterior
- Changelog automático

**Armazenamento**:
- Snapshots em `~/.uocm/snapshots/`
- Metadados em DB

#### 8. Exportador/Instalador (`core/exporter/packager.py`)

**Objetivo**: Exportar EFI e criar instaladores

**Formatos**:
- `.zip`: EFI compactada
- `.dmg`: Imagem macOS (opcional)
- `.pkg`: Instalador que copia EFI para pendrive

**Funcionalidades**:
- Selecionar destino (pendrive EFI)
- Backup automático da EFI anterior
- Verificação de espaço disponível
- Confirmação antes de sobrescrever

### Base de Dados (SQLite)

**Tabelas principais**:

```sql
-- Perfis de hardware
CREATE TABLE hardware_profiles (
    id INTEGER PRIMARY KEY,
    cpu_codename TEXT,
    igpu_id TEXT,
    gpu_id TEXT,
    chipset TEXT,
    smbios_suggestion TEXT,
    notes TEXT
);

-- Catálogo de kexts
CREATE TABLE kexts (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    repo TEXT,
    latest_version TEXT,
    homepage TEXT,
    hash TEXT,
    last_checked TIMESTAMP
);

-- Compatibilidade kexts
CREATE TABLE kext_compat (
    id INTEGER PRIMARY KEY,
    kext_id INTEGER REFERENCES kexts(id),
    macos_min TEXT,
    macos_max TEXT,
    required_kexts TEXT,  -- JSON array
    conflicts TEXT,      -- JSON array
    notes TEXT
);

-- Templates SSDT
CREATE TABLE ssdt_templates (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    source_url TEXT,
    template_path TEXT
);

-- Regras de validação
CREATE TABLE validation_rules (
    id INTEGER PRIMARY KEY,
    type TEXT,  -- 'schema', 'dortania', 'custom'
    key TEXT,
    value TEXT,
    source_url TEXT,
    version_range TEXT
);

-- Histórico de ações
CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    action TEXT,
    payload_json TEXT,
    created_at TIMESTAMP
);
```

### UI/UX (QML Liquid Glass)

**Tema Visual**:
- Translucidez: `NSVisualEffectView` equivalente em QML
- Blur: `GaussianBlur` do Qt GraphicalEffects
- Cores: Dark mode com acentos dinâmicos
- Ícones: SF Symbols equivalentes (SVG)
- Animações: Suaves (0.3s easeInOut)

**Telas principais**:
1. **Dashboard**: Visão geral, status da EFI atual
2. **Detector**: Interface de detecção de hardware
3. **Gerador**: Configuração e geração de EFI
4. **Editor**: Editor visual de config.plist
5. **Kext Manager**: Catálogo e gestão de kexts
6. **ACPI Builder**: Gerador de SSDTs
7. **Debug**: Painel de validação e logs
8. **Comparador**: Diff de EFIs
9. **Exportador**: Interface de exportação

**Popups/Tooltips**:
- Explicações curtas (1-2 linhas)
- Links para documentação quando relevante
- Sem modo de ensino formal

### Integrações GitHub

**Repositórios monitorados**:
- `acidanthera/OpenCorePkg`: Releases OpenCore
- `acidanthera/Lilu`: Base kext
- `acidanthera/WhateverGreen`: GPU
- `acidanthera/VirtualSMC`: SMC
- `acidanthera/AppleALC`: Áudio
- `VoodooI2C/VoodooI2C`: Input
- Outros via DB

**APIs**:
- GitHub REST API: Releases, tags, assets
- Rate limiting: Cache local + ETag
- Fallback offline: DB local

### Build e Distribuição

**Scripts**:
- `scripts/build_mac.sh`: PyInstaller → .app
- `scripts/sign_and_notarize.sh`: Assinatura + notarização

**Processo**:
1. `pyinstaller --onefile --windowed app.py`
2. `codesign --deep --force --sign "Developer ID" app.app`
3. `xcrun notarytool submit app.app`
4. `xcrun stapler staple app.app`

**CI/CD**:
- GitHub Actions: Lint, testes, build
- Artefatos: .app assinado

---

## 🪟 Fase 2: Windows em Python

### Adaptações Necessárias

**Detector de Hardware**:
- **WMI/PowerShell**: Substituir `system_profiler` por:
  ```powershell
  Get-CimInstance Win32_Processor
  Get-CimInstance Win32_VideoController
  Get-CimInstance Win32_BaseBoard
  ```
- **PCI/USB**: `Get-PnpDevice`, `Get-CimInstance Win32_PnPEntity`
- **Armazenamento**: `Get-CimInstance Win32_DiskDrive`

**Montagem de EFI**:
- **Windows**: Não monta EFI automaticamente
- **Solução**: Exportar `.zip` + instruções para montar via `diskpart` ou utilitário externo
- **Alternativa**: Integração com Rufus/DiskImage (se permitido)

**Empacotamento**:
- **PyInstaller**: `.exe` (não `.app`)
- **MSI**: Opcional (WiX/NSIS)
- **Assinatura**: `signtool` (opcional, SmartScreen)

**Dependências Externas**:
- `iasl`: Instruir download manual (popup)
- Outros: Documentação clara

### Estrutura (mesma do macOS)

Mantém a mesma arquitetura, apenas adapta:
- `core/detector/detect.py`: Implementação Windows
- `scripts/build_windows.sh`: Build para .exe

### Testes CI

- GitHub Actions: Windows runner
- Build e smoke tests

---

## 🍎 Fase 3: macOS nativo em Swift/SwiftUI

### Stack Tecnológica

- **Linguagem**: Swift 6
- **UI**: SwiftUI (macOS 26 Tahoe)
- **Frameworks**: Combine, SwiftData/CoreData, URLSession
- **Arquitetura**: MVVM
- **Build**: Xcode 16+, Swift Package Manager

### Arquitetura Swift

```
UniversalOpenCoreManager/
├── App/
│   ├── AppDelegate.swift
│   └── ContentView.swift
│
├── Views/
│   ├── Dashboard/
│   ├── Detector/
│   ├── Generator/
│   ├── Editor/
│   ├── KextManager/
│   ├── ACBIBuilder/
│   ├── Debug/
│   ├── Comparer/
│   └── Exporter/
│
├── ViewModels/
│   └── [Equivalente aos serviços Python]
│
├── Models/
│   ├── HardwareProfile.swift
│   ├── EFIStructure.swift
│   └── Kext.swift
│
├── Services/
│   ├── HardwareDetector.swift
│   ├── EFIGenerator.swift
│   ├── ConfigValidator.swift
│   ├── GitHubClient.swift
│   └── DatabaseManager.swift
│
├── Resources/
│   ├── Assets.xcassets
│   ├── Schemas/
│   └── Templates/
│
└── Tests/
    └── [Unit tests Swift]
```

### Diferenças Principais

**Detector**:
- IOKit nativo (C/C++ interop opcional)
- SystemProfiler via Process
- IORegistry parsing Swift

**DB**:
- SwiftData (preferencial) ou CoreData
- SQLite via GRDB (alternativa)

**UI**:
- SwiftUI nativo (translucidez, blur automático)
- NSVisualEffectView materials
- Animações suaves nativas
- Menus contextuais nativos

**Rede**:
- URLSession (nativo)
- Combine para reatividade

**PLIST**:
- PropertyListSerialization
- Validação via JSONDecoder + schema

**Plugins**:
- Swift Packages (sandbox)
- Manifesto em Package.swift

### Build e Distribuição

**Xcode**:
- Assinatura automática (Developer ID)
- Notarização via Xcode Organizer
- Sparkle (atualização opcional)

**Artefatos**:
- `.app` nativo
- `.dmg` (opcional)
- App Store (futuro, se aplicável)

---

## 🏗️ Arquitetura Geral

### Princípios

1. **Separação de responsabilidades**: UI ↔ ViewModels ↔ Services
2. **Testabilidade**: Serviços puros, sem side-effects
3. **Extensibilidade**: Plugin API para novas heurísticas
4. **Manutenibilidade**: Código limpo, documentado, testado

### Padrões

- **MVVM**: UI separada da lógica
- **Repository**: Acesso a dados abstraído
- **Factory**: Criação de objetos complexos
- **Observer**: Sinais/notificações para UI

### Segurança

- **Backup automático**: Antes de alterações destrutivas
- **Validação**: Sempre validar antes de salvar
- **Permissões**: Pedir permissão antes de acessar disco
- **Assinatura**: Código assinado (macOS/Windows)

---

## 📅 Roadmap e Marcos

### Fase 1: macOS Python

**M1: Base (2-3 semanas)**
- ✅ Estrutura de pastas
- ✅ UI base (QML)
- ✅ Detector básico
- ✅ DB inicial
- ✅ Schema manager

**M2: Gerador EFI (2-3 semanas)**
- ⏳ Gerador completo
- ⏳ Templates config.plist
- ⏳ Validação schema
- ⏳ Editor básico

**M3: Gestão Kexts (2 semanas)**
- ⏳ Catálogo GitHub
- ⏳ Download/atualização
- ⏳ Instalação automática
- ⏳ Verificação de conflitos

**M4: ACPI/SSDT (2 semanas)**
- ⏳ Builder SSDT
- ⏳ Templates prebuilts
- ⏳ Editor patches
- ⏳ Integração iasl

**M5: Debug/Validação (2 semanas)**
- ⏳ Checagens automáticas
- ⏳ Relatórios
- ⏳ Logs coloridos
- ⏳ Simulação de boot

**M6: Comparador/Versionamento (2 semanas)**
- ⏳ Snapshots
- ⏳ Diff visual
- ⏳ Restauração
- ⏳ Changelog

**M7: Exportador (1-2 semanas)**
- ⏳ Export .zip/.dmg/.pkg
- ⏳ Cópia para pendrive
- ⏳ Backup automático

**M8: Plugin API (1-2 semanas)**
- ⏳ Sistema de plugins
- ⏳ Documentação
- ⏳ Exemplo funcional

**M9: Polish (1-2 semanas)**
- ⏳ Performance
- ⏳ UX refinada
- ⏳ Testes completos
- ⏳ Documentação

### Fase 2: Windows Python

**M10: Adaptação Windows (3-4 semanas)**
- ⏳ Detector Windows
- ⏳ Build .exe
- ⏳ Testes Windows
- ⏳ Documentação

### Fase 3: macOS Swift

**M11: Migração Swift (6-8 semanas)**
- ⏳ Reescrita SwiftUI
- ⏳ Integração nativa
- ⏳ Performance otimizada
- ⏳ Testes nativos

---

## 📚 Referências e Documentação

### Fontes Técnicas

- **Dortania OpenCore Install Guide**: https://dortania.github.io/OpenCore-Install-Guide/
- **Dortania ACPI Guide**: https://dortania.github.io/Getting-Started-With-ACPI/
- **OpenCore Post-Install**: https://dortania.github.io/OpenCore-Post-Install/
- **OpenCore Multiboot**: https://dortania.github.io/OpenCore-Multiboot/
- **OC-Little**: https://github.com/5T33Z0/OC-Little-Translated
- **VoodooI2C**: https://voodooi2c.github.io/
- **ChefKiss**: https://chefkiss.dev/guides/hackintosh/
- **Hackintool**: https://github.com/headkaze/Hackintool

### Inspirações

- **OC Auxiliary Tools (OCAT)**: https://github.com/ic005k/OCAuxiliaryTools
- **OpenCore Simplify**: https://github.com/lzhoang2801/OpCore-Simplify

---

## ✅ Critérios de Aceite

### Funcionalidades Core

- [x] Estrutura de projeto criada
- [x] Schema manager implementado
- [x] Validador básico funcionando
- [ ] Detector de hardware completo
- [ ] Gerador de EFI funcional
- [ ] Editor config.plist visual
- [ ] Gestor de kexts integrado
- [ ] ACPI/SSDT builder
- [ ] Debug e validação completa
- [ ] Comparador de EFIs
- [ ] Exportador funcional

### Qualidade

- [ ] Testes unitários (cobertura > 70%)
- [ ] Linting sem erros
- [ ] Type hints completos
- [ ] Documentação de código
- [ ] README completo

### UX

- [ ] Interface fluida e responsiva
- [ ] Feedback visual imediato
- [ ] Mensagens de erro claras
- [ ] Tooltips informativos
- [ ] Tema Liquid Glass implementado

### Distribuição

- [ ] Build .app funcionando
- [ ] Assinatura de código
- [ ] Notarização (macOS)
- [ ] CI/CD configurado

---

**Última atualização**: 2024  
**Mantenedor**: Mestre EFI

