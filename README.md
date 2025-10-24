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

The backend application is configured for automatic deployment to Render.

#### Deployment Methods

**Option 1: Using render.yaml (Recommended)**

1. Connect your GitHub repository to Render:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Blueprint"
   - Connect your GitHub account and select the `monkeymadness98/AetherCrown20` repository
   - Render will automatically detect the `render.yaml` file and create the service

2. Configure environment variables in Render Dashboard:
   - Navigate to your service settings
   - Add the following environment variables:
     - `ENV`: `production`
     - `PAYPAL_CLIENT_ID`: Your PayPal client ID
     - `PAYPAL_SECRET`: Your PayPal secret key
     - `DATABASE_URL`: Your database connection string (if using a database)

3. Deploy:
   - Render will automatically build and deploy your application
   - The service will be available at the provided Render URL

**Option 2: Manual Setup**

1. Create a new Web Service on Render
2. Configure the following settings:
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 2 --log-level info`
   - **Plan**: Free (or choose your preferred plan)
3. Add environment variables as listed above

**Option 3: Using GitHub Actions (Automated CI/CD)**

The repository includes a GitHub Actions workflow that automatically deploys to Render on push to the main branch. To enable:

1. Add the following secrets to your GitHub repository:
   - `RENDER_API_KEY`: Your Render API key
   - `RENDER_SERVICE_ID`: Your Render service ID
2. Push to the main branch, and the deployment will trigger automatically

#### Health Check

Once deployed, verify your service is running by accessing:
- Health endpoint: `https://your-app.onrender.com/healthz`
- Clock endpoint: `https://your-app.onrender.com/clocks`

#### Troubleshooting

- **Build failures**: Check that all dependencies in `requirements.txt` are compatible
- **Start command issues**: Ensure gunicorn and uvicorn workers are properly installed
- **Port binding**: Render automatically sets the `$PORT` environment variable; ensure your app uses it
- **Environment variables**: Verify all required environment variables are set in Render Dashboard

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