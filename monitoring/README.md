# Aether Empire Monitoring

This directory contains monitoring tools for the Aether AI Empire infrastructure.

## Environment Validator

The `env-validator.js` script validates that all required environment variables are configured.

### Usage

```bash
node monitoring/env-validator.js
```

This will:
- Check which variables are set in your local environment
- Generate a comprehensive checklist (`ENV_CHECKLIST.md`)
- Provide platform-specific configuration guidance
- List all required and optional variables

### Output

- Console report showing variable status
- `ENV_CHECKLIST.md` - Generated checklist for tracking setup progress

## Status Checker

The `status-checker.js` script monitors all critical services in the empire stack.

### Usage

**Run manually:**
```bash
node monitoring/status-checker.js
```

**Run with custom endpoints:**
```bash
SUPABASE_FUNCTION_URL=https://your-project.supabase.co/functions/v1/aether-sync \
VERCEL_APP_URL=https://your-app.vercel.app \
node monitoring/status-checker.js
```

**Automated via GitHub Actions:**
- Runs daily at 00:00 UTC
- Triggered by the `daily-health-check.yml` workflow
- Results stored in `/logs/system_status.json`

### Monitored Endpoints

**Note:** Update URLs in `status-checker.js` CONFIG section with your actual deployment URLs.

1. **Render Backend**
   - Health endpoint: `/healthz`
   - API endpoint: `/clocks`
   - Example: `https://your-app.onrender.com/healthz`

2. **Supabase Edge Function** (optional)
   - Edge Function: `/functions/v1/aether-sync`
   - Configure via `SUPABASE_FUNCTION_URL` environment variable

3. **Vercel Frontend** (optional)
   - Health endpoint: `/api/health`
   - Configure via `VERCEL_APP_URL` environment variable

### Output

Results are saved to `/logs/system_status.json` with the following structure:

```json
{
  "checks": [
    {
      "timestamp": "2025-10-27T00:00:00.000Z",
      "results": [
        {
          "name": "Render Backend Health",
          "url": "https://your-app.onrender.com/healthz",
          "status": "healthy",
          "statusCode": 200,
          "responseTime": 150,
          "timestamp": "2025-10-27T00:00:00.000Z",
          "type": "backend"
        }
      ],
      "summary": {
        "total": 4,
        "healthy": 3,
        "unhealthy": 0,
        "errors": 0,
        "skipped": 1
      }
    }
  ]
}
```

### Exit Codes

- `0` - All services healthy
- `1` - One or more services unhealthy or error occurred

### Configuration

Edit `status-checker.js` to add or modify endpoints in the `CONFIG.endpoints` array.

## Logs

Health check logs are stored in `/logs/system_status.json`:
- Keeps last 100 checks
- Automatically managed by the status checker
- Ignored by git (but directory is tracked)

## GitHub Actions Integration

The daily health check workflow:
- Runs the status checker
- Uploads results as artifacts
- Commits logs back to the repository
- Sends notifications on failures

Manual trigger:
```bash
gh workflow run daily-health-check.yml
```
