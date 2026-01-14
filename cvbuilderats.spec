# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files

project_root = os.path.abspath(".")
datas = []

# Include project folders
for folder in ["components", "exporters", "utils", "ats_profiles"]:
    datas.append((os.path.join(project_root, folder), folder))

# Include top-level app.py
datas.append((os.path.join(project_root, "app.py"), "."))

# Streamlit + its data files
datas += collect_data_files("streamlit")

block_cipher = None

a = Analysis(
    ["run_desktop.py"],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=[],
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
    name="CVBuilderATS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # set True if you want console logs
)
