# Enhanced OCR Document Converter - Windows Dependency Installer (PowerShell)
# Run with: powershell -ExecutionPolicy Bypass -File install_dependencies_windows.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Enhanced OCR Document Converter - Dependency Installer" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $null = Get-Command $command -ErrorAction SilentlyContinue
    return $?
}

# Check Python installation
if (-not (Test-CommandExists "python")) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonVersion = python --version 2>&1
Write-Host "Found $pythonVersion" -ForegroundColor Green
Write-Host ""

# Function to install package with error handling
function Install-Package {
    param(
        [string]$package,
        [string]$description = ""
    )
    
    if ($description) {
        Write-Host "Installing $description..." -ForegroundColor Yellow
    } else {
        Write-Host "Installing $package..." -ForegroundColor Yellow
    }
    
    $output = python -m pip install $package 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Successfully installed $package" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install $package" -ForegroundColor Red
        Write-Host $output
    }
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

Write-Host ""
Write-Host "Installing core dependencies with compatibility fixes..." -ForegroundColor Cyan
Write-Host ""

# Critical dependencies with specific versions
$coreDependencies = @(
    @{package="numpy==1.26.4"; desc="NumPy (v1.26.4 for OpenCV compatibility)"},
    @{package="opencv-python==4.8.1.78"; desc="OpenCV"},
    @{package="pytesseract==0.3.13"; desc="Pytesseract OCR wrapper"},
    @{package="packaging==25.0"; desc="Packaging utilities"},
    @{package="Pillow==10.4.0"; desc="Python Imaging Library"}
)

foreach ($dep in $coreDependencies) {
    Install-Package -package $dep.package -description $dep.desc
}

Write-Host ""
Write-Host "Installing document processing packages..." -ForegroundColor Cyan
$docDependencies = @(
    "python-docx==1.2.0",
    "beautifulsoup4==4.13.4",
    "reportlab==4.4.2",
    "markdown==3.8.2",
    "lxml==6.0.0"
)

foreach ($dep in $docDependencies) {
    Install-Package -package $dep
}

Write-Host ""
Write-Host "Installing security and utility packages..." -ForegroundColor Cyan
$utilDependencies = @(
    @{package="cryptography==43.0.3"; desc="Cryptography for secure storage"},
    @{package="requests==2.32.4"; desc="HTTP library"},
    @{package="psutil==6.2.0"; desc="System utilities"},
    @{package="pywin32==306"; desc="Windows API support"}
)

foreach ($dep in $utilDependencies) {
    Install-Package -package $dep.package -description $dep.desc
}

# Optional development tools
Write-Host ""
$installDev = Read-Host "Install development tools (PyInstaller, pytest)? (y/n)"
if ($installDev -eq 'y') {
    Write-Host ""
    Write-Host "Installing development tools..." -ForegroundColor Cyan
    Install-Package -package "pyinstaller==6.12.0" -description "PyInstaller"
    Install-Package -package "pytest==8.4.1" -description "pytest"
    Install-Package -package "pytest-cov==6.0.0" -description "pytest coverage"
}

# Check for Tesseract
Write-Host ""
Write-Host "Checking for Tesseract OCR..." -ForegroundColor Cyan
$tesseractPaths = @(
    "C:\Program Files\Tesseract-OCR\tesseract.exe",
    "C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
)

$tesseractFound = $false
foreach ($path in $tesseractPaths) {
    if (Test-Path $path) {
        Write-Host "✓ Tesseract found at: $path" -ForegroundColor Green
        $tesseractFound = $true
        break
    }
}

if (-not $tesseractFound) {
    Write-Host "✗ Tesseract OCR not found" -ForegroundColor Red
    Write-Host "Please download and install from:" -ForegroundColor Yellow
    Write-Host "https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Install Tesseract OCR if not already installed" -ForegroundColor White
Write-Host "2. Run 'python enhanced_ocr_gui.py' to start the application" -ForegroundColor White
Write-Host "3. Configure API keys in the Settings tab" -ForegroundColor White
Write-Host ""
Write-Host "For Visual C++ errors, install:" -ForegroundColor Yellow
Write-Host "https://aka.ms/vs/17/release/vc_redist.x64.exe" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"