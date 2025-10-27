# AetherCrown20

A comprehensive automation platform for empire management with PayPal integration and deployment automation.

## 🚀 Quick Start

**New to the project?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide.

## Features

- **Backend API**: FastAPI-based backend with uvicorn server
- **Empire Automation**: One-shot automation script for empire management tasks
- **Payment Integration**: PayPal client integration for payment processing
- **Deployment Automation**: CI/CD pipelines for Render and Vercel deployments
- **Health Monitoring**: Automated health checks and status reporting
- **Multi-Platform**: Integrated deployment across Render, Vercel, and Supabase

## Prerequisites

- Python 3.8+
- Node.js 14+ (for monitoring and frontend)
- **Platform Accounts:**
  - PayPal Developer Account
  - Render Account
  - Vercel Account
  - Supabase Account
  - OpenAI API Account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/monkeymadness98/AetherCrown20.git
cd AetherCrown20
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example environment file:
```bash
cp .env.example .env
```

4. Configure your environment variables in `.env`

## Configuration

Create a `.env` file based on `.env.example` and configure the following:

- **PayPal Credentials**: `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`
- **Deployment Keys**: `RENDER_API_KEY`, `RENDER_SERVICE_ID`, `VERCEL_TOKEN`
- **Database**: Connection strings and credentials
- **API Keys**: External service API keys

## Running the Application

### Start the Backend Server

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

### Running Empire Automation

The empire automation script can be run as a one-shot task:

```bash
python backend/empire_automation.py
```

**Note**: Ensure that `backend/empire_automation.py` has proper locking mechanism if running concurrently or is designed as a one-shot script.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

### GitHub Pages Deployment

The Futuristic Todo 2030 UI can be deployed to GitHub Pages for free hosting:

#### Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** > **Pages** (in the left sidebar)
3. Under **Source**, select the branch you want to deploy (e.g., `main` or `chore/add-ui-features`)
4. Select **/ (root)** as the folder
5. Click **Save**
6. GitHub will provide you with a URL where your site is published (usually `https://<username>.github.io/<repository-name>/`)

#### Local Development Server

To test the Todo application locally before deploying:

**Option 1: Using Python's built-in HTTP server**
```bash
# Navigate to the repository root
cd AetherCrown20

# Start a local server on port 8000
python3 -m http.server 8000
```

**Option 2: Using Node.js http-server**
```bash
# Install http-server globally (one-time setup)
npm install -g http-server

# Navigate to the repository root
cd AetherCrown20

# Start the server
http-server -p 8000
```

**Option 3: Using VS Code Live Server Extension**
- Install the "Live Server" extension in VS Code
- Right-click on `index.html` and select "Open with Live Server"

Once the server is running, open your browser and navigate to:
- `http://localhost:8000` (or the port you specified)

The Todo application will load with all its features including:
- ✨ Futuristic neon/glassmorphism UI
- 📅 Due dates for tasks
- 🏷️ Tags for organization
- 💾 localStorage persistence (data saved in your browser)
- 🔄 Drag and drop to reorder tasks
- 🔍 Filters (All, Active, Completed, Overdue)

### Render Deployment

The backend application is configured for automatic deployment to Render via GitHub Actions.

### Vercel Deployment

Backend deployment to Vercel is handled through the CI/CD pipeline.

## CI/CD

GitHub Actions workflows are configured in `.github/workflows/ci.yml` for:
- Automated testing
- Code quality checks
- Deployment to Render (backend)
- Deployment to Vercel (frontend)

### Required GitHub Secrets

Configure the following secrets in your GitHub repository settings:

- `RENDER_API_KEY`: Render API key for deployment
- `RENDER_SERVICE_ID`: Render service ID
- `VERCEL_TOKEN`: Vercel authentication token
- `PAYPAL_CLIENT_ID`: PayPal client ID
- `PAYPAL_SECRET`: PayPal secret key
- Additional service credentials as needed

## Development

### Project Structure

```
AetherCrown20/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── empire_automation.py # Empire automation script
│   └── ...
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD pipeline configuration
├── .env.example             # Example environment variables
├── .gitignore
└── README.md
```

### Important Notes for Maintainers

1. **Backend Entry Point**: Ensure that `backend/main.py` exports an `app` object (FastAPI instance) for uvicorn to run
2. **Empire Automation**: Verify that `backend/empire_automation.py` is either:
   - A one-shot script that runs to completion, OR
   - Has proper locking mechanism to prevent concurrent execution issues

## Testing

```bash
pytest
```

## License

