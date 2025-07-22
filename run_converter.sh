#!/bin/bash
# Quick Document Convertor - Unix/Linux/macOS Launcher
# Enhanced with error handling and user guidance

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}###########################################################${NC}"
echo -e "${CYAN}# QUICK DOCUMENT CONVERTOR v2.0                          #${NC}"
echo -e "${CYAN}###########################################################${NC}"
echo ""

# Check Python installation
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ PYTHON NOT FOUND IN SYSTEM PATH${NC}"
    echo ""
    echo "Please install Python 3.6+:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  CentOS/RHEL: sudo yum install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}✅ $PYTHON_VERSION${NC}"

# Check if main script exists
MAIN_SCRIPT="universal_document_converter.py"
if [[ ! -f "$MAIN_SCRIPT" ]]; then
    echo -e "${RED}❌ APPLICATION FILES MISSING${NC}"
    echo ""
    echo "Required files not found! Please:"
    echo "1. Download the full application package"
    echo "2. Extract all files to a folder"
    echo "3. Run this script from that folder"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Run the application
echo ""
echo -e "${GREEN}Starting application...${NC}"
echo -e "${CYAN}-----------------------------------------------------------${NC}"

$PYTHON_CMD -X utf8 "$MAIN_SCRIPT" "$@"

# Pause if launched by double-click
if [[ $# -eq 0 ]]; then
    echo ""
    read -p "Press Enter to exit..."
fi
