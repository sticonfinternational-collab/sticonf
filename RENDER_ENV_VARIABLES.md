# 🔧 FIX 400 Error - Update Render Environment Variables

## YOUR RENDER DOMAIN: sticonf.onrender.com

Go to Render Dashboard and update these environment variables:

### Step 1: Go to Dashboard
1. Open https://render.com/dashboard
2. Click your `sticonf` web service
3. Go to **Settings** tab
4. Scroll to **Environment** section

### Step 2: Set/Update These Variables

| Variable | Value | 
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate at https://djecrety.ir/ (use: `django-insecure-11j2tf5%ajj3(8)on3g1!n*5g6pyi8^=7**^ng^4^a$abcp(ln)` if no preference) |
| `ALLOWED_HOSTS` | `sticonf.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://sticonf.onrender.com` |
| `BREVO_API_KEY` | `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` |
| `BREVO_LIST_ID` | `2` |
| `BREVO_SMTP_USER` | `a85adf001@smtp-brevo.com` |
| `BREVO_SMTP_PASSWORD` | `xsmtpsib-eb48300c68b5bd82f7a25d9eb92cd06969b932493e6767556e9a4404dc27b690-qcDJrceXozAubRd8` |
| `ADMIN_EMAIL` | `sticonfinternational@gmail.com` |
| `FLUTTERWAVE_PUBLIC_KEY` | `your_flutterwave_public_key_here` |
| `FLUTTERWAVE_SECRET_KEY` | `your_flutterwave_secret_key_here` |

### Step 3: For Each Variable
1. Click the variable name
2. Change the value 
3. Click "Update"
4. **Move to next variable**

### Step 4: After Updating All
1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Wait for deployment to complete
3. Visit `https://sticonf.onrender.com` again

---

## ⚠️ Important Notes

- ✅ Make sure `ALLOWED_HOSTS` is **exactly**: `sticonf.onrender.com` (no http://, no trailing slash)
- ✅ Make sure `CSRF_TRUSTED_ORIGINS` is **exactly**: `https://sticonf.onrender.com` (with https://)
- ✅ Check for extra spaces when copying values
- ✅ After updating variables, click "Manual Deploy"

---

## If It Still Shows 400 After Redeployment

The actual Django error is being hidden. Check the **Logs** for the full error:
1. Click **Logs** tab
2. Scroll down to see the full error message
3. Share the error with me

Likely issues:
- Missing or incorrect ALLOWED_HOSTS value
- SECRET_KEY is blank
- Database connection issue

Let me know once you've updated these! 🎯
