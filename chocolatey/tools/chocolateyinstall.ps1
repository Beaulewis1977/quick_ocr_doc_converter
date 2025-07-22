$ErrorActionPreference = 'Stop'

$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$url        = 'https://github.com/Beaulewis1977/quick_ocr_doc_converter/releases/download/v3.1.0/Universal-Document-Converter-v3.1.0-Windows-Complete.zip'
$packageName = 'ocr-document-converter'

$packageArgs = @{
  packageName   = $packageName
  unzipLocation = $toolsDir
  url           = $url
  checksum      = 'GET_CHECKSUM_AFTER_BUILD'
  checksumType  = 'sha256'
}

# Download and extract the package
Install-ChocolateyZipPackage @packageArgs

# Create Start Menu shortcut
$targetPath = Join-Path $toolsDir "run_ocr_converter.bat"
$shortcutPath = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\OCR Document Converter.lnk"

Install-ChocolateyShortcut `
  -ShortcutFilePath $shortcutPath `
  -TargetPath $targetPath `
  -WorkingDirectory $toolsDir `
  -Description "OCR Document Converter - Convert documents with OCR"

# Create Desktop shortcut
$desktopPath = [Environment]::GetFolderPath("Desktop")
$desktopShortcut = Join-Path $desktopPath "OCR Document Converter.lnk"

Install-ChocolateyShortcut `
  -ShortcutFilePath $desktopShortcut `
  -TargetPath $targetPath `
  -WorkingDirectory $toolsDir `
  -Description "OCR Document Converter - Convert documents with OCR"

Write-Host "OCR Document Converter has been installed successfully!" -ForegroundColor Green
Write-Host "You can launch it from the Start Menu or Desktop shortcut." -ForegroundColor Green
Write-Host "" -ForegroundColor Green
Write-Host "CLI Usage:" -ForegroundColor Yellow
Write-Host "  ocr-convert input.pdf -o output.txt --ocr" -ForegroundColor White
Write-Host "  doc-convert input.md -o output.pdf" -ForegroundColor White