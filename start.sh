#!/bin/bash

# Startup script for AI-Powered Company Brochure Generator
# This ensures the correct virtual environment is used

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting AI-Powered Company Brochure Generator${NC}"
echo "=================================================="

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}✓${NC} Activating virtual environment..."
source venv/bin/activate

# Check Python version
PYTHON_VERSION=$(python --version)
echo -e "${GREEN}✓${NC} Using $PYTHON_VERSION"

# Install/upgrade dependencies
echo -e "${GREEN}✓${NC} Checking dependencies..."
pip install -q -r requirements.txt

# Check if PDF libraries are installed
if python -c "from reportlab.lib.pagesizes import A4; import markdown2" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} PDF export available (ReportLab + markdown2 installed)"
else
    echo -e "${YELLOW}⚠️  PDF export not available. Installing PDF libraries...${NC}"
    pip install -q reportlab markdown2
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} PDF libraries installed successfully"
    else
        echo -e "${RED}✗${NC} Failed to install PDF libraries. PDF export will be disabled."
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found${NC}"
    echo "   Create a .env file with your GENAI_API_KEY"
    echo "   Example: cp .env.example .env"
fi

echo "=================================================="
echo -e "${GREEN}✓${NC} All checks complete!"
echo ""
echo -e "${GREEN}Starting Streamlit app...${NC}"
echo "Open your browser to: ${GREEN}http://localhost:8501${NC}"
echo ""

# Start Streamlit
streamlit run app.py
