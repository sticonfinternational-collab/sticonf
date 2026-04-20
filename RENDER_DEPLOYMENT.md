# Render Deployment Guide for STICONF

## Prerequisites
- GitHub repository with your code pushed
- Render account (https://render.com)

## Step-by-Step Deployment

### 1. Create a New Web Service on Render
- Go to https://render.com/dashboard
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Choose the branch to deploy (usually `main`)

### 2. Configure Environment Variables
In the Render dashboard, set these environment variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Never set to True in production |
| `SECRET_KEY` | Generate a new strong key | Use: https://djecrety.ir/ |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` | Replace with your actual Render domain |
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.onrender.com` | Same as ALLOWED_HOSTS with https:// |
| `BREVO_API_KEY` | Your existing key | From your .env |
| `BREVO_LIST_ID` | `2` | From your .env |
| `BREVO_SMTP_USER` | Your existing key | From your .env |
| `BREVO_SMTP_PASSWORD` | Your existing key | From your .env |
| `ADMIN_EMAIL` | `sticonfinternational@gmail.com` | From your .env |
| `FLUTTERWAVE_PUBLIC_KEY` | Your key | From your .env |
| `FLUTTERWAVE_SECRET_KEY` | Your key | From your .env |
| `PYTHON_VERSION` | `3.11.4` | Python version to use |

### 3. (Optional) Add a PostgreSQL Database
For production, it's recommended to use PostgreSQL instead of SQLite:
- Click "New +" → "PostgreSQL"
- Create a new database
- The `DATABASE_URL` will be automatically set as an environment variable

### 4. Deploy Settings
- **Build Command**: `./build.sh` (already configured in render.yaml)
- **Start Command**: `gunicorn sticonf.wsgi:application --worker-tmp-dir /dev/shm`
- **Plan**: Start with Free tier for testing

### 5. Deploy
- Click "Create Web Service"
- Render will automatically start the deployment
- Monitor the logs to ensure everything works

## What the build.sh Does
1. Installs Python dependencies from `requirements.txt`
2. Runs database migrations with `python manage.py migrate`
3. Collects static files with `python manage.py collectstatic`

## Troubleshooting

### "Not Found" Error
- ✅ Check `ALLOWED_HOSTS` includes your Render domain
- ✅ Check `DEBUG=False` in environment variables
- ✅ Check that static files were collected (look in build logs)

### 404 on Static Files (CSS/JS)
- Ensure `STATIC_URL = '/static/'` (with leading slash)
- Check that WhiteNoise middleware is enabled
- Verify `staticfiles` directory was created

### Database Errors
- If using PostgreSQL, ensure `DATABASE_URL` environment variable is set
- Run migrations: They should run automatically during build
- If migrations fail, check the build logs

### Email Not Working
- Verify Brevo credentials in environment variables
- Check SMTP settings in `settings.py`

## After Deployment

### First Time Setup
1. Access your site: `https://yourdomain.onrender.com`
2. Create a superuser (if database is fresh):
   ```bash
   render-ps web python manage.py createsuperuser
   ```
3. Access admin: `https://yourdomain.onrender.com/admin/`

### Ongoing Maintenance
- Monitor logs regularly in Render dashboard
- Set up automatic deploys on GitHub push (check "Auto-Deploy" option)
- Backup database regularly if using PostgreSQL

## Security Checklist
- [ ] SECRET_KEY is different from development and stored in environment variables
- [ ] DEBUG is False
- [ ] ALLOWED_HOSTS includes your Render domain only
- [ ] Using HTTPS (default on Render)
- [ ] Database password is secure (if using PostgreSQL)

---
For more help: https://render.com/docs
