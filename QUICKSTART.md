# Quick Start Guide - AetherCrown20 AI Automation

Get up and running with AetherCrown20's AI agent automation in minutes.

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/monkeymadness98/AetherCrown20.git
cd AetherCrown20

# 2. Install dependencies
npm install
pip install -r requirements.txt

# 3. Set up environment
cp .env.template .env
# Edit .env with your credentials

# 4. Verify setup
npm run verify-env
```

## ⚡ Quick Commands

### Check System Health
```bash
npm run health-check
```

### Run Deployment Fix
```bash
npm run deploy-fix
```

### Run Full System Sweep
```bash
npm run sweep
```

### Deploy Services
```bash
# Deploy backend only
npm run deploy:backend

# Deploy frontend only
npm run deploy:frontend

# Deploy both
npm run deploy:all
```

## 🔧 Configuration Priority

### Minimum Required Variables
```env
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
ENVIRONMENT=development
```

### For Production Deployment
Add these to your `.env`:
```env
RENDER_API_KEY=your_key
RENDER_SERVICE_ID=your_id
VERCEL_TOKEN=your_token
```

### For Full Features
See `.env.template` for all available options.

## 📊 What Each Command Does

### `npm run deploy-fix`
Fast recovery script that:
- ✅ Loads missing env vars from `.env`
- ✅ Checks backend health
- ✅ Redeploys if needed
- ✅ Updates dependencies
- ✅ Redeploys frontend
- ✅ Validates connections
- ✅ Restarts AI agents

**Use when:** Quick fix needed, deployment issues

### `npm run sweep`
Comprehensive automation that:
- ✅ All features from `deploy-fix`
- ✅ Database connectivity checks
- ✅ Payment provider validation
- ✅ UI/Dashboard verification
- ✅ Generates detailed JSON report
- ✅ Sends to monitoring service

**Use when:** Full system check, scheduled maintenance

### `npm run health-check`
Simple health verification:
- ✅ Backend `/healthz` endpoint
- ✅ Frontend accessibility
- ✅ Quick status overview

**Use when:** Quick status check, monitoring integration

## 🔄 Scheduled Automation

### Option 1: Cron (Linux/Mac)
```bash
# Set up daily sweep at 2 AM
./scripts/schedule-sweep.sh --cron
```

### Option 2: PM2 (Cross-platform)
```bash
# Set up with PM2
./scripts/schedule-sweep.sh --pm2

# View status
pm2 status

# View logs
pm2 logs aether-sweep
```

### Option 3: GitHub Actions
Already configured! Check `.github/workflows/scheduled-sweep.yml`

## 🐛 Troubleshooting

### "Missing environment variables"
```bash
# Check what's missing
npm run verify-env

# Copy template and fill in values
cp .env.template .env
nano .env
```

### "Backend unhealthy"
The automation will try to fix this automatically. If it persists:
1. Check Render dashboard for errors
2. Review backend logs
3. Verify environment variables in Render

### "Vercel deploy failed"
```bash
# Install Vercel CLI
npm install -g vercel

# Test manually
vercel --prod --confirm
```

### "PM2 not found"
```bash
# Install PM2 globally
npm install -g pm2
```

## 📖 Learn More

- **Full Documentation**: [AUTOMATION.md](AUTOMATION.md)
- **Environment Setup**: [.env.template](.env.template)
- **Main README**: [README.md](README.md)

## 🎯 Common Workflows

### Local Development
```bash
# 1. Start backend
uvicorn backend.main:app --reload

# 2. Run health check
npm run health-check

# 3. Make changes...

# 4. Test automation
npm run deploy-fix
```

### Production Deployment
```bash
# 1. Update code
git pull origin main

# 2. Install dependencies
npm install
pip install -r requirements.txt

# 3. Deploy everything
npm run deploy:all

# 4. Verify
npm run health-check
```

### Emergency Recovery
```bash
# Quick fix and redeploy
npm run deploy-fix

# If that doesn't work, full sweep
npm run sweep

# Check the report
cat /tmp/sweep-report-*.json | tail -1 | jq '.'
```

## 🔐 Security Notes

- **Never commit** `.env` files
- Store secrets in GitHub Secrets for CI/CD
- Use service role keys appropriately
- Regularly rotate API keys

## 💡 Pro Tips

1. **Set up health monitoring**: Configure `HEALTHCHECKS_URL` for external monitoring
2. **Use Sentry**: Set `SENTRY_DSN` for error tracking
3. **Schedule sweeps**: Run daily to catch issues early
4. **Review reports**: Check `/tmp/sweep-report-*.json` for insights
5. **Test locally first**: Always test with `ENVIRONMENT=development`

## 🆘 Need Help?

- Check logs: `/tmp/sweep.log`, `/tmp/health.log`
- Review reports: `/tmp/sweep-report-*.json`
- See full docs: [AUTOMATION.md](AUTOMATION.md)
- Open an issue on GitHub

---

**Ready to automate?** Run `npm run sweep` and let the AI agent do the work! 🤖
