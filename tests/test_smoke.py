from pathlib import Path
from universal_oc_manager.core.engine.generator import generate_efi

def test_generate_structure(tmp_path: Path):
    efi = generate_efi(tmp_path, {"profile": "test"})
    assert (efi / "OC").exists()
    assert (efi / "OC" / "Kexts").exists()
