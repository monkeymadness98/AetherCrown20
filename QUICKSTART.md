# Quick Start Guide - AetherCrown20

Get AetherCrown20 up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Git
- curl (for testing)

## Local Development Setup

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/monkeymadness98/AetherCrown20.git
cd AetherCrown20

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Minimum required for local development:
# - ENV=development
# - DEBUG=True
# - PORT=8000
```

### 3. Run Backend

```bash
# Start the backend server
python backend/main.py

# Server will start on http://localhost:8000
```

### 4. Test Backend

```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/healthz

# Expected response:
# {"ok": true, "env": "development"}

# Test API endpoint
curl http://localhost:8000/clocks

# Expected response:
# {"message": "Backend is alive and connected."}
```

### 5. View API Documentation

Open your browser and visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

### Quick Deploy to Render + Vercel

1. **Fork this repository** to your GitHub account

2. **Set up Render**
   - Go to https://dashboard.render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Add environment variables (see DEPLOYMENT_GUIDE.md)
   - Click "Create Web Service"

3. **Set up Vercel**
   - Go to https://vercel.com/dashboard
   - Click "New Project"
   - Import your GitHub repository
   - Add environment variables (see DEPLOYMENT_GUIDE.md)
   - Click "Deploy"

4. **Configure GitHub Actions**
   - Go to repository Settings → Secrets and variables → Actions
   - Add required secrets (see DEPLOYMENT_GUIDE.md)
   - Push to main branch to trigger deployment

5. **Verify Deployment**
   ```bash
   # Run verification script
   ./verify-deployment.sh
   ```

## Testing the Frontend

The repository includes a static HTML frontend:

### Local Testing

```bash
# Option 1: Python HTTP server
python3 -m http.server 8080

# Option 2: Using Node.js (if installed)
npx http-server -p 8080

# Open browser: http://localhost:8080
```

### Features
- ✨ Futuristic Todo app with neon UI
- 💾 localStorage persistence
- 🏷️ Tags and due dates
- 🔍 Filters (All, Active, Completed, Overdue)
- 🔄 Drag and drop

## Common Commands

### Backend

```bash
# Start backend
python backend/main.py

# Check health
curl http://localhost:8000/healthz

# View logs with reload
uvicorn backend.main:app --reload --log-level debug
```

### Deployment

```bash
# Check deployment status
./verify-deployment.sh

# Run health check
./healthcheck.sh

# Manual Vercel deploy
vercel --prod
```

### Testing

```bash
# Run Python linter
flake8 backend/ --max-line-length=127

# Check Python code
python -c "from backend.main import app; print('OK')"

# Validate YAML files
python -c "import yaml; yaml.safe_load(open('render.yaml')); print('OK')"
```

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check for errors
python backend/main.py
```

### Health check fails

```bash
# Check if server is running
curl http://localhost:8000/healthz

# Check logs
python backend/main.py
# Look for errors in output

# Verify port
netstat -an | grep 8000
```

### Import errors

```bash
# Ensure you're in the right directory
pwd  # Should be /path/to/AetherCrown20

# Check Python path
python -c "import sys; print(sys.path)"

# Try running from repo root
cd /path/to/AetherCrown20
python backend/main.py
```

## Environment Variables Quick Reference

### Required for Local Development
```bash
ENV=development
DEBUG=True
PORT=8000
```

### Required for Production
```bash
ENV=production
PORT=10000
PAYPAL_CLIENT_ID=xxx
PAYPAL_SECRET=xxx
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
STRIPE_SECRET_KEY=sk_xxx
SENTRY_DSN=https://xxx@sentry.io/xxx
SECRET_KEY=your-secret-key-32-chars-min
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

### Optional
```bash
REDIS_URL=redis://localhost:6379/0
HEALTHCHECKS_PING_URL=https://hc-ping.com/xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## Next Steps

1. ✅ Backend running locally
2. ✅ Health check passing
3. 📖 Read [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for production deployment
4. 🔧 Configure integrations (Supabase, PayPal, Stripe)
5. 📊 Set up monitoring (Sentry, Healthchecks.io)
6. 🚀 Deploy to production

## Resources

- **Documentation**: See README.md and DEPLOYMENT_GUIDE.md
- **API Docs**: http://localhost:8000/docs
- **GitHub**: https://github.com/monkeymadness98/AetherCrown20
- **Issues**: https://github.com/monkeymadness98/AetherCrown20/issues

## Support

If you encounter issues:

1. Check [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) troubleshooting section
2. Review backend logs for errors
3. Verify environment variables are set correctly
4. Check GitHub Issues for similar problems
5. Create a new issue with error details

---

**Happy coding! 🚀**
