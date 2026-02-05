# Quick Start Guide

## I just want to build the Mac app NOW!

```bash
cd "/Volumes/RAID 4TB/[ PROJECTS ]/APPS/Cubase-Nuendo Multiple Clips Duration Calculator"
./build_mac.sh
```

Done! Your app is in `dist/Multiple Events Duration Calculator.app`

---

## I want to build the Windows version (but I'm on Mac)

### Easiest way - GitHub Actions:

1. **Create GitHub repo** (if you haven't):
   ```bash
   cd "/Volumes/RAID 4TB/[ PROJECTS ]/APPS/Cubase-Nuendo Multiple Clips Duration Calculator"
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create new repo on GitHub.com**
   - Go to https://github.com/new
   - Name it: `cubase-duration-calculator`
   - Don't initialize with README (we already have files)

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/cubase-duration-calculator.git
   git branch -M main
   git push -u origin main
   ```

4. **Download Windows build**:
   - Go to your repo on GitHub
   - Click "Actions" tab
   - Wait ~5 minutes for build to complete
   - Click latest workflow
   - Download "windows-exe" artifact
   - Unzip and test!

### Want to test locally? Use Wine:
See `WINDOWS_BUILD_OPTIONS.md` for Wine/Wineskin instructions

---

## I want to distribute this to others

### Mac:
```bash
# After building
cd dist
zip -r "Multiple Events Duration Calculator-macOS.zip" "Multiple Events Duration Calculator.app"
```

Upload the zip file to:
- Your website
- Google Drive/Dropbox
- GitHub Releases

### Windows:
GitHub Actions creates the zip automatically!

---

## First time setup checklist

✅ Python 3.8+ installed
✅ Dependencies installed: `pip3 install py2app pillow customtkinter`
✅ Icon files present in `assets/` folder
✅ Build script executable: `chmod +x build_mac.sh`

Ready to build!

---

## Common Issues

### "py2app not found"
```bash
pip3 install py2app
```

### "Module not found: customtkinter"
```bash
pip3 install customtkinter pillow
```

### "Permission denied: build_mac.sh"
```bash
chmod +x build_mac.sh
```

### Mac app shows "damaged" warning
```bash
xattr -cr "dist/Multiple Events Duration Calculator.app"
```

Then right-click → Open (first time only)

---

## Testing

### Mac:
```bash
open "dist/Multiple Events Duration Calculator.app"
```

### Windows (on real Windows):
```
dist\Multiple Events Duration Calculator.exe
```

### Windows (on Mac via Wine):
```bash
wine "dist/Multiple Events Duration Calculator.exe"
```

---

## Questions?

- Check `BUILD_INSTRUCTIONS.md` for detailed steps
- Check `WINDOWS_BUILD_OPTIONS.md` for Windows-specific options
- Check `README.md` for full documentation
