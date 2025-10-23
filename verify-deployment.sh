#!/bin/bash
# Comprehensive deployment verification script
# This script checks all the key components mentioned in the problem statement

set -e

BACKEND_URL="${BACKEND_URL:-https://aethercrown98-backend.onrender.com}"
FRONTEND_URL="${FRONTEND_URL:-}"

echo "================================================"
echo "🔍 AetherCrown20 Deployment Verification"
echo "================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success message
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print error message
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to print warning message
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "1️⃣  Checking Backend Health..."
echo "   URL: ${BACKEND_URL}/healthz"

response=$(curl -s -w "\n%{http_code}" "${BACKEND_URL}/healthz" || echo "000")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

if [ "$http_code" = "200" ]; then
    success "Backend health check passed (HTTP 200)"
    echo "   Response: $body"
else
    error "Backend health check failed (HTTP ${http_code})"
    echo "   Response: $body"
    echo ""
    error "Backend is not responding correctly. Check Render logs:"
    echo "   https://dashboard.render.com/"
    exit 1
fi

echo ""
echo "2️⃣  Checking Backend Endpoints..."

# Check /clocks endpoint
echo "   Testing /clocks endpoint..."
response=$(curl -s -w "%{http_code}" "${BACKEND_URL}/clocks" -o /dev/null)
if [ "$response" = "200" ]; then
    success "Backend /clocks endpoint is accessible"
else
    warning "Backend /clocks endpoint returned HTTP ${response}"
fi

echo ""
echo "3️⃣  Checking Environment Variables..."
echo "   Testing /_env_check endpoint..."

env_response=$(curl -s "${BACKEND_URL}/_env_check" || echo "{}")
if [ -n "$env_response" ] && [ "$env_response" != "{}" ]; then
    success "Environment variables endpoint accessible"
    echo "   Response: $env_response"
    
    # Check for critical env vars
    if echo "$env_response" | grep -q '"ENV"'; then
        success "ENV variable is set"
    else
        error "ENV variable is missing"
    fi
else
    warning "Could not check environment variables"
fi

echo ""
echo "4️⃣  Checking CORS Configuration..."
echo "   Testing CORS headers..."

cors_check=$(curl -s -H "Origin: http://localhost:3000" -I "${BACKEND_URL}/healthz" | grep -i "access-control-allow-origin" || echo "")
if [ -n "$cors_check" ]; then
    success "CORS is configured"
    echo "   $cors_check"
else
    warning "CORS headers not detected (may still work for same-origin requests)"
fi

echo ""
echo "5️⃣  Port & URL Configuration..."
success "Backend is listening on correct port (detected via successful health check)"
success "Backend URL is accessible: ${BACKEND_URL}"

if [ -n "$FRONTEND_URL" ]; then
    echo ""
    echo "6️⃣  Checking Frontend..."
    echo "   URL: ${FRONTEND_URL}"
    
    frontend_response=$(curl -s -w "%{http_code}" "${FRONTEND_URL}" -o /dev/null || echo "000")
    if [ "$frontend_response" = "200" ]; then
        success "Frontend is accessible (HTTP 200)"
    else
        error "Frontend returned HTTP ${frontend_response}"
    fi
else
    warning "Frontend URL not provided, skipping frontend check"
    echo "   Set FRONTEND_URL environment variable to check frontend"
fi

echo ""
echo "================================================"
echo "✨ Verification Summary"
echo "================================================"
echo ""
echo "Backend Status:"
echo "  - Health Check: ✅ Passing"
echo "  - URL: ${BACKEND_URL}"
echo ""
echo "Next Steps:"
echo "  1. Test API calls from frontend to backend"
echo "  2. Verify all required env vars in Render dashboard"
echo "  3. Check logs for any warnings or errors"
echo "  4. Test integrations (Supabase, PayPal, Stripe)"
echo ""
echo "Dashboard Links:"
echo "  - Render: https://dashboard.render.com/"
echo "  - Vercel: https://vercel.com/dashboard"
echo ""
echo "================================================"
