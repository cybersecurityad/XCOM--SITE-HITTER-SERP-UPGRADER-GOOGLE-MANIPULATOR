#!/bin/bash
# XCOM.DEV -- ADVANCED WEB SITE HITTER -- SERP UPGRADER- GOOGLE MANIPULATOR - Quick Deployment Script

echo "🚀 XCOM.DEV -- ADVANCED WEB SITE HITTER -- SERP UPGRADER- GOOGLE MANIPULATOR Setup"
echo "=================================================================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is designed for macOS. Please install manually.${NC}"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo -e "${RED}❌ Homebrew not found. Please install Homebrew first:${NC}"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Install Tor via Homebrew
echo -e "${YELLOW}📦 Installing Tor via Homebrew...${NC}"
if brew list tor &> /dev/null; then
    echo -e "${GREEN}✅ Tor already installed${NC}"
else
    brew install tor
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Tor installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install Tor${NC}"
        exit 1
    fi
fi

# Create virtual environment
echo -e "${YELLOW}🐍 Creating Python virtual environment...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
else
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Virtual environment created${NC}"
    else
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source .venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}📋 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Check if Chrome is installed
echo -e "${YELLOW}🌐 Checking for Chrome/Chromium...${NC}"
if [ -d "/Applications/Google Chrome.app" ] || [ -d "/Applications/Chromium.app" ]; then
    echo -e "${GREEN}✅ Chrome/Chromium found${NC}"
else
    echo -e "${YELLOW}⚠️  Chrome/Chromium not found. Please install Google Chrome.${NC}"
    echo "   Download from: https://www.google.com/chrome/"
fi

# Test basic functionality
echo -e "${YELLOW}🧪 Testing basic functionality...${NC}"
python3 -c "
try:
    from tor_menu import GLOBAL_CONFIG
    from dutch_rotation_browser import DutchRotationBrowser
    print('✅ Import test passed')
except ImportError as e:
    print(f'❌ Import test failed: {e}')
    exit(1)
"

# Success message
echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo "📋 Quick Start:"
echo "   source .venv/bin/activate"
echo "   python tor_menu.py"
echo ""
echo "📖 Documentation:"
echo "   README.md - Full documentation"
echo "   INSTALL.md - Installation guide"
echo "   ENHANCED_FEATURES_SUMMARY.md - Feature overview"
echo ""
echo "🔧 Configuration:"
echo "   Use menu option 4 for 18 configuration options"
echo "   Set page stay time (10-60 minutes)"
echo "   Configure simulation repeats (1 to infinite)"
echo ""
echo -e "${GREEN}Ready to launch XCOM.DEV -- ADVANCED WEB SITE HITTER -- SERP UPGRADER- GOOGLE MANIPULATOR! 🚀${NC}"
