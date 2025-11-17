# Deployment Guide for Idea Factory

This guide covers deploying the Idea Factory app to production.

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended for Frontend)

Streamlit Cloud provides free hosting for Streamlit apps with built-in SSL and authentication.

#### Steps:

1. **Prepare Repository**
   - Ensure your code is pushed to GitHub
   - Make sure `.gitignore` excludes `.env` files
   - Verify `frontend/requirements.txt` is up to date

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set:
     - **Main file path**: `frontend/app.py`
     - **Python version**: 3.11
   - Click "Advanced settings"
   - Add secrets:
     ```toml
     ANTHROPIC_API_KEY = "your_api_key_here"
     ```
   - Click "Deploy"

3. **Custom Domain (Optional)**
   - Go to app settings
   - Add custom domain
   - Update DNS records

#### Expected URL Format:
`https://your-app-name.streamlit.app`

---

### Option 2: Render (For Backend API)

Render provides free tier hosting for web services.

#### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up/login with GitHub

2. **Deploy Backend**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `idea-factory-backend`
     - **Region**: Choose closest to your users
     - **Branch**: `main` or your deployment branch
     - **Root Directory**: Leave blank
     - **Environment**: `Python 3`
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Instance Type**: Free

3. **Add Environment Variables**
   - In the Render dashboard, go to "Environment"
   - Add:
     ```
     ANTHROPIC_API_KEY=your_api_key_here
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your service URL

#### Expected URL Format:
`https://idea-factory-backend.onrender.com`

---

### Option 3: Vercel (Alternative for Frontend)

#### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add ANTHROPIC_API_KEY
   ```

---

### Option 4: Railway (Full Stack)

Railway can host both frontend and backend in one platform.

#### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python

3. **Configure Services**
   - Add two services: frontend and backend
   - For backend:
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - For frontend:
     - **Start Command**: `cd frontend && streamlit run app.py --server.port $PORT`

4. **Add Environment Variables**
   - Add `ANTHROPIC_API_KEY` to both services

---

## 🔒 Security Best Practices

### Environment Variables

**Never commit `.env` files to Git!**

Always use platform-specific secrets management:

- **Streamlit Cloud**: Use Secrets management in settings
- **Render**: Use Environment tab
- **Vercel**: Use `vercel env` command
- **Railway**: Use Variables tab

### API Key Protection

1. **Rate Limiting**
   - Consider adding rate limiting to prevent abuse
   - Use libraries like `slowapi` for FastAPI

2. **CORS Configuration**
   - Update `CORSMiddleware` in `backend/main.py`
   - Only allow your frontend domain:
   ```python
   allow_origins=["https://your-app.streamlit.app"]
   ```

3. **HTTPS Only**
   - All platforms provide SSL by default
   - Ensure your app redirects HTTP to HTTPS

---

## 📊 Monitoring

### Health Checks

Both backend and frontend should implement health checks:

**Backend** (`/` endpoint):
```bash
curl https://your-backend.onrender.com/
```

**Frontend**:
- Check Streamlit Cloud dashboard
- Monitor app logs

### Logging

**Streamlit Cloud**:
- View logs in the app dashboard
- Click "Manage app" → "Logs"

**Render**:
- View logs in service dashboard
- Click on service → "Logs" tab

---

## 🚀 Deployment Checklist

Before deploying:

- [ ] Test app locally with production settings
- [ ] Update `README.md` with deployment URLs
- [ ] Add `ANTHROPIC_API_KEY` to platform secrets
- [ ] Configure CORS for production domains
- [ ] Test on mobile devices
- [ ] Set up monitoring/alerts
- [ ] Document any custom configurations
- [ ] Test error handling
- [ ] Verify SSL certificates
- [ ] Check API rate limits

After deploying:

- [ ] Test all features on production
- [ ] Verify mobile responsiveness
- [ ] Check API endpoints
- [ ] Test error scenarios
- [ ] Monitor logs for issues
- [ ] Share demo link with users
- [ ] Update documentation with live URLs

---

## 🐛 Troubleshooting

### Common Issues

**1. "Module not found" errors**
- Check `requirements.txt` includes all dependencies
- Verify Python version matches `runtime.txt`
- Clear build cache and redeploy

**2. API Key errors**
- Verify environment variable name matches code
- Check for typos in API key
- Ensure no quotes around the key in secrets

**3. CORS errors**
- Update `allow_origins` in `backend/main.py`
- Add your frontend domain to allowed origins

**4. Slow cold starts (Render/Railway)**
- Free tier services sleep after inactivity
- Consider upgrading to paid tier for production
- Use keep-alive services (UptimeRobot)

**5. Streamlit caching issues**
- Clear cache: Click menu → "Clear cache"
- Restart app from dashboard

---

## 💰 Cost Estimates

### Free Tier Limits:

**Streamlit Cloud**:
- 1 public app free
- Unlimited viewers
- 1 GB RAM
- Community support

**Render**:
- 750 hours/month free
- Sleeps after 15 min inactivity
- 512 MB RAM
- SSL included

**Railway**:
- $5 credit/month free
- Pay for usage beyond credit
- No sleep time

**Anthropic API**:
- Pay per token usage
- Claude Sonnet: ~$3/$15 per million input/output tokens
- Monitor usage in Anthropic console

---

## 📈 Scaling Considerations

When your app grows:

1. **Upgrade to paid tiers**
   - More RAM
   - No sleep time
   - Better performance

2. **Add caching**
   - Redis for API responses
   - CDN for static assets

3. **Database**
   - Store user sessions
   - Cache AI responses
   - Consider PostgreSQL on Render/Railway

4. **Load balancing**
   - Multiple backend instances
   - Geographic distribution

---

## 🔄 CI/CD

### Automatic Deployments

All platforms support auto-deploy on git push:

**Streamlit Cloud**:
- Auto-deploys on push to connected branch
- Configure in app settings

**Render**:
- Auto-deploys on push to main branch
- Configure in service settings
- Can set up preview environments

**Railway**:
- Auto-deploys on push
- Supports PR previews

### Manual Deployments

**Streamlit Cloud**:
- Dashboard → "Reboot app"

**Render**:
- Dashboard → "Manual Deploy" → "Deploy latest commit"

---

## 📱 Mobile Testing

Before launch, test on:

- [ ] iOS Safari
- [ ] Android Chrome
- [ ] Various screen sizes
- [ ] Portrait/landscape modes
- [ ] Touch interactions
- [ ] Network conditions (slow 3G)

Use browser dev tools device emulation for quick testing.

---

## 🎉 Going Live

1. **Announce**: Share your demo link
2. **Monitor**: Watch logs for errors
3. **Iterate**: Collect feedback and improve
4. **Document**: Keep README updated
5. **Support**: Be responsive to user issues

---

**Happy Deploying! 🚀**
