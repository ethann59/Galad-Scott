# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all, copy_metadata, collect_dynamic_libs
import glob

# NOTE: Building with a single Analysis (above) may add excluded modules or
# heavy libs to all executables. To have finer control we create one
# Analysis per executable. This mirrors the CI flags used in GitHub Actions.

# --- Dependency analysis ---
# We analyze each entry script to find its dependencies.
# Game (main) Analysis: needs assets + models and sklearn forest import
analysis_game = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    datas=[('assets', 'assets')],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

exe_config_tool = EXE(
    pyz_config,
    analysis_config.scripts,
    [],
    exclude_binaries=True,
    name='galad-config-tool',
    console=False,  # No console for the config tool
    icon='assets/logo.ico'
)


# --- Final collect ---
# This is where all exe outputs and related files are placed into
# the final output directories. This structure is the recommended
# practice for multi-executable applications.
coll_game = COLLECT(exe_game,
                    analysis_game.binaries, analysis_game.datas,
                    name='galad-scott',)