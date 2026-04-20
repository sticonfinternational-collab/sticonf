from django.shortcuts import render
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from main.models import Sponsorship, SponsorshipTier, Registration, Contact
import requests
import uuid
from decimal import Decimal


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def schedule(request):
    return render(request, 'schedule.html')

def contact(request):
    return render(request, 'contact.html')

def handle_contact(request):
    if request.method == 'POST':
        name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('category', '').strip()
        organisation = request.POST.get('organisation', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('interest', '').strip()

        if not all([name, email, subject, message]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'contact.html')

        # Parse name into first and last
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        try:
            # Save contact to database
            contact = Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                category=subject,
                organisation=organisation,
                phone=phone,
                interest=message,
                read=False,
                responded=False
            )
            
            # Prepare email content
            email_subject = f"STICONF 2026 Contact: {subject}"
            context = {
                'name': name,
                'email': email,
                'subject': subject,
                'organisation': organisation,
                'message': message,
                'submitted_at': request.POST.get('submitted_at', '')
            }

            # Render HTML email template
            html_message = render_to_string('emails/contact_form.html', context)
            plain_message = strip_tags(html_message)

            # Send email to admin
            send_mail(
                subject=email_subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                html_message=html_message,
                fail_silently=False,
            )

            # Send confirmation email to user
            confirmation_subject = "Thank you for contacting STICONF 2026"
            confirmation_html = render_to_string('emails/contact_confirmation.html', context)
            confirmation_plain = strip_tags(confirmation_html)

            send_mail(
                subject=confirmation_subject,
                message=confirmation_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=confirmation_html,
                fail_silently=False,
            )

            messages.success(request, "Thank you for your message! We've received your inquiry and will respond within 24 hours.")
            return render(request, 'contact.html')

        except Exception as e:
            messages.error(request, f"Sorry, there was an error sending your message. Please try again or contact us directly at info@sticonf.com")
            print(f"Contact form error: {e}")
            return render(request, 'contact.html')

    return redirect('contact')

def sponsorship(request):
    context = {
        'FLUTTERWAVE_PUBLIC_KEY': settings.FLUTTERWAVE_PUBLIC_KEY
    }
    return render(request, 'sponsorship.html', context)

def register(request):
    return render(request, 'register.html')

@csrf_exempt
def subscribe_to_brevo(request):

    if request.method == 'POST':
        # Preserve the page to redirect back to after submission.
        return_url = request.POST.get('return_url') or 'register'

        # Extract all form fields
        email = request.POST.get('email')
        full_name = request.POST.get('first_name', '')
        if full_name.strip() and ' ' in full_name.strip():
            first_name, last_name = full_name.strip().split(' ', 1)
        else:
            first_name = full_name.strip()
            last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '')
        organisation = request.POST.get('organisation', '')
        category = request.POST.get('category', '')
        country = request.POST.get('country', '')
        interest = request.POST.get('interest', '')

        if not email:
            messages.error(request, "Please provide an email address to register.")
            return redirect(return_url)

        if not settings.BREVO_API_KEY or not settings.BREVO_LIST_ID:
            messages.error(request, "Brevo is not configured. Please check BREVO_API_KEY and BREVO_LIST_ID.")
            return redirect('register')

        if settings.BREVO_API_KEY.startswith('xsmtpsib-'):
            messages.error(request, "Brevo API key is invalid: you are using an SMTP key. Use a Brevo REST API key instead.")
            return redirect('register')

        try:
            list_id = int(settings.BREVO_LIST_ID)
        except (TypeError, ValueError):
            messages.error(request, "Brevo list ID is invalid. Please check BREVO_LIST_ID.")
            return redirect('register')

        try:
            # Save registration to database
            registration, created = Registration.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'organisation': organisation,
                    'category': category,
                    'country': country,
                    'interest': interest,
                    'brevo_synced': False,
                }
            )

            # Configure API
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY
            api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))

            # Build attributes
            attributes = {
                "FIRSTNAME": first_name,
                "LASTNAME": last_name,
                "PHONE": phone,
                "ORGANISATION": organisation,
                "CATEGORY": category,
                "COUNTRY": country,
                "INTEREST": interest,
            }

            new_contact = sib_api_v3_sdk.CreateContact(
                email=email,
                attributes=attributes,
                list_ids=[list_id],
                update_enabled=True
            )

            api_instance.create_contact(new_contact)
            
            # Mark as synced to Brevo
            registration.brevo_synced = True
            registration.save()
            
            messages.success(request, "Registration successful! Thank you for signing up for STICONF 2026. We'll contact you soon.")
            return redirect(return_url)
            
        except ApiException as e:
            error_message = getattr(e, 'body', None) or str(e)
            messages.error(request, f"Registration failed: {error_message}")
            print('Brevo subscription error:', error_message)
            return redirect(return_url)
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            print('Unexpected subscription error:', repr(e))
            return redirect(return_url)

    return render(request, 'register.html')


# ===== FLUTTERWAVE SPONSORSHIP PAYMENT =====
def get_sponsorship_tiers_json(request):
    """Get sponsorship tiers as JSON for frontend"""
    tiers = SponsorshipTier.objects.all().values('id', 'tier_name', 'amount', 'description')
    return JsonResponse(list(tiers), safe=False)


