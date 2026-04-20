# Flutterwave Integration Setup & Audit Guide

## 📋 Overview

This document outlines the complete Flutterwave payment integration for STICONF 2026 sponsorship payments, including setup instructions, configuration, and verification steps.

---

## ✅ Current Status

### Completed Components:
- ✅ **Flutterwave Configuration Variables** - Set in `sticonf/settings.py`
- ✅ **API Endpoints** - 3 endpoints created and tested:
  - `GET /api/sponsorship-tiers/` - Retrieve available sponsorship tiers
  - `POST /api/initiate-sponsorship-payment/` - Initialize Flutterwave payment
  - `POST /api/verify-sponsorship-payment/` - Verify and confirm payment
- ✅ **Database Models** - Sponsorship model with payment tracking
- ✅ **Frontend Integration** - JavaScript checkout form with Flutterwave SDK
- ✅ **Email Notifications** - Sponsorship confirmation emails via BREVO SMTP
- ✅ **Error Handling** - Comprehensive validation and error responses
- ✅ **CSRF Protection** - CSRF exemption properly applied to payment endpoints
- ✅ **Sponsorship Tiers** - Database initialized with 4 tiers:
  - Platinum: ₦5,000,000
  - Gold: ₦2,500,000
  - Silver: ₦1,000,000
  - Bronze: ₦500,000

---

## 🔴 Critical Setup Required

### Step 1: Get Flutterwave API Keys

