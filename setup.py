# setup.py - For building macOS .app with py2app
from setuptools import setup

APP = ['AudioTally.py']
DATA_FILES = [('assets', ['assets/logo.png', 'assets/pinned.png', 'assets/unpinned.png'])]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'app_icon.png',
    'plist': {
        'CFBundleName': 'AudioTally',
        'CFBundleDisplayName': 'AudioTally',
        'CFBundleGetInfoString': "Calculate duration of multiple Cubase/Nuendo clips",
        'CFBundleIdentifier': "com.initpatch.audiotally",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025 InitPatch",
        'NSHighResolutionCapable': True,
    },
    'packages': ['customtkinter', 'PIL', 'tkinter'],
    'includes': ['xml.etree.ElementTree', 'subprocess', 'json', 'os'],
}

setup(
    app=APP,
    name='AudioTally',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)