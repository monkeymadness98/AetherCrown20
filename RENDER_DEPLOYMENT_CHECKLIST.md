# Render Deployment Checklist

Use this checklist to ensure your Render deployment is properly configured.

## Pre-Deployment Checklist

### ✅ Repository Files
- [x] `runtime.txt` exists and specifies Python version
- [x] `render.yaml` exists with correct configuration
- [x] `build.sh` exists and is executable
- [x] `Procfile` exists (alternative to startCommand)
- [x] `requirements.txt` exists with all dependencies
- [x] `backend/main.py` exists and exports `app` object
- [x] `.renderignore` exists (optional but recommended)

### ✅ Documentation
- [x] `DEPLOYMENT.md` - Comprehensive deployment guide
- [x] `RENDER_QUICKSTART.md` - Quick start guide
- [x] `RENDER_DEPLOYMENT_SUMMARY.md` - Technical summary
- [x] `README.md` - Updated with deployment instructions

### ✅ Configuration Validation
Run the validation script to check everything:
```bash
./validate-render-config.sh
```

Expected output: ✅ All validations passed!

## Render Account Setup

### Account Creation
- [ ] Create account at [render.com](https://render.com)
- [ ] Verify email address
- [ ] Connect GitHub account

### Repository Connection
- [ ] Fork or have access to the repository
- [ ] Repository is accessible from your GitHub account
- [ ] Repository contains all required deployment files

## Environment Variables

Before deploying, gather these credentials:

### Required Variables
- [ ] **PAYPAL_CLIENT_ID**
  - Get from: [PayPal Developer Dashboard](https://developer.paypal.com)
  - Where: API Credentials section
  - Note: Use sandbox credentials for testing
  
- [ ] **PAYPAL_SECRET**
  - Get from: Same as PAYPAL_CLIENT_ID
  - Where: API Credentials section
  - Note: Keep this secret, never commit to repository

### Optional Variables
- [ ] **DATABASE_URL** (if using a database)
  - Example: `postgresql://user:pass@host:5432/dbname`
  - Where: Your PostgreSQL provider (Render, Railway, Supabase, etc.)
  
- [ ] **REDIS_URL** (if using Redis)
  - Example: `redis://host:6379/0`
  - Where: Your Redis provider

- [ ] **CORS_ORIGINS** (if you have a frontend)
  - Example: `https://yourfrontend.com`
  - Comma-separated list of allowed origins

## Deployment Steps

### Method 1: Blueprint Deployment (Recommended)

- [ ] 1. Log in to [Render Dashboard](https://dashboard.render.com)
- [ ] 2. Click "New +" → "Blueprint"
- [ ] 3. Connect GitHub and select repository
- [ ] 4. Review detected `render.yaml` configuration
- [ ] 5. Add environment variables (see above)
- [ ] 6. Click "Apply" to create service
- [ ] 7. Wait for build to complete (2-5 minutes)
- [ ] 8. Note the provided URL (e.g., `https://aethercrown20-backend.onrender.com`)

### Method 2: Manual Service Creation

- [ ] 1. Log in to Render Dashboard
- [ ] 2. Click "New +" → "Web Service"
- [ ] 3. Connect repository
- [ ] 4. Configure settings:
  - Name: `aethercrown20-backend`
  - Region: Oregon (or preferred)
  - Branch: `main`
  - Runtime: Python 3
  - Build Command: `./build.sh`
  - Start Command: `cd backend && gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 2 --log-level info`
- [ ] 5. Select plan (Free tier for testing)
- [ ] 6. Add environment variables
- [ ] 7. Click "Create Web Service"
- [ ] 8. Wait for deployment

### Method 3: GitHub Actions (Automated CI/CD)

- [ ] 1. Get Render API key from [Account Settings](https://dashboard.render.com/account)
- [ ] 2. Get Service ID from service dashboard URL
- [ ] 3. Add GitHub secrets:
  - `RENDER_API_KEY`
  - `RENDER_SERVICE_ID`
  - `PAYPAL_CLIENT_ID`
  - `PAYPAL_SECRET`
- [ ] 4. Push to `main` branch
- [ ] 5. Monitor deployment in GitHub Actions tab

## Post-Deployment Verification

### Test Endpoints
- [ ] Health check works: `GET https://your-app.onrender.com/healthz`
  - Expected: `{"ok": true, "env": "production"}`
  
- [ ] API endpoint works: `GET https://your-app.onrender.com/clocks`
  - Expected: `{"message": "Backend is alive and connected."}`

### Check Logs
- [ ] Go to Render Dashboard → Your Service → Logs
- [ ] Verify no error messages
- [ ] Look for: "Application startup complete"

### Verify Environment
- [ ] Environment variables are set correctly
- [ ] Service shows "Live" status (green)
- [ ] No build or runtime errors

## Monitoring Setup

### Configure Notifications
- [ ] Go to service Settings → Notifications
- [ ] Add email for deploy notifications
- [ ] Enable health check notifications
- [ ] Set up Slack/Discord webhooks (optional)

### Check Metrics
- [ ] Review CPU usage in Metrics tab
- [ ] Review Memory usage
- [ ] Monitor response times
- [ ] Check error rates

## Optional Enhancements

### Custom Domain
- [ ] Purchase/own a domain
- [ ] Add domain in Render Settings → Custom Domains
- [ ] Configure DNS records
- [ ] Wait for SSL certificate provisioning

### Scaling
- [ ] Decide if free tier is sufficient
- [ ] Upgrade plan if needed:
  - Starter: $7/month (512 MB RAM)
  - Standard: $25/month (2 GB RAM)
  - Pro: $85/month (4 GB RAM)
- [ ] Consider horizontal scaling (multiple instances)

### Database Setup
- [ ] Create PostgreSQL database (if needed)
  - Option 1: Render PostgreSQL
  - Option 2: External provider
- [ ] Add DATABASE_URL to environment variables
- [ ] Run migrations if applicable

### CI/CD Pipeline
- [ ] Set up GitHub Actions (see Method 3 above)
- [ ] Configure branch protection rules
- [ ] Add status checks
- [ ] Enable automatic deployments

## Troubleshooting

If deployment fails, check:

- [ ] Build logs for errors
- [ ] All required files are present
- [ ] Environment variables are set
- [ ] Python version is compatible
- [ ] Dependencies are correct
- [ ] Start command is correct

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting.

## Security Checklist

- [ ] No secrets committed to repository
- [ ] Environment variables stored in Render Dashboard only
- [ ] HTTPS enabled (automatic on Render)
- [ ] Regular dependency updates scheduled
- [ ] PayPal credentials are for correct environment (sandbox/live)
- [ ] Database has strong password
- [ ] CORS properly configured

## Documentation Review

Before going live, ensure you've read:
- [ ] [RENDER_QUICKSTART.md](./RENDER_QUICKSTART.md) - Quick start guide
- [ ] [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [ ] [RENDER_DEPLOYMENT_SUMMARY.md](./RENDER_DEPLOYMENT_SUMMARY.md) - Technical details

## Success Criteria

Your deployment is successful when:
- ✅ Service shows "Live" (green) in Render Dashboard
- ✅ Health check endpoint returns `{"ok": true}`
- ✅ No errors in logs
- ✅ Application responds to requests
- ✅ Environment variables are working
- ✅ All endpoints accessible

## Next Steps After Deployment

- [ ] Share URL with team/users
- [ ] Monitor performance for first 24 hours
- [ ] Set up alerting for issues
- [ ] Plan for regular updates
- [ ] Consider upgrading plan if needed
- [ ] Document any custom configurations

## Getting Help

If you encounter issues:

1. Check [DEPLOYMENT.md](./DEPLOYMENT.md) troubleshooting section
2. Review Render service logs
3. Visit [Render Status](https://status.render.com)
4. Check [Render Community](https://community.render.com)
5. Open GitHub issue in this repository

## Maintenance Schedule

Regular maintenance tasks:
- [ ] Weekly: Review logs for errors
- [ ] Weekly: Check resource usage
- [ ] Monthly: Update dependencies
- [ ] Monthly: Review and rotate secrets
- [ ] Quarterly: Review and optimize costs

---

**Deployment Date**: _______________

**Deployed By**: _______________

**Service URL**: _______________

**Notes**: 
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
