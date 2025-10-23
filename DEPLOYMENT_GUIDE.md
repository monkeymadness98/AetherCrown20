# Deployment Guide - AetherCrown20

This guide walks through the complete deployment and verification process for AetherCrown20, addressing the issues identified in the CI/CD workflow.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables Setup](#environment-variables-setup)
3. [Backend Deployment (Render)](#backend-deployment-render)
4. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
5. [Verification Steps](#verification-steps)
6. [Troubleshooting](#troubleshooting)
7. [Monitoring Setup](#monitoring-setup)

## Prerequisites

Before deploying, ensure you have:

- [ ] GitHub account with repository access
- [ ] Render account (https://render.com)
- [ ] Vercel account (https://vercel.com)
- [ ] Supabase project (https://supabase.com)
- [ ] PayPal Developer account (https://developer.paypal.com)
- [ ] Stripe account (https://stripe.com)
- [ ] Sentry account for error tracking (optional)
- [ ] Healthchecks.io account for monitoring (optional)

## Environment Variables Setup

### 1. GitHub Secrets

Configure these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

#### Deployment Keys
```
RENDER_API_KEY=rnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID=srv-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VERCEL_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VERCEL_ORG_ID=team_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Database & Storage
```
DATABASE_URL=postgresql://user:password@host:5432/database
REDIS_URL=redis://default:password@host:6379
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Payment Providers
```
PAYPAL_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYPAL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Monitoring & Security
```
SENTRY_DSN=https://xxxxxxxxxxxxx@o123456.ingest.sentry.io/7890123
HEALTHCHECKS_PING_URL=https://hc-ping.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
SECRET_KEY=your_random_secret_key_min_32_chars_long
```

### 2. Render Environment Variables

In your Render service dashboard, configure:

```
ENV=production
PORT=10000
PAYPAL_CLIENT_ID=<from_secrets>
PAYPAL_SECRET=<from_secrets>
PAYPAL_MODE=sandbox
DATABASE_URL=<from_secrets>
REDIS_URL=<from_secrets>
SUPABASE_URL=<from_secrets>
SUPABASE_KEY=<from_secrets>
STRIPE_SECRET_KEY=<from_secrets>
STRIPE_PUBLISHABLE_KEY=<from_secrets>
SENTRY_DSN=<from_secrets>
HEALTHCHECKS_PING_URL=<from_secrets>
SECRET_KEY=<from_secrets>
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://your-app.vercel.app
```

### 3. Vercel Environment Variables

In your Vercel project settings, add:

```
NEXT_PUBLIC_API_URL=https://aethercrown98-backend.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Backend Deployment (Render)

### Automatic Deployment via GitHub Actions

1. **Trigger Deployment**
   - Push to `main` branch
   - GitHub Actions will automatically trigger deployment

2. **Monitor Deployment**
   ```bash
   # Check GitHub Actions
   # Go to: https://github.com/monkeymadness98/AetherCrown20/actions
   
   # Check Render Dashboard
   # Go to: https://dashboard.render.com/
   ```

3. **Wait for Health Check**
   - The CI/CD pipeline will automatically verify the health endpoint
   - Wait ~60 seconds for deployment to complete

### Manual Deployment via Render Dashboard

1. Go to https://dashboard.render.com/
2. Navigate to your service
3. Click "Manual Deploy" → "Deploy latest commit"
4. Wait for deployment to complete
5. Check logs for any errors

### Verify Backend Deployment

```bash
# Health check
curl https://aethercrown98-backend.onrender.com/healthz

# Expected response:
# {"ok": true, "env": "production"}

# API endpoint check
curl https://aethercrown98-backend.onrender.com/clocks

# Expected response:
# {"message": "Backend is alive and connected."}
```

## Frontend Deployment (Vercel)

### Automatic Deployment via GitHub Actions

The frontend deploys automatically after backend deployment succeeds.

### Manual Deployment via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Verify Frontend Deployment

1. Visit your Vercel URL
2. Open browser DevTools (F12) → Network tab
3. Verify API calls to backend succeed
4. Check console for any errors

## Verification Steps

### Automated Verification

Use the provided verification script:

```bash
./verify-deployment.sh
```

Or with custom URLs:

```bash
export BACKEND_URL=https://aethercrown98-backend.onrender.com
export FRONTEND_URL=https://your-app.vercel.app
./verify-deployment.sh
```

### Manual Verification Checklist

#### 1. Backend Health Check ✅
```bash
curl https://aethercrown98-backend.onrender.com/healthz
# Should return: {"ok": true, "env": "production"}
```

#### 2. Backend API Endpoints ✅
```bash
curl https://aethercrown98-backend.onrender.com/clocks
# Should return: {"message": "Backend is alive and connected."}
```

#### 3. Environment Variables ✅
```bash
curl https://aethercrown98-backend.onrender.com/_env_check
# Should show ENV and presence of key variables
# ⚠️ Remove this endpoint in production!
```

#### 4. CORS Configuration ✅
```bash
curl -I -H "Origin: https://your-app.vercel.app" \
  https://aethercrown98-backend.onrender.com/healthz
# Should include: Access-Control-Allow-Origin header
```

#### 5. Frontend Loading ✅
- Visit frontend URL
- Page should load without errors
- Check Network tab for successful API calls

#### 6. Frontend → Backend Communication ✅
- Open browser console
- Look for successful API requests
- No CORS errors

## Troubleshooting

### Problem: Backend Health Check Fails (Not 200 OK)

**Symptoms:**
```bash
curl https://aethercrown98-backend.onrender.com/healthz
# Returns 502, 503, or times out
```

**Solutions:**

1. **Check Render Logs**
   ```
   Go to: https://dashboard.render.com/
   → Your Service → Logs tab
   ```

2. **Common Issues:**
   - ❌ Service still deploying (wait 2-3 minutes)
   - ❌ Missing environment variables
   - ❌ Port configuration wrong (should use $PORT)
   - ❌ Dependencies failed to install
   - ❌ Python version mismatch

3. **Fix Missing Environment Variables:**
   - Check Render dashboard → Environment tab
   - Ensure all required vars are set
   - Redeploy after adding missing vars

4. **Fix Port Issues:**
   - Render provides `PORT` environment variable
   - Backend automatically uses `$PORT` from env
   - Default is 10000 in render.yaml

### Problem: GitHub Actions Workflow Failing

**Check Workflow Logs:**
```
GitHub → Actions tab → Click on failed workflow
```

**Common Issues:**

1. **Missing GitHub Secrets**
   ```
   Error: secret RENDER_API_KEY not found
   ```
   **Fix:** Add missing secrets in GitHub Settings → Secrets

2. **Build Failures**
   ```
   Error: pip install failed
   ```
   **Fix:** Check requirements.txt for incompatible versions

3. **Deployment API Errors**
   ```
   Error: 401 Unauthorized
   ```
   **Fix:** Regenerate API keys (Render/Vercel)

### Problem: Frontend Can't Connect to Backend

**Symptoms:**
- CORS errors in browser console
- API requests failing with 0 status

**Solutions:**

1. **Check CORS Configuration**
   - Backend should include frontend URL in CORS_ORIGINS
   - Update Render env var: `CORS_ORIGINS=...,https://your-app.vercel.app`
   - Redeploy backend

2. **Verify Backend URL**
   - Check Vercel env var: `NEXT_PUBLIC_API_URL`
   - Should point to: `https://aethercrown98-backend.onrender.com`
   - Redeploy frontend after fixing

3. **Check Network Tab**
   - Look for actual error message
   - Verify request URL is correct
   - Check response headers

### Problem: Environment Variables Not Loading

**Symptoms:**
```bash
curl https://aethercrown98-backend.onrender.com/_env_check
# Shows false for required variables
```

**Solutions:**

1. **Render Dashboard**
   - Go to service → Environment tab
   - Click "Add Environment Variable"
   - Add missing variables
   - Click "Save Changes"
   - Manual deploy or wait for auto-deploy

2. **GitHub Secrets**
   - Ensure secrets are added in repository settings
   - Secrets are case-sensitive
   - Re-run workflow after adding secrets

### Problem: Database Connection Fails

**Symptoms:**
```
Error: could not connect to server
```

**Solutions:**

1. **Check DATABASE_URL Format**
   ```
   postgresql://user:password@host:5432/database
   ```

2. **Verify Database Access**
   - Ensure database accepts connections from Render
   - Check firewall/whitelist settings
   - For Supabase: Should work by default

3. **Check Connection Pool Settings**
   - Render free tier has connection limits
   - Adjust pool size in code if needed

## Monitoring Setup

### 1. Healthchecks.io

```bash
# Sign up at https://healthchecks.io
# Create a check
# Get your ping URL

# Add to environment variables
HEALTHCHECKS_PING_URL=https://hc-ping.com/your-uuid

# Run health check script
./healthcheck.sh
```

### 2. Sentry Error Tracking

```bash
# Sign up at https://sentry.io
# Create a project
# Get your DSN

# Add to environment variables
SENTRY_DSN=https://xxx@sentry.io/123

# Errors will automatically be reported
```

### 3. Manual Health Checks

Set up a cron job to ping your health endpoint:

```bash
# Add to crontab
*/5 * * * * /path/to/healthcheck.sh
```

## Best Practices

1. **Deployment Order**
   - Always deploy backend first
   - Wait for health check to pass
   - Then deploy frontend

2. **Environment Variables**
   - Never commit secrets to Git
   - Use GitHub Secrets for CI/CD
   - Set directly in Render/Vercel dashboards

3. **Testing**
   - Test locally first with `.env` file
   - Verify in staging environment
   - Then deploy to production

4. **Monitoring**
   - Set up health checks
   - Enable error tracking
   - Monitor logs regularly

5. **Security**
   - Remove `/_env_check` endpoint in production
   - Use strong SECRET_KEY (32+ characters)
   - Enable HTTPS only
   - Restrict CORS to specific origins

## Quick Reference

### URLs
- Backend: https://aethercrown98-backend.onrender.com
- Health Check: https://aethercrown98-backend.onrender.com/healthz
- Frontend: https://your-app.vercel.app (configure in Vercel)

### Dashboards
- Render: https://dashboard.render.com/
- Vercel: https://vercel.com/dashboard
- GitHub Actions: https://github.com/monkeymadness98/AetherCrown20/actions
- Supabase: https://app.supabase.com/
- Sentry: https://sentry.io/

### Scripts
```bash
# Health check
./healthcheck.sh

# Comprehensive verification
./verify-deployment.sh

# Run backend locally
python backend/main.py

# Manual Vercel deploy
vercel --prod
```

## Support

If you encounter issues not covered in this guide:

1. Check GitHub Issues: https://github.com/monkeymadness98/AetherCrown20/issues
2. Review Render logs: https://dashboard.render.com/
3. Check Vercel deployment logs: https://vercel.com/dashboard
4. Verify all environment variables are set correctly
5. Ensure all secrets are configured in GitHub

---

**Last Updated:** 2025-10-23
**Version:** 1.0
