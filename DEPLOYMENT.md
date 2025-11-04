# Deployment Guide for AetherCrown20

This guide covers deploying the AetherCrown20 application to Render.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Render Deployment](#render-deployment)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- GitHub account with access to the repository
- Render account ([Sign up here](https://render.com))
- PayPal Developer account (for PayPal integration)
- Database (PostgreSQL recommended for production)

## Render Deployment

### Method 1: Blueprint Deployment (Recommended)

This is the easiest method as it uses the `render.yaml` configuration file.

1. **Connect GitHub to Render**
   - Log in to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" in the top right
   - Select "Blueprint"

2. **Select Repository**
   - Connect your GitHub account if you haven't already
   - Select the `monkeymadness98/AetherCrown20` repository
   - Click "Connect"

3. **Review Blueprint**
   - Render will automatically detect the `render.yaml` file
   - Review the service configuration:
     - Service name: `aethercrown20-backend`
     - Environment: Python
     - Plan: Free (can be upgraded later)
     - Region: Oregon

4. **Configure Environment Variables**
   - Before deploying, you'll be prompted to add environment variables
   - Add the following (see [Environment Variables](#environment-variables) section):
     - `ENV`: `production`
     - `PAYPAL_CLIENT_ID`: Your PayPal client ID
     - `PAYPAL_SECRET`: Your PayPal secret key
     - `DATABASE_URL`: Your database connection string (optional)

5. **Deploy**
   - Click "Apply" to create the service
   - Render will automatically:
     - Clone your repository
     - Run the build command (`./build.sh`)
     - Start your application
   - Wait for the build to complete (usually 2-5 minutes)

6. **Access Your Application**
   - Once deployed, Render will provide a URL like: `https://aethercrown20-backend.onrender.com`
   - Test the health endpoint: `https://aethercrown20-backend.onrender.com/healthz`

### Method 2: Manual Service Creation

If you prefer to set up the service manually:

1. **Create New Web Service**
   - Go to Render Dashboard
   - Click "New +" → "Web Service"
   - Connect your repository

2. **Configure Service**
   - **Name**: `aethercrown20-backend` (or your preferred name)
   - **Region**: Oregon (or your preferred region)
   - **Branch**: `main`
   - **Root Directory**: Leave empty (use repository root)
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT --workers 2 --log-level info`

3. **Select Plan**
   - Choose "Free" for testing or a paid plan for production

4. **Add Environment Variables**
   - Scroll down to "Environment Variables"
   - Add all required variables (see section below)

5. **Create Service**
   - Click "Create Web Service"
   - Render will build and deploy your application

### Method 3: Automated Deployment via GitHub Actions

The repository includes CI/CD workflows for automated deployment.

1. **Configure GitHub Secrets**
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `RENDER_API_KEY`: Your Render API key (get from Render Account Settings)
     - `RENDER_SERVICE_ID`: Your Render service ID (from service dashboard URL)
     - `PAYPAL_CLIENT_ID`: Your PayPal client ID
     - `PAYPAL_SECRET`: Your PayPal secret key

2. **Trigger Deployment**
   - Push to the `main` branch
   - GitHub Actions will automatically:
     - Run tests
     - Perform code quality checks
     - Deploy to Render

3. **Monitor Deployment**
   - Go to the "Actions" tab in your GitHub repository
   - Click on the latest workflow run
   - Monitor the "Deploy to Render" job

## Environment Variables

Configure these environment variables in Render Dashboard:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV` | Application environment | `production` |
| `PAYPAL_CLIENT_ID` | PayPal API client ID | `AXxxx...` |
| `PAYPAL_SECRET` | PayPal API secret | `ELxxx...` |

### Optional Variables

| Variable | Description | Example | Default |
|----------|-------------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` | None |
| `PAYPAL_MODE` | PayPal environment | `sandbox` or `live` | `sandbox` |
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG`, `ERROR` | `INFO` |
| `CORS_ORIGINS` | Allowed CORS origins | `https://example.com,https://app.example.com` | `*` |
| `SECRET_KEY` | JWT secret key | Random string | Auto-generated |
| `REDIS_URL` | Redis connection string | `redis://host:6379/0` | None |

### Setting Environment Variables

**In Render Dashboard:**
1. Navigate to your service
2. Click on "Environment" in the left sidebar
3. Click "Add Environment Variable"
4. Enter the key and value
5. Click "Save Changes"
6. Render will automatically redeploy with the new variables

**Note:** Variables marked as `sync: false` in `render.yaml` must be manually added in the Render Dashboard.

## Continuous Deployment

### Auto-Deploy from GitHub

By default, the service is configured to automatically deploy when you push to the main branch:

- Render watches the `main` branch
- When you push changes, Render automatically:
  - Pulls the latest code
  - Runs the build command
  - Restarts the service with the new code

### Manual Deployment

To manually trigger a deployment:

1. Go to your service in Render Dashboard
2. Click "Manual Deploy" button
3. Select "Deploy latest commit" or choose a specific commit

## Health Checks

Render automatically performs health checks on your service. The application includes a health check endpoint:

```
GET /healthz
```

**Response:**
```json
{
  "ok": true,
  "env": "production"
}
```

## Troubleshooting

### Build Failures

**Problem:** Build fails with dependency installation errors

**Solution:**
- Check `requirements.txt` for any incompatible package versions
- Review build logs in Render Dashboard
- Ensure `runtime.txt` specifies a compatible Python version (3.11.0)

### Application Won't Start

**Problem:** Application builds successfully but fails to start

**Solution:**
- Verify the start command is correct
- Check that gunicorn and uvicorn are in `requirements.txt`
- Review application logs in Render Dashboard
- Ensure all required environment variables are set

### Port Binding Issues

**Problem:** Application fails to bind to port

**Solution:**
- Render automatically sets the `PORT` environment variable
- The start command uses `$PORT` - don't hardcode a port number
- Check that your application listens on `0.0.0.0:$PORT`

### Environment Variable Not Found

**Problem:** Application can't find an environment variable

**Solution:**
- Verify the variable is set in Render Dashboard
- Check spelling and case (variables are case-sensitive)
- Ensure the service has been redeployed after adding variables

### Database Connection Errors

**Problem:** Can't connect to database

**Solution:**
- Verify `DATABASE_URL` is correctly formatted
- Check database is accessible from Render's IP addresses
- Ensure database credentials are correct
- For Render PostgreSQL, use the internal connection string

### Memory or CPU Limits

**Problem:** Application crashes or performs poorly

**Solution:**
- Free tier has limited resources (512 MB RAM)
- Reduce number of Gunicorn workers (try 1-2 workers)
- Upgrade to a paid plan for more resources
- Optimize your application code

### Checking Logs

To view logs:
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" in the left sidebar
4. Use filters to search for specific log entries

### Getting Help

- **Render Status**: Check [status.render.com](https://status.render.com) for service outages
- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)
- **GitHub Issues**: Open an issue in this repository

## Monitoring

### View Application Metrics

In Render Dashboard:
1. Navigate to your service
2. Click "Metrics" to view:
   - CPU usage
   - Memory usage
   - Request rate
   - Response times

### Setting Up Alerts

1. Go to service settings
2. Configure notifications for:
   - Deploy failures
   - Service health issues
   - High resource usage

## Scaling

### Horizontal Scaling

To handle more traffic:
1. Upgrade to a paid plan
2. Increase number of workers in start command
3. Consider using Render's autoscaling features (paid plans)

### Vertical Scaling

Upgrade your plan for more resources:
- **Starter**: $7/month - 512 MB RAM, 0.5 CPU
- **Standard**: $25/month - 2 GB RAM, 1 CPU
- **Pro**: $85/month - 4 GB RAM, 2 CPU

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use HTTPS** - Render provides free SSL certificates
3. **Rotate secrets regularly** - Update PayPal credentials, database passwords
4. **Monitor logs** - Watch for suspicious activity
5. **Keep dependencies updated** - Regularly update `requirements.txt`

## Rollback

If a deployment causes issues:

1. Go to service dashboard
2. Click "Events" tab
3. Find a previous successful deployment
4. Click "Rollback to this version"
5. Confirm rollback

Render will redeploy the previous version.

## Additional Resources

- [Render Python Documentation](https://render.com/docs/deploy-fastapi)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [Uvicorn Workers](https://www.uvicorn.org/deployment/#gunicorn)
