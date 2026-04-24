# Flutterwave Sponsorship Integration - Setup & Testing Checklist

## ✅ What's Been Implemented

### Frontend (sponsorship.html)
- [x] Payment modal with form validation
- [x] Real-time tier and amount display
- [x] Flutterwave checkout integration
- [x] Payment verification callback
- [x] Error handling and user feedback via toast notifications
- [x] Loading states and duplicate submission prevention
- [x] Backup tier pricing (in case API fails)
- [x] Email validation
- [x] Professional form styling

### Backend (views.py)
- [x] `get_sponsorship_tiers_json()` - API endpoint for tier data
- [x] `initiate_sponsorship_payment()` - Creates sponsorship record & initiates Flutterwave payment
- [x] `verify_sponsorship_payment()` - Verifies payment with Flutterwave API
- [x] `send_sponsorship_confirmation()` - Sends confirmation emails
- [x] CSRF exemption for API endpoints
- [x] Error handling and logging
- [x] Database transaction management

### Database (models.py)
- [x] `SponsorshipTier` model with 4 tiers (Platinum, Gold, Silver, Bronze)
- [x] `Sponsorship` model with complete payment tracking
- [x] Status tracking (pending, paid, failed, cancelled)
- [x] Timestamp recording (created_at, updated_at, paid_at)
- [x] Unique reference generation

### Email Templates
- [x] `sponsorship_confirmation.html` - Professional sponsor confirmation email
- [x] `sponsorship_admin_notification.html` - Admin notification email with action items
- [x] Both use Brevo SMTP for sending

### Admin Dashboard
- [x] Sponsorship admin interface at `/admin/main/sponsorship/`
- [x] List view with status badges and filtering
- [x] Readonly fields protection
- [x] Organized fieldsets

### Documentation
- [x] `FLUTTERWAVE_INTEGRATION.md` - Complete integration guide
- [x] Payment flow diagram
- [x] Troubleshooting guide
- [x] Environment configuration guide

---

## 🔧 Setup Instructions

### 1. Update Environment Variables (.env)

```bash
# Flutterwave Keys (get from https://dashboard.flutterwave.com)
FLUTTERWAVE_PUBLIC_KEY=pk_test_xxxxx  # or pk_live_xxxxx for production
FLUTTERWAVE_SECRET_KEY=sk_test_xxxxx  # or sk_live_xxxxx for production

# Email Configuration
BREVO_SMTP_USER=your-email@example.com
BREVO_SMTP_PASSWORD=your-brevo-password
ADMIN_EMAIL=admin@sticonf.com
```

### 2. Create Database Records (Django Admin)

Go to `/admin/main/sponsorshiptier/` and create tiers:

**Platinum**
- Amount: 10000000 (₦10M)
- Description: Exclusive top-tier partnership

**Gold**
- Amount: 5000000 (₦5M)
- Description: Premium visibility package

**Silver**
- Amount: 2000000 (₦2M)
- Description: Strong brand presence

**Bronze**
- Amount: 1000000 (₦1M)
- Description: Community engagement

### 3. Run Migrations (if needed)

```bash
python manage.py migrate
```

### 4. Collect Static Files

```bash
python manage.py collectstatic
```

### 5. Test the Setup

```bash
python manage.py runserver
```

---

## 🧪 Testing the Integration

### Test Case 1: Frontend Load & Display
1. Visit http://localhost:8000/sponsorship/
2. ✓ Page loads without errors
3. ✓ All 4 sponsorship tiers are visible
4. ✓ "Become [Tier]" buttons are clickable
5. ✓ Console shows no JavaScript errors

### Test Case 2: Modal Opening
1. Click any "Become [Tier]" button
2. ✓ Payment modal opens
3. ✓ Tier name and amount display correctly
4. ✓ Modal closes when clicking the X button
5. ✓ Form is empty on open

### Test Case 3: Form Validation
1. Click "Become Bronze" button
2. Leave all fields empty
3. Click "Proceed to Payment"
4. ✓ Error message: "Please fill in all required fields"
5. Fill company name only
6. Click "Proceed to Payment"
7. ✓ Error message appears
8. Fill all fields except with invalid email (e.g., "test")
9. Click "Proceed to Payment"
10. ✓ Error message: "Please enter a valid email address"

### Test Case 4: Backend API - Get Tiers
1. In browser console, run:
   ```javascript
   fetch('/api/sponsorship-tiers/')
     .then(r => r.json())
     .then(d => console.log(d))
   ```
2. ✓ Returns JSON array with all 4 tiers
3. ✓ Each tier has: id, tier_name, amount, description

### Test Case 5: Backend API - Initiate Payment
1. Fill payment form with test data:
   - Company: "Test Company Ltd"
   - Contact: "John Doe"
   - Email: "john@test.com"
   - Phone: "+2341234567890"
   - Country: "Nigeria"
2. Submit form
3. ✓ Loading state shows "Processing..."
4. ✓ No JavaScript errors in console
5. ✓ Flutterwave modal should open (or error if keys invalid)

