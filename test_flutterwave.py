#!/usr/bin/env python3
'''
Flutterwave API Test Script
Tests your payment gateway configuration
Run: python test_flutterwave.py
'''

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def test_flutterwave():
    print('🔍 Testing Flutterwave API...')
    
    public_key = os.getenv('FLUTTERWAVE_PUBLIC_KEY')
    secret_key = os.getenv('FLUTTERWAVE_SECRET_KEY')
    
    print(f'Public Key: {"✅ Present" if public_key else "❌ Missing"}')
    print(f'Secret Key: {"✅ Present" if secret_key else "❌ Missing"}')
    
    if not secret_key:
        print('❌ Add FLUTTERWAVE_SECRET_KEY to .env')
        return False
    
    if not secret_key.startswith('FLWSECK'):
        print('❌ Invalid secret key format. Must start with FLWSECK_TEST- or FLWSECK_LIVE-')
        return False
    
    print('\\n🌐 Testing payment initiation...')
    
    # Test payment payload (₦100) - Added redirect_url
    payload = {
        'tx_ref': f'TEST-{os.urandom(4).hex().upper()}',
        'amount': '100',
        'currency': 'NGN',
        'redirect_url': 'https://sticonf.onrender.com/sponsorship/',
        'payment_options': 'card',
        'customer': {
            'email': 'test@example.com',
            'name': 'Test User'
        },
        'customizations': {
            'title': 'STICONF Test',
            'description': 'Test Payment'
        }
    }
    
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'https://api.flutterwave.com/v3/payments',
            json=payload,
            headers=headers,
            timeout=10
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get('status') == 'success':
            print(f'✅ Flutterwave works! Payment link: {result["data"]["link"]}')
            print(f'Reference: {result["data"]["tx_ref"]}')
            return True
        else:
            print(f'❌ API Error {response.status_code}: {result}')
            print('Likely: Invalid/expired secret key')
            return False
            
    except Exception as e:
        print(f'❌ Request failed: {e}')
        return False

if __name__ == '__main__':
    if test_flutterwave():
        print('\\n🎉 Flutterwave ready! Update Render dashboard.')
        print('Go to: https://dashboard.render.com → sticonf → Environment')
    else:
        print('\\n❌ Fix local keys first.')
        print('Flutterwave Dashboard: https://dashboard.flutterwave.com')

