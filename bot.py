#!/usr/bin/env python3
import os
import requests
from datetime import datetime

print("="*60)
print("🌐 THE6ISLAND.BLOG - 24/7 NEWS BOT")
print("="*60)
print(f"Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

# Get environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')

print("Testing connections...")

# Test Supabase
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/bot_logs",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        },
        timeout=10
    )
    print(f"✅ Supabase: Connected ({response.status_code})")
except:
    print("❌ Supabase: Failed")

# Test News API
try:
    url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&size=1"
    response = requests.get(url, timeout=10)
    print(f"✅ News API: Connected ({response.status_code})")
except:
    print("❌ News API: Failed")

print("="*60)
print("✅ Bot ready - will fetch and post news every 4 hours")
print("="*60)

# Log to Supabase
try:
    requests.post(
        f"{SUPABASE_URL}/rest/v1/bot_logs",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "message": "GitHub Actions bot initialized",
            "level": "info",
            "created_at": datetime.now().isoformat() + "Z"
        }
    )
except:
    pass
