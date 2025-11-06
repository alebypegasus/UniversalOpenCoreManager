# Coding Standards - Universal OpenCore Manager

## 🌍 Language Policy

**English is the PRIMARY language** for all development:

- ✅ **All code comments** must be in English
- ✅ **All documentation** must be written first in English
- ✅ **All variable names, function names, class names** must be in English
- ✅ **All commit messages** must be in English
- ✅ **All error messages** must be in English
- ✅ **All UI strings** must have English as primary (with translations in `i18n/`)

**Translation support:**
- Secondary language: Portuguese (Brazil) - `pt-BR`
- Translations are stored in `universal_oc_manager/ui/i18n/`
- UI strings are loaded from translation files based on user preference

## 📝 Code Style

### Comments

```python
# ✅ Good: English comment
def generate_efi(output_dir: Path, profile: dict) -> Path:
    """Generate complete EFI structure in output_dir and return EFI folder path."""
    # Create EFI/OC structure
    efi = output_dir / "EFI" / "OC"
    ...

# ❌ Bad: Portuguese comment
def gerar_efi(diretorio: Path, perfil: dict) -> Path:
    """Gera estrutura EFI completa no diretório de saída."""
    # Criar estrutura EFI/OC
    ...
```

### Docstrings

All docstrings must be in English, following Google/NumPy style:

```python
def validate_config(config: dict[str, Any], schema: dict[str, Any] | None = None) -> list[ValidationErrorInfo]:
    """Validate a config.plist against OpenCore schema.
    
    Args:
        config: Configuration dictionary (parsed from plist)
        schema: Optional OpenCore JSON schema (uses default if None)
    
    Returns:
        List of ValidationErrorInfo objects with detailed error information
    
    Raises:
        ValueError: If config is not a valid dictionary
    """
    ...
```

### Variable and Function Names

- Use English names with clear, descriptive meaning
- Follow PEP 8 conventions
- Use snake_case for functions and variables
- Use PascalCase for classes

```python
# ✅ Good
def detect_hardware() -> HardwareProfile:
    cpu_info = get_cpu_info()
    ...

# ❌ Bad
def detectar_hardware() -> PerfilHardware:
    info_cpu = obter_info_cpu()
    ...
```

## 🔤 Translation Files

### Structure

Translations are stored in JSON format:

```json
// universal_oc_manager/ui/i18n/en.json (PRIMARY)
{
  "app.title": "Universal OpenCore Manager",
  "menu.preferences": "Preferences",
  "button.detect": "Detect Hardware",
  "button.generate": "Generate EFI"
}

// universal_oc_manager/ui/i18n/pt-BR.json (TRANSLATION)
{
  "app.title": "Universal OpenCore Manager",
  "menu.preferences": "Preferências",
  "button.detect": "Detectar Hardware",
  "button.generate": "Gerar EFI"
}
```

### Usage in Code

```python
from ...infra.i18n import tr

# In code
label.text = tr("app.title")  # Automatically uses correct language
```

### Adding New Strings

1. **Always add English first** in `en.json`
2. Then add translation to `pt-BR.json`
3. If translation is missing, fallback to English

## 📚 Documentation

### README and Guides

- Primary language: **English**
- Secondary translations can be added later (e.g., `README.pt-BR.md`)

### Code Documentation

- All docstrings: English
- All inline comments: English
- All type hints: English variable names

## 🚫 What NOT to Do

- ❌ Don't write comments in Portuguese
- ❌ Don't use Portuguese variable names
- ❌ Don't write documentation in Portuguese first
- ❌ Don't hardcode UI strings in code (use translation files)
- ❌ Don't mix languages in the same file

## ✅ Checklist

Before committing:
- [ ] All comments are in English
- [ ] All docstrings are in English
- [ ] All variable/function names are in English
- [ ] All UI strings use translation keys (not hardcoded)
- [ ] English translation file (`en.json`) is updated
- [ ] Portuguese translation file (`pt-BR.json`) is updated (if applicable)

---

**Remember**: English first, then translate. This ensures consistency and makes the codebase accessible to international contributors.

