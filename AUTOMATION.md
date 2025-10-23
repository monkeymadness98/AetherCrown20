# AI Agent Deployment Sweep Automation

This document describes the comprehensive AI agent automation system for AetherCrown20, including deployment sweeps, monitoring, and auto-fix capabilities.

## Overview

The automation system provides:

1. **Automated Deployment**: Continuous deployment to Render (backend) and Vercel (frontend)
2. **Health Monitoring**: Regular health checks and auto-recovery
3. **Error Sweeps**: Automatic detection and fixing of common issues
4. **Environment Management**: Validation and auto-loading of configuration
5. **Comprehensive Reporting**: Detailed logs and status reports

## Quick Start

### Prerequisites

- Node.js 14+ installed
- Python 3.8+ installed
- Required environment variables configured (see `.env.template`)

### Installation

1. Install Node.js dependencies:
```bash
npm install
```

2. Copy and configure environment variables:
```bash
cp .env.template .env
# Edit .env with your actual values
```

3. Verify environment setup:
```bash
npm run verify-env
```

## Main Automation Scripts

### 1. AI Deploy Fix (`ai-deploy-fix.js`)

Quick deployment fix and recovery script.

**Usage:**
```bash
node ai-deploy-fix.js
# or
npm run deploy-fix
```

**What it does:**
- ✅ Checks and loads missing environment variables
- ✅ Verifies backend health and redeploys if needed
- ✅ Installs/updates backend and frontend dependencies
- ✅ Redeploys frontend to Vercel
- ✅ Validates API connections
- ✅ Restarts AI agents (PM2)

### 2. AI Agent Sweep (`ai-agent-sweep.js`)

Comprehensive automation sweep for full system monitoring and recovery.

**Usage:**
```bash
node ai-agent-sweep.js
# or
npm run sweep

# For specific environments:
npm run sweep:dev   # Development
npm run sweep:prod  # Production
```

**What it does:**

#### 1️⃣ Environment Verification
- Checks all required environment variables
- Auto-loads missing values from `.env` file
- Validates URL configurations

#### 2️⃣ Backend Health & Redeploy
- Checks `/healthz` endpoint
- Triggers Render redeploy if unhealthy
- Monitors backend logs for errors

#### 3️⃣ Dependency Fix & Build
- Runs `pip install` for backend
- Runs `npm install` for frontend
- Builds both applications
- Resolves version conflicts

#### 4️⃣ Frontend Deployment
- Deploys to Vercel with production flag
- Verifies deployment accessibility
- Tests critical routes

#### 5️⃣ AI Agent Verification
- Checks PM2 agent status
- Restarts failed/stopped agents
- Logs agent health

#### 6️⃣ Database & Service Check
- Tests Supabase connectivity
- Validates payment provider credentials
- Checks external service availability

#### 7️⃣ UI & Dashboard Check
- Tests Dev Hub and Live Dashboard
- Verifies component rendering
- Checks for broken routes

#### 8️⃣ Monitoring & Reporting
- Generates comprehensive JSON report
- Sends to health check service
- Highlights issues requiring manual intervention

#### 9️⃣ Post-Fix Deployment
- Retries deployments after critical fixes
- Final health validation
- Confirms operational status

## Utility Scripts

Located in the `scripts/` directory:

### Health Check
```bash
node scripts/health-check.js
# or
npm run health-check
```
Performs a quick health check on backend and frontend services.

### Deploy Backend
```bash
node scripts/deploy-backend.js
```
Triggers a backend deployment to Render with cache clearing.

### Deploy Frontend
```bash
node scripts/deploy-frontend.js
```
Deploys frontend to Vercel in production mode.

### Verify Environment
```bash
node scripts/verify-env.js
```
Validates that all required environment variables are set.

## Environment Variables

See `.env.template` for a complete list of required and optional variables.

### Required Variables
```
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
PAYPAL_CLIENT_ID
PAYPAL_SECRET
STRIPE_SECRET_KEY
FRONTEND_URL
BACKEND_URL
SENTRY_DSN
HEALTHCHECKS_URL
ENVIRONMENT
```