[Specify your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions, please open an issue on GitHub.

---

## Empire Infrastructure Overview

### 🏗️ Architecture

The Aether AI Empire stack is a fully automated, multi-platform deployment system spanning:

```
GitHub (Source Control & CI/CD)
    ↓
    ├─→ Render (Backend API)
    │   └─→ https://aetherai-8wcw.onrender.com
    │
    ├─→ Vercel (Frontend/Next.js)
    │   └─→ [Your Vercel App URL]
    │
    └─→ Supabase (Database & Edge Functions)
        └─→ Edge Function: aether-sync
```

### 🔗 Key Platforms

| Platform | Purpose | URL/Dashboard |
|----------|---------|---------------|
| **Render** | Backend API & Services | https://dashboard.render.com/ |
| **Vercel** | Frontend Deployment | https://vercel.com/dashboard |
| **Supabase** | Database & Edge Functions | https://app.supabase.com/ |
| **OpenAI** | AI/ML Services | https://platform.openai.com/ |
| **PayPal** | Payment Processing | https://developer.paypal.com/ |

### 🚀 Deployment Flow

#### Automatic Deployments

1. **Push to `main` branch** triggers:
   - GitHub Actions CI/CD pipeline
   - Automated testing and linting
   - Parallel deployment to Render & Vercel

2. **Backend Changes** (files in `/backend`, `/api`, `/server`, `/functions`):
   - Triggers Render deployment workflow
   - Backend redeploys with zero-downtime
   - Health checks verify deployment

3. **Frontend/Config Changes**:
   - Triggers Vercel deployment workflow
   - Frontend builds and deploys to edge network

#### Manual Redeployment

**Render Backend:**
```bash
# Using Render API
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"clearCache": false}'

# Or use the GitHub Action
gh workflow run render-deploy.yml
```

**Vercel Frontend:**
```bash
# Using Vercel CLI
vercel --prod

# Or use the GitHub Action
gh workflow run vercel-deploy.yml
```

**Supabase Edge Functions:**
```bash
# Deploy edge function
supabase functions deploy aether-sync

# View logs
supabase functions logs aether-sync
```

### 📍 Key Endpoints

| Service | Endpoint | Purpose |
|---------|----------|---------|
| Render Backend | `/healthz` | Health check |
| Render Backend | `/clocks` | API status |
| Render Backend | `/_env_check` | Environment verification (temp) |
| Supabase | `/functions/v1/aether-sync` | Backend sync & AI summaries |
| Vercel | `/api/health` | Frontend health check |

### 🔍 Monitoring

**Automated Health Checks:**
- Runs daily at 00:00 UTC via GitHub Actions
- Checks all critical endpoints
- Logs results to `/logs/system_status.json`
- Alerts on failures

**Manual Health Check:**
```bash
# Run health checker locally
node monitoring/status-checker.js

# Or trigger via GitHub Actions
gh workflow run daily-health-check.yml
```

**View Logs:**
```bash
# View latest health check results
cat logs/system_status.json | jq '.checks[-1]'
```

### 🔐 Environment Variables

All services require proper environment configuration. See `.env.template` for the complete list of required variables.

**Critical Variables:**
- `OPENAI_API_KEY` - OpenAI API access
- `SUPABASE_URL` & `SUPABASE_ANON_KEY` - Supabase connection
- `DATABASE_URL` - PostgreSQL database
- `PAYPAL_CLIENT_ID` & `PAYPAL_SECRET` - Payment processing
- `RENDER_API_KEY` & `RENDER_SERVICE_ID` - Render deployments
- `VERCEL_TOKEN`, `VERCEL_PROJECT_ID`, `VERCEL_ORG_ID` - Vercel deployments

### 🔧 Troubleshooting

**Deployment Issues:**
1. Check GitHub Actions logs in the "Actions" tab
2. Verify environment variables are set in GitHub Secrets
3. Check platform-specific dashboards (Render/Vercel/Supabase)
4. Review health check logs in `/logs/system_status.json`

**Service Down:**
1. Run health checker: `node monitoring/status-checker.js`
2. Check service logs on respective platforms
3. Trigger manual redeployment if needed

**CI/CD Pipeline Fails:**
1. Review workflow logs in GitHub Actions
2. Ensure all required secrets are configured
3. Verify API tokens haven't expired
4. Check for rate limiting on external APIs

### 📊 Status Badges

![Render Deploy](https://github.com/monkeymadness98/AetherCrown20/workflows/Deploy%20to%20Render/badge.svg)
![Vercel Deploy](https://github.com/monkeymadness98/AetherCrown20/workflows/Deploy%20to%20Vercel/badge.svg)
![Health Check](https://github.com/monkeymadness98/AetherCrown20/workflows/Daily%20Health%20Check/badge.svg)
![CI/CD Pipeline](https://github.com/monkeymadness98/AetherCrown20/workflows/CI%2FCD%20Pipeline/badge.svg)

---

## Todo App

The repository now includes a **Futuristic Todo 2030** application with neon/glassmorphism UI design. See the deployment section above for instructions on how to deploy to GitHub Pages or run locally.