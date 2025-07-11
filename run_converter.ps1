# Document to Markdown Converter
# PowerShell script to run the GUI converter application

Write-Host "🚀 Starting Document to Markdown Converter..." -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the converter
try {
    python document_converter_gui.py
} catch {
    Write-Host "❌ Error running converter: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
} 