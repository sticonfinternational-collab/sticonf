# ✅ SPONSORSHIP 500 ERROR - FIXES APPLIED

## Summary of Issues Found & Fixed

### 🔴 **CRITICAL: Flutterwave Keys** 
**Issue:** Keys had invalid `-X` suffix
```
❌ FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08-X
❌ FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d-X

✅ FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
✅ FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d
```
**Status:** ✅ FIXED in `.env`

---

### 🟠 **CRITICAL: ALLOWED_HOSTS Format**
**Issue:** Malformed with inconsistent quoting
```
❌ ALLOWED_HOSTS='127.0.0.1', sticonf.onrender.com, localhost, 127.0.0.1 , '127.0.0.1' , '127.0.0.1:3000'

✅ ALLOWED_HOSTS=127.0.0.1,sticonf.onrender.com,localhost
```
**Status:** ✅ FIXED in `.env`

---

### 🟡 **CRITICAL: CSRF_TRUSTED_ORIGINS Format**
**Issue:** Had unnecessary ports and inconsistent formatting
```
❌ CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com, http://localhost:8000, https://127.0.0.1, https://127.0.0.1:3000

✅ CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com,http://localhost:8000
```
**Status:** ✅ FIXED in `.env`

---

## Next Steps to Complete

### Step 1: Verify Environment Variables
```bash
# View your current .env
cat .env | grep FLUTTERWAVE
cat .env | grep ALLOWED_HOSTS
cat .env | grep CSRF_TRUSTED
```

Expected output:
```
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d
ALLOWED_HOSTS=127.0.0.1,sticonf.onrender.com,localhost
CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com,http://localhost:8000
```

---

### Step 2: Initialize Sponsorship Tiers
This ensures the database has the required sponsorship tier data.

**Option A - Using the script (RECOMMENDED):**
```bash
python setup_sponsorship_tiers.py
```

**Option B - Manual via Django shell:**
```bash
python manage.py shell
```

Then paste:
```python
from main.models import SponsorshipTier

tiers_data = [
    {'tier_name': 'platinum', 'amount': 10000000, 'description': 'Platinum Sponsorship Package'},
    {'tier_name': 'gold', 'amount': 5000000, 'description': 'Gold Sponsorship Package'},
    {'tier_name': 'silver', 'amount': 2000000, 'description': 'Silver Sponsorship Package'},
    {'tier_name': 'bronze', 'amount': 1000000, 'description': 'Bronze Sponsorship Package'},
]

for tier_data in tiers_data:
    tier, created = SponsorshipTier.objects.get_or_create(
        tier_name=tier_data['tier_name'],
        defaults={'amount': tier_data['amount'], 'description': tier_data['description']}
    )
    print(f"{'Created' if created else 'Exists'}: {tier.tier_name} - ₦{tier.amount:,.0f}")

print(f"\nTotal tiers: {SponsorshipTier.objects.count()}")
exit()
```

---

### Step 3: Test Locally
```bash
# Start development server
python manage.py runserver

# In another terminal, test the API
curl http://localhost:8000/api/sponsorship-tiers/
```

Expected response:
```json
[
  {
    "id": 1,
    "tier_name": "platinum",
    "amount": "10000000.00",
    "description": "Platinum Sponsorship Package"
  },
  ...
]
```

---

### Step 4: Deploy to Render

1. **Commit changes:**
   ```bash
   git add .env setup_sponsorship_tiers.py SPONSORSHIP_500_ERROR_FIX.md
   git commit -m "Fix: Correct Flutterwave keys and ALLOWED_HOSTS format"
   git push
   ```

2. **Update Render Environment Variables:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click on your `sticonf` service
   - Go to **Settings** → **Environment**
   - Update these variables:
     ```
     FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_TEST-0e7916b9711179d64611bf155e47fe08
     FLUTTERWAVE_SECRET_KEY=FLWSECK_TEST-c1543c47b46354447f6afc90b5b9827d
     ALLOWED_HOSTS=sticonf.onrender.com,localhost,127.0.0.1
     CSRF_TRUSTED_ORIGINS=https://sticonf.onrender.com
     ```

3. **Deploy:**
   - Click **Manual Deploy**
   - Wait for completion

4. **Verify Tiers on Production:**
   ```bash
   # Connect to Render shell
   render connect <service-name>
   
   # Then run:
   python setup_sponsorship_tiers.py
   ```

---

### Step 5: Test Payment Flow

1. Navigate to: `https://sticonf.onrender.com/sponsorship`
2. Click any "Become [Tier]" button
3. Fill in the payment form:
   - Company: Test Company
   - Contact: Test Contact
   - Email: test@example.com
   - Phone: +234 123 456 7890
4. Click Submit
5. You should see the Flutterwave payment modal
6. Test with Flutterwave test card if available

---

## If Still Getting 500 Error

### Check Render Logs
1. Go to Render Dashboard
2. Click your service
3. Click **Logs** tab
4. Scroll to find the error message

### Common Issues & Solutions

| Error | Solution |
|-------|----------|
| `ValueError: invalid literal for int()` in Flutterwave API | API key still has `-X` suffix or is truncated |
| `DisallowedHost` exception | ALLOWED_HOSTS still incorrect or domain not added |
| `CSRF verification failed` | Check endpoint has `@csrf_exempt` decorator (it should) |
| `SponsorshipTier.DoesNotExist` | Run `python setup_sponsorship_tiers.py` to create tiers |
| `Connection refused` to Flutterwave | API key is invalid or firewall blocking requests |

---

## Files Modified

- ✅ `.env` - Fixed Flutterwave keys, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS
- ✅ `setup_sponsorship_tiers.py` - Created helper script to initialize database
- ✅ `SPONSORSHIP_500_ERROR_FIX.md` - Detailed troubleshooting guide

---

## Verification Checklist

- [ ] Flutterwave keys updated (no `-X` suffix)
- [ ] ALLOWED_HOSTS format corrected
- [ ] CSRF_TRUSTED_ORIGINS format corrected
- [ ] Sponsorship tiers created in database
- [ ] API endpoint `/api/sponsorship-tiers/` returns JSON
- [ ] Local testing successful
- [ ] Changes pushed to GitHub
- [ ] Render environment variables updated
- [ ] Manual deploy completed on Render
- [ ] Render logs checked for errors
- [ ] Payment flow tested on production

---

## Questions or Issues?

If you encounter any errors after these fixes:

1. **Check the error message in Render logs** - Copy the exact error
2. **Verify all environment variables** - Use Render dashboard to confirm
3. **Test locally first** - Ensure it works before deploying
4. **Check database migrations** - Run `python manage.py migrate` if needed

The main issue was the malformed Flutterwave API keys. This should resolve the 500 error!
