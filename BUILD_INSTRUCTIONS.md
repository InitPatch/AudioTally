# BUILD INSTRUCTIONS

## macOS Build (creates .app bundle)

### Prerequisites:
```bash
pip install py2app pillow customtkinter
```

### Build:
```bash
python setup.py py2app
```

### Output:
- `dist/Multiple Events Duration Calculator.app` - Ready to use!

### Clean build (if needed):
```bash
rm -rf build dist
python setup.py py2app
```

### To make it distributable:
1. Code sign: `codesign --deep --force --sign "Developer ID Application: Your Name" "dist/Multiple Events Duration Calculator.app"`
2. Create DMG: Use DiskImageMounter or `create-dmg` tool

---

## Windows Build (creates .exe)

### Prerequisites (on Windows or via Wine):
```bash
pip install pyinstaller pillow customtkinter
```

### Build:
```bash
pyinstaller build_windows.spec
```

### Output:
- `dist/Multiple Events Duration Calculator.exe` - Single executable!

### Clean build:
```bash
rmdir /s build dist
pyinstaller build_windows.spec
```

---

## Notes:

### Icon Files:
- **Mac**: Needs `.icns` file (use `app_icon.png` or convert)
- **Windows**: Needs `.ico` file (convert from PNG)

Convert PNG to ICNS (Mac):
```bash
sips -s format icns app_icon.png --out app_icon.icns
```

Or use online converters:
- https://cloudconvert.com/png-to-icns
- https://convertico.com

### CustomTkinter Theme Files:
Both builders should automatically include CustomTkinter's theme files. If you get theme errors:
- Manually copy CustomTkinter's theme folder to the app bundle

### Testing:
- **Mac**: Open `dist/Multiple Events Duration Calculator.app`
- **Windows**: Run `dist/Multiple Events Duration Calculator.exe`

### Distribution:
- **Mac**: DMG file or zip the .app
- **Windows**: Installer (use Inno Setup) or zip the .exe

---

## Troubleshooting:

### "Module not found" errors:
Add missing modules to `hiddenimports` in the spec files

### CustomTkinter theme missing:
```python
# Add to OPTIONS in setup.py:
'includes': ['customtkinter'],
```

### Assets not loading:
Check that `assets/` folder is being copied correctly