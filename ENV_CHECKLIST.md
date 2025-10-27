# Environment Variables Checklist

Use this checklist to ensure all environment variables are configured across all platforms.

## Platform Setup Status

- [ ] GitHub Secrets configured
- [ ] Render Environment configured
- [ ] Vercel Environment configured
- [ ] Supabase Edge Function secrets configured

## Required Variables by Platform

### GitHub Secrets

- [ ] DATABASE_URL
- [ ] OPENAI_API_KEY
- [ ] PAYPAL_CLIENT_ID
- [ ] PAYPAL_SECRET
- [ ] RENDER_API_KEY
- [ ] RENDER_SERVICE_ID
- [ ] SUPABASE_ANON_KEY
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] SUPABASE_URL
- [ ] VERCEL_ORG_ID
- [ ] VERCEL_PROJECT_ID
- [ ] VERCEL_TOKEN

### Render

- [ ] DATABASE_URL
- [ ] OPENAI_API_KEY
- [ ] PAYPAL_CLIENT_ID
- [ ] PAYPAL_SECRET
- [ ] SUPABASE_ANON_KEY
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] SUPABASE_URL

### Vercel

- [ ] NEXT_PUBLIC_API_URL
- [ ] NEXT_PUBLIC_SUPABASE_ANON_KEY
- [ ] NEXT_PUBLIC_SUPABASE_URL
- [ ] OPENAI_API_KEY
- [ ] PAYPAL_CLIENT_ID
- [ ] SUPABASE_ANON_KEY
- [ ] SUPABASE_URL
- [ ] VERCEL_ENV

### Supabase Edge

- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] SUPABASE_URL

## Optional Variables

- [ ] REDIS_URL (Caching and sessions)
- [ ] SECRET_KEY (JWT and session encryption)
- [ ] ENV (Environment identifier (development/production))
- [ ] LOG_LEVEL (Logging verbosity)
- [ ] CORS_ORIGINS (Cross-origin resource sharing)

## Verification Steps

1. **Local Development**: Run `node monitoring/env-validator.js`
2. **Render**: Visit `https://aetherai-8wcw.onrender.com/_env_check`
3. **GitHub Actions**: Check workflow runs for errors
4. **Vercel**: Check deployment logs
5. **Supabase**: Test edge function invocation