### Test Case 6: Flutterwave Payment (Test Mode)
1. In Flutterwave modal, select "Card"
2. Use test card: `4242 4242 4242 4242`
3. Expiry: Any future date (e.g., 12/25)
4. CVV: Any 3 digits (e.g., 123)
5. Enter OTP (if required): Any 6 digits
6. ✓ Payment processes
7. ✓ Modal closes with success
8. ✓ Success toast: "Sponsorship payment confirmed!"

### Test Case 7: Database Record Creation
1. Open Django admin: http://localhost:8000/admin/
2. Navigate to Sponsorships
3. ✓ New sponsorship record appears
4. ✓ Status: "Paid" (green badge)
5. ✓ Reference starts with "STICONF-"
6. ✓ Transaction ID is populated
7. ✓ Amount matches what was paid
8. ✓ paid_at timestamp is recent

### Test Case 8: Email Sending
If using console backend (in development):

1. Check Django server console output
2. ✓ Two emails sent: one to sponsor, one to admin
3. ✓ Sponsor email subject: "STICONF 2026 Sponsorship Confirmed - ₦..."
4. ✓ Admin email subject: "New STICONF 2026 Sponsorship: ..."

For production (with Brevo):

1. Check sponsor email inbox
2. ✓ Email arrives within 1-2 minutes
3. ✓ Contains sponsorship details
4. ✓ Professional HTML formatting
5. ✓ Check admin email for notification

### Test Case 9: Failed Payment
1. Click "Become Silver" button
2. Fill form with test data
3. In Flutterwave modal, click "X" or "Cancel"
4. ✓ Toast: "Payment was not completed. Please try again."
5. ✓ Modal closes
6. ✓ Check database - sponsorship status still "pending"

### Test Case 10: Duplicate Submission Prevention
1. Fill payment form
2. Click "Proceed to Payment"
3. Immediately click button again (before modal opens)
4. ✓ Toast: "Payment is being processed. Please wait..."
5. ✓ Button doesn't trigger multiple requests

---

## 📊 Production Deployment Checklist

- [ ] Replace Flutterwave test keys with live keys
- [ ] Update ADMIN_EMAIL to production email
- [ ] Verify Brevo SMTP credentials
- [ ] Set DEBUG=False in settings
- [ ] Set ALLOWED_HOSTS to production domain
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Test payment with real transaction (small amount)
- [ ] Verify emails deliver to production inbox
- [ ] Monitor payment success rate
- [ ] Set up admin access for team
- [ ] Test database backups
- [ ] Configure email forwarding for sponsorship@sticonf.com

---

## 🐛 Common Issues & Solutions

### Issue: "Payment gateway is not configured"
**Solution**: 
1. Check `.env` file has FLUTTERWAVE_PUBLIC_KEY and FLUTTERWAVE_SECRET_KEY
2. Restart Django development server
3. Check keys are not wrapped in quotes

### Issue: Flutterwave modal doesn't open
**Solution**:
1. Check browser console for JavaScript errors
2. Verify FLUTTERWAVE_PUBLIC_KEY is correct
3. Check internet connection
4. Try incognito/private mode (to clear cache)

### Issue: Payment verifies but emails don't send
**Solution**:
1. Check Brevo SMTP credentials in `.env`
2. Enable "Less secure apps" if using Brevo
3. Test with console backend first: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
4. Check Django logs for email errors

### Issue: Database record created but status not updated after payment
**Solution**:
1. Check Flutterwave transaction ID is received
2. Verify Flutterwave secret key is correct
3. Check Django logs for verification errors
4. Try payment again

### Issue: Admin can't see sponsorships
**Solution**:
1. Run migrations: `python manage.py migrate`
2. Check Sponsorship model is registered in admin.py
3. Refresh browser and clear cache

---

## 📝 Files Modified/Created

### New Files
- ✅ `main/templates/emails/sponsorship_confirmation.html`
- ✅ `main/templates/emails/sponsorship_admin_notification.html`
- ✅ `FLUTTERWAVE_INTEGRATION.md`

### Modified Files
- ✅ `main/templates/sponsorship.html` (JavaScript payment handling)
- ✅ `main/views.py` (email sending function)

### Pre-existing (No changes needed)
- ✅ `main/models.py` (Sponsorship & SponsorshipTier already set up)
- ✅ `main/admin.py` (Admin interface already configured)
- ✅ `main/urls.py` (API endpoints already mapped)

---

## 🎯 Next Steps

1. **Test locally** using the test cases above
2. **Get live Flutterwave keys** from https://dashboard.flutterwave.com
3. **Configure production environment** with live keys
4. **Test payment with small amount** in production
5. **Monitor first few sponsorships** to ensure emails deliver
6. **Set up admin user** for managing sponsorships
7. **Announce** sponsorship opportunities to organizations

---

## 📞 Support

For questions or issues:
- Check `FLUTTERWAVE_INTEGRATION.md` for detailed documentation
- Review Flutterwave API docs: https://developer.flutterwave.com
- Check Django error logs: `python manage.py runserver` output
- Monitor email delivery: Check email provider dashboard

---

**Last Updated**: April 24, 2026
**Status**: ✅ Complete and Ready for Testing
