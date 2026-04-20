#!/usr/bin/env python
"""
Test contact form functionality
"""
import os
import django
from django.test import RequestFactory
from django.contrib import messages

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticonf.settings')
django.setup()

from main.views import handle_contact
from main.models import Contact

def test_contact_form():
    """Test the contact form functionality"""
    print("🧪 Testing Contact Form Functionality...")

    # Create a mock request
    factory = RequestFactory()
    request = factory.post('/contact/handle-contact/', {
        'first_name': 'John Doe',
        'email': 'john@example.com',
        'category': 'General Inquiry',
        'organisation': 'Test Company',
        'phone': '+1234567890',
        'interest': 'I would like to know more about STICONF 2026'
    })

    # Add session and messages middleware
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.messages.middleware import MessageMiddleware

    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware(lambda x: None)
    middleware.process_request(request)

    try:
        # Call the view
        response = handle_contact(request)

        # Check if contact was saved to database
        contact = Contact.objects.filter(email='john@example.com').last()
        if contact:
            print("✅ Contact saved to database:")
            print(f"   Name: {contact.first_name} {contact.last_name}")
            print(f"   Email: {contact.email}")
            print(f"   Category: {contact.category}")
            print(f"   Organization: {contact.organisation}")
            print(f"   Phone: {contact.phone}")
            print(f"   Message: {contact.interest}")
            print(f"   Read: {contact.read}")
            print(f"   Responded: {contact.responded}")
        else:
            print("❌ Contact was not saved to database")

        # Check messages
        storage = messages.get_messages(request)
        message_list = list(storage)
        if message_list:
            print("✅ Success message shown to user:")
            for msg in message_list:
                print(f"   {msg}")
        else:
            print("❌ No success message found")

        print("✅ Contact form test completed successfully!")

    except Exception as e:
        print(f"❌ Error testing contact form: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_contact_form()