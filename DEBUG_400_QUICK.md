# 🔍 Debugging 400 Error - QUICK FIX

## The Real Problem
The 400 error is happening because Django is rejecting the request. Most likely cause: **ALLOWED_HOSTS is empty or wrong in Render**.

## Quick Fix - Check Your Render Settings NOW

### Go to Render Dashboard
1. https://render.com/dashboard
2. Click `sticonf` service
3. Go to **Settings** tab
4. Find **Environment**

### Check These Variables Exist:
- [ ] `ALLOWED_HOSTS` = `sticonf.onrender.com` (NOT `*.onrender.com`, NOT with http://)
- [ ] `DEBUG` = `False`
- [ ] `SECRET_KEY` = (should be set to something)

### If Any Are Missing or Wrong:
1. Click the variable
2. Fix the value
3. Click "Update"
4. After all fixes, click **"Manual Deploy"**

---

## Temporary DEBUG to See Real Error

If you want to see the actual error (advanced):

### In Render Settings:
1. Change `DEBUG` from `False` to `True` (temporarily)
2. Click "Update"
3. Click "Manual Deploy"
4. Reload the website
5. You'll now see the actual Django error page

### Then Fix Based on Error:
- If you see "DisallowedHost" → ALLOWED_HOSTS is wrong
- If you see "CSRF" → CSRF_TRUSTED_ORIGINS is wrong
- If you see database error → DATABASE_URL might be needed

### After Fixing, Set DEBUG Back to False

---

## Most Common Fixes

**If ALLOWED_HOSTS was wrong:**
- Should be: `sticonf.onrender.com`
- NOT: `*.onrender.com`
- NOT: `https://sticonf.onrender.com` (no protocol!)
- NOT: `sticonf.onrender.com/` (no trailing slash!)

**If CSRF_TRUSTED_ORIGINS was wrong:**
- Should be: `https://sticonf.onrender.com` (WITH protocol)

---

## Quick Checklist
- [ ] I checked ALLOWED_HOSTS in Render
- [ ] I checked it's exactly: `sticonf.onrender.com`
- [ ] I fixed any wrong variables
- [ ] I clicked "Manual Deploy"
- [ ] I'm waiting for deployment to complete

**Let me know what you find in those environment variables!** 🎯
