@echo off
echo Uninstalling Quick Document Convertor...

REM Remove shortcuts
del "%USERPROFILE%\Desktop\Quick Document Convertor.lnk" 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Quick Document Convertor.lnk" 2>nul

REM Remove file associations
reg delete "HKCU\Software\Classes\.pdf" /f 2>nul
reg delete "HKCU\Software\Classes\.docx" /f 2>nul
reg delete "HKCU\Software\Classes\.txt" /f 2>nul
reg delete "HKCU\Software\Classes\.html" /f 2>nul
reg delete "HKCU\Software\Classes\.rtf" /f 2>nul
reg delete "HKCU\Software\Classes\.epub" /f 2>nul
reg delete "HKCU\Software\Classes\.odt" /f 2>nul
reg delete "HKCU\Software\Classes\.csv" /f 2>nul

REM Remove application files
echo Removing application files...
rmdir /s /q "C:\dev\quick_doc_convertor" 2>nul

echo Quick Document Convertor has been uninstalled.
pause