### Deployment Variables
```
RENDER_API_KEY
RENDER_SERVICE_ID
VERCEL_TOKEN
VERCEL_PROJECT_ID
VERCEL_ORG_ID
```

## Scheduled Automation

### Using Cron

Add to your crontab for scheduled sweeps:

```bash
# Daily sweep at 2 AM
0 2 * * * cd /path/to/AetherCrown20 && npm run sweep >> /tmp/sweep.log 2>&1

# Health check every 15 minutes
*/15 * * * * cd /path/to/AetherCrown20 && npm run health-check >> /tmp/health.log 2>&1
```

### Using PM2

For continuous monitoring with PM2:

```bash
# Install PM2 globally
npm install -g pm2

# Start sweep as a cron job (daily at 2 AM)
pm2 start ai-agent-sweep.js --name "aether-sweep" --cron "0 2 * * *"

# Or run continuously with restart on changes
pm2 start ai-agent-sweep.js --name "aether-sweep" --watch
```

## CI/CD Integration

### GitHub Actions

The automation scripts integrate with existing GitHub Actions workflows:

- **Auto-Fix & Deploy** (`.github/workflows/auto-fix-deploy.yml`)
- **CI/CD Pipeline** (`.github/workflows/ci.yml`)

### Manual Trigger

You can manually trigger the automation in CI/CD:

```yaml
- name: Run AI Sweep
  run: |
    npm install
    node ai-agent-sweep.js
  env:
    BACKEND_URL: ${{ secrets.BACKEND_URL }}
    FRONTEND_URL: ${{ secrets.FRONTEND_URL }}
    # ... other environment variables
```

## Monitoring and Reports

### Report Format

The sweep generates a JSON report with:

```json
{
  "timestamp": "2024-10-23T04:00:00.000Z",
  "environment": "production",
  "checks": [...],
  "errors": [...],
  "fixes": [...],
  "warnings": [...],
  "summary": {
    "totalChecks": 50,
    "errors": 2,
    "fixes": 5,
    "warnings": 3,
    "environment": "production"
  }
}
```

### Report Location

Reports are saved to `/tmp/sweep-report-[timestamp].json`

### Health Check Integration

If `HEALTHCHECKS_URL` is set, reports are automatically sent to your health monitoring service (e.g., healthchecks.io).

## Troubleshooting

### Common Issues

#### "Missing environment variables"
**Solution:** Copy `.env.template` to `.env` and fill in your values, or set them in your shell/CI environment.

#### "Backend unhealthy"
**Solution:** The script will automatically attempt to redeploy. Check Render logs for detailed errors.

#### "Vercel deploy failed"
**Solution:** Ensure `VERCEL_TOKEN` is set and valid. Verify Vercel CLI is installed: `npm install -g vercel`

#### "PM2 not found"
**Solution:** Install PM2 globally: `npm install -g pm2`, or the script will skip agent restart.

### Debug Mode

For verbose logging, set:
```bash
LOG_LEVEL=DEBUG node ai-agent-sweep.js
```

## Best Practices

1. **Environment Management**
   - Keep `.env` files secure and never commit them
   - Use GitHub Secrets for CI/CD variables
   - Regularly rotate API keys and tokens

2. **Monitoring**
   - Set up `HEALTHCHECKS_URL` for external monitoring
   - Review sweep reports regularly
   - Set up alerts for critical errors

3. **Deployment**
   - Test automation scripts in development first
   - Run sweeps during low-traffic periods
   - Keep backups before major deployments

4. **Security**
   - Never expose sensitive data in logs
   - Use service role keys appropriately
   - Implement rate limiting on automation endpoints

## Contributing

When adding new automation features:

1. Follow existing script structure
2. Add comprehensive error handling
3. Log all actions with appropriate levels
4. Update this documentation
5. Test in development environment first

## Support

For issues or questions:
- Check the troubleshooting section above
- Review generated sweep reports
- Open an issue on GitHub
- Contact the development team

## License

See main repository LICENSE file.