@csrf_exempt
def initiate_sponsorship_payment(request):
    """Initiate Flutterwave payment for sponsorship"""
    if request.method == 'POST':
        try:
            # Validate Flutterwave configuration
            if not settings.FLUTTERWAVE_PUBLIC_KEY or not settings.FLUTTERWAVE_SECRET_KEY:
                return JsonResponse({
                    'success': False, 
                    'message': 'Payment gateway is not configured. Please contact administrator.'
                }, status=500)
            
            import json
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['company_name', 'contact_name', 'email', 'phone', 'tier_id']
            if not all(field in data for field in required_fields):
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)
            
            # Get tier
            tier = SponsorshipTier.objects.get(id=data['tier_id'])
            
            # Generate unique reference
            reference = f"STICONF-{uuid.uuid4().hex[:12].upper()}"
            
            # Create sponsorship record
            sponsorship = Sponsorship.objects.create(
                company_name=data['company_name'],
                contact_name=data['contact_name'],
                email=data['email'],
                phone=data['phone'],
                country=data.get('country', 'Nigeria'),
                tier=tier,
                amount=tier.amount,
                reference=reference,
                status='pending'
            )
            
            # Prepare Flutterwave payload
            flutterwave_data = {
                'tx_ref': reference,
                'amount': float(tier.amount),
                'currency': 'NGN',
                'payment_options': 'card,ussd,account_transfer',
                'customer': {
                    'email': data['email'],
                    'name': data['contact_name'],
                    'phonenumber': data['phone']
                },
                'customizations': {
                    'title': 'STICONF 2026 Sponsorship',
                    'description': f"{tier.get_tier_name_display()} Sponsorship Package",
                    'logo': request.build_absolute_uri('/static/images/logo.png')
                },
                'meta': {
                    'sponsorship_id': sponsorship.id,
                    'tier': tier.tier_name,
                    'company': data['company_name']
                }
            }
            
            # Call Flutterwave API
            headers = {
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                'https://api.flutterwave.com/v3/payments',
                json=flutterwave_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                flutterwave_response = response.json()
                if flutterwave_response.get('status') == 'success':
                    return JsonResponse({
                        'success': True,
                        'link': flutterwave_response.get('data', {}).get('link'),
                        'reference': reference
                    })
            
            # If Flutterwave fails, delete the sponsorship record
            sponsorship.delete()
            return JsonResponse({
                'success': False,
                'message': 'Failed to initialize payment. Please try again.'
            }, status=500)
            
        except SponsorshipTier.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid sponsorship tier'}, status=404)
        except Exception as e:
            print(f"Payment initiation error: {e}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def verify_sponsorship_payment(request):
    """Verify Flutterwave payment and update sponsorship status"""
    if request.method == 'POST':
        try:
            # Validate Flutterwave configuration
            if not settings.FLUTTERWAVE_SECRET_KEY:
                return JsonResponse({
                    'success': False, 
                    'message': 'Payment gateway is not configured. Please contact administrator.'
                }, status=500)
            
            import json
            data = json.loads(request.body)
            
            transaction_id = data.get('transaction_id')
            if not transaction_id:
                return JsonResponse({'success': False, 'message': 'Transaction ID required'}, status=400)
            
            # Verify with Flutterwave
            headers = {
                'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
            }
            
            verify_url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
            response = requests.get(verify_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                verify_response = response.json()
                
                if verify_response.get('status') == 'success' and verify_response.get('data', {}).get('status') == 'successful':
                    reference = verify_response.get('data', {}).get('tx_ref')
                    
                    # Update sponsorship
                    sponsorship = Sponsorship.objects.filter(reference=reference).first()
                    if sponsorship:
                        sponsorship.mark_as_paid()
                        sponsorship.transaction_id = transaction_id
                        sponsorship.save()
                        
                        # Send confirmation email
                        try:
                            send_sponsorship_confirmation(sponsorship)
                        except Exception as e:
                            print(f"Email sending error: {e}")
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Payment verified successfully',
                            'reference': reference
                        })
            
            return JsonResponse({
                'success': False,
                'message': 'Payment verification failed'
            }, status=400)
            
        except Exception as e:
            print(f"Payment verification error: {e}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def send_sponsorship_confirmation(sponsorship):
    """Send sponsorship confirmation email"""
    context = {
        'company_name': sponsorship.company_name,
        'contact_name': sponsorship.contact_name,
        'tier': sponsorship.tier.get_tier_name_display(),
        'amount': f"₦{sponsorship.amount:,.0f}",
        'reference': sponsorship.reference,
        'email': sponsorship.email
    }
    
    # You can create a template like emails/sponsorship_confirmation.html
    html_message = f"""
    <html>
        <body>
            <h2>Thank you for sponsoring STICONF 2026!</h2>
            <p>Dear {context['contact_name']},</p>
            <p>Your sponsorship has been confirmed. Here are the details:</p>
            <table>
                <tr><td><strong>Company:</strong></td><td>{context['company_name']}</td></tr>
                <tr><td><strong>Tier:</strong></td><td>{context['tier']}</td></tr>
                <tr><td><strong>Amount:</strong></td><td>{context['amount']}</td></tr>
                <tr><td><strong>Reference:</strong></td><td>{context['reference']}</td></tr>
            </table>
            <p>Our team will contact you shortly to discuss the next steps and maximize your sponsorship impact.</p>
            <p>Best regards,<br/>STICONF 2026 Team</p>
        </body>
    </html>
    """
    
    send_mail(
        subject=f"STICONF 2026 Sponsorship Confirmed - {context['amount']}",
        message=strip_tags(html_message),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[sponsorship.email],
        html_message=html_message,
        fail_silently=True,
    )
    
    # Also notify admin
    send_mail(
        subject=f"New STICONF Sponsor: {sponsorship.company_name}",
        message=f"""
New sponsorship received:
Company: {sponsorship.company_name}
Contact: {sponsorship.contact_name}
Email: {sponsorship.email}
Phone: {sponsorship.phone}
Tier: {context['tier']}
Amount: {context['amount']}
Reference: {context['reference']}
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )
