# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for building the QuestTools UI launcher."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

project_root = Path(__file__).resolve().parent.parent

_datas = [
    (str(project_root / "questtools" / "web" / "templates"), "questtools/web/templates"),
    (str(project_root / "questtools" / "web" / "static"), "questtools/web/static"),
    (str(project_root / "data" / "quests" / "tan_thu.json"), "data/quests"),
]

_hiddenimports = []
for package in ["questtools", "uvicorn", "fastapi", "starlette", "pydantic"]:
    _hiddenimports.extend(collect_submodules(package))

block_cipher = None


a = Analysis(
    [str(project_root / "questtools" / "ui_launcher.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=_datas,
    hiddenimports=_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="QuestToolsUI",
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
    icon=None,
)
