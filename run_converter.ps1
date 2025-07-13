# Quick Document Convertor - PowerShell Launcher
# Enhanced with error handling and user guidance

param(
    [switch]$NoPause = $false
)

# Set console colors
$Host.UI.RawUI.BackgroundColor = 'Black'
$Host.UI.RawUI.ForegroundColor = 'Green'
Clear-Host

Write-Host "###########################################################" -ForegroundColor Cyan
Write-Host "# QUICK DOCUMENT CONVERTOR v2.0                          #" -ForegroundColor Cyan
Write-Host "###########################################################" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonPath = (Get-Command python -ErrorAction Stop).Source
    Write-Host "✅ Python found: $pythonPath" -ForegroundColor Green
} catch {
    Write-Host "❌ PYTHON NOT FOUND IN SYSTEM PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.6+ from:"
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Write-Host ""
    if (-not $NoPause) {
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    exit 1
}

# Check if main script exists
$mainScript = "universal_document_converter.py"
if (-not (Test-Path $mainScript)) {
    Write-Host "❌ APPLICATION FILES MISSING" -ForegroundColor Red
    Write-Host ""
    Write-Host "Required files not found! Please:"
    Write-Host "1. Download the full application package"
    Write-Host "2. Extract all files to a folder"
    Write-Host "3. Run this script from that folder"
    Write-Host ""
    if (-not $NoPause) {
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    exit 1
}

# Check Python version
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Could not determine Python version" -ForegroundColor Yellow
}

# Run the application
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "-----------------------------------------------------------" -ForegroundColor DarkGray

try {
    & python -X utf8 $mainScript $args
} catch {
    Write-Host ""
    Write-Host "❌ Error running application:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running: python install_converter.py" -ForegroundColor Yellow
}

# Pause if launched by double-click
if (-not $NoPause -and $args.Count -eq 0) {
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
