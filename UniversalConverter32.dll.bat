@echo off
REM UniversalConverter32.dll Simulator
REM This batch file simulates DLL functionality for testing
REM It calls the Python CLI in the background

set INPUT=%1
set OUTPUT=%2
set INPUT_FORMAT=%3
set OUTPUT_FORMAT=%4

if "%INPUT%"=="" goto usage
if "%OUTPUT%"=="" goto usage

REM Call the Python CLI
python3 dll_builder_cli.py "%INPUT%" -o "%OUTPUT%" -t "%OUTPUT_FORMAT%" --quiet

REM Return appropriate exit code
if %errorlevel%==0 (
    exit /b 1
) else (
    exit /b 0
)

:usage
echo UniversalConverter32.dll Simulator
echo Usage: UniversalConverter32.dll.bat input output input_format output_format
exit /b -1