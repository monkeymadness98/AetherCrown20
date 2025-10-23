# AetherCrown20

A comprehensive automation platform for empire management with PayPal integration and deployment automation.

## Features

- **Backend API**: FastAPI-based backend with uvicorn server
- **Empire Automation**: One-shot automation script for empire management tasks
- **Payment Integration**: PayPal client integration for payment processing
- **Deployment Automation**: CI/CD pipelines for Render and Vercel deployments

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
- `RENDER_SERVICE_ID`: Your Render service ID
- `VERCEL_TOKEN`: Vercel authentication token
- `VERCEL_ORG_ID`: Vercel organization ID
- `VERCEL_PROJECT_ID`: Vercel project ID
- `DATABASE_URL`: PostgreSQL database connection string
- `PAYPAL_CLIENT_ID`: PayPal API client ID
- `PAYPAL_SECRET`: PayPal API secret
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anonymous key
- `STRIPE_SECRET_KEY`: Stripe secret API key
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `SENTRY_DSN`: Sentry error tracking DSN
- `HEALTHCHECKS_PING_URL`: Healthchecks.io monitoring URL
- `SECRET_KEY`: Application secret key for JWT/sessions

## Deployment Verification

After deployment, verify that everything is working correctly:

### Quick Health Check

```bash
curl https://aethercrown98-backend.onrender.com/healthz
```

Expected response:
```json
{"ok": true, "env": "production"}
```

### Comprehensive Verification

Run the verification script to check all components:

```bash
./verify-deployment.sh
```

Or manually check each component:

1. **Backend Health Check**
   ```bash
   curl https://aethercrown98-backend.onrender.com/healthz
   ```
   ✅ Should return HTTP 200 with `{"ok": true}`

2. **Backend API Endpoint**
   ```bash
   curl https://aethercrown98-backend.onrender.com/clocks
   ```
   ✅ Should return `{"message": "Backend is alive and connected."}`

3. **Environment Variables Check**
   ```bash
   curl https://aethercrown98-backend.onrender.com/_env_check
   ```
   ⚠️ Remove this endpoint in production (it's for verification only)

4. **Frontend Check**
   - Visit your Vercel URL
   - Open browser DevTools → Network tab
   - Verify API calls to backend succeed

### Troubleshooting

If deployment fails, check each layer systematically:

#### 1. GitHub Actions CI/CD
- Check workflow runs in GitHub Actions tab
- Look for errors in build logs, npm install, or pip install
- Verify all secrets are configured correctly

#### 2. Render Backend
- Visit: https://dashboard.render.com/
- Check service logs for errors
- Verify environment variables are set:
  - `ENV=production`
  - `PORT=10000` (or Render's auto-assigned port)
  - `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`
  - `DATABASE_URL`
  - All other required secrets

Common issues:
- ❌ Missing environment variables
- ❌ Port misconfiguration (should use `$PORT`)
- ❌ Dependency installation failures
- ❌ Python version mismatch

#### 3. Vercel Frontend
- Visit: https://vercel.com/dashboard
- Check deployment logs
- Verify environment variables:
  - `NEXT_PUBLIC_API_URL` → Points to Render backend
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

#### 4. Service Connections
Test each integration independently:

**Supabase**
```bash
curl -H "apikey: YOUR_SUPABASE_KEY" https://your-project.supabase.co/rest/v1/
```

**Backend → Supabase**
- Check backend logs for database connection errors
- Verify DATABASE_URL format: `postgresql://user:pass@host:port/dbname`

**Frontend → Backend**
- Open browser console
- Check for CORS errors
- Verify API URL is correct

### Monitoring

Set up continuous monitoring:

1. **Healthchecks.io** (recommended)
   - Sign up at https://healthchecks.io
   - Create a check and get your ping URL
   - Add to GitHub Secrets: `HEALTHCHECKS_PING_URL`
   - Run periodic health checks:
     ```bash
     ./healthcheck.sh
     ```

2. **Sentry** (error tracking)
   - Backend automatically reports errors if `SENTRY_DSN` is configured
   - Monitor at https://sentry.io

3. **Manual Verification**
   ```bash
   # Set environment variables
   export BACKEND_URL=https://aethercrown98-backend.onrender.com
   export FRONTEND_URL=https://your-app.vercel.app
   
   # Run verification
   ./verify-deployment.sh
   ```

### Deployment Order

For successful deployment:

1. **Backend First**: Deploy to Render, wait for health check ✅
2. **Verify Backend**: Run `curl $BACKEND_URL/healthz`
3. **Frontend Second**: Deploy to Vercel with backend URL
4. **Final Verification**: Test end-to-end functionality
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