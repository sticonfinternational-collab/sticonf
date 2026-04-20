# 🚨 URGENT: Fix Render Start Command

## The Problem
Render is running: `gunicorn app:app` (Flask default)
We need it to run: `gunicorn sticonf.wsgi:application --worker-tmp-dir /dev/shm --timeout 120` (Django)

## IMMEDIATE FIX - Do This Now

### Step 1: Go to Render Dashboard
1. Open https://render.com/dashboard
2. Click on your `sticonf` web service
3. Go to **Settings** tab

### Step 2: Update Start Command
1. Find the **"Start Command"** field
2. Replace whatever is there with:
   ```
   gunicorn sticonf.wsgi:application --worker-tmp-dir /dev/shm --timeout 120
   ```
3. Click **"Save Changes"**

### Step 3: Update Python Version
1. Still in Settings, find **"Python Version"** (or scroll down)
2. Change from `3.14` to `3.11.4`
3. Click **"Save Changes"**

### Step 4: Redeploy
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Watch the logs - it should now use correct Python version and start command

---

## If Manual Deploy Doesn't Work

### Option A: Delete & Recreate Service
If the above doesn't work, delete the service and recreate from scratch:
1. Delete the service
2. Create new web service from GitHub
3. Render will ask for Start Command - paste:
   ```
   gunicorn sticonf.wsgi:application --worker-tmp-dir /dev/shm --timeout 120
   ```

### Option B: Alternative Start Command
If the above has issues, try simpler version:
```
gunicorn sticonf.wsgi:application
```

---

## What You'll See When It Works
✅ Build logs show: `Python 3.11.4`
✅ Build completes migrations and collects static files
✅ Service starts without gunicorn errors
✅ Website loads at your Render domain

---

Let me know once you update the Start Command in Render! 🎯
