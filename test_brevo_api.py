#!/usr/bin/env python3
"""
Brevo API Test Script - Test your API key and List ID
Run: python test_brevo_api.py
"""

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import os
from dotenv import load_dotenv
import sys
import uuid

# Load environment variables
load_dotenv()

def test_brevo_api():
    print("🔍 Testing Brevo API Configuration...")
    
    # Check config
    api_key = os.getenv('BREVO_API_KEY')
    list_id = os.getenv('BREVO_LIST_ID')
    
    print(f"API Key: {'✅ Present' if api_key else '❌ Missing'}")
    print(f"List ID: {'✅ Present' if list_id else '❌ Missing'}")
    
    if api_key and api_key.startswith('xsmtpsib-'):
        print("❌ ERROR: Using SMTP key! Need REST API key (starts with 'xkeysib-')")
        return False
    
    if not api_key or not list_id:
        print("❌ Missing BREVO_API_KEY or BREVO_LIST_ID in .env")
        return False
    
    try:
        list_id = int(list_id)
    except ValueError:
        print("❌ BREVO_LIST_ID must be a number")
        return False
    
    print("\n🌐 Testing API connectivity...")
    
    # Configure API
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key
    api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Test 1: Create test contact (proves API key works)
    print("1. Testing API key with contact creation...")
    try:
        test_contact = sib_api_v3_sdk.CreateContact(
            email="test-" + str(uuid.uuid4())[:8] + "@example.com",
            attributes={"FIRSTNAME": "Test", "LASTNAME": "User"},
            list_ids=[list_id],
            update_enabled=True
        )
        result = api_instance.create_contact(test_contact)
        print(f"✅ API key works! Created test contact: {result.email}")
        
        # Clean up test contact
        api_instance.delete_contact(result.email)
        print("🧹 Cleaned up test contact")
    except ApiException as e:
        print(f"❌ API Error {e.status}: {getattr(e, 'body', str(e))}")
        return False
    
    # Test 2: Get lists
    print("\n2. Testing list access...")
    try:
        lists = api_instance.get_lists()
        print(f"✅ Found {len(lists.lists)} lists")
        list_exists = any(lst.list_id == list_id for lst in lists.lists)
        if list_exists:
            print(f"✅ List ID {list_id} exists")
        else:
            print(f"❌ List ID {list_id} does NOT exist!")
            print("Available lists:", [lst.list_id for lst in lists.lists])
        return list_exists
    except ApiException as e:
        print(f"❌ Lists error: {e}")
        return False

if __name__ == '__main__':
    success = test_brevo_api()
    if success:
        print("\n🎉 Brevo API is working correctly!")
        print("\n✅ You can now test registration form.")
    else:
        print("\n❌ Fix issues above before testing registration.")
        print("\n💡 Get new REST API key: app.brevo.com → SMTP & API → API Keys → Generate new")

