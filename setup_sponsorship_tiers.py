#!/usr/bin/env python
"""
Script to verify and initialize sponsorship tiers in database
Run with: python manage.py shell < setup_sponsorship_tiers.py
Or: python setup_sponsorship_tiers.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticonf.settings')
django.setup()

from main.models import SponsorshipTier

# Define sponsorship tiers
TIERS = [
    {
        'tier_name': 'platinum',
        'amount': 10000000,
        'description': 'Platinum Sponsorship Package - Premium brand visibility, speaking slot, and exclusive partnership opportunities'
    },
    {
        'tier_name': 'gold',
        'amount': 5000000,
        'description': 'Gold Sponsorship Package - Enhanced brand visibility, exhibition booth, and networking events'
    },
    {
        'tier_name': 'silver',
        'amount': 2000000,
        'description': 'Silver Sponsorship Package - Logo placement, conference materials, and attendee list'
    },
    {
        'tier_name': 'bronze',
        'amount': 1000000,
        'description': 'Bronze Sponsorship Package - Basic brand visibility and website listing'
    }
]

def setup_tiers():
    """Initialize sponsorship tiers"""
    print("=" * 60)
    print("SPONSORSHIP TIERS SETUP")
    print("=" * 60)
    
    # Check existing tiers
    existing_count = SponsorshipTier.objects.count()
    print(f"\n✓ Current tiers in database: {existing_count}")
    
    if existing_count > 0:
        print("\nExisting tiers:")
        for tier in SponsorshipTier.objects.all():
            print(f"  - {tier.tier_name}: ₦{tier.amount:,.0f}")
    
    # Create tiers if they don't exist
    created_count = 0
    for tier_data in TIERS:
        tier, created = SponsorshipTier.objects.get_or_create(
            tier_name=tier_data['tier_name'],
            defaults={
                'amount': tier_data['amount'],
                'description': tier_data['description']
            }
        )
        
        if created:
            print(f"  ✓ Created: {tier.tier_name} - ₦{tier.amount:,.0f}")
            created_count += 1
        else:
            print(f"  ✓ Already exists: {tier.tier_name} - ₦{tier.amount:,.0f}")
    
    print(f"\n{'=' * 60}")
    print(f"Created: {created_count} new tier(s)")
    print(f"Total tiers: {SponsorshipTier.objects.count()}")
    print("=" * 60)

if __name__ == '__main__':
    setup_tiers()
