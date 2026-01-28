#!/usr/bin/env python3
"""
CLEAN BOT - Uses GitHub Secrets only
No hardcoded keys!
"""
import os
import sys
import requests
from datetime import datetime

# All keys come from GitHub Secrets
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')

print("="*60)
print("🌐 THE6ISLAND.BLOG - SECURE GITHUB BOT")
print("="*60)
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

# Validate environment
if not all([SUPABASE_URL, SUPABASE_KEY, NEWSDATA_KEY, WP_TOKEN, SITE_ID]):
    print("❌ ERROR: Missing environment variables!")
    print("Please add these GitHub Secrets:")
    print("1. SUPABASE_URL")
    print("2. SUPABASE_KEY")
    print("3. NEWSDATA_KEY")
    print("4. WP_TOKEN")
    print("5. SITE_ID")
    sys.exit(1)

print("✅ All environment variables loaded")
print("✅ No hardcoded keys - Secure!")

# Test Supabase connection
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/bot_logs",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        },
        params={"select": "count"},
        timeout=10
    )
    print(f"✅ Supabase connected: {response.json()}")
except Exception as e:
    print(f"⚠️ Supabase test failed: {e}")

print("="*60)
print("✅ Bot is ready for GitHub Actions!")
print("="*60)
