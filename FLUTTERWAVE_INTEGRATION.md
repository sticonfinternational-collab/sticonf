# STICONF 2026 Flutterwave Sponsorship Integration Guide

## Overview

This document describes the complete Flutterwave payment integration for the STICONF 2026 sponsorship page. The system handles:

1. **Payment Processing**: Secure payment collection through Flutterwave
2. **Data Persistence**: Sponsorship records saved to database
3. **Email Notifications**: Automated confirmation emails to sponsors and admins
4. **Admin Dashboard**: Management interface for tracking sponsorships

---

## System Components

### 1. **Frontend (sponsorship.html)**

#### Payment Modal
- Form to collect company and contact information
- Validates all required fields before submission
- Real-time validation for email addresses
- Displays sponsorship tier and amount

#### JavaScript Payment Handler
- `initializeSponsorshipTiers()` - Loads tier data from backend API
- `openPaymentModal(tierName)` - Opens payment modal with tier details
- `closePaymentModal()` - Closes the modal (blocked while processing)
- Payment form submission with validation
- Flutterwave checkout integration
- Payment verification callback

**Key Features:**
- Backup pricing configuration if API fails
- Loading states and error handling
- Prevents duplicate submissions with `isProcessingPayment` flag
- Proper form reset on successful payment

### 2. **Backend (views.py)**

#### API Endpoints

**GET `/api/sponsorship-tiers/`**
- Returns JSON list of all sponsorship tiers with ID, name, amount, description
- Used by frontend to populate modal with current pricing

**POST `/api/initiate-sponsorship-payment/`**
- Creates a `Sponsorship` record in the database with `pending` status
- Generates unique payment reference (e.g., `STICONF-ABC123DEF456`)
- Calls Flutterwave API to create payment session
- Returns payment link and reference for frontend

**POST `/api/verify-sponsorship-payment/`**
- Receives transaction ID from Flutterwave callback
- Verifies payment with Flutterwave API
- Updates sponsorship status to `paid` and records transaction ID
- Sends confirmation emails to sponsor and admin
- Returns success/failure response to frontend

#### Email Sending Function

**`send_sponsorship_confirmation(sponsorship)`**
- Renders HTML email templates with sponsorship details
- Sends confirmation email to sponsor (`emails/sponsorship_confirmation.html`)
- Sends notification email to admin (`emails/sponsorship_admin_notification.html`)
- Handles email errors gracefully with try-catch blocks

### 3. **Database Models**

#### SponsorshipTier
```python
tier_name: CharField (platinum, gold, silver, bronze)
amount: DecimalField (e.g., 10000000 for ₦10M)
description: TextField
```

#### Sponsorship
```python
company_name: CharField
contact_name: CharField
email: EmailField
phone: CharField
country: CharField (default: Nigeria)
tier: ForeignKey to SponsorshipTier
amount: DecimalField
status: CharField (pending, paid, failed, cancelled)
reference: CharField (unique, auto-generated)
transaction_id: CharField (Flutterwave transaction ID)
created_at: DateTimeField (auto-set on creation)
updated_at: DateTimeField (auto-updated)
paid_at: DateTimeField (set when payment confirmed)
```

### 4. **Email Templates**

#### `emails/sponsorship_confirmation.html`
Sent to the sponsor after successful payment. Includes:
- Professional header with STICONF branding
- Sponsorship details (tier, amount, reference)
- Next steps (team will contact within 24 hours)
- Conference details and contact information
- Footer with website and email links

#### `emails/sponsorship_admin_notification.html`
Sent to admin (ADMIN_EMAIL) for each new sponsorship. Includes:
- Company and contact information
- Payment details and amount
- Payment reference and transaction ID
- Next steps for sponsorship fulfillment
- Link to admin dashboard for managing sponsorship

---

## Payment Flow

```
1. User opens sponsorship.html
   ↓
2. JavaScript loads tier data from /api/sponsorship-tiers/
   ↓
3. User clicks "Become [Tier]" button
   ↓
4. Payment modal opens with tier details
   ↓
5. User fills form and submits
   ↓
6. Form data sent to /api/initiate-sponsorship-payment/
   ↓
7. Backend creates Sponsorship record (status=pending)
   ↓
8. Backend calls Flutterwave API to create payment session
   ↓
9. Flutterwave modal opens (payment options: card, USSD, account transfer)
   ↓
10. User completes payment on Flutterwave
    ↓
11. Flutterwave returns to callback function
    ↓
12. Frontend receives transaction_id
    ↓
13. Frontend calls /api/verify-sponsorship-payment/
    ↓
14. Backend verifies with Flutterwave API
    ↓
15. Backend updates Sponsorship status to 'paid'
    ↓
16. Backend sends confirmation emails
    ↓
17. Frontend shows success message
    ↓
18. Modal closes and form resets
```

