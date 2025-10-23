# Pre-Deployment Checklist

Use this checklist before deploying to production to ensure everything is configured correctly.

## GitHub Configuration

### GitHub Secrets (Settings → Secrets and variables → Actions)

- [ ] `RENDER_API_KEY` - Get from Render Dashboard → Account Settings → API Keys
- [ ] `RENDER_SERVICE_ID` - Get from Render service URL (srv-xxxxx)
- [ ] `VERCEL_TOKEN` - Get from Vercel → Account Settings → Tokens
- [ ] `VERCEL_ORG_ID` - Get from Vercel project settings
- [ ] `VERCEL_PROJECT_ID` - Get from Vercel project settings
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `PAYPAL_CLIENT_ID` - From PayPal Developer Dashboard
- [ ] `PAYPAL_SECRET` - From PayPal Developer Dashboard
- [ ] `SUPABASE_URL` - From Supabase project settings
- [ ] `SUPABASE_KEY` - From Supabase project settings (anon key)
- [ ] `STRIPE_SECRET_KEY` - From Stripe Dashboard
- [ ] `STRIPE_PUBLISHABLE_KEY` - From Stripe Dashboard
- [ ] `SENTRY_DSN` - From Sentry project settings (optional)
- [ ] `HEALTHCHECKS_PING_URL` - From Healthchecks.io (optional)
- [ ] `SECRET_KEY` - Generate random 32+ character string

## Render Configuration

### Service Settings
- [ ] Service created and connected to GitHub repository
- [ ] Build command: `pip install -r ../requirements.txt`
- [ ] Start command: `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 2 --log-level info`
- [ ] Root directory: `backend`
- [ ] Auto-deploy enabled for main branch

### Environment Variables (Render Dashboard → Environment)
- [ ] `ENV=production`
- [ ] `PORT=10000`
- [ ] `PAYPAL_CLIENT_ID=<your_value>`
- [ ] `PAYPAL_SECRET=<your_value>`
- [ ] `PAYPAL_MODE=sandbox` (or `live` for production)
- [ ] `DATABASE_URL=<your_postgresql_url>`
- [ ] `REDIS_URL=<your_redis_url>` (if using Redis)
- [ ] `SUPABASE_URL=<your_supabase_url>`
- [ ] `SUPABASE_KEY=<your_supabase_key>`
- [ ] `STRIPE_SECRET_KEY=<your_stripe_key>`
- [ ] `STRIPE_PUBLISHABLE_KEY=<your_stripe_key>`
- [ ] `SENTRY_DSN=<your_sentry_dsn>` (optional)
- [ ] `HEALTHCHECKS_PING_URL=<your_healthchecks_url>` (optional)
- [ ] `SECRET_KEY=<random_32_char_string>`
- [ ] `CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://your-app.vercel.app`

### Health Check
- [ ] Health check path set to `/healthz` (configured in render.yaml)

## Vercel Configuration

### Project Settings
- [ ] Project created and connected to GitHub repository
- [ ] Root directory: `.` (repository root)
- [ ] Build command: Leave empty (static HTML)
- [ ] Output directory: Leave empty
- [ ] Auto-deploy enabled for main branch

### Environment Variables (Vercel Dashboard → Settings → Environment Variables)
- [ ] `NEXT_PUBLIC_API_URL=https://aethercrown98-backend.onrender.com`
- [ ] `NEXT_PUBLIC_SUPABASE_URL=<your_supabase_url>`
- [ ] `NEXT_PUBLIC_SUPABASE_ANON_KEY=<your_supabase_key>`

## External Services

### Supabase
- [ ] Project created at https://supabase.com
- [ ] Database tables created (if needed)
- [ ] API keys copied to secrets
- [ ] Connection tested

### PayPal
- [ ] Developer account created at https://developer.paypal.com
- [ ] App created in PayPal Dashboard
- [ ] Client ID and Secret copied to secrets
- [ ] Mode set correctly (sandbox/live)

### Stripe
- [ ] Account created at https://stripe.com
- [ ] API keys generated
- [ ] Webhook endpoint configured (if needed)
- [ ] Keys copied to secrets

### Sentry (Optional)
- [ ] Account created at https://sentry.io
- [ ] Project created
- [ ] DSN copied to secrets

