# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from platform import system, machine
import pathlib

hiddenimports =[]
# hiddenimports += collect_submodules('swingmusic')

datas = collect_data_files('swingmusic', True, excludes=['**/*.py'], includes=['**/*.*'])
datas += collect_data_files('flask_openapi3', True, excludes=['**/*.py'], includes=['**/*.*'])

def getFlaskOpenApiPath():
    return importlib.resources.files("flask_openapi3")



a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name=f'swingmusic_{system().lower()}_{machine().lower()}',
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
    icon=[pathlib.Path('src\\swingmusic\\assets\\logo-fill.light.ico')],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='name_test',
)