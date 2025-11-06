# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['uocm/main.py'],
    pathex=[],
    binaries=[],
    datas=[('translations', 'translations'), ('templates', 'templates'), ('plugins', 'plugins')],
    hiddenimports=['PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'sqlalchemy', 'uocm', 'uocm.core', 'uocm.ui', 'uocm.db', 'uocm.detector', 'uocm.engine_generator', 'uocm.plist_editor', 'uocm.kext_manager', 'uocm.acpi_manager', 'uocm.debugger', 'uocm.plugins'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='UOCM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/icon.icns'],
)
app = BUNDLE(
    exe,
    name='UOCM.app',
    icon='assets/icon.icns',
    bundle_identifier='dev.mestre.efi.uocm',
)
