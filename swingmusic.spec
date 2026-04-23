# -*- mode: python ; coding: utf-8 -*-
import argparse
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from platform import system, machine
import pathlib

# Build mode is chosen via args after `--`, per the canonical PyInstaller
# pattern (see: https://pyinstaller.org/en/stable/spec-files):
#   pyinstaller swingmusic.spec               -> onefile (single executable)
#   pyinstaller swingmusic.spec -- --onedir   -> onedir at dist/swingmusic/
parser = argparse.ArgumentParser()
parser.add_argument("--onedir", action="store_true",
                    help="Build as a directory tree instead of a single executable")
options = parser.parse_args()

# PyInstaller can't see inside Nuitka-compiled .so/.pyd files to discover
# their imports. Rather than manually tracking which modules the compiled
# premium code needs, pull in every swingmusic submodule unconditionally.
hiddenimports = collect_submodules('swingmusic')
datas = [('client.zip', '.'), ('version.txt', '.')]
datas += collect_data_files('swingmusic', True, excludes=['**/*.py'], includes=['**/*.*'])
datas += collect_data_files('flask_openapi3', True, excludes=['**/*.py'], includes=['**/*.*'])

def getFlaskOpenApiPath():
    return importlib.resources.files("flask_openapi3")


binary_name = f'swingmusic_{system().lower()}_{machine().lower()}'

a = Analysis(
    ['run.py'],
    pathex=['src'],
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

if options.onedir:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=binary_name,
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
        name='swingmusic',
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=binary_name,
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
