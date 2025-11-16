# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Belvedere
# 
# Build with: poetry run pyinstaller belvedere.spec
# 
# This creates a single executable file for Windows with all dependencies included.

from PyInstaller.utils.hooks import collect_data_files

# Collect resource files
datas = [
    ('resources/belvedere.ico', 'resources'),
    ('resources/belvederename.png', 'resources'),
    ('resources/both.png', 'resources'),
]

a = Analysis(
    ['belvedere.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
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
    name='belvedere',
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
    icon='resources/belvedere.ico',
)
