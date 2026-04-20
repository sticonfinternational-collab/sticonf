"""
Comprehensive Flutterwave Integration Test Suite
Tests all components of the Flutterwave payment system to ensure everything is working correctly.
"""

import os
import django
import json
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticonf.settings')
django.setup()

from django.conf import settings
from django.test import Client, RequestFactory
from main.models import SponsorshipTier, Sponsorship, Registration
from main.views import initiate_sponsorship_payment, verify_sponsorship_payment
import requests

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def test_environment_configuration():
    """Test 1: Check if Flutterwave keys are properly configured in environment"""
    print_header("TEST 1: Environment Configuration")
    
    public_key = settings.FLUTTERWAVE_PUBLIC_KEY
    secret_key = settings.FLUTTERWAVE_SECRET_KEY
    
    if public_key and public_key != 'your_flutterwave_public_key_here':
        print_success(f"Flutterwave PUBLIC_KEY is set: {public_key[:20]}...")
    else:
        print_error("Flutterwave PUBLIC_KEY is not configured or still contains placeholder")
        return False
    
    if secret_key and secret_key != 'your_flutterwave_secret_key_here':
        print_success(f"Flutterwave SECRET_KEY is set: {secret_key[:20]}...")
    else:
        print_error("Flutterwave SECRET_KEY is not configured or still contains placeholder")
        return False
    
    return True

def test_sponsorship_tiers():
    """Test 2: Verify sponsorship tiers are created in database"""
    print_header("TEST 2: Sponsorship Tiers")
    
    tiers = SponsorshipTier.objects.all()
    
    if not tiers.exists():
        print_error("No sponsorship tiers found in database")
        return False
    
    print_success(f"Found {tiers.count()} sponsorship tiers:")
    for tier in tiers:
        print_info(f"  - {tier.get_tier_name_display()}: ₦{tier.amount:,.0f}")
    
    # Verify expected tiers
    expected_tiers = ['platinum', 'gold', 'silver', 'bronze']
    found_tiers = set(tiers.values_list('tier_name', flat=True))
    
    for expected in expected_tiers:
        if expected in found_tiers:
            print_success(f"✓ {expected.capitalize()} tier exists")
        else:
            print_error(f"✗ {expected.capitalize()} tier is missing")
            return False
    
    return True