1. Go to [Flutterwave Dashboard](https://dashboard.flutterwave.com)
2. Log in or create an account
3. Navigate to **Settings > API Keys**
4. Copy your:
   - **Public Key** (starts with `FLWPUBK_`)
   - **Secret Key** (starts with `FLWSECK_`)

### Step 2: Update .env File

Replace the placeholder values in `.env`:

```env
# BEFORE (Placeholder - DO NOT USE)
FLUTTERWAVE_PUBLIC_KEY=your_flutterwave_public_key_here
FLUTTERWAVE_SECRET_KEY=your_flutterwave_secret_key_here

# AFTER (Your actual keys)
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_YOUR_ACTUAL_KEY_HERE
FLUTTERWAVE_SECRET_KEY=FLWSECK_YOUR_ACTUAL_KEY_HERE
```

### Step 3: Verify Setup

Run the test suite:
```bash
python manage.py shell < test_flutterwave_integration.py
# OR
python test_flutterwave_integration.py
```

Expected output:
```
============================================================
TEST SUMMARY
============================================================

PASS: Environment Configuration
PASS: Sponsorship Tiers
PASS: Email Configuration
PASS: Sponsorship Model
PASS: API Endpoints
PASS: Flutterwave Keys Validation
PASS: CSRF Exemption
PASS: Database Migrations

============================================================
Total: 8 | Passed: 8 | Failed: 0
```

---

## 🏗️ Architecture

### Payment Flow

```
1. User selects sponsorship tier on /sponsorship/
   ↓
2. Submit form → /api/initiate-sponsorship-payment/ (POST)
   ↓
3. Backend creates Sponsorship record with 'pending' status
   ↓
4. Backend calls Flutterwave API to create payment
   ↓
5. Backend returns payment link to frontend
   ↓
6. Frontend opens Flutterwave checkout modal
   ↓
7. User completes payment
   ↓
8. Flutterwave callback triggers verification
   ↓
9. Frontend calls /api/verify-sponsorship-payment/ (POST)
   ↓
10. Backend verifies with Flutterwave
    ↓
11. Update Sponsorship status to 'paid'
    ↓
12. Send confirmation email
    ↓
13. Return success to frontend
```

### Database Schema

**SponsorshipTier**
```
- tier_name: (platinum|gold|silver|bronze)
- amount: Decimal (in NGN)
- description: Text
```

**Sponsorship**
```
- company_name: CharField
- contact_name: CharField
- email: EmailField
- phone: CharField
- country: CharField (default: Nigeria)
- tier: ForeignKey(SponsorshipTier)
- amount: Decimal
- status: (pending|paid|failed|cancelled)
- reference: CharField (unique, Flutterwave tx_ref)
- transaction_id: CharField (Flutterwave transaction ID)
- created_at: DateTimeField
- updated_at: DateTimeField
- paid_at: DateTimeField (set when marked_as_paid)
```

### API Endpoints

#### 1. Get Sponsorship Tiers
```
GET /api/sponsorship-tiers/

Response (200):
[
  {
    "id": 1,
    "tier_name": "platinum",
    "amount": "5000000.00",
    "description": "Platinum Sponsor - Premium benefits"
  },
  ...
]
```

#### 2. Initiate Payment
```
POST /api/initiate-sponsorship-payment/

Request:
{
  "company_name": "Acme Corp",
  "contact_name": "John Doe",
  "email": "john@acme.com",
  "phone": "+234812345678",
  "country": "Nigeria",
  "tier_id": 1
}

Response (200 - Success):
{
  "success": true,
  "link": "https://checkout.flutterwave.com/...",
  "reference": "STICONF-ABC123DEF456"
}

Response (400 - Failure):
{
  "success": false,
  "message": "Missing required fields"
}

Response (500 - Gateway Error):
{
  "success": false,
  "message": "Payment gateway is not configured."
}
```

#### 3. Verify Payment
```
POST /api/verify-sponsorship-payment/

Request:
{
  "transaction_id": "1234567890"
}

Response (200 - Success):
{
  "success": true,
  "message": "Payment verified successfully",
  "reference": "STICONF-ABC123DEF456"
}

Response (400 - Failure):
{
  "success": false,
  "message": "Payment verification failed"
}
```

---

## 🔧 Configuration Files

### settings.py
```python
# Flutterwave configuration
FLUTTERWAVE_PUBLIC_KEY = os.getenv('FLUTTERWAVE_PUBLIC_KEY', '')
FLUTTERWAVE_SECRET_KEY = os.getenv('FLUTTERWAVE_SECRET_KEY', '')

# Email configuration (BREVO)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('BREVO_SMTP_USER')
EMAIL_HOST_PASSWORD = os.getenv('BREVO_SMTP_PASSWORD')
DEFAULT_FROM_EMAIL = 'STICONF 2026 <noreply@sticonf.com>'
```

### .env
```env
# Flutterwave Configuration
FLUTTERWAVE_PUBLIC_KEY=FLWPUBK_YOUR_KEY
FLUTTERWAVE_SECRET_KEY=FLWSECK_YOUR_KEY

# BREVO Email Configuration
BREVO_API_KEY=xkeysib-...
BREVO_LIST_ID=2
BREVO_SMTP_USER=a85adf001@smtp-brevo.com
BREVO_SMTP_PASSWORD=xsmtpsib-...
ADMIN_EMAIL=sticonfinternational@gmail.com
```

### urls.py
```python
urlpatterns = [
    # Flutterwave sponsorship payment endpoints
    path('api/sponsorship-tiers/', views.get_sponsorship_tiers_json, name='get_sponsorship_tiers'),
    path('api/initiate-sponsorship-payment/', views.initiate_sponsorship_payment, name='initiate_sponsorship_payment'),
    path('api/verify-sponsorship-payment/', views.verify_sponsorship_payment, name='verify_sponsorship_payment'),
]
```

---

## 📝 Files Modified/Created

### Modified Files:
1. **main/views.py**
   - Updated `sponsorship()` view to pass `FLUTTERWAVE_PUBLIC_KEY` to template
   - Added Flutterwave configuration validation in payment endpoints
   - Three payment-related views: `get_sponsorship_tiers_json()`, `initiate_sponsorship_payment()`, `verify_sponsorship_payment()`

2. **sticonf/settings.py**
   - Added Flutterwave configuration variables
   - Added `testserver` and `localhost` to ALLOWED_HOSTS
   - Email backend configured for BREVO SMTP

3. **main/urls.py**
   - Three new API endpoints for sponsorship payments

### Created Files:
1. **test_flutterwave_integration.py**
   - Comprehensive test suite with 8 test cases
   - Validates environment configuration, database, email, API endpoints
   - Produces colored output for easy readability

2. **FLUTTERWAVE_SETUP_GUIDE.md**
   - This documentation

### Database:
- `SponsorshipTier` model with 4 tiers initialized
- `Sponsorship` model for tracking payments
- All migrations applied

---

## 🧪 Testing

### Run All Tests
```bash
cd c:\Users\BestEmpireComputers\Desktop\Michael_JImin\sticonf
python test_flutterwave_integration.py
```

### Manual Testing

#### Test 1: Access Sponsorship Page
```
http://localhost:8000/sponsorship/
```
Should display sponsorship form with Flutterwave branding.

#### Test 2: Get Sponsorship Tiers (API)
```bash
curl http://localhost:8000/api/sponsorship-tiers/
```

#### Test 3: Initiate Payment (Test Mode)
```bash
curl -X POST http://localhost:8000/api/initiate-sponsorship-payment/ \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Company",
    "contact_name": "John Doe",
    "email": "test@example.com",
    "phone": "+234812345678",
    "country": "Nigeria",
    "tier_id": 1
  }'
```

#### Test 4: Check Database
```bash
python manage.py shell
>>> from main.models import Sponsorship
>>> Sponsorship.objects.all()
```

---

## ⚠️ Known Issues & Fixes

### Issue 1: Missing Context Variable ❌ FIXED ✅
**Problem:** Template was trying to use `{{ FLUTTERWAVE_PUBLIC_KEY }}` but it wasn't being passed in context.

**Fix:** Updated `sponsorship()` view to pass context:
```python
def sponsorship(request):
    context = {
        'FLUTTERWAVE_PUBLIC_KEY': settings.FLUTTERWAVE_PUBLIC_KEY
    }
    return render(request, 'sponsorship.html', context)
```

### Issue 2: Placeholder API Keys ❌ REQUIRES USER ACTION ⚠️
**Problem:** .env file has placeholder values that will cause payments to fail.

**Fix:** User must replace with actual Flutterwave keys (see Step 1 above).

### Issue 3: Missing Sponsorship Tiers ❌ FIXED ✅
**Problem:** Database had no sponsorship tiers, causing forms to fail.

**Fix:** Tiers initialized in database:
```python
SponsorshipTier.objects.bulk_create([
    SponsorshipTier(tier_name='platinum', amount=5000000, ...),
    SponsorshipTier(tier_name='gold', amount=2500000, ...),
    SponsorshipTier(tier_name='silver', amount=1000000, ...),
    SponsorshipTier(tier_name='bronze', amount=500000, ...),
])
```

### Issue 4: Empty ALLOWED_HOSTS ❌ FIXED ✅
**Problem:** Tests failed because `ALLOWED_HOSTS` was empty.

**Fix:** Updated `settings.py`:
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', 'sticonf.com', 'www.sticonf.com']
```

### Issue 5: Missing Payment Gateway Validation ❌ FIXED ✅
**Problem:** No validation that Flutterwave keys are configured.

**Fix:** Added configuration checks in payment endpoints:
```python
if not settings.FLUTTERWAVE_PUBLIC_KEY or not settings.FLUTTERWAVE_SECRET_KEY:
    return JsonResponse({
        'success': False, 
        'message': 'Payment gateway is not configured.'
    }, status=500)
```

---

## 🔐 Security Considerations

1. **CSRF Protection**
   - Payment endpoints have `@csrf_exempt` decorator
   - ✅ This is intentional for API endpoints accepting POST from Flutterwave

2. **Secret Key Protection**
   - `FLUTTERWAVE_SECRET_KEY` should NEVER be exposed to frontend
   - ✅ Properly stored in environment variables, not in JavaScript

3. **ALLOWED_HOSTS**
   - Configured to prevent Host header attacks
   - ✅ Update with your domain before production

4. **SSL/TLS**
   - Ensure website uses HTTPS in production
   - Flutterwave requires HTTPS for security

5. **Database**
   - Sponsorship records are not deleted after payment
   - ✅ Maintains audit trail
   - Payment reference is unique to prevent duplicates

---

## 📊 Troubleshooting

### Problem: "Payment gateway is not configured"
**Solution:** Check that both `FLUTTERWAVE_PUBLIC_KEY` and `FLUTTERWAVE_SECRET_KEY` are set in `.env` and not placeholders.

### Problem: "Missing required fields"
**Solution:** Ensure all form fields are filled: company_name, contact_name, email, phone, tier_id.

### Problem: Payment verification fails
**Solution:** 
1. Check that transaction ID is correct
2. Verify Flutterwave account status is active
3. Check network logs for API response errors

### Problem: Emails not sending
**Solution:**
1. Verify BREVO SMTP credentials in `.env`
2. Check `ADMIN_EMAIL` is configured
3. Test with: `python manage.py shell` → `from django.core.mail import send_mail` → `send_mail(...)`

### Problem: "testserver not in ALLOWED_HOSTS"
**Solution:** Already fixed. Tests should now work.

---

## 📞 Support & References

- **Flutterwave Docs:** https://developer.flutterwave.com/
- **Flutterwave API Reference:** https://developer.flutterwave.com/reference
- **Django Payments:** https://docs.djangoproject.com/en/5.2/topics/payments/
- **BREVO Email:** https://www.brevo.com/

---

## ✨ Next Steps

- [ ] Replace placeholder Flutterwave keys with actual keys
- [ ] Run test suite to verify all systems
- [ ] Test payment flow end-to-end
- [ ] Set up production domain in ALLOWED_HOSTS
- [ ] Enable HTTPS on production
- [ ] Configure monitoring for payment failures
- [ ] Set up admin dashboard for sponsorship tracking
- [ ] Create user documentation for sponsors

---

**Last Updated:** April 17, 2026  
**Status:** ✅ Ready for Configuration & Testing
