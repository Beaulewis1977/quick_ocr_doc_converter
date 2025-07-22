@echo off
title UniversalConverter32 DLL Builder
color 0B

echo.
echo ========================================================
echo  UniversalConverter32 DLL Builder v3.1.0
echo  Creates Windows DLL for VB6/VFP9 Integration
echo ========================================================
echo.

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found in system PATH
    echo    Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version

:: Check for PyInstaller
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo 📦 Installing PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)

:: Check for main converter
if not exist "..\universal_document_converter_ocr.py" (
    echo.
    echo ❌ Main converter application not found
    echo    Please ensure this script is run from the vb6_vfp9_integration directory
    echo    within the OCR Document Converter folder structure.
    echo.
    pause
    exit /b 1
)

echo.
echo 🔨 Building Windows DLL...
echo.

:: Create build directory
if not exist "build" mkdir build
cd build

:: Copy necessary files
echo Copying files...
copy "..\UniversalConverter32.py" "." >nul
copy "..\..\cli.py" "." >nul 2>nul
copy "..\..\universal_document_converter_ocr.py" "." >nul 2>nul
xcopy "..\..\ocr_engine" "ocr_engine\" /E /I /Q >nul 2>nul

:: Create PyInstaller spec file for DLL
echo Creating DLL specification...

(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo a = Analysis^(
echo     ['UniversalConverter32.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[],
echo     hiddenimports=['cli', 'ocr_engine', 'ocr_engine.ocr_integration', 'ocr_engine.config_manager'],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     cipher=None,
echo ^)
echo.
echo pyz = PYZ^(a.pure, a.zipped_data, cipher=None^)
echo.
echo exe = EXE^(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='UniversalConverter32',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=True,
echo     disable_windowed_traceback=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None
echo ^)
) > UniversalConverter32.spec

:: Build with PyInstaller
echo Building executable...
python -m PyInstaller --clean UniversalConverter32.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ Build failed
    cd ..
    pause
    exit /b 1
)

:: Copy result to parent directory
if exist "dist\UniversalConverter32.exe" (
    copy "dist\UniversalConverter32.exe" "..\UniversalConverter32.exe" >nul
    echo.
    echo ✅ Build successful!
    echo    Created: UniversalConverter32.exe
    echo.
) else (
    echo.
    echo ❌ Build completed but exe not found
    echo.
)

cd ..

:: Create batch wrapper for DLL-like functionality  
echo Creating DLL wrapper...

(
echo @echo off
echo REM UniversalConverter32.dll Wrapper
echo REM Provides DLL-like interface for VB6/VFP9
echo.
echo set INPUT=%%1
echo set OUTPUT=%%2
echo set FORMAT=%%3
echo set USE_OCR=%%4
echo.
echo if "%%INPUT%%"=="" goto usage
echo if "%%OUTPUT%%"=="" goto usage
echo if "%%FORMAT%%"=="" set FORMAT=txt
echo.
echo REM Call the executable
echo if "%%USE_OCR%%"=="1" ^(
echo     UniversalConverter32.exe "%%INPUT%%" "%%OUTPUT%%" %%FORMAT%% --ocr
echo ^) else ^(
echo     UniversalConverter32.exe "%%INPUT%%" "%%OUTPUT%%" %%FORMAT%%
echo ^)
echo.
echo REM Return success/failure
echo if %%errorlevel%%==0 ^(
echo     exit /b 1
echo ^) else ^(
echo     exit /b 0
echo ^)
echo.
echo :usage
echo echo UniversalConverter32.dll Wrapper v3.1.0
echo echo Usage: UniversalConverter32.dll.bat input output format [use_ocr]
echo echo   input:    Input file path
echo echo   output:   Output file path  
echo echo   format:   Output format ^(txt, docx, pdf, html, markdown^)
echo echo   use_ocr:  1 to enable OCR, 0 to disable ^(optional^)
echo exit /b -1
) > UniversalConverter32.dll.bat

echo.
echo 📦 Creating package...

:: Create package directory
if not exist "package" mkdir package
copy "UniversalConverter32.exe" "package\" >nul 2>nul
copy "UniversalConverter32.dll.bat" "package\" >nul
copy "UniversalConverter32.py" "package\" >nul
copy "VB6_Example.vb" "package\" >nul  
copy "VFP9_Example.prg" "package\" >nul
copy "README.md" "package\" >nul

:: Create zip package
if exist package (
    echo Creating ZIP package...
    
    :: Use PowerShell to create zip if available
    powershell -command "Compress-Archive -Path 'package\*' -DestinationPath 'UniversalConverter32.zip' -Force" 2>nul
    
    if exist "UniversalConverter32.zip" (
        echo ✅ Package created: UniversalConverter32.zip
        echo    Size: 
        dir UniversalConverter32.zip | find ".zip"
    ) else (
        echo ⚠️  ZIP creation failed, but files are in 'package' folder
    )
)

echo.
echo ========================================================
echo  Build Complete!
echo ========================================================
echo.
echo Created files:
echo  📄 UniversalConverter32.exe        - Standalone executable
echo  📄 UniversalConverter32.dll.bat    - DLL wrapper script
echo  📄 UniversalConverter32.py         - Python module
echo  📁 package\                        - Complete package
echo  📦 UniversalConverter32.zip        - Distributable package
echo.
echo Usage in VB6/VFP9:
echo  Call UniversalConverter32.dll.bat with parameters
echo  Or use Python module directly
echo.
echo Documentation:
echo  See README.md and example files for integration details
echo.
pause