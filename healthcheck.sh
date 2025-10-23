#!/bin/bash
# Health check script for monitoring backend status
# This can be used by external monitoring services or cron jobs

BACKEND_URL="${BACKEND_URL:-https://aethercrown98-backend.onrender.com}"
HEALTHCHECK_ENDPOINT="${BACKEND_URL}/healthz"
HEALTHCHECKS_PING_URL="${HEALTHCHECKS_PING_URL:-}"

echo "Checking backend health at ${HEALTHCHECK_ENDPOINT}..."

# Try to reach the health endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" "${HEALTHCHECK_ENDPOINT}")

if [ "$response" = "200" ]; then
    echo "✅ Backend is healthy (HTTP 200)"
    
    # Ping healthchecks.io if configured
    if [ -n "$HEALTHCHECKS_PING_URL" ]; then
        curl -fsS -m 10 --retry 5 -o /dev/null "${HEALTHCHECKS_PING_URL}" || echo "Warning: Failed to ping healthchecks.io"
    fi
    
    exit 0
else
    echo "❌ Backend health check failed (HTTP ${response})"
    
    # Ping healthchecks.io failure endpoint if configured
    if [ -n "$HEALTHCHECKS_PING_URL" ]; then
        curl -fsS -m 10 --retry 5 -o /dev/null "${HEALTHCHECKS_PING_URL}/fail" || echo "Warning: Failed to ping healthchecks.io"
    fi
    
    exit 1
fi
