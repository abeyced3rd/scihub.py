#!/bin/bash

# Test script to verify the SciHub Web App installation
# This script checks if all dependencies are installed and the app can start

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     SciHub Web App - Installation Verification              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

error_count=0

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 is not installed"
    error_count=$((error_count + 1))
fi

echo ""

# Check required packages
echo "Checking required Python packages..."

packages=("flask" "requests" "beautifulsoup4" "retrying" "pysocks")

for package in "${packages[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $package is installed"
    else
        echo -e "${RED}✗${NC} $package is NOT installed"
        error_count=$((error_count + 1))
    fi
done

echo ""

# Check file structure
echo "Checking file structure..."

files=(
    "app.py"
    "run.py"
    "config.py"
    "requirements.txt"
    "templates/index.html"
    "scihub/scihub.py"
    "QUICKSTART.md"
    "WEB_APP_README.md"
    "DEPLOYMENT.md"
    "FEATURES.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file is MISSING"
        error_count=$((error_count + 1))
    fi
done

echo ""

# Check folders
echo "Checking directories..."

folders=(
    "scihub"
    "templates"
    "downloads"
)

for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        echo -e "${GREEN}✓${NC} $folder/ directory exists"
    else
        echo -e "${YELLOW}~${NC} $folder/ directory missing (will be created on first run)"
    fi
done

echo ""

# Try to import app
echo "Testing Flask app import..."
if python3 -c "from app import app" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Flask app can be imported successfully"
else
    echo -e "${RED}✗${NC} Flask app import failed"
    error_count=$((error_count + 1))
fi

echo ""

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
if [ $error_count -eq 0 ]; then
    echo -e "║${GREEN}                ✓ VERIFICATION PASSED!                 ${NC}║"
    echo "║                                                            ║"
    echo "║  The application is ready to run. Start it with:          ║"
    echo "║                                                            ║"
    echo "║    python run.py                                          ║"
    echo "║                                                            ║"
    echo "║  Or use the startup script:                               ║"
    echo "║                                                            ║"
    echo "║    ./start.sh                                             ║"
    echo "║                                                            ║"
    echo "║  Then open: http://localhost:5000                         ║"
else
    echo -e "║${RED}            ✗ VERIFICATION FAILED!                 ${NC}║"
    echo "║                                                            ║"
    echo -e "║  ${RED}Errors found: $error_count${NC}                                        ║"
    echo "║                                                            ║"
    echo "║  Please run:                                              ║"
    echo "║    pip install -r requirements.txt                        ║"
fi
echo "╚════════════════════════════════════════════════════════════╝"

exit $error_count
