"""
Testes do editor de PLIST
"""

import pytest
import tempfile
from pathlib import Path
import plistlib

from uocm.plist_editor.editor import PlistEditor


def test_plist_editor_load_save(temp_dir):
    """Testa carregar e salvar PLIST"""
    # Criar PLIST de teste
    test_plist = {
        "ACPI": {"Add": []},
        "Boot": {"Arguments": ""},
    }
    
    plist_path = temp_dir / "test.plist"
    with open(plist_path, "wb") as f:
        plistlib.dump(test_plist, f)
    
    # Carregar
    editor = PlistEditor()
    assert editor.load(plist_path) is True
    assert editor.data["ACPI"]["Add"] == []
    
    # Salvar
    save_path = temp_dir / "test_saved.plist"
    assert editor.save(save_path) is True
    assert save_path.exists()


def test_plist_editor_get_set_value():
    """Testa obter e definir valores"""
    editor = PlistEditor()
    editor.data = {"ACPI": {"Add": []}}
    
    # Obter valor
    value = editor.get_value("ACPI.Add", [])
    assert value == []
    
    # Definir valor
    editor.set_value("Boot.Arguments", "debug=0x100")
    assert editor.data["Boot"]["Arguments"] == "debug=0x100"


def test_plist_editor_undo_redo():
    """Testa undo/redo"""
    editor = PlistEditor()
    editor.data = {"test": "value1"}
    editor._save_to_history()
    
    editor.set_value("test", "value2")
    assert editor.data["test"] == "value2"
    
    editor.undo()
    assert editor.data["test"] == "value1"
    
    editor.redo()
    assert editor.data["test"] == "value2"

