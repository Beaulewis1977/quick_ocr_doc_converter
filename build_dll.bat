@echo off
REM Build script for UniversalConverter32.dll
REM Creates production-ready 32-bit DLL for VB6/VFP9 integration

echo ========================================
echo Universal Document Converter DLL Builder
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "dll_source\UniversalConverter32.cpp" (
    echo ERROR: Source files not found!
    echo Make sure you're running this from the repo root directory.
    echo Expected: dll_source\UniversalConverter32.cpp
    pause
    exit /b 1
)

REM Create output directory
if not exist "dist" mkdir dist

REM Change to source directory
cd dll_source

REM Check for MinGW compiler
echo Checking for MinGW compiler...
g++ --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: MinGW g++ compiler not found!
    echo.
    echo Please install MinGW-w64 and add it to your PATH.
    echo Download from: https://www.mingw-w64.org/
    echo.
    echo Alternative: Install through MSYS2
    echo   pacman -S mingw-w64-i686-gcc
    echo.
    pause
    cd ..
    exit /b 1
)

echo MinGW compiler found!
echo.

REM Build the 32-bit DLL
echo Building UniversalConverter32.dll...
echo Command: g++ -m32 -O2 -std=c++17 -shared -DWIN32 -D_WIN32 -DNDEBUG -Wl,--enable-stdcall-fixup -Wl,--kill-at -o UniversalConverter32.dll UniversalConverter32.cpp UniversalConverter32.def

g++ -m32 -O2 -std=c++17 -shared -DWIN32 -D_WIN32 -DNDEBUG -Wl,--enable-stdcall-fixup -Wl,--kill-at -o UniversalConverter32.dll UniversalConverter32.cpp UniversalConverter32.def

if %errorlevel% neq 0 (
    echo.
    echo ERROR: DLL compilation failed!
    echo Check the error messages above for details.
    pause
    cd ..
    exit /b 1
)

if not exist "UniversalConverter32.dll" (
    echo.
    echo ERROR: DLL was not created!
    echo Check compiler output for errors.
    pause
    cd ..
    exit /b 1
)

echo.
echo ✓ DLL compiled successfully!

REM Move DLL to dist directory
move UniversalConverter32.dll ..\dist\
echo ✓ DLL moved to dist directory

REM Go back to root
cd ..

REM Copy required files to distribution
echo.
echo Creating distribution package...

copy cli.py dist\ >nul
echo ✓ CLI script copied

copy requirements.txt dist\ >nul
echo ✓ Requirements file copied

copy VB6_UniversalConverter.bas dist\ >nul
echo ✓ VB6 integration module copied

copy UniversalConverter_VFP9.prg dist\ >nul
echo ✓ VFP9 integration module copied

if exist "README_DLL.md" (
    copy README_DLL.md dist\ >nul
    echo ✓ DLL documentation copied
)

REM Create installation batch file
echo @echo off > dist\install.bat
echo REM Installation script for UniversalConverter32.dll >> dist\install.bat
echo echo Installing UniversalConverter32.dll... >> dist\install.bat
echo copy UniversalConverter32.dll %%WINDIR%%\System32\ >> dist\install.bat
echo if %%errorlevel%%==0 ( >> dist\install.bat
echo     echo ✓ DLL installed to System32 >> dist\install.bat
echo     echo You can now use the DLL from any VB6/VFP9 application >> dist\install.bat
echo ^) else ( >> dist\install.bat
echo     echo ✗ Installation failed - try running as administrator >> dist\install.bat
echo ^) >> dist\install.bat
echo pause >> dist\install.bat

echo ✓ Installation script created

REM Create test script
echo @echo off > dist\test_dll.bat
echo REM Test script for UniversalConverter32.dll >> dist\test_dll.bat
echo echo Testing UniversalConverter32.dll... >> dist\test_dll.bat
echo echo. >> dist\test_dll.bat
echo echo Creating test file... >> dist\test_dll.bat
echo echo # Test Document > test.md >> dist\test_dll.bat
echo echo This is a test markdown document. >> test.md >> dist\test_dll.bat
echo echo. >> dist\test_dll.bat
echo echo Testing conversion... >> dist\test_dll.bat
echo python cli.py test.md -o test.txt -t txt >> dist\test_dll.bat
echo if exist test.txt ( >> dist\test_dll.bat
echo     echo ✓ Conversion successful! >> dist\test_dll.bat
echo     echo Check test.txt for results >> dist\test_dll.bat
echo     del test.md >> dist\test_dll.bat
echo ^) else ( >> dist\test_dll.bat
echo     echo ✗ Conversion failed >> dist\test_dll.bat
echo ^) >> dist\test_dll.bat
echo pause >> dist\test_dll.bat

echo ✓ Test script created

REM Show final results
echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Distribution package created in: dist\
echo.
echo Files included:
echo   ✓ UniversalConverter32.dll    - Main 32-bit DLL
echo   ✓ cli.py                      - Python CLI backend
echo   ✓ requirements.txt            - Python dependencies
echo   ✓ VB6_UniversalConverter.bas  - VB6 integration module
echo   ✓ UniversalConverter_VFP9.prg - VFP9 integration module
echo   ✓ install.bat                 - System installation script
echo   ✓ test_dll.bat                - Test conversion script
echo.
echo To install the DLL system-wide:
echo   1. Run dist\install.bat as Administrator
echo.
echo To test the DLL:
echo   1. Copy the dist\ folder to your project directory
echo   2. Run test_dll.bat to verify functionality
echo.
echo For VB6/VFP9 integration:
echo   1. Import VB6_UniversalConverter.bas (for VB6)
echo   2. Use UniversalConverter_VFP9.prg (for VFP9)
echo.
echo The DLL requires Python and the CLI script in the same directory
echo or in the system PATH.
echo.
pause