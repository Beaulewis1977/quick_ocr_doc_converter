#\!/bin/bash
# Universal Document Converter - Unix/Linux/macOS Launcher

echo "🚀 Starting Universal Document Converter..."

# Detect Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found\!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Launch the application
$PYTHON_CMD universal_document_converter_ultimate.py

# Keep terminal open on error
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Application exited with an error"
    echo "Press Enter to close..."
    read
fi
EOF < /dev/null