### Healthchecks.io (Optional)
- [ ] Account created at https://healthchecks.io
- [ ] Check created
- [ ] Ping URL copied to secrets

## Pre-Deploy Verification

### Local Testing
- [ ] Backend runs locally: `python backend/main.py`
- [ ] Health check works: `curl http://localhost:8000/healthz`
- [ ] API endpoint works: `curl http://localhost:8000/clocks`
- [ ] Frontend loads: Open `index.html` in browser
- [ ] All dependencies install: `pip install -r requirements.txt`

### Code Validation
- [ ] YAML files are valid: `python -c "import yaml; yaml.safe_load(open('render.yaml'))"`
- [ ] JSON files are valid: `python -c "import json; json.load(open('vercel.json'))"`
- [ ] Backend imports: `python -c "from backend.main import app"`
- [ ] Shell scripts are valid: `bash -n healthcheck.sh && bash -n verify-deployment.sh`

## Deployment

### Deploy Backend First
1. [ ] Push to main branch
2. [ ] Wait for GitHub Actions to complete
3. [ ] Check Render Dashboard for deployment status
4. [ ] Wait for deployment to complete (~2-3 minutes)
5. [ ] Verify health check: `curl https://aethercrown98-backend.onrender.com/healthz`

### Deploy Frontend Second
1. [ ] Ensure backend is healthy
2. [ ] GitHub Actions will auto-deploy to Vercel
3. [ ] Check Vercel Dashboard for deployment status
4. [ ] Wait for deployment to complete (~1-2 minutes)
5. [ ] Visit frontend URL and verify it loads

## Post-Deployment Verification

### Automated Verification
- [ ] Run verification script: `./verify-deployment.sh`
- [ ] All checks pass

### Manual Verification
- [ ] Backend health check: `curl https://aethercrown98-backend.onrender.com/healthz`
  - Expected: `{"ok": true, "env": "production"}`
- [ ] Backend API: `curl https://aethercrown98-backend.onrender.com/clocks`
  - Expected: `{"message": "Backend is alive and connected."}`
- [ ] Frontend loads without errors
- [ ] Browser console shows no errors
- [ ] API calls from frontend succeed
- [ ] No CORS errors

### Check Logs
- [ ] Render logs show no errors
- [ ] Vercel logs show successful deployment
- [ ] GitHub Actions workflow completed successfully
- [ ] No error alerts in Sentry (if configured)

## Monitoring Setup

### Continuous Monitoring
- [ ] Set up cron job for healthcheck.sh (optional)
- [ ] Configure alerting in Healthchecks.io (optional)
- [ ] Monitor Sentry for errors (optional)
- [ ] Check logs daily for first week

### Regular Checks
- [ ] Weekly: Check all service logs
- [ ] Weekly: Verify all endpoints still working
- [ ] Monthly: Review and rotate secrets
- [ ] Monthly: Check for dependency updates

## Security Checklist

- [ ] Remove or secure `/_env_check` endpoint after initial verification
- [ ] SECRET_KEY is strong (32+ random characters)
- [ ] All secrets stored securely (not in code)
- [ ] HTTPS enabled for all services
- [ ] CORS restricted to specific origins
- [ ] Database credentials rotated
- [ ] API keys have appropriate permissions

## Rollback Plan

If deployment fails:

1. [ ] Check GitHub Actions logs for errors
2. [ ] Check Render logs for backend errors
3. [ ] Check Vercel logs for frontend errors
4. [ ] Revert to previous commit if needed: `git revert HEAD`
5. [ ] Re-run verification: `./verify-deployment.sh`

## Documentation

- [ ] DEPLOYMENT_GUIDE.md reviewed
- [ ] QUICKSTART.md reviewed
- [ ] README.md updated with current URLs
- [ ] Team notified of deployment

## Success Criteria

All of the following must be true:

- ✅ Backend health check returns 200 OK
- ✅ Frontend loads without errors
- ✅ API calls from frontend succeed
- ✅ No CORS errors
- ✅ All logs clean (no errors)
- ✅ GitHub Actions workflow passes
- ✅ Monitoring configured (if applicable)

---

**Date Completed**: _______________
**Deployed By**: _______________
**Backend URL**: https://aethercrown98-backend.onrender.com
**Frontend URL**: https://_______________
**Notes**: _______________________________________________
