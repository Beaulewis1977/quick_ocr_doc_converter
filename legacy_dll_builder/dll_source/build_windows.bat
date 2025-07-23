@echo off
REM Windows-specific build script for UniversalConverter32.dll
REM This script builds the actual 32-bit DLL for VB6/VFP9

echo Building UniversalConverter32.dll for Windows...

REM Check for Visual Studio Build Tools or MinGW
where cl.exe >nul 2>&1
if %errorlevel%==0 (
    echo Using Microsoft Visual C++ compiler...
    
    REM Visual Studio build command
    cl /LD /O2 /DWIN32 /D_WIN32 /DNDEBUG UniversalConverter32.cpp /Fe:UniversalConverter32.dll /link /DEF:UniversalConverter32.def
    
) else (
    where g++.exe >nul 2>&1
    if %errorlevel%==0 (
        echo Using MinGW g++ compiler...
        
        REM MinGW build command for 32-bit DLL
        g++ -m32 -O2 -std=c++17 -shared -DWIN32 -D_WIN32 -DNDEBUG -Wl,--enable-stdcall-fixup -Wl,--kill-at -o UniversalConverter32.dll UniversalConverter32.cpp UniversalConverter32.def
        
    ) else (
        echo ERROR: No suitable compiler found!
        echo Please install either:
        echo   - Visual Studio Build Tools, or
        echo   - MinGW-w64
        pause
        exit /b 1
    )
)

if exist UniversalConverter32.dll (
    echo.
    echo ✓ DLL built successfully!
    echo File: UniversalConverter32.dll
    
    REM Show DLL info
    dir UniversalConverter32.dll
    
) else (
    echo.
    echo ✗ DLL build failed!
    echo Check the compiler output above.
)

pause