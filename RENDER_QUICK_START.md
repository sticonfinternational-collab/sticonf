# RENDER DEPLOYMENT CHECKLIST - Quick Start

## ✅ What's Been Done Locally
- [x] Updated Django settings for production
- [x] Created `build.sh` script for automatic deployment
- [x] Created `render.yaml` configuration
- [x] Updated `.env` with production placeholders
- [x] Enabled WhiteNoise for static file serving
- [x] Configured HTTPS and security headers
- [x] Made build.sh executable

## 🚀 Next Steps - What YOU Need to Do

### 1. Generate a Secure SECRET_KEY
```bash
# Use this website to generate a strong SECRET_KEY:
# https://djecrety.ir/
# Copy the generated key - you'll need it in step 4
```

### 2. Find Your Render Domain
- After creating the web service in Render, you'll get a domain like: `sticonf-xxxxx.onrender.com`
- Write it down - you'll need it in step 4

### 3. Commit and Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 4. Create Web Service on Render
1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the branch (usually `main`)
5. Choose a name (e.g., `sticonf`)
6. Select **Free** plan
7. Click **"Create Web Service"**

### 5. Set Environment Variables on Render
After creating the service, click **"Environment"** and add these variables:

| Variable | Value |
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Paste the key from step 1 |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` (from step 2) |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.onrender.com` |
| `BREVO_API_KEY` | From your .env |
| `BREVO_LIST_ID` | `2` |
| `BREVO_SMTP_USER` | From your .env |
| `BREVO_SMTP_PASSWORD` | From your .env |
| `ADMIN_EMAIL` | `sticonfinternational@gmail.com` |
| `FLUTTERWAVE_PUBLIC_KEY` | From your .env |
| `FLUTTERWAVE_SECRET_KEY` | From your .env |

### 6. Deploy
- Render will automatically start deployment after you set environment variables
- Check the **"Logs"** tab to monitor the build process
- Wait for the deployment to complete (usually 2-5 minutes)

### 7. Test Your Site
- Visit `https://yourdomain.onrender.com` in your browser
- You should see your STICONF website
- If you see "Not Found", check the troubleshooting section in RENDER_DEPLOYMENT.md

### 8. (Optional) Add PostgreSQL Database
For production reliability, add a database:
1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Create the database
3. It will automatically set `DATABASE_URL` environment variable
4. Render will redeploy automatically with the new database

## 📝 Important Notes
- ⚠️ Never commit `.env` file to GitHub (it's in .gitignore)
- ⚠️ Keep your `SECRET_KEY` secret - never share it
- ⚠️ Always set `DEBUG=False` in production
- 💾 The Free plan on Render will spin down after 15 minutes of inactivity, causing a delay on first request

## 🆘 If Something Goes Wrong
1. Check **Logs** tab on Render dashboard
2. Look for error messages
3. Common issues:
   - `ALLOWED_HOSTS` doesn't match your domain
   - Missing environment variables
   - Static files not collected (should be in build logs)

See **RENDER_DEPLOYMENT.md** for detailed troubleshooting

---
**You're almost there! 🎉**
