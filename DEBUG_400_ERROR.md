# 🔍 Diagnosing 400 Error on Render

## What You Need to Check

### 1. Look at Render Logs
In Render Dashboard:
1. Click your `sticonf` service
2. Go to **"Logs"** tab
3. **Scroll down** to find the actual error message (should show more details than just "400")
4. Copy the error and send it to me

### 2. Common 400 Error Causes

**Most Likely: ALLOWED_HOSTS Issue**
```
DisallowedHost at /
The domain name you're accessing is not in the ALLOWED_HOSTS setting
```
**Fix:** Your ALLOWED_HOSTS in environment variables doesn't match your Render domain

**Second: CSRF Issue**
```
CSRF verification failed
```
**Fix:** Your CSRF_TRUSTED_ORIGINS doesn't include your domain with https://

**Third: Missing Variables**
```
Error creating new instance of settings class
```
**Fix:** Missing environment variables like SECRET_KEY, DATABASE_URL

---

## Quick Verification Steps

1. **Get your Render domain URL** from dashboard (looks like: `sticonf-xxxxx.onrender.com`)

2. **Check your Environment Variables** in Render Settings:
   - Is `ALLOWED_HOSTS` set to your domain?
   - Is `CSRF_TRUSTED_ORIGINS` set to `https://yourdomain.onrender.com`?
   - Is `DEBUG` set to `False`?

3. **Send me the error from the Logs tab**

---

## Quick Fixes to Try

### If it's ALLOWED_HOSTS issue:
In Render Dashboard → Settings → Environment:
- Change `ALLOWED_HOSTS` to: `yourdomain.onrender.com` (replace with actual domain)
- Click "Save Changes"
- Click "Manual Deploy"

### If it's CSRF issue:
- Change `CSRF_TRUSTED_ORIGINS` to: `https://yourdomain.onrender.com`
- Click "Save Changes"  
- Click "Manual Deploy"

---

## What's Your Render Domain?
Can you tell me your Render service domain (from the Render dashboard URL bar)?
