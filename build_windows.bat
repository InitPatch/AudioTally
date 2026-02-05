@echo off
REM build_windows.bat - Automated Windows build script

echo Building Windows executable...
echo.

REM Check if pyinstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller pillow customtkinter
)

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable
echo Building executable...
pyinstaller build_windows.spec

if %errorlevel% == 0 (
    echo.
    echo Build successful!
    echo Executable location: dist\Multiple Events Duration Calculator.exe
    echo.
    echo To test: dist\Multiple Events Duration Calculator.exe
    pause
) else (
    echo.
    echo Build failed. Check errors above.
    pause
    exit /b 1
)
