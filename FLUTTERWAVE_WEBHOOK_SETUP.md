# 🔄 FLUTTERWAVE WEBHOOK IMPLEMENTATION - COMPLETE GUIDE

## What's Changed

### Before (Unreliable):
```
1. User pays via Flutterwave
2. Frontend receives callback with transaction_id
3. Frontend calls /api/verify-sponsorship-payment/
4. Backend verifies with Flutterwave API
❌ Problem: Network issues could prevent verification
```

### After (Reliable with Webhooks):
```
1. User pays via Flutterwave
2. Flutterwave securely calls our webhook endpoint
3. Webhook verifies signature & processes payment
4. Database updated reliably
✅ Problem solved: Works even if user closes browser
```

---

## Files Modified

### 1. Backend Files Created/Updated:

#### `main/flutterwave_utils.py` ✅ CREATED
- `verify_webhook_signature()` - Securely verifies Flutterwave webhooks
- `get_payment_status_from_webhook()` - Extracts payment status
- `verify_payment_with_flutterwave()` - Manual verification fallback

#### `main/views.py` ✅ UPDATED
- Added `flutterwave_webhook()` endpoint
- Handles webhook from Flutterwave
- Updates sponsorship records
- Sends confirmation emails

#### `main/urls.py` ✅ UPDATED
- Added webhook URL: `/api/webhooks/flutterwave/`

---

## How to Configure Flutterwave Webhook

### Step 1: Get Your Webhook URL

**Local Development (for testing):**
- You need `ngrok` to expose localhost to internet
- OR skip local testing and test on Render

**Production (Render):**
```
https://sticonf.onrender.com/api/webhooks/flutterwave/
```

### Step 2: Add Webhook to Flutterwave Dashboard

