# Windows Build Options for Mac Users

You have several options to build and test the Windows version without a Windows PC:

---

## Option 1: GitHub Actions (RECOMMENDED ⭐)

**Best for**: Clean, reproducible builds

### Setup:
1. Create a GitHub repository
2. Push your code
3. GitHub automatically builds Windows .exe for free!

### How it works:
- `.github/workflows/build.yml` defines the build process
- On every push, GitHub builds both Mac and Windows versions
- Download the builds from the "Actions" tab

### Steps:
```bash
# Initialize git repo (if not already)
cd "/Volumes/RAID 4TB/[ PROJECTS ]/APPS/Cubase-Nuendo Multiple Clips Duration Calculator"
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
# (Create empty repo on github.com first)
git remote add origin https://github.com/yourusername/cubase-duration-calculator.git
git push -u origin main
```

### Download builds:
1. Go to your GitHub repo
2. Click "Actions" tab
3. Click latest workflow run
4. Download "windows-exe" artifact

**Pros**: 
- ✅ 100% reliable Windows builds
- ✅ Free (GitHub Actions)
- ✅ Automatic on every commit
- ✅ Can build for multiple platforms

**Cons**: 
- ⏱️ Takes 5-10 minutes per build

---

## Option 2: Wineskin (LOCAL TESTING)

**Best for**: Quick local testing only

### Prerequisites:
```bash
brew install --cask wineskin-winery
```

### Setup Wineskin:
1. Open Wineskin Winery
2. Click "Install Software"
3. Install "Winetricks" if prompted
4. Create new wrapper with Windows Python 3.11

### Install Python in Wineskin:
1. Download Python 3.11 Windows installer (.exe)
2. In Wineskin → "Advanced" → "Tools" → "Winetricks"
3. Install Python 3.11
4. Install dependencies via Wine pip

### Build under Wine:
```bash
# If Wine is installed via Homebrew
brew install wine-stable

# Navigate to project
cd "/Volumes/RAID 4TB/[ PROJECTS ]/APPS/Cubase-Nuendo Multiple Clips Duration Calculator"

# Install Windows Python packages via Wine
wine pip install pyinstaller pillow customtkinter

# Build Windows .exe
wine pyinstaller build_windows.spec
```

**Pros**:
- ✅ Local builds (no internet required)
- ✅ Can test immediately

**Cons**:
- ⚠️ Wine quirks may cause issues
- ⚠️ Not guaranteed to work on real Windows
- ⚠️ Complex setup

---

## Option 3: Cloud Windows VM

**Best for**: Occasional builds

### Free Options:
- **Azure**: Free trial with Windows VM
- **AWS**: Free tier Windows instance
- **Google Cloud**: Free trial

### Steps:
1. Create free Windows VM
2. RDP into it
3. Install Python + dependencies
4. Copy your code
5. Run `build_windows.bat`

**Pros**:
- ✅ Real Windows environment
- ✅ 100% accurate builds

**Cons**:
- ⏱️ Time-consuming setup
- 💰 May require credit card (free tier)

---

## Option 4: Friend/Colleague's Windows PC

**Best for**: Simple one-time builds

### Steps:
1. Copy project folder to USB/cloud
2. On Windows PC:
   ```
   pip install pyinstaller pillow customtkinter
   build_windows.bat
   ```
3. Copy `dist/Multiple Events Duration Calculator.exe` back

**Pros**:
- ✅ Real Windows testing
- ✅ Simple

**Cons**:
- 🤝 Requires access to Windows PC

---

## Recommendation

**For distribution**: Use **GitHub Actions** (Option 1)
**For quick testing**: Use **Wineskin** (Option 2)

---

## Testing Windows .exe on Wineskin

Once you have a Windows .exe (from any method):

1. Open Wineskin wrapper
2. Copy .exe into wrapper
3. Set .exe as main executable
4. Test functionality

⚠️ **Note**: Even if it works in Wineskin, always test on real Windows before distributing!

---

## Icon Conversion for Windows

If you need a proper .ico file:

### Online converters:
- https://convertico.com
- https://cloudconvert.com/png-to-ico

### Mac command:
```bash
# Using ImageMagick
brew install imagemagick
convert app_icon.png -define icon:auto-resize=256,128,64,48,32,16 app_icon.ico
```

Then update `build_windows.spec`:
```python
icon='app_icon.ico',  # Use .ico instead of .png
```
