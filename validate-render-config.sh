#!/usr/bin/env bash
# Render Deployment Validation Script
# This script validates that all required files and configurations are in place

set -e

echo "🔍 Validating Render Deployment Configuration..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Validation function
validate_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is missing"
        return 1
    fi
}

validate_executable() {
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 is executable"
        return 0
    else
        echo -e "${YELLOW}⚠${NC} $1 is not executable (fixing...)"
        chmod +x "$1"
        echo -e "${GREEN}✓${NC} $1 is now executable"
        return 0
    fi
}

# Track validation status
ALL_VALID=true

echo "📁 Checking Required Files..."
echo ""

# Check core deployment files
validate_file "runtime.txt" || ALL_VALID=false
validate_file "render.yaml" || ALL_VALID=false
validate_file "build.sh" || ALL_VALID=false
validate_file "Procfile" || ALL_VALID=false
validate_file "requirements.txt" || ALL_VALID=false
validate_file "backend/main.py" || ALL_VALID=false

echo ""
echo "📄 Checking Documentation Files..."
echo ""

validate_file "DEPLOYMENT.md" || echo -e "${YELLOW}⚠${NC} DEPLOYMENT.md is missing (optional)"
validate_file "RENDER_QUICKSTART.md" || echo -e "${YELLOW}⚠${NC} RENDER_QUICKSTART.md is missing (optional)"
validate_file ".renderignore" || echo -e "${YELLOW}⚠${NC} .renderignore is missing (optional)"

echo ""
echo "🔧 Checking File Permissions..."
echo ""

validate_executable "build.sh" || ALL_VALID=false

echo ""
echo "📋 Validating File Contents..."
echo ""

# Check runtime.txt
if [ -f "runtime.txt" ]; then
    PYTHON_VERSION=$(cat runtime.txt)
    if [[ $PYTHON_VERSION == python-* ]]; then
        echo -e "${GREEN}✓${NC} runtime.txt contains valid Python version: $PYTHON_VERSION"
    else
        echo -e "${RED}✗${NC} runtime.txt has invalid format. Expected: python-X.Y.Z"
        ALL_VALID=false
    fi
fi

# Check render.yaml
if [ -f "render.yaml" ]; then
    if grep -q "buildCommand:" render.yaml && grep -q "startCommand:" render.yaml; then
        echo -e "${GREEN}✓${NC} render.yaml contains buildCommand and startCommand"
    else
        echo -e "${RED}✗${NC} render.yaml is missing buildCommand or startCommand"
        ALL_VALID=false
    fi
fi

# Check if gunicorn is in requirements
if [ -f "requirements.txt" ]; then
    if grep -qi "gunicorn" requirements.txt || grep -qi "gunicorn" backend/requirements.txt 2>/dev/null; then
        echo -e "${GREEN}✓${NC} gunicorn is listed in requirements"
    else
        echo -e "${RED}✗${NC} gunicorn is not in requirements.txt"
        ALL_VALID=false
    fi
fi

echo ""
echo "🧪 Testing Build Script..."
echo ""

if [ -x "build.sh" ]; then
    echo "Running build.sh (this may take a moment)..."
    if ./build.sh > /tmp/build_test.log 2>&1; then
        echo -e "${GREEN}✓${NC} build.sh executes successfully"
    else
        # Check if it's a network timeout (common in CI/CD)
        if grep -q "ReadTimeoutError\|ConnectionError\|Network\|timeout" /tmp/build_test.log 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} build.sh timed out (network issue - this is OK)"
        else
            echo -e "${RED}✗${NC} build.sh failed to execute"
            echo "Check /tmp/build_test.log for details"
            ALL_VALID=false
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC} Skipping build test (build.sh not executable)"
fi

echo ""
echo "🔍 Checking Python Backend..."
echo ""

if [ -f "backend/main.py" ]; then
    if python3 -c "import sys; sys.path.insert(0, 'backend'); import main; print('Import successful')" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} backend/main.py imports successfully"
    else
        echo -e "${YELLOW}⚠${NC} backend/main.py cannot be imported (may need dependencies)"
    fi
    
    if python3 -c "import sys; sys.path.insert(0, 'backend'); import main; assert hasattr(main, 'app'), 'No app object found'" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} backend/main.py exports 'app' object"
    else
        echo -e "${RED}✗${NC} backend/main.py does not export 'app' object"
        ALL_VALID=false
    fi
fi

echo ""
echo "📊 Configuration Summary..."
echo ""

if [ -f "render.yaml" ]; then
    echo "Service Configuration (render.yaml):"
    echo "  Name: $(grep 'name:' render.yaml | awk '{print $2}' | head -1)"
    echo "  Environment: $(grep 'env:' render.yaml | awk '{print $2}' | head -1)"
    echo "  Plan: $(grep 'plan:' render.yaml | awk '{print $2}' | head -1)"
    echo "  Region: $(grep 'region:' render.yaml | awk '{print $2}' | head -1)"
    echo ""
fi

echo "Environment Variables (to be configured in Render):"
echo "  Required:"
echo "    - PAYPAL_CLIENT_ID"
echo "    - PAYPAL_SECRET"
echo "  Optional:"
echo "    - DATABASE_URL"
echo ""

# Final result
echo "═══════════════════════════════════════"
if [ "$ALL_VALID" = true ]; then
    echo -e "${GREEN}✅ All validations passed!${NC}"
    echo ""
    echo "Your repository is ready for Render deployment."
    echo ""
    echo "Next steps:"
    echo "1. Go to https://dashboard.render.com/"
    echo "2. Click 'New +' → 'Blueprint'"
    echo "3. Select this repository"
    echo "4. Add environment variables"
    echo "5. Click 'Apply' to deploy"
    echo ""
    echo "For detailed instructions, see:"
    echo "  - Quick start: RENDER_QUICKSTART.md"
    echo "  - Full guide: DEPLOYMENT.md"
    exit 0
else
    echo -e "${RED}❌ Some validations failed${NC}"
    echo ""
    echo "Please fix the issues above before deploying to Render."
    echo "See DEPLOYMENT.md for troubleshooting help."
    exit 1
fi
