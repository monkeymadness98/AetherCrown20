# AetherCrown — Monorepo

This repository contains the AetherCrown application scaffold (backend + frontend + automation) and CI/CD configuration for Render (backend) and Vercel (frontend).

Contents
- backend/        — FastAPI backend (uvicorn)
- frontend/       — Next.js 14 frontend
- render.yaml     — Render service & cron configuration
- vercel.json     — Vercel monorepo configuration (build frontend)
- .github/        — GitHub Actions workflows (CI and deploy)
- .env.example    — Environment variable template

Quickstart — local (backend)
1. cd backend
2. python -m venv .venv
3. source .venv/bin/activate   # Windows: .venv\Scripts\activate
4. pip install -r requirements.txt
5. uvicorn main:app --reload --port 8000
6. Verify: curl -i http://localhost:8000/health

Quickstart — local (frontend)
1. cd frontend
2. Use Node 18.17.0+ (Next 14 requires Node >= 18.17.0)
3. npm ci
4. npm run dev
5. Verify: http://localhost:3000

Environment variables
See .env.example for the complete list. Key variables to set in production:
- NEXT_PUBLIC_API_URL — frontend base API (e.g. https://api.example.com)
- NEXT_PUBLIC_PAYPAL_CLIENT_ID — PayPal client id (public)
- PAYPAL_SECRET — PayPal secret (server-only)
- DATABASE_URL — production DB connection string (backend)
- RENDER_API_KEY, VERCEL_TOKEN — CI/CD deploy tokens (GitHub Actions secrets)

Deployment
- Render: Use render.yaml to provision a web service (backend) and a cron job (empire_automation.py). Set RENDER_API_KEY and any runtime env vars in Render.
- Vercel: Configure a project with Root Directory set to `frontend` (monorepo). Add NEXT_PUBLIC_* and server secrets in Project Settings.

CI/CD
- `.github/workflows/ci.yml` runs frontend builds and backend checks on push & PR.
- `.github/workflows/deploy.yml` can deploy to Render & Vercel on push to `main` (requires repository secrets).

Notes & recommendations
- Regenerate frontend package-lock.json locally: cd frontend && npm ci && git add package-lock.json && commit.
- Validate Node version (match Vercel / local) and Python version (Render).
- After merge, verify Vercel & Render deployments and test the `/api/health` and `/api/create-order` endpoints.

Contributing
- Follow the branch / PR rules: create feature branches, include tests, run linter and build locally before opening PRs.
