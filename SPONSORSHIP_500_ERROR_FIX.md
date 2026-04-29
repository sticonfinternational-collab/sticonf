# 🔴 SPONSORSHIP PAYMENT 500 ERROR - TROUBLESHOOTING GUIDE

## Root Causes Identified

### 1. ❌ **INVALID FLUTTERWAVE API KEYS** (CRITICAL)
Your `.env` file has malformed Flutterwave keys:
```
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08-X
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d-X
```

The `-X` suffix at the end is **invalid**. This is causing the API calls to fail with 500 errors.

**Fix:** Remove the trailing `-X`
```
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d
```

---

### 2. ⚠️ **MALFORMED ALLOWED_HOSTS** (CRITICAL)
Your `.env` has inconsistent quoting:
```
ALLOWED_HOSTS='127.0.0.1', sticonf.onrender.com, localhost, 127.0.0.1 , '127.0.0.1' , '127.0.0.1:3000'
```

This is parsed as a string with comma-separated values, but the quotes are confusing Django.

**Fix:** Use proper format
```
ALLOWED_HOSTS=127.0.0.1,sticonf.onrender.com,localhost,127.0.0.1:3000
```

---

### 3. ⚠️ **POTENTIAL MISSING EMAIL BACKEND VARIABLE**
Your email configuration requires `EMAIL_USE_INSECURE_BACKEND` setting in production.

**Check:** Verify this is set in your `.env`
```
EMAIL_USE_INSECURE_BACKEND=False
```

---

## Step-by-Step Fix

### Step 1: Update `.env` File

Replace your current `.env` with corrected values:

```env
DEBUG=False

SECRET_KEY=django-insecure-11j2tf5%ajj3(8)on3g1!n*5g6pyi8^=7**^ng^4^a$abcp(ln)

# Fix ALLOWED_HOSTS - remove quotes and extra spaces
ALLOWED_HOSTS=127.0.0.1,sticonf.onrender.com,localhost,127.0.0.1:3000

# CSRF_TRUSTED_ORIGINS
CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com,http://localhost:8000,https://127.0.0.1,https://127.0.0.1:3000

BREVO_API_KEY=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
BREVO_LIST_ID=2
ADMIN_EMAIL=sticonfinternational@gmail.com

BREVO_SMTP_USER=a85adf001@smtp-brevo.com
BREVO_SMTP_PASSWORD=xsmtpsib-eb48300c68b5bd82f7a25d9eb92cd06969b932493e6767556e9a4404dc27b690-qcDJrceXozAubRd8

# Fix Flutterwave - REMOVE THE TRAILING -X
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d

# Email configuration
EMAIL_USE_INSECURE_BACKEND=False
```

---

### Step 2: Verify Database Has Sponsorship Tiers

Run these commands:

```bash
# Check if tiers exist
python manage.py shell
```

Then in Django shell:
```python
from main.models import SponsorshipTier
tiers = SponsorshipTier.objects.all()
print(f"Total tiers: {tiers.count()}")
for tier in tiers:
    print(f"  - {tier.tier_name}: {tier.amount} NGN")
```

**If no tiers exist**, create them:
```python
SponsorshipTier.objects.create(
    tier_name='platinum',
    amount=10000000,
    description='Platinum Sponsorship Package'
)
SponsorshipTier.objects.create(
    tier_name='gold',
    amount=5000000,
    description='Gold Sponsorship Package'
)
SponsorshipTier.objects.create(
    tier_name='silver',
    amount=2000000,
    description='Silver Sponsorship Package'
)
SponsorshipTier.objects.create(
    tier_name='bronze',
    amount=1000000,
    description='Bronze Sponsorship Package'
)
```

Exit shell:
```python
exit()
```

---

### Step 3: Test the API Endpoint

```bash
curl -X GET http://localhost:8000/api/sponsorship-tiers/
```

Should return:
```json
[
  {"id": 1, "tier_name": "platinum", "amount": "10000000.00", "description": "Platinum Sponsorship Package"},
  ...
]
```

