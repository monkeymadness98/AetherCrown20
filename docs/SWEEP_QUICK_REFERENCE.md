# AI Agent Sweep - Quick Reference

## Common Commands

```bash
# Run basic sweep
python backend/sweep_cli.py

# With auto-fix
python backend/sweep_cli.py --auto-fix

# Save to file
python backend/sweep_cli.py --output report.md

# JSON format
python backend/sweep_cli.py --format json

# Verbose mode
python backend/sweep_cli.py --verbose

# All options combined
python backend/sweep_cli.py --auto-fix --format markdown --output sweep.md --verbose
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sweep/status` | GET | Quick status check |
| `/sweep/run` | POST | Start full sweep |
| `/sweep/report` | GET | Get latest report |
| `/healthz` | GET | Backend health check |

### cURL Examples

```bash
# Get status
curl http://localhost:8000/sweep/status

# Run sweep
curl -X POST http://localhost:8000/sweep/run?auto_fix=false

# Get report
curl http://localhost:8000/sweep/report?format=json
```

## Python Usage

```python
import asyncio
from backend.sweep import SweepAgent

# Basic usage
async def main():
    agent = SweepAgent(auto_fix=False)
    report = await agent.run_full_sweep()
    print(report.to_markdown())

asyncio.run(main())
```

## Environment Variables

### Required
- `DATABASE_URL`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_SECRET`
- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`

### Optional
- `VERCEL_TOKEN`
- `VERCEL_PROJECT_ID`
- `BACKEND_URL`
- `FRONTEND_URL`
- `REDIS_URL`
- `STRIPE_API_KEY`

## Checklist Categories

✅ **Deployment & Connectivity**
- Backend (Render) deployment status
- Frontend (Vercel) deployment status
- Health endpoint checks
- API connectivity

✅ **Environment Variables**
- Required variables validation
- Optional variables check
- Format validation

✅ **Dependencies**
- Outdated packages detection
- Version conflicts
- Security vulnerabilities

✅ **AI Agent Tasks**
- Running status
- Stale lock detection
- Process health

✅ **Database & Services**
- Database connectivity
- PayPal integration
- Stripe integration

✅ **Frontend & UI**
- Route accessibility
- Static files
- Component rendering

## Exit Codes

- `0` - Success, no errors found
- `1` - Errors detected (check report)

## Report Sections

1. **Summary** - Error and warning counts
2. **Deployment Status** - Service health
3. **Connection Health** - API and database
4. **AI Agent Status** - Running tasks
5. **Database Status** - Connectivity
6. **Payment Status** - Integration health
7. **UI Status** - Frontend health
8. **Errors** - Detailed error list
9. **Warnings** - Non-critical issues
10. **Fixes Applied** - Auto-fix results

## Auto-Fix Capabilities

### ✅ Safe (Always Enabled)
- Remove stale lock files
- Clear Redis cache
- Set session environment variables

### ⚠️ Requires Configuration
- Update dependencies (`AUTO_UPDATE_DEPENDENCIES=true`)
- Service restarts (deployment-dependent)
- Frontend rebuild (requires tools)

## Troubleshooting

### Import Errors
```bash
pip install -r requirements.txt
pip install httpx pytest pytest-asyncio
```

### Connection Timeouts
- Check network connectivity
- Verify service URLs
- Increase timeout in checkers

### Missing Dependencies
```bash
# Install all dependencies
pip install fastapi uvicorn httpx sqlalchemy psycopg2-binary redis aiofiles gunicorn
```

## Testing

```bash
# Run all tests
pytest tests/test_sweep.py -v

# Run specific test
pytest tests/test_sweep.py::TestSweepReport::test_add_error -v

# With coverage
pytest tests/test_sweep.py --cov=backend.sweep --cov-report=html
```

## GitHub Actions

Trigger manual sweep:
1. Go to **Actions** tab
2. Select **Scheduled Sweep** workflow
3. Click **Run workflow**

## Scheduling

### Cron (Linux/Mac)
```bash
# Every 6 hours
0 */6 * * * cd /path/to/AetherCrown20 && python backend/sweep_cli.py --output /var/log/sweep/report.md
```

### Task Scheduler (Windows)
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily, repeat every 6 hours
4. Action: Start program
5. Program: `python`
6. Arguments: `backend/sweep_cli.py --output C:\logs\sweep\report.md`
7. Start in: `C:\path\to\AetherCrown20`

## Best Practices

1. ✅ Run sweeps regularly (at least daily)
2. ✅ Review reports for patterns
3. ✅ Test auto-fix in staging first
4. ✅ Keep dependencies updated
5. ✅ Rotate credentials regularly
6. ⚠️ Don't commit secrets
7. ⚠️ Use different credentials per environment
8. ⚠️ Monitor for exposed secrets

## Quick Health Check

```bash
# One-liner to check overall health
python backend/sweep_cli.py --format json | python -c "import sys, json; data = json.load(sys.stdin); print('✅ Healthy' if data['summary']['total_errors'] == 0 else f'❌ {data[\"summary\"][\"total_errors\"]} errors'); sys.exit(0 if data['summary']['total_errors'] == 0 else 1)"
```

## Support

- Documentation: `docs/SWEEP_GUIDE.md`
- Configuration: `docs/SWEEP_CONFIGURATION.md`
- Tests: `tests/test_sweep.py`
- Examples: Run with `--help` for usage

## Version

System Version: 1.0.0
Last Updated: 2025-10-23
