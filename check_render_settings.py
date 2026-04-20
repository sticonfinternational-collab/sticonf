#!/usr/bin/env python
"""
Diagnostic script to check Django settings for Render deployment
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sticonf.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("DJANGO SETTINGS CHECK")
print("=" * 60)

print(f"\n✓ DEBUG: {settings.DEBUG}")
print(f"✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✓ CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
print(f"✓ SECRET_KEY set: {'Yes' if settings.SECRET_KEY else 'NO - PROBLEM!'}")
print(f"✓ DATABASE: {settings.DATABASES['default']['ENGINE']}")
print(f"✓ STATIC_URL: {settings.STATIC_URL}")
print(f"✓ STATIC_ROOT: {settings.STATIC_ROOT}")

print("\n" + "=" * 60)
print("ENVIRONMENT VARIABLES")
print("=" * 60)

env_vars = [
    'DEBUG',
    'SECRET_KEY',
    'ALLOWED_HOSTS',
    'CSRF_TRUSTED_ORIGINS',
    'DATABASE_URL',
    'PORT',
]

for var in env_vars:
    value = os.getenv(var, "NOT SET")
    if var in ['SECRET_KEY', 'DATABASE_URL']:
        value = "***HIDDEN***" if value != "NOT SET" else value
    print(f"{var}: {value}")

print("\n" + "=" * 60)
print("CHECKS")
print("=" * 60)

checks = {
    "DEBUG is False": settings.DEBUG == False,
    "ALLOWED_HOSTS is set": bool(settings.ALLOWED_HOSTS),
    "sticonf.onrender.com in ALLOWED_HOSTS": "sticonf.onrender.com" in settings.ALLOWED_HOSTS,
    "CSRF_TRUSTED_ORIGINS is set": bool(settings.CSRF_TRUSTED_ORIGINS),
    "https://sticonf.onrender.com in CSRF_TRUSTED_ORIGINS": "https://sticonf.onrender.com" in settings.CSRF_TRUSTED_ORIGINS,
    "SECRET_KEY is set": bool(settings.SECRET_KEY),
    "SECRET_KEY is not default": settings.SECRET_KEY != 'django-insecure-11j2tf5%ajj3(8)on3g1!n*5g6pyi8^=7**^ng^4^a$abcp(ln)',
}

for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check}")

print("\n" + "=" * 60)
