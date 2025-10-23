# AetherCrown20

A comprehensive automation platform for empire management with PayPal integration and deployment automation.

## Features

- **Backend API**: FastAPI-based backend with uvicorn server
- **Empire Automation**: One-shot automation script for empire management tasks
- **Payment Integration**: PayPal and Stripe integration for payment processing
- **Deployment Automation**: CI/CD pipelines for Render and Vercel deployments
- **AI Agent Sweep**: Comprehensive automation system for deployment, monitoring, and auto-fixing
- **Health Monitoring**: Automated health checks and recovery mechanisms
- **Environment Management**: Automatic environment variable validation and loading

## Prerequisites

- Python 3.8+
- Node.js 14+ (for automation scripts and frontend)
- PayPal Developer Account
- Stripe Account
- Render Account
- Vercel Account
- Supabase Account (for database)

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

3. Install Node.js dependencies (for automation scripts):
```bash
npm install
```

4. Copy the example environment file:
```bash
cp .env.template .env
```

5. Configure your environment variables in `.env` (see `.env.template` for all options)

6. Verify your environment setup:
```bash
npm run verify-env
```

## Configuration

Create a `.env` file based on `.env.template` and configure the following:

- **URLs**: `BACKEND_URL`, `FRONTEND_URL`
- **Database (Supabase)**: `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
- **Payment Providers**: `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`, `STRIPE_SECRET_KEY`
- **Deployment Keys**: `RENDER_API_KEY`, `RENDER_SERVICE_ID`, `VERCEL_TOKEN`
- **Monitoring**: `SENTRY_DSN`, `HEALTHCHECKS_URL`
- **Environment**: `ENVIRONMENT` (development, staging, or production)

See `.env.template` for a complete list of all configuration options.

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

## AI Agent Automation System

AetherCrown20 includes a comprehensive AI agent automation system for deployment, monitoring, and auto-fixing. See [AUTOMATION.md](AUTOMATION.md) for detailed documentation.

### Quick Start with Automation

#### Run a Quick Deployment Fix
```bash
npm run deploy-fix
```

#### Run a Full System Sweep
```bash
npm run sweep
```

#### Check System Health
```bash
npm run health-check
```

#### Deploy Services
```bash
# Deploy backend to Render
npm run deploy:backend

# Deploy frontend to Vercel
npm run deploy:frontend

# Deploy both
npm run deploy:all
```

### Automation Features

- **Environment Verification**: Automatic validation and loading of environment variables
- **Health Monitoring**: Continuous health checks with auto-recovery
- **Dependency Management**: Automatic installation and updates
- **Deployment Automation**: One-command deployment to Render and Vercel
- **Error Detection**: Automatic detection and fixing of common issues
- **Comprehensive Reporting**: Detailed JSON reports of all operations
- **Scheduled Sweeps**: GitHub Actions workflow for daily automated checks

For complete automation documentation, see [AUTOMATION.md](AUTOMATION.md).

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

## Todo App

The repository now includes a **Futuristic Todo 2030** application with neon/glassmorphism UI design. See the deployment section above for instructions on how to deploy to GitHub Pages or run locally.