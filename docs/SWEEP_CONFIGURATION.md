# AI Agent Sweep Configuration Guide

## Environment Variables

### Required Variables

These variables must be set for core functionality:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Payment Integration
PAYPAL_CLIENT_ID=your_paypal_client_id_here
PAYPAL_SECRET=your_paypal_secret_here

# Render Deployment
RENDER_API_KEY=rnd_xxxxxxxxxxxxxxxxxxxx
RENDER_SERVICE_ID=srv-xxxxxxxxxxxxxxxxxxxx
```

### Optional Variables

These enhance sweep capabilities but are not required:

```bash
# Vercel Deployment (for frontend checks)
VERCEL_TOKEN=your_vercel_token_here
VERCEL_PROJECT_ID=prj_xxxxxxxxxxxxxxxxxxxx
VERCEL_ORG_ID=team_xxxxxxxxxxxxxxxxxxxx

# Service URLs (for health checks)
BACKEND_URL=https://your-backend.render.com
FRONTEND_URL=https://your-frontend.vercel.app

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# Stripe Integration
STRIPE_API_KEY=sk_test_xxxxxxxxxxxxxxxxxxxx

# Security
SECRET_KEY=your_jwt_secret_key_here

# PayPal Mode
PAYPAL_MODE=sandbox  # or 'live' for production

# AI Agent Configuration
EMPIRE_AUTOMATION_ENABLED=true
EMPIRE_LOCK_TIMEOUT=300

# Auto-fix Configuration
AUTO_UPDATE_DEPENDENCIES=false  # Set to true to enable automatic package updates
```

## Configuration Files

### .env File Example

Create a `.env` file in the project root:

```bash
# Copy from .env.example
cp .env.example .env

# Edit with your values
nano .env
```

### Docker Environment

For Docker deployments, use `docker-compose.yml`:

```yaml
version: '3.8'
services:
  backend:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - PAYPAL_CLIENT_ID=${PAYPAL_CLIENT_ID}
      - PAYPAL_SECRET=${PAYPAL_SECRET}
      - RENDER_API_KEY=${RENDER_API_KEY}
      - RENDER_SERVICE_ID=${RENDER_SERVICE_ID}
    env_file:
      - .env
```

### GitHub Actions Secrets

Configure secrets in GitHub repository settings:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each required variable

Required secrets for CI/CD:
- `DATABASE_URL`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_SECRET`
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`
- `VERCEL_TOKEN` (optional)
- `VERCEL_PROJECT_ID` (optional)

## Render Configuration

### Environment Variables in Render Dashboard

1. Go to your service in Render Dashboard
2. Navigate to **Environment** tab
3. Add each variable:
   - Click **Add Environment Variable**
   - Enter key and value
   - Click **Save**

### render.yaml Configuration

Update `render.yaml` to include all required variables:

```yaml
services:
  - type: web
    name: aethercrown20-backend
    env: python
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: PAYPAL_CLIENT_ID
        sync: false
      - key: PAYPAL_SECRET
        sync: false
      - key: RENDER_API_KEY
        sync: false
      - key: RENDER_SERVICE_ID
        sync: false
```

## Vercel Configuration

### Using Vercel CLI

```bash
# Add environment variables
vercel env add DATABASE_URL production
vercel env add PAYPAL_CLIENT_ID production
vercel env add PAYPAL_SECRET production

# Or add via vercel.json
```

### vercel.json Example

```json
{
  "env": {
    "DATABASE_URL": "@database-url",
    "PAYPAL_CLIENT_ID": "@paypal-client-id",
    "PAYPAL_SECRET": "@paypal-secret"
  }
}
```

## Local Development

### Using python-dotenv

The backend automatically loads `.env` in non-production environments:

```python
# backend/main.py handles this automatically
if ENV != "production":
    from dotenv import load_dotenv
    load_dotenv()
```

### Setting Environment Variables Manually

```bash
# Linux/Mac
export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
export PAYPAL_CLIENT_ID="your_client_id"

# Windows PowerShell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
$env:PAYPAL_CLIENT_ID="your_client_id"

# Windows CMD
set DATABASE_URL=postgresql://user:password@localhost:5432/dbname
set PAYPAL_CLIENT_ID=your_client_id
```

## Security Best Practices

### 1. Never Commit Secrets

Ensure `.env` is in `.gitignore`:

```bash
# Check .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

### 2. Use Different Keys per Environment

- **Development**: Use sandbox/test credentials
- **Staging**: Use separate test credentials
- **Production**: Use production credentials only

### 3. Rotate Keys Regularly

Schedule regular key rotation:
- PayPal credentials: Every 90 days
- API tokens: Every 30-90 days
- Database passwords: As needed

### 4. Limit Access

- Use read-only credentials where possible
- Apply principle of least privilege
- Use service accounts with minimal permissions

### 5. Monitor for Exposed Secrets

Use tools like:
- `git-secrets`
- `truffleHog`
- GitHub secret scanning

## Validation

### Check Configuration

Run the sweep to validate configuration:

```bash
python backend/sweep_cli.py --verbose
```

### Environment Variable Checker

Create a simple checker script:

```python
import os

required_vars = [
    'DATABASE_URL',
    'PAYPAL_CLIENT_ID',
    'PAYPAL_SECRET',
    'RENDER_API_KEY',
    'RENDER_SERVICE_ID',
]

missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f"❌ Missing required variables: {', '.join(missing)}")
    exit(1)
else:
    print("✅ All required environment variables are set")
```

## Troubleshooting

### Common Issues

1. **"Missing RENDER_API_KEY"**
   - Ensure variable is set in Render dashboard
   - Check for typos in variable name
   - Redeploy service after adding variable

2. **"Database connection failed"**
   - Verify DATABASE_URL format
   - Check database server is running
   - Verify network connectivity
   - Check credentials are correct

3. **"PayPal integration unconfigured"**
   - Ensure both CLIENT_ID and SECRET are set
   - Verify credentials are for correct mode (sandbox/live)
   - Check credentials are not expired

### Debug Commands

```bash
# Check if variables are set
env | grep -E 'DATABASE_URL|PAYPAL|RENDER|VERCEL'

# Test database connection
python -c "import os; from sqlalchemy import create_engine; engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✅ Database connected')"

# Run sweep with verbose output
python backend/sweep_cli.py --verbose --format markdown
```

## Production Checklist

Before deploying to production:

- [ ] All required environment variables are set
- [ ] Credentials use production values (not sandbox/test)
- [ ] Database connection tested and working
- [ ] Payment integrations tested
- [ ] API keys are valid and not expired
- [ ] Secrets are not committed to version control
- [ ] `.env` file is in `.gitignore`
- [ ] GitHub Actions secrets are configured
- [ ] Render environment variables are set
- [ ] Vercel environment variables are set (if used)
- [ ] Sweep report shows no critical errors

## Maintenance

### Regular Tasks

**Weekly:**
- Review sweep reports for new warnings
- Check for outdated dependencies

**Monthly:**
- Verify all credentials are still valid
- Review and update optional configurations
- Check for security advisories

**Quarterly:**
- Rotate sensitive credentials
- Review and update environment variable documentation
- Audit access to production secrets

## Additional Resources

- [Render Environment Variables](https://render.com/docs/environment-variables)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
