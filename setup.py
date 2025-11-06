from setuptools import setup
from pathlib import Path

APP = ['uocm/main.py']
DATA_FILES = [
    ('translations', ['translations']),
    ('templates', ['templates']),
    ('plugins', ['plugins']),
]

OPTIONS = {
    'argv_emulation': False,
    'packages': ['uocm', 'PyQt6', 'sqlalchemy'],
    'includes': ['uocm.*'],
    'iconfile': 'assets/icon.icns' if Path('assets/icon.icns').exists() else None,
    'plist': {
        'CFBundleName': 'UOCM',
        'CFBundleDisplayName': 'Universal OpenCore Manager',
        'CFBundleIdentifier': 'dev.mestre.efi.uocm',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHighResolutionCapable': True,
        'NSHumanReadableCopyright': 'Copyright © 2024 Mestre EFI',
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
