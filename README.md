# AetherCrown20

A comprehensive automation platform for empire management with PayPal integration and deployment automation.

## Features

- **Backend API**: FastAPI-based backend with uvicorn server
- **Dev Hub**: Internal developer dashboard for monitoring, debugging, and system management
  - API Documentation with interactive testing
  - Build and deployment status tracking
  - AI agent monitoring and control
  - Database analytics and event logs
  - Developer tools and one-click scripts
- **Empire Live**: External dashboard for business metrics and user engagement
  - Real-time business KPIs (revenue, users, AI tasks)
  - Payment and subscription tracking
  - Live AI activity feed
  - Marketing content and social metrics
  - Enterprise features and SLA monitoring
- **Empire Automation**: One-shot automation script for empire management tasks
- **Payment Integration**: PayPal client integration for payment processing
- **Deployment Automation**: CI/CD pipelines for Render and Vercel deployments
- **Monitoring**: Automated healthcheck system with 15-minute intervals

## Prerequisites

- Python 3.8+
- Node.js 14+ (for frontend, if applicable)
- PayPal Developer Account
- Render Account
- Vercel Account

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

### Access the Dashboards

Once the server is running, you can access:

- **Dev Hub (Internal)**: `http://localhost:8000/dev/index.html`
  - API Documentation: `/dev/api-docs.html`
  - Build Logs: `/dev/logs.html`
  - AI Agents: `/dev/ai-agents.html`
  - Analytics: `/dev/analytics.html`
  - Developer Tools: `/dev/tools.html`

- **Empire Live (External)**: `http://localhost:8000/live/index.html`
  - Business Metrics: `/live/metrics.html`
  - Payments: `/live/payments.html`
  - AI Activity Feed: `/live/ai-feed.html`
  - Marketing: `/live/marketing.html`
  - Enterprise Features: `/live/enterprise.html`

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
- Dev Hub API Docs: `http://localhost:8000/dev/api-docs.html` (with interactive testing)

### API Endpoints

#### Dev Hub APIs
- `GET /api/dev/status` - System status (backend, database, Redis)
- `GET /api/dev/builds` - Recent builds and deployments
- `GET /api/dev/ai-agents` - AI agent status and metrics
- `GET /api/dev/analytics` - Database tables and events
- `GET /api/dev/logs` - Application logs

#### Live Dashboard APIs
- `GET /api/live/metrics` - Business metrics (revenue, users, AI tasks)
- `GET /api/live/payments` - Payment and subscription data
- `GET /api/live/ai-activity` - Real-time AI activity feed
- `GET /api/live/marketing` - Marketing content and social stats
- `GET /api/live/enterprise` - Enterprise features and SLA

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

## Developer Scripts

The `scripts/` directory contains utility scripts for common development and operations tasks:

```bash
# Deploy to staging environment
./scripts/deploy_staging.sh

# Reset sandbox database
./scripts/reset_sandbox_db.sh

# Refresh analytics data
./scripts/refresh_analytics.sh
```

**Note**: These scripts require appropriate environment variables to be set. See `.env.example` for required variables.

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

## Todo App

The repository now includes a **Futuristic Todo 2030** application with neon/glassmorphism UI design. See the deployment section above for instructions on how to deploy to GitHub Pages or run locally.