---

### Step 4: Restart Your Application

**Local Development:**
```bash
python manage.py runserver
```

**On Render:**
1. Go to Render Dashboard
2. Click your `sticonf` service
3. Click "Manual Deploy"
4. Wait for deployment to complete

---

## If You Still Get 500 Error

### Check Render Logs

1. Go to Render Dashboard → Your service
2. Click **"Logs"** tab
3. Look for the actual error message (scroll down)
4. Copy the full error and analyze:

**Common errors:**

**A) "Invalid Flutterwave key"**
- Solution: Your key format is still wrong. Check `.env` again.

**B) "DisallowedHost"**
- Solution: Your ALLOWED_HOSTS is still malformed or doesn't include your domain.

**C) "Missing required fields"**
- Solution: Check the frontend JavaScript is sending all fields correctly.

**D) "CSRF verification failed"**
- Solution: The `@csrf_exempt` decorator should prevent this, but check if frontend is sending JSON properly.

---

## Local Testing Checklist

- [ ] `.env` file updated with correct Flutterwave keys (no `-X` suffix)
- [ ] `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` have correct format
- [ ] Run migrations: `python manage.py migrate`
- [ ] Sponsorship tiers exist in database
- [ ] Test `/api/sponsorship-tiers/` returns JSON
- [ ] Restart dev server
- [ ] Try payment in browser console: `initializeSponsorshipTiers()` should return tiers
- [ ] Click a "Become [Tier]" button

---

## Production Deployment Checklist

**Before deploying to Render:**

- [ ] Update `.env` in Render dashboard with corrected keys
- [ ] Ensure `DEBUG=False` in Render environment
- [ ] Run migrations on Render database
- [ ] Verify sponsorship tiers exist: `python manage.py shell` on Render
- [ ] Manual deploy
- [ ] Check Render logs for errors

**Set Render environment variables:**

Navigate to Render Dashboard → Service Settings → Environment and add:

```
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d
ALLOWED_HOSTS=sticonf.onrender.com,127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com
```

---

## Payment Flow Debugging

If API calls are still failing, add debug logging to `views.py`:

Replace in `initiate_sponsorship_payment()`:
```python
@csrf_exempt
def initiate_sponsorship_payment(request):
    """Initiate Flutterwave payment for sponsorship"""
    print(f"DEBUG: Request method = {request.method}")
    print(f"DEBUG: Request body = {request.body}")
    print(f"DEBUG: Flutterwave Secret Key = {settings.FLUTTERWAVE_SECRET_KEY}")
    
    if request.method == 'POST':
        try:
            if not settings.FLUTTERWAVE_PUBLIC_KEY or not settings.FLUTTERWAVE_SECRET_KEY:
                print("DEBUG: Missing Flutterwave keys!")
                return JsonResponse({...}, status=500)
            
            # ... rest of code
```

Then check Render logs for debug output.

---

## Quick Reference: Valid Environment Variables

```env
# Required
DEBUG=False
SECRET_KEY=<your-key>
ALLOWED_HOSTS=your-domain.com,localhost
CSRF_TRUSTED_ORIGINS=https://your-domain.com,http://localhost:8000

# Flutterwave (REMOVE TRAILING -X IF PRESENT)
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-xxxxxxxxxxxx
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-xxxxxxxxxxxx

# Email
BREVO_API_KEY=xkeysib-xxxxxxxx
BREVO_SMTP_USER=xxx@smtp-brevo.com
BREVO_SMTP_PASSWORD=xsmtpsib-xxxxxxxx
ADMIN_EMAIL=your-email@gmail.com
EMAIL_USE_INSECURE_BACKEND=False
```

---

## Still Stuck?

If the issue persists after all fixes:

1. Check the exact error from Render logs
2. Verify the database migration for `Sponsorship` and `SponsorshipTier` tables exist
3. Test with curl/Postman to isolate frontend vs backend issues
4. Enable DEBUG=True temporarily to see full error messages