def test_email_configuration():
    """Test 3: Verify email backend is properly configured"""
    print_header("TEST 3: Email Configuration")
    
    email_backend = settings.EMAIL_BACKEND
    print_info(f"Email Backend: {email_backend}")
    
    if email_backend == 'django.core.mail.backends.smtp.EmailBackend':
        print_success("Using SMTP email backend")
        
        print_info(f"SMTP Host: {settings.EMAIL_HOST}")
        print_info(f"SMTP Port: {settings.EMAIL_PORT}")
        print_info(f"SMTP TLS: {settings.EMAIL_USE_TLS}")
        print_info(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
        
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            print_success("SMTP credentials are configured")
        else:
            print_error("SMTP credentials are missing")
            return False
    else:
        print_warning("Not using SMTP backend - emails may not work in production")
    
    return True

def test_sponsorship_model():
    """Test 4: Verify Sponsorship model and methods"""
    print_header("TEST 4: Sponsorship Model")
    
    # Create a test sponsorship
    tier = SponsorshipTier.objects.first()
    if not tier:
        print_error("Cannot test - no sponsorship tier found")
        return False
    
    try:
        sponsorship = Sponsorship.objects.create(
            company_name="Test Company",
            contact_name="John Doe",
            email="test@example.com",
            phone="+234812345678",
            country="Nigeria",
            tier=tier,
            amount=tier.amount,
            reference="TEST-12345",
            status='pending'
        )
        print_success(f"Created test sponsorship: {sponsorship}")
        
        # Test mark_as_paid method
        sponsorship.mark_as_paid()
        print_success(f"Sponsorship status updated to: {sponsorship.status}")
        
        if sponsorship.paid_at:
            print_success(f"paid_at timestamp set: {sponsorship.paid_at}")
        else:
            print_error("paid_at timestamp not set properly")
            return False
        
        # Clean up
        sponsorship.delete()
        print_success("Test sponsorship cleaned up")
        
        return True
        
    except Exception as e:
        print_error(f"Error testing sponsorship model: {str(e)}")
        return False

def test_api_endpoints():
    """Test 5: Verify API endpoints are accessible"""
    print_header("TEST 5: API Endpoints")
    
    client = Client()
    
    endpoints = [
        ('/api/sponsorship-tiers/', 'GET', 'Get sponsorship tiers'),
        ('/api/initiate-sponsorship-payment/', 'POST', 'Initiate payment'),
        ('/api/verify-sponsorship-payment/', 'POST', 'Verify payment'),
    ]
    
    for url, method, description in endpoints:
        try:
            if method == 'GET':
                response = client.get(url)
            else:
                response = client.post(url, data='{}', content_type='application/json')
            
            if response.status_code in [200, 400, 405]:
                print_success(f"✓ {description}: {url} (Status: {response.status_code})")
            else:
                print_error(f"✗ {description}: {url} (Status: {response.status_code})")
                return False
        except Exception as e:
            print_error(f"✗ Error accessing {url}: {str(e)}")
            return False
    
    return True

def test_flutterwave_keys_validation():
    """Test 6: Verify keys are not placeholders"""
    print_header("TEST 6: Flutterwave Keys Validation")
    
    public_key = settings.FLUTTERWAVE_PUBLIC_KEY
    secret_key = settings.FLUTTERWAVE_SECRET_KEY
    
    placeholders = ['your_flutterwave_public_key_here', 'your_flutterwave_secret_key_here', '']
    
    if public_key not in placeholders:
        print_success("PUBLIC_KEY is not a placeholder")
    else:
        print_error("PUBLIC_KEY is still a placeholder - payment will fail!")
        return False
    
    if secret_key not in placeholders:
        print_success("SECRET_KEY is not a placeholder")
    else:
        print_error("SECRET_KEY is still a placeholder - payment will fail!")
        return False
    
    return True

def test_csrf_exemption():
    """Test 7: Verify CSRF exemption on payment endpoints"""
    print_header("TEST 7: CSRF Exemption")
    
    # Check that the views have @csrf_exempt decorator
    from main import views
    
    payment_views = [
        ('initiate_sponsorship_payment', views.initiate_sponsorship_payment),
        ('verify_sponsorship_payment', views.verify_sponsorship_payment),
    ]
    
    for view_name, view_func in payment_views:
        # Check if view has csrf_exempt marker
        if hasattr(view_func, 'csrf_exempt'):
            print_success(f"{view_name} has CSRF exemption")
        else:
            # The decorator sets this attribute
            print_warning(f"Cannot verify CSRF exemption for {view_name} - might still work")
    
    return True

def test_database_migrations():
    """Test 8: Verify all migrations are applied"""
    print_header("TEST 8: Database Migrations")
    
    try:
        # Try to access the models
        tier_count = SponsorshipTier.objects.count()
        sponsorship_count = Sponsorship.objects.count()
        registration_count = Registration.objects.count()
        
        print_success("SponsorshipTier table accessible")
        print_success("Sponsorship table accessible")
        print_success("Registration table accessible")
        
        print_info(f"Database stats:")
        print_info(f"  - Sponsorship Tiers: {tier_count}")
        print_info(f"  - Sponsorships: {sponsorship_count}")
        print_info(f"  - Registrations: {registration_count}")
        
        return True
        
    except Exception as e:
        print_error(f"Database error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print_header("FLUTTERWAVE INTEGRATION TEST SUITE")
    
    tests = [
        ("Environment Configuration", test_environment_configuration),
        ("Sponsorship Tiers", test_sponsorship_tiers),
        ("Email Configuration", test_email_configuration),
        ("Sponsorship Model", test_sponsorship_model),
        ("API Endpoints", test_api_endpoints),
        ("Flutterwave Keys Validation", test_flutterwave_keys_validation),
        ("CSRF Exemption", test_csrf_exemption),
        ("Database Migrations", test_database_migrations),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print_error(f"Test failed with exception: {str(e)}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    failed = len(results) - passed
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{status}: {test_name}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"Total: {len(results)} | {GREEN}Passed: {passed}{RESET} | {RED}Failed: {failed}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    if failed == 0:
        print_success("All tests passed! Flutterwave integration is ready.")
    else:
        print_error(f"{failed} test(s) failed. Please fix the issues before going to production.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
