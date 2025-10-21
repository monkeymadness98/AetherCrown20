# AetherCrown20

Enterprise automation and management platform with FastAPI backend and Next.js frontend.

## 🚀 Features

- **FastAPI Backend**: High-performance REST API with automatic documentation
- **Next.js Frontend**: Modern React-based frontend with TypeScript support
- **Empire Automation**: Cron-ready automation module for scheduled tasks
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions
- **Cloud Deployment**: Ready for Render (backend) and Vercel (frontend)

## 📁 Repository Structure

```
AetherCrown20/
├── backend/
│   ├── main.py                    # FastAPI application entry point (uvicorn)
│   ├── empire_automation.py       # Cron-ready automation module
│   ├── requirements.txt           # Python dependencies
│   └── __init__.py
├── frontend/
│   ├── pages/                     # Next.js pages directory
│   │   ├── index.tsx             # Home page
│   │   ├── _app.tsx              # App wrapper
│   │   └── _document.tsx         # Document wrapper
│   ├── styles/                    # CSS styles
│   │   ├── globals.css
│   │   └── Home.module.css
│   ├── package.json              # Node.js dependencies
│   ├── tsconfig.json             # TypeScript configuration
│   └── next.config.js            # Next.js configuration
├── .github/
│   └── workflows/
│       ├── ci.yml                # CI/CD pipeline
│       └── deploy.yml            # Deployment workflow
├── render.yaml                   # Render deployment configuration
├── vercel.json                   # Vercel deployment configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from `.env.example`:
   ```bash
   cp ../.env.example .env
   ```

5. Run the backend:
   ```bash
   python main.py
   ```

   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

   API will be available at: http://localhost:8000
   API Documentation: http://localhost:8000/docs

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

### Automation Module

The `empire_automation.py` module is cron-ready and can be run:

1. Manually:
   ```bash
   cd backend
   python empire_automation.py
   ```

2. Via cron (example - runs every 6 hours):
   ```bash
   0 */6 * * * cd /path/to/AetherCrown20/backend && python empire_automation.py
   ```

3. Via Render Cron (configured in `render.yaml`)

## 🚢 Deployment

### Backend Deployment (Render)

1. Connect your GitHub repository to Render
2. Render will automatically detect `render.yaml`
3. Configure required environment variables in Render dashboard
4. Backend will auto-deploy on push to main branch

Required secrets in Render:
- `ENVIRONMENT=production`
- Add any API keys or database URLs as needed

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Vercel will automatically detect Next.js configuration
3. Set the root directory to `frontend`
4. Configure environment variables:
   - `NEXT_PUBLIC_API_URL` - Your Render backend URL

### GitHub Secrets

Configure these secrets in your GitHub repository settings:
- `RENDER_API_KEY` - (Optional) For manual Render deployments
- `VERCEL_TOKEN` - (Optional) For manual Vercel deployments

## 🔄 CI/CD Pipeline

The repository includes two GitHub Actions workflows:

### CI Workflow (`.github/workflows/ci.yml`)
- Runs on push and pull requests
- Tests backend Python imports
- Builds and tests frontend
- Runs linting checks

### Deploy Workflow (`.github/workflows/deploy.yml`)
- Runs on push to main branch
- Deploys backend to Render
- Deploys frontend to Vercel
- References GitHub secrets for authentication

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest  # If tests are added
```

### Frontend Tests
```bash
cd frontend
npm run test  # If tests are added
```

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Development

### Backend Development
- FastAPI with automatic reload
- Uvicorn ASGI server
- CORS middleware configured
- Health check endpoint at `/health`

### Frontend Development
- Next.js with TypeScript
- Hot module replacement
- API status monitoring on home page
- Responsive design with CSS modules

## 📦 Dependencies

### Backend
- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- python-dotenv: Environment management
- httpx: HTTP client

### Frontend
- Next.js: React framework
- React: UI library
- TypeScript: Type safety

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is part of the AetherCrown20 system.

## 🆘 Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the CI/CD logs in GitHub Actions
- Check deployment logs in Render/Vercel dashboards