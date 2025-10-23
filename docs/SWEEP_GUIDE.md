# AI Agent Sweep & Auto-Fix Guide

## Overview

The AI Agent Sweep & Auto-Fix system provides comprehensive health checks, diagnostics, and automated repair capabilities for the AetherCrown20 deployment.

## Features

- Deployment & connectivity checks (Render, Vercel, health endpoints)
- Environment variable validation
- Dependency management (version conflicts, auto-updates)
- AI agent task monitoring
- Database & payment service validation
- Frontend UI validation
- Comprehensive reporting

## Quick Start

```bash
# Run a complete system sweep
python backend/sweep_cli.py

# With auto-fix enabled
python backend/sweep_cli.py --auto-fix

# Save report to file
python backend/sweep_cli.py --output sweep_report.md
```

## API Endpoints

- `GET /sweep/status` - Quick status check
- `POST /sweep/run?auto_fix=false` - Run full sweep
- `GET /sweep/report?format=json` - Get latest report

## Configuration

Set required environment variables:
- DATABASE_URL
- PAYPAL_CLIENT_ID, PAYPAL_SECRET
- RENDER_API_KEY, RENDER_SERVICE_ID

See .env.example for full configuration options.

## Testing

```bash
pytest tests/test_sweep.py -v
```

For detailed documentation, see the full guide in this file.
