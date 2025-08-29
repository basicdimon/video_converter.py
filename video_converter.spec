# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['video_converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'moviepy',
        'moviepy.video.io.VideoFileClip',
        'moviepy.audio.io.AudioFileClip',
        'moviepy.config',
        'moviepy.video.fx',
        'moviepy.audio.fx',
        'moviepy.video.tools',
        'moviepy.audio.tools',
        'imageio',
        'imageio_ffmpeg',
        'imageio.plugins',
        'imageio.plugins.ffmpeg',
        'PIL',
        'PIL.Image',
        'numpy',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'subprocess',
        'os',
        'threading',
        'pathlib'
    ],
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
    name='VideoToMP3Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI приложение без консоли
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Можно добавить иконку позже
)