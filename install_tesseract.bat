@echo off
echo Installing Tesseract OCR...
echo.

REM Download Tesseract installer
if not exist "tesseract-ocr-setup.exe" (
    echo Downloading Tesseract OCR...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tesseract-ocr/tesseract/releases/download/v5.3.3.20231005/tesseract-ocr-w64-setup-v5.3.3.20231005.exe' -OutFile 'tesseract-ocr-setup.exe'"
)

echo Running Tesseract installer...
tesseract-ocr-setup.exe /S

echo.
echo Adding Tesseract to PATH...
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR" /M

echo.
echo Tesseract installation complete!
echo Please restart your terminal or run 'refreshenv' to update PATH.
pause