1. Go to [Flutterwave Dashboard](https://dashboard.flutterwave.com/settings/webhooks)
2. Click **+ Add Webhook**
3. Paste webhook URL: `https://sticonf.onrender.com/api/webhooks/flutterwave/`
4. Select events: 
   - ✅ Charge Completed
   - ✅ Charge Failed
   - ✅ Transfer Completed
5. Click **Save**

---

## Payment Flow with Webhooks

### Frontend Flow:
```javascript
1. User fills sponsorship form
2. Click "Pay Now"
3. API call to /api/initiate-sponsorship-payment/
   ↓
4. Sponsorship created with status='pending'
5. Flutterwave payment link returned
   ↓
6. Flutterwave modal opens
7. User completes payment (or cancels)
   ↓
8. Flutterwave modal closes
9. Show loading message
10. Poll for payment status (check database)
```

### Backend Flow (Webhook):
```
1. User completes payment on Flutterwave
2. Flutterwave calls our webhook
3. Webhook signature verified ✅
4. Payment status extracted from payload
5. Sponsorship record updated
6. Confirmation emails sent
7. Return 200 OK to Flutterwave
```

---

## Updated Frontend Code

Replace your current payment script in `sponsorship.html` with this:

```javascript
// Handle payment form submission
document.getElementById('paymentForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (isProcessingPayment) {
        showToast('Payment is being processed. Please wait...', true);
        return;
    }
    
    if (!currentTier) {
        showToast('No sponsorship tier selected. Please try again.', true);
        return;
    }
    
    if (!flutterwavePublicKey) {
        showToast('Payment gateway is not configured. Please contact support.', true);
        return;
    }
    
    // Get form data
    const companyName = document.getElementById('companyName').value.trim();
    const contactName = document.getElementById('contactName').value.trim();
    const email = document.getElementById('paymentEmail').value.trim();
    const phone = document.getElementById('paymentPhone').value.trim();
    const country = (document.getElementById('paymentCountry').value || 'Nigeria').trim();
    
    // Validate form
    if (!companyName || !contactName || !email || !phone) {
        showToast('Please fill in all required fields.', true);
        return;
    }
    
    if (!isValidEmail(email)) {
        showToast('Please enter a valid email address.', true);
        return;
    }
    
    isProcessingPayment = true;
    
    const formData = {
        company_name: companyName,
        contact_name: contactName,
        email: email,
        phone: phone,
        country: country,
        tier_id: currentTier.id
    };
    
    try {
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Processing...</span>';
        
        // Initiate payment
        const response = await fetch('/api/initiate-sponsorship-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (!data.success) {
            showToast(data.message || 'Failed to initiate payment. Please try again.', true);
            isProcessingPayment = false;
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            return;
        }
        
        // Store reference for polling
        const paymentReference = data.reference;
        
        // Initialize Flutterwave payment
        FlutterwaveCheckout({
            public_key: flutterwavePublicKey,
            tx_ref: paymentReference,
            amount: parseFloat(currentTier.amount),
            currency: 'NGN',
            payment_options: 'card,ussd,account_transfer',
            customer: {
                email: email,
                name: contactName,
                phonenumber: phone
            },
            customizations: {
                title: 'STICONF 2026 Sponsorship',
                description: currentTier.tier_name.toUpperCase() + ' Sponsorship Package',
                logo: '/static/images/logo.png'
            },
            callback: function(response) {
                console.log('Flutterwave callback:', response);
                if (response.status === 'successful') {
                    // Payment successful - start polling for webhook confirmation
                    pollPaymentStatus(paymentReference);
                } else {
                    isProcessingPayment = false;
                    showToast('Payment was not completed. Please try again.', true);
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            },
            onclose: function() {
                console.log('Flutterwave modal closed');
                // Don't immediately set isProcessingPayment = false
                // Let polling verify the payment
            }
        });
        
    } catch (error) {
        console.error('Payment error:', error);
        showToast('An error occurred while processing your payment. Please try again.', true);
        isProcessingPayment = false;
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = false;
    }
});

// Poll for payment confirmation (webhook may take a few seconds)
async function pollPaymentStatus(reference) {
    const maxAttempts = 30; // 30 attempts * 1 second = 30 seconds
    let attempts = 0;
    
    const pollInterval = setInterval(async () => {
        attempts++;
        
        try {
            const response = await fetch(`/api/sponsorship-status/?reference=${reference}`);
            const data = await response.json();
            
            if (data.success && data.status === 'paid') {
                // Payment confirmed!
                clearInterval(pollInterval);
                isProcessingPayment = false;
                
                closePaymentModal();
                document.getElementById('paymentForm').reset();
                
                showToast('🎉 Payment successful! Thank you for sponsoring STICONF 2026!', false);
                
                // Reload page after 3 seconds
                setTimeout(() => {
                    location.reload();
                }, 3000);
            } else if (data.success && data.status === 'failed') {
                // Payment failed
                clearInterval(pollInterval);
                isProcessingPayment = false;
                showToast('Payment was declined. Please try again.', true);
            } else if (attempts >= maxAttempts) {
                // Timeout
                clearInterval(pollInterval);
                isProcessingPayment = false;
                showToast('Payment verification timed out. Please check your email for confirmation.', true);
            }
        } catch (error) {
            console.error('Polling error:', error);
            if (attempts >= maxAttempts) {
                clearInterval(pollInterval);
                isProcessingPayment = false;
                showToast('Unable to verify payment. Please check your email for confirmation.', true);
            }
        }
    }, 1000); // Poll every 1 second
}
```

---

## Add Status Check Endpoint

Add this endpoint to `main/views.py`:

```python
@csrf_exempt
def get_sponsorship_status(request):
    """Get current status of a sponsorship payment"""
    if request.method == 'GET':
        reference = request.GET.get('reference')
        if not reference:
            return JsonResponse({'success': False, 'message': 'Missing reference'}, status=400)
        
        try:
            sponsorship = Sponsorship.objects.get(reference=reference)
            return JsonResponse({
                'success': True,
                'status': sponsorship.status,
                'reference': reference
            })
        except Sponsorship.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Sponsorship not found'}, status=404)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
```

Add to `main/urls.py`:
```python
path('api/sponsorship-status/', views.get_sponsorship_status, name='get_sponsorship_status'),
```

---

## Testing the Webhook

### Test Locally (Render):

1. Deploy to Render with the changes
2. Go to Flutterwave Dashboard
3. Add webhook URL: `https://sticonf.onrender.com/api/webhooks/flutterwave/`
4. Make a test payment
5. Check Render logs for webhook debug output:
   ```
   Webhook: Processing payment STICONF-XXXXX - Status: paid
   Webhook: Confirmation emails sent for STICONF-XXXXX
   ```

### Check Webhook Delivery:

1. Go to Flutterwave Dashboard → Webhooks
2. Click your webhook URL
3. View delivery logs to see if Flutterwave successfully called your endpoint

---

## Error Handling & Logging

Check logs in Render for debugging:

```bash
# Connect to Render
render connect sticonf

# View logs
tail -f logs/error.log
```

Look for:
- ✅ `Webhook: Processing payment...` - Webhook received
- ✅ `Webhook: Invalid signature` - Security issue
- ✅ `Webhook: Confirmation emails sent` - Success
- ❌ `Webhook: Payment failed` - Payment declined
- ❌ `Webhook: Sponsorship not found` - Reference mismatch

---

## Security Features

✅ **Webhook Signature Verification**
- Every webhook verified with Flutterwave secret key
- HMAC-SHA256 signature check
- Prevents fake webhook requests

✅ **CSRF Protection**
- Webhook endpoint uses `@csrf_exempt` (Flutterwave sends no CSRF token)
- Other endpoints protected

✅ **Error Handling**
- Invalid signatures rejected
- Malformed payloads handled
- Exceptions logged and reported

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Webhook not being called | Check URL in Flutterwave dashboard (must be HTTPS) |
| "Invalid signature" in logs | Verify FLUTTERWAVE_SECRET_KEY is correct |
| Payment not updated | Check Render logs for webhook delivery |
| Emails not sent | Check BREVO email settings |
| Payment stuck as pending | Webhook may be delayed, check again in 30 seconds |

---

## Deployment Checklist

- [ ] Commit changes to GitHub
- [ ] Push to Render
- [ ] Wait for deployment to complete
- [ ] Check Render logs for errors
- [ ] Add webhook to Flutterwave dashboard
- [ ] Test with small amount
- [ ] Verify confirmation email received
- [ ] Check admin dashboard for new sponsorship record

You're all set! The webhook implementation is more reliable than client-side verification. 🚀
