"""
Flutterwave Payment Utilities
Handles webhook verification and payment processing
"""

import hmac
import hashlib
import json
import requests
from django.conf import settings


def verify_webhook_signature(payload_body, signature):
    """
    Verify Flutterwave webhook signature to ensure request is authentic
    
    Args:
        payload_body: Raw request body (as bytes or string)
        signature: Signature from X-Flutterwave-Signature header
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Ensure payload is bytes
        if isinstance(payload_body, str):
            payload_body = payload_body.encode('utf-8')
        
        # Flutterwave uses SHA256 HMAC
        hash_object = hmac.new(
            settings.FLUTTERWAVE_SECRET_KEY.encode('utf-8'),
            payload_body,
            hashlib.sha256
        )
        computed_signature = hash_object.hexdigest()
        
        # Compare signatures (constant-time comparison to prevent timing attacks)
        return hmac.compare_digest(computed_signature, signature)
    
    except Exception as e:
        print(f"Webhook signature verification error: {e}")
        return False


def verify_payment_with_flutterwave(transaction_id):
    """
    Verify a payment directly with Flutterwave API
    
    Args:
        transaction_id: Flutterwave transaction ID
    
    Returns:
        dict: Payment verification response or None if failed
    """
    try:
        headers = {
            'Authorization': f'Bearer {settings.FLUTTERWAVE_SECRET_KEY}'
        }
        
        url = f'https://api.flutterwave.com/v3/transactions/{transaction_id}/verify'
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            verify_response = response.json()
            if verify_response.get('status') == 'success':
                return verify_response.get('data', {})
        
        print(f"Flutterwave verification failed: {response.status_code} - {response.text}")
        return None
    
    except Exception as e:
        print(f"Payment verification error: {e}")
        return None


def get_payment_status_from_webhook(webhook_data):
    """
    Extract and normalize payment status from webhook data
    
    Args:
        webhook_data: Webhook payload data
    
    Returns:
        tuple: (status, tx_ref, transaction_id) or (None, None, None) if invalid
    """
    try:
        payment_data = webhook_data.get('data', {})
        status = payment_data.get('status')
        tx_ref = payment_data.get('tx_ref')
        transaction_id = payment_data.get('id')
        
        # Flutterwave considers "successful" as paid
        if status == 'successful':
            return ('paid', tx_ref, transaction_id)
        elif status == 'failed':
            return ('failed', tx_ref, transaction_id)
        elif status == 'cancelled':
            return ('cancelled', tx_ref, transaction_id)
        else:
            return ('pending', tx_ref, transaction_id)
    
    except Exception as e:
        print(f"Error extracting payment status: {e}")
        return (None, None, None)
