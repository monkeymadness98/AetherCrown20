#!/bin/bash
# Deploy to Staging Environment

set -e

echo "🚀 Deploying to Staging..."

# Check if required environment variables are set
if [ -z "$RENDER_API_KEY" ]; then
    echo "❌ Error: RENDER_API_KEY not set"
    exit 1
fi

if [ -z "$RENDER_SERVICE_ID" ]; then
    echo "❌ Error: RENDER_SERVICE_ID not set"
    exit 1
fi

# Trigger Render deployment
echo "📦 Triggering Render deployment..."
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"clearCache": false}'

echo "✅ Deployment triggered successfully!"
echo "🔍 Check Render dashboard for status"
