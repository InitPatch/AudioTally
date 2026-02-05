#!/bin/bash
# build_mac.sh - Automated macOS build script

echo "🍎 Building macOS app..."
echo ""

# Check if py2app is installed
if ! python3 -c "import py2app" 2>/dev/null; then
    echo "❌ py2app not found. Installing..."
    pip3 install py2app pillow customtkinter
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build the app
echo "🔨 Building app bundle..."
python3 setup.py py2app

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo "📦 App location: dist/Multiple Events Duration Calculator.app"
    echo ""
    echo "To test: open 'dist/Multiple Events Duration Calculator.app'"
    echo ""
    
    # Optional: Open the app
    read -p "Open app now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "dist/Multiple Events Duration Calculator.app"
    fi
else
    echo ""
    echo "❌ Build failed. Check errors above."
    exit 1
fi
