@echo off
REM ========================================
REM IMPORTANT: DLL Builder Has Been Moved!
REM ========================================
echo.
echo ******************************************************************
echo *                    IMPORTANT NOTICE                            *
echo *                                                                *
echo * The DLL builder has been moved to a dedicated module for       *
echo * better organization and maintenance.                           *
echo *                                                                *
echo * NEW LOCATION: legacy_dll_builder\                              *
echo ******************************************************************
echo.
echo To build the 32-bit DLL for VB6/VFP9 integration:
echo.
echo   1. Navigate to the legacy module:
echo      cd legacy_dll_builder
echo.
echo   2. Build the DLL:
echo      python cli.py build
echo.
echo   3. Or use the enhanced CLI with better error handling:
echo      python cli_new.py build --source dll_source --output UniversalConverter32.dll
echo.
echo For more information, see:
echo   - legacy_dll_builder\README.md
echo   - VFP9_VB6_INTEGRATION_GUIDE.md
echo.
pause