# Aether Empire - Quick Start Guide

This guide will help you set up and deploy the complete Aether AI Empire stack.

## 🚀 Quick Setup (5 minutes)

### 1. Clone and Install

```bash
git clone https://github.com/monkeymadness98/AetherCrown20.git
cd AetherCrown20
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy template
cp .env.template .env

# Edit .env and fill in your values
nano .env  # or use your preferred editor
```

**Required Values:**
- OpenAI API key
- Supabase project credentials
- Database connection string
- PayPal credentials
- Deployment API keys (Render, Vercel)

### 3. Validate Configuration

```bash
# Check your local environment
node monitoring/env-validator.js

# Review the generated checklist
cat ENV_CHECKLIST.md
```

### 4. Set Up GitHub Secrets

Go to: https://github.com/monkeymadness98/AetherCrown20/settings/secrets/actions

Add these secrets:
- `OPENAI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DATABASE_URL`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_SECRET`
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`
- `VERCEL_TOKEN`
- `VERCEL_PROJECT_ID`
- `VERCEL_ORG_ID`

### 5. Configure Render

1. Go to https://dashboard.render.com/
2. Select your service
3. Go to Environment tab
4. Add the required environment variables (see `ENV_CHECKLIST.md`)

### 6. Configure Vercel

1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add all `NEXT_PUBLIC_*` and other required variables

### 7. Configure Supabase

1. Go to https://app.supabase.com/
2. Select your project
3. Go to Edge Functions → Secrets
4. Add required secrets for edge functions

## 📦 Deployment

### Automatic Deployment

Push to `main` branch triggers automatic deployment:

```bash
git add .
git commit -m "feat: your changes"
git push origin main
```

This will automatically:
- Run tests and linting
- Deploy backend to Render
- Deploy frontend to Vercel
- Run health checks

### Manual Deployment

**Trigger workflows manually:**

```bash
# Deploy to Render
gh workflow run render-deploy.yml

# Deploy to Vercel
gh workflow run vercel-deploy.yml

# Run health checks
gh workflow run daily-health-check.yml
```

**Or use platform CLIs:**

```bash
# Render
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"clearCache": false}'

# Vercel
vercel --prod
```

## 🔍 Monitoring

### Health Checks

```bash
# Run status checker
node monitoring/status-checker.js

# Check specific endpoints (replace with your actual Render URL)
curl https://your-app.onrender.com/health
curl https://your-app.onrender.com/healthz
```

### View Logs

```bash
# Local health check logs
cat logs/system_status.json | jq '.checks[-1]'

# GitHub Actions logs
gh run list
gh run view [run-id]
```

### Platform Dashboards

- **Render**: https://dashboard.render.com/
- **Vercel**: https://vercel.com/dashboard
- **Supabase**: https://app.supabase.com/
- **GitHub Actions**: https://github.com/monkeymadness98/AetherCrown20/actions

## 🧪 Local Development

### Run Backend

```bash
# Start the FastAPI backend
uvicorn backend.main:app --reload

# Or using Python directly
python backend/main.py
```

Backend available at: http://localhost:8000

API docs at: http://localhost:8000/docs

### Test Endpoints

```bash
# Health check
curl http://localhost:8000/health

# API test
curl http://localhost:8000/clocks

# Environment check (development only)
curl http://localhost:8000/_env_check
```

## 🔧 Troubleshooting

### Environment Variables Not Set

```bash
# Validate your configuration
node monitoring/env-validator.js

# Check which variables are missing
grep "❌" ENV_CHECKLIST.md
```

### Deployment Failures

1. Check GitHub Actions logs
2. Verify all secrets are set correctly
3. Check platform-specific dashboards
4. Run health checks to identify issues

### Service Down

```bash
# Check all services
node monitoring/status-checker.js

# Check specific service (replace with your Render URL)
curl -I https://your-app.onrender.com/health
```

### CI/CD Pipeline Issues

1. Verify GitHub Secrets are configured
2. Check workflow files for syntax errors
3. Review build logs in Actions tab
4. Ensure API tokens haven't expired

## 📚 Additional Resources

- [Full README](README.md) - Complete documentation
- [Monitoring Guide](monitoring/README.md) - Health check details
- [ENV_CHECKLIST.md](ENV_CHECKLIST.md) - Environment setup checklist
- [.env.template](.env.template) - Environment variables template

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review platform-specific logs
3. Run the environment validator and status checker
4. Open an issue on GitHub with:
   - Error messages
   - Logs (sanitized, no secrets!)
   - Steps to reproduce

## 📊 Health Status

![Render Deploy](https://github.com/monkeymadness98/AetherCrown20/workflows/Deploy%20to%20Render/badge.svg)
![Vercel Deploy](https://github.com/monkeymadness98/AetherCrown20/workflows/Deploy%20to%20Vercel/badge.svg)
![Health Check](https://github.com/monkeymadness98/AetherCrown20/workflows/Daily%20Health%20Check/badge.svg)
![CI/CD Pipeline](https://github.com/monkeymadness98/AetherCrown20/workflows/CI%2FCD%20Pipeline/badge.svg)

---

**Ready to deploy?** Start with step 1 above! 🚀
