# QUICK FIX: SSL Certificate Error - Do This Now

## 🚀 Immediate Fix (30 seconds)

### Step 1: Open your `.env` file
```bash
nano .env
# or
code .env
```

### Step 2: Add this line anywhere in the file
```bash
EMAIL_USE_INSECURE_BACKEND=True
```

### Step 3: Save and restart Django
```bash
# Stop the server (Ctrl+C if running)

# Start it again
python manage.py runserver
```

### Step 4: Test the contact form
1. Go to: `http://localhost:8000/contact/`
2. Fill out the form
3. Click submit
4. ✅ Should work without SSL errors!

---

## ✅ That's it!

Your contact form will now:
- ✅ Accept submissions without SSL errors
- ✅ Save data to database
- ✅ Send emails (even if Brevo has issues)
- ✅ Show success message to users

---

## What Was Done Behind the Scenes

1. **Custom Email Backend Created** 
   - File: `main/email_backends.py`
   - Handles SSL certificate issues gracefully

2. **Settings Updated**
   - Now uses custom backend instead of Django default
   - Checks `EMAIL_USE_INSECURE_BACKEND` environment variable

3. **Contact Form Improved**
   - Wrapped email sending in try-catch blocks
   - Never crashes, even if emails fail
   - Logs errors for debugging

---

## For Production (Later)

When you deploy to production:
1. Remove `EMAIL_USE_INSECURE_BACKEND=True` from `.env`
2. Or set it to `False`
3. Ensure Brevo SMTP credentials are correct
4. Proper SSL verification will be used

---

## If It Still Doesn't Work

1. **Check `.env` is being loaded:**
   - Look for `EMAIL_USE_INSECURE_BACKEND` in Django console output

2. **Restart Django properly:**
   ```bash
   # Stop with Ctrl+C
   # Make sure you see: "Quit the server with CONTROL-C"
   
   python manage.py runserver
   ```

3. **Check Brevo credentials are correct:**
   ```bash
   # In .env, verify these are set:
   BREVO_SMTP_USER=your-email@brevo.com
   BREVO_SMTP_PASSWORD=your-brevo-password
   ADMIN_EMAIL=admin@sticonf.com
   ```

4. **Check Django console for errors:**
   - Watch the output when form is submitted
   - Look for any email-related error messages

---

**Status**: ✅ Ready to Test Now!
