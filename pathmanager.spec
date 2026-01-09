# -*- mode: python ; coding: utf-8 -*-

# PathManager - PyInstaller spec file for Windows executable
# Version: 0.2.0d
# Updated: 2026-01-09

a = Analysis(
    ['pathmanager.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icons/ICON_PathMgr.ico', 'icons'),  # Include icon file in the bundle
        ('icons/ICON_PathMgr.png', 'icons'),  # Include PNG fallback
        ('CHANGELOG.md', '.'),                # Include changelog for Help menu
        ('QUICK_REFERENCE.md', '.'),          # Include quick reference for Help menu
    ],
    hiddenimports=[],
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
    name='PathManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console window for CLI mode (can be hidden when using --gui)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/ICON_PathMgr.ico',  # Use ICO file for Windows taskbar icon
)