---

## Environment Configuration

Required environment variables in `.env`:

```bash
# Flutterwave Payment Gateway
FLUTTERWAVE_PUBLIC_KEY=pk_test_xxxxx or pk_live_xxxxx
FLUTTERWAVE_SECRET_KEY=sk_test_xxxxx or sk_live_xxxxx

# Email Configuration (Brevo SMTP)
BREVO_SMTP_USER=your-email@brevo.com
BREVO_SMTP_PASSWORD=your-brevo-password
ADMIN_EMAIL=admin@sticonf.com

# Django Settings
SECRET_KEY=your-django-secret-key
DEBUG=False (for production)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## Admin Dashboard

Access sponsorships at `/admin/main/sponsorship/`

### Features
- **List View**: See all sponsorships with status badges
- **Filter**: By status, tier, country, date
- **Search**: By company name, contact, email, or reference
- **Readonly Fields**: Reference, transaction ID, timestamps
- **Fieldsets**: Organized by information type

### Status Badges
- **Pending** (Orange): Payment initiated, awaiting completion
- **Paid** (Green): Payment confirmed
- **Failed** (Red): Payment failed
- **Cancelled** (Red): Payment cancelled

---

## Troubleshooting

### "Payment gateway is not configured"
- Check `FLUTTERWAVE_PUBLIC_KEY` and `FLUTTERWAVE_SECRET_KEY` are set in `.env`
- Restart Django development server after setting variables

### Payment verification fails
- Check transaction ID format from Flutterwave
- Verify Flutterwave API keys are correct (not expired)
- Check Django logs for specific error messages

### Emails not sending
- Verify `BREVO_SMTP_USER` and `BREVO_SMTP_PASSWORD` are correct
- Check email templates exist in `main/templates/emails/`
- In development, set `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` to see emails in console

### Form validation errors
- Check all required fields are filled (company name, contact, email, phone)
- Email must be in valid format (user@domain.com)
- Phone should include country code (e.g., +234...)

---

## Testing the Integration

### 1. Local Development
```bash
# Set test Flutterwave keys
FLUTTERWAVE_PUBLIC_KEY=pk_test_...
FLUTTERWAVE_SECRET_KEY=sk_test_...

# Run development server
python manage.py runserver

# Access sponsorship page
http://localhost:8000/sponsorship/
```

### 2. Test Payment
- Use Flutterwave test cards:
  - **Visa**: 4242 4242 4242 4242
  - **MasterCard**: 5531 8866 5592 2950
- Use any future expiry date (MM/YY)
- Use any 3-digit CVV

### 3. Verify Records
- Check admin dashboard: http://localhost:8000/admin/main/sponsorship/
- Check email console (if using console backend)
- Check database: `Sponsorship.objects.all()`

### 4. Production Testing
- Replace test keys with live Flutterwave keys
- Test with small amount before full deployment
- Monitor email delivery

---

## Security Considerations

1. **API Keys**: Never commit `.env` file with keys
2. **CSRF Protection**: `@csrf_exempt` used for API endpoints (already handles CSRF validation via POST)
3. **Data Validation**: All inputs validated before processing
4. **HTTPS**: Ensure production uses HTTPS for all Flutterwave transactions
5. **Error Messages**: Avoid exposing internal errors to users
6. **Payment Verification**: Always verify payments with Flutterwave API, don't trust client alone

---

## Monitoring & Maintenance

### Daily
- Check admin dashboard for new sponsorships
- Verify confirmation emails were sent
- Monitor payment success rate

### Weekly
- Review sponsorship metrics
- Check for failed payments
- Ensure email delivery is working

### Monthly
- Reconcile payments with Flutterwave
- Update sponsor list for marketing
- Generate sponsorship reports

---

## Support

For issues or questions:
- **Email**: sponsorship@sticonf.com
- **Documentation**: See README.md
- **Flutterwave API Docs**: https://developer.flutterwave.com
