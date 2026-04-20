# 🚨 FINAL FIX FOR 400 ERROR - CRITICAL STEPS

## Problem
Still getting 400 errors because **environment variables are not set in Render's dashboard**.

## Solution - Follow These Steps EXACTLY

### STEP 1: Delete the Current Service (Fresh Start)
1. Go to https://render.com/dashboard
2. Click your `sticonf` service
3. Go to **Settings** → scroll to bottom → Click **"Delete Service"**
4. Type the name to confirm deletion
5. Wait 10 seconds for it to delete

### STEP 2: Create a Brand New Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select `main` branch
4. Fill in:
   - **Name:** `sticonf`
   - **Root Directory:** (leave empty)
   - **Build Command:** (leave empty for now - we set in dashboard)
   - **Start Command:** (leave empty for now)
5. Click **"Create Web Service"** (don't deploy yet)

### STEP 3: Add Environment Variables (Before Deployment!)
Before it deploys, you'll see a screen with environment variables. Add these:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | `django-insecure-11j2tf5%ajj3(8)on3g1!n*5g6pyi8^=7**^ng^4^a$abcp(ln)` |
| `ALLOWED_HOSTS` | `sticonf.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://sticonf.onrender.com` |
| `BREVO_API_KEY` | `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` |
| `BREVO_LIST_ID` | `2` |
| `BREVO_SMTP_USER` | `a85adf001@smtp-brevo.com` |
| `BREVO_SMTP_PASSWORD` | `xsmtpsib-eb48300c68b5bd82f7a25d9eb92cd06969b932493e6767556e9a4404dc27b690-qcDJrceXozAubRd8` |
| `ADMIN_EMAIL` | `sticonfinternational@gmail.com` |
| `FLUTTERWAVE_PUBLIC_KEY` | `your_flutterwave_public_key_here` |
| `FLUTTERWAVE_SECRET_KEY` | `your_flutterwave_secret_key_here` |

### STEP 4: Set Build & Start Commands
Still in Settings:

1. Find **"Build Command"** field, set to:
   ```
   pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput --clear
   ```

2. Find **"Start Command"** field, set to:
   ```
   gunicorn sticonf.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

3. Click **"Save"** (or similar - depends on Render UI)

### STEP 5: Deploy
1. Render should auto-deploy, OR
2. Click **"Manual Deploy"** → **"Deploy latest commit"**
3. Watch the logs - should see:
   ```
   Python 3.11.4
   Successfully installed requirements
   Migrations completed
   Static files collected
   ```

### STEP 6: Test
1. Visit `https://sticonf.onrender.com`
2. Should see your website homepage (NOT a 400 error!)

---

## If Still Getting 400

Tell me:
1. **What's in your Render Logs tab?** (copy the full error)
2. **Did you set all the environment variables?**
3. **What's your exact Render domain?** (from URL bar when you're in the service)

---

## Quick Checklist
- [ ] Service deleted
- [ ] New service created from GitHub
- [ ] All 10 environment variables set
- [ ] Build Command entered
- [ ] Start Command entered
- [ ] Deployment started
- [ ] Waiting for it to complete...

Let me know when you've done this! 🚀
