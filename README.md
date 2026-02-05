# AudioTally

**Duration Calculator for Cubase & Nuendo**

Beautiful desktop app that automatically calculates the total duration of multiple selected clips in Cubase or Nuendo.

![AudioTally Logo](assets/logo.png)

## ✨ Features

- ✅ **Auto-detection**: Automatically detects when you copy clips
- 🎨 **Modern UI**: Clean interface with CustomTkinter
- 📌 **Always-on-top**: Optional pin to keep window visible
- 📊 **Detailed Analysis**: View individual clip durations
- 🔊 **Multiple Sample Rates**: Support for 8kHz to 192kHz
- 💾 **Preserves Clipboard**: Original data intact for pasting back

## 🚀 How to Use

1. Select your project sample rate in the app
2. Select multiple clips in Cubase/Nuendo
3. Copy them (Cmd+C or Ctrl+C)
4. Duration appears automatically!
5. Click "Show Details" to see individual clip analysis

## 📥 Download

### macOS
Download `AudioTally-macOS.zip` from [Releases](../../releases)

### Windows
Download `AudioTally-Windows.zip` from [Releases](../../releases)

## 🛠️ Building from Source

### Prerequisites
- Python 3.8+
- Dependencies: `pip install py2app pillow customtkinter` (Mac) or `pip install pyinstaller pillow customtkinter` (Windows)

### macOS (.app bundle)

**Quick build:**
```bash
./build_mac.sh
```

**Manual build:**
```bash
pip3 install py2app pillow customtkinter
python3 setup.py py2app
```

Output: `dist/AudioTally.app`

### Windows (.exe)

**Option 1 - GitHub Actions (Recommended for Mac users):**
Push to GitHub and download built .exe from Actions tab. See `WINDOWS_BUILD_OPTIONS.md`

**Option 2 - On Windows PC:**
```
build_windows.bat
```

**Option 3 - On Mac via Wine (Advanced):**
See detailed instructions in `WINDOWS_BUILD_OPTIONS.md`

Output: `dist/AudioTally.exe`

## 📦 Distribution

### macOS
```bash
# After building
cd dist
zip -r "AudioTally-macOS.zip" "AudioTally.app"
```

### Windows
GitHub Actions creates the zip automatically!

## 📂 Project Structure

```
AudioTally/
├── AudioTally.py                  # Main application
├── setup.py                       # py2app config (Mac)
├── build_windows.spec            # PyInstaller config (Windows)
├── build_mac.sh                  # Mac build script
├── build_windows.bat             # Windows build script
├── .github/workflows/build.yml   # Automated builds
├── BUILD_INSTRUCTIONS.md         # Detailed build guide
├── WINDOWS_BUILD_OPTIONS.md      # Windows build options for Mac users
├── QUICKSTART.md                 # Quick reference
├── assets/
│   ├── logo.png                  # App logo
│   ├── pinned.png                # Pin icon
│   └── unpinned.png              # Unpin icon
└── app_icon.png                  # App icon
```

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install customtkinter pillow
```

### CustomTkinter theme not loading
```bash
pip install --force-reinstall customtkinter
```

### macOS "App is damaged" warning
```bash
xattr -cr "AudioTally.app"
```
Then right-click app → Open (first time only)

### Windows antivirus blocking
Add exception for the `.exe` file. PyInstaller executables sometimes trigger false positives.

## 📄 License

MIT License - Free to use and modify

## 🙏 Credits

Made with ❤️ for Cubase & Nuendo users by [InitPatch](https://github.com/InitPatch)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

Having issues? Please [open an issue](../../issues) on GitHub.

---

**Enjoy using AudioTally!** 🎵