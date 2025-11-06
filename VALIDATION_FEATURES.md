# Funcionalidades de Validação Implementadas

## ✅ Schema Manager (`infra/schemas/schema_manager.py`)

- **Busca de schema oficial**: Tenta buscar schema do repositório OpenCorePkg (GitHub)
- **Cache local**: Armazena schema em `~/.uocm/cache/schemas/opencore_schema.json`
- **Fallback inteligente**: Se não conseguir buscar remoto, usa schema local mínimo
- **Atualização sob demanda**: Função `get_schema(force_refresh=True)` para forçar atualização

## ✅ Validador (`core/validator/schema_validator.py`)

- **Validação detalhada**: Retorna `ValidationErrorInfo` com:
  - `message`: Mensagem de erro legível
  - `path`: Caminho no JSON (ex: "ACPI.Add.0")
  - `validator`: Tipo de validador que falhou
  - `value`: Valor que causou o erro
- **Função helper**: `validate_config_simple()` retorna apenas mensagens
- **Integração automática**: Usa `SchemaManager` para obter schema atualizado

## ✅ Integração Backend → UI (`ui/backend.py`)

- **Métodos QML-ready**:
  - `validateConfigFile(file_path)`: Valida arquivo config.plist
  - `validateCurrentConfig()`: Valida config em memória
  - `validateConfigJSON(config_json)`: Valida a partir de JSON string
  - `loadConfig(file_path)`: Carrega e valida automaticamente
  - `saveConfig(file_path, config_json)`: Salva config validado

- **Sinais Qt**:
  - `validationErrorsChanged`: Emitido quando erros são encontrados
  - `hardwareDetected`: Emitido quando hardware é detectado
  - `efiGenerated`: Emitido quando EFI é gerada

## ✅ UI QML (`ui/qml/`)

- **ValidationPanel.qml**: Componente visual que exibe:
  - Lista de erros com mensagem e caminho
  - Contador de erros
  - Layout responsivo e estilizado

- **Main.qml atualizado**:
  - Conexão de sinais backend → UI
  - Painel de validação visível quando há erros
  - Botões de teste para validação
  - Status em tempo real na barra superior

## 🔄 Fluxo de Validação

1. **Usuário carrega config.plist** → `backend.loadConfig(path)`
2. **Backend valida automaticamente** → `validate_config()`
3. **Erros são emitidos via sinal** → `validationErrorsChanged`
4. **UI atualiza painel** → `ValidationPanel` exibe erros
5. **Usuário corrige** → Validação pode ser reexecutada

## 📋 Próximos Passos (Sugeridos)

- [ ] Editor visual de config.plist (tree view editável)
- [ ] Validação em tempo real durante edição
- [ ] Auto-correção de erros comuns
- [ ] Dicas contextuais (tooltips) baseadas em erros
- [ ] Integração com documentação Dortania (links nos erros)

