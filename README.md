# AetherCrown20

AetherCrown20 is a two-part application: a Python backend and a Next.js frontend. This repository contains the backend in `backend/` and the frontend in `frontend/`.

Quickstart (local)

Backend
- Create and activate a virtual environment:
  - python3 -m venv .venv
  - source .venv/bin/activate
- Install dependencies:
  - pip install -r backend/requirements.txt
- Set environment variables (see `.env.example`) and run:
  - uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
- Health check: confirm `GET /health` or `/` returns 200.

Frontend
- cd frontend
- npm ci
- npm run dev
- Visit http://localhost:3000

Running tests
- Backend (if pytest present):
  - pip install -r backend/requirements-dev.txt
  - pytest -q
- Frontend (if tests present):
  - cd frontend
  - npm test or npm run test

Deployment recommendations

Backend (Render)
1. Ensure `backend/requirements.txt` exists and the app binds to `$PORT`.
   Example start command for FastAPI:
   - uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   Or with Gunicorn + Uvicorn worker:
   - gunicorn -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT
2. Create a Render Web Service and set the root to `backend` (if the service code is in that folder).
3. Add environment variables in the Render dashboard from the values listed in `.env.example`.
4. Add a Render Cron Job (or schedule) to run one-shot scripts in `backend/`, e.g. `python backend/empire_automation.py`.

Frontend (Vercel)
1. Import the repo in Vercel and set the Root Directory to `frontend` (if applicable).
2. Set environment variables in Vercel (do not use `NEXT_PUBLIC_` for secrets).
3. Vercel will build and deploy automatically using `npm run build`.

CI/CD guidance
- Add CI that runs tests and builds for both backend and frontend before deploying.
- Use GitHub Secrets for deployment tokens: `RENDER_API_KEY`, `RENDER_SERVICE_ID`, `VERCEL_TOKEN`.
- Trigger deploys only from `main` after successful build & tests.

Environment variables
- Use `.env.example` to document required env vars. Never commit real secrets.

Production checklist
- Run DB migrations as part of deploy (Alembic/Django migrations).
- Verify webhooks with signature checks and secrets stored in env vars.
- Ensure session & cookie security flags are set (Secure, HttpOnly, SameSite).
- Add monitoring (Sentry), structured logging, and health checks.
- Ensure cron/automation jobs are one-shot and idempotent, or implement distributed locks.
- Enable Dependabot or other dependency scanning.

Contributing
- Run tests and linters locally before opening a PR.
- Do not commit secrets or credentials to the repository.

License
- Add license information if applicable.