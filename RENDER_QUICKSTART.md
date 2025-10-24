# Quick Start: Deploy to Render

This guide will help you deploy AetherCrown20 to Render in 5 minutes.

## Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up for a free account
3. Verify your email address

## Step 2: Deploy Using Blueprint

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Select the `monkeymadness98/AetherCrown20` repository
5. Render will detect the `render.yaml` file automatically

## Step 3: Configure Environment Variables

Before deploying, add these environment variables:

**Required:**
- `ENV` = `production` (already set in render.yaml)
- `PAYPAL_CLIENT_ID` = Your PayPal client ID
- `PAYPAL_SECRET` = Your PayPal secret key

**Optional:**
- `DATABASE_URL` = Your PostgreSQL connection string

## Step 4: Deploy

1. Click **"Apply"** to create the service
2. Wait 2-5 minutes for the build to complete
3. Your app will be live at: `https://aethercrown20-backend.onrender.com`

## Step 5: Verify Deployment

Test these endpoints:
- Health check: `https://aethercrown20-backend.onrender.com/healthz`
- API endpoint: `https://aethercrown20-backend.onrender.com/clocks`

## Troubleshooting

**Build fails?**
- Check the build logs in Render Dashboard
- Ensure all dependencies are in `requirements.txt`

**App won't start?**
- Verify environment variables are set
- Check the service logs for errors

**Need more help?**
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions
- Check [Render documentation](https://render.com/docs)

## What's Next?

- Set up automatic deployments (enabled by default)
- Add a custom domain
- Upgrade to a paid plan for better performance
- Set up monitoring and alerts

## Files Included for Render

- ✅ `render.yaml` - Service configuration
- ✅ `build.sh` - Build script
- ✅ `runtime.txt` - Python version
- ✅ `Procfile` - Process definition
- ✅ `requirements.txt` - Dependencies

## Free Tier Limitations

The free tier includes:
- 750 hours of runtime per month
- Automatic sleep after 15 minutes of inactivity
- First request after sleep may be slow (cold start)
- 512 MB RAM, 0.1 CPU

For production use, consider upgrading to a paid plan.

## Need Help?

- 📖 Full documentation: [DEPLOYMENT.md](./DEPLOYMENT.md)
- 🐛 Report issues: [GitHub Issues](https://github.com/monkeymadness98/AetherCrown20/issues)
- 💬 Render Community: [community.render.com](https://community.render.com)
