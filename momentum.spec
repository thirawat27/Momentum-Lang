# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['momentum.py'],
    pathex=[],
    binaries=[],
    # --- เพิ่ม: แนบไฟล์ไอคอนเข้าไปกับโปรแกรม ---
    datas=[('momentum_logo.ico', '.')],
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
    name='momentum',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # --- เพิ่ม: ฝังไอคอนลงในไฟล์ .exe ---
    icon='momentum_logo.ico'
)