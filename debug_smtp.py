#!/usr/bin/env python
"""
Test script to debug Brevo SMTP configuration
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticonf.settings')
django.setup()

def test_smtp_connection():
    """Test SMTP connection manually"""
    print("🔍 Testing Brevo SMTP Connection...")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"User: {settings.EMAIL_HOST_USER}")
    print(f"TLS: {settings.EMAIL_USE_TLS}")
    print(f"From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"To: {settings.ADMIN_EMAIL}")
    print()

    try:
        # Create SMTP connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.set_debuglevel(1)  # Enable debug output

        # Start TLS
        if settings.EMAIL_USE_TLS:
            server.starttls()

        # Login
        print("🔐 Attempting login...")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("✅ Login successful!")

        # Create test message
        msg = MIMEMultipart()
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = settings.ADMIN_EMAIL
        msg['Subject'] = 'STICONF 2026 - SMTP Test'

        body = "This is a test email to verify SMTP configuration."
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        print("📤 Sending test email...")
        server.sendmail(settings.DEFAULT_FROM_EMAIL, settings.ADMIN_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")

        # Close connection
        server.quit()
        print("✅ SMTP test completed successfully!")

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ AUTHENTICATION ERROR: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if your Brevo SMTP key is correct")
        print("2. Verify your Brevo account has SMTP enabled")
        print("3. Make sure your Brevo account is not suspended")
        print("4. Check if you've exceeded sending limits")

    except smtplib.SMTPConnectError as e:
        print(f"❌ CONNECTION ERROR: {e}")
        print("Check your internet connection and Brevo SMTP server status")

    except Exception as e:
        print(f"❌ GENERAL ERROR: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    test_smtp_connection()