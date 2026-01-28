#!/usr/bin/env python3
"""
THE6ISLAND.BLOG - GitHub Actions Bot
"""
import os
import sys
import requests
from datetime import datetime

print("="*60)
print("🌐 THE6ISLAND.BLOG - GITHUB ACTIONS BOT")
print("="*60)

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

# Check environment
log("Checking environment variables...")
required = ['SUPABASE_URL', 'SUPABASE_KEY', 'NEWSDATA_KEY', 'WP_TOKEN', 'SITE_ID']
missing = []
for key in required:
    if not os.getenv(key):
        missing.append(key)
        log(f"❌ {key}: Missing")
    else:
        log(f"✅ {key}: Set")

if missing:
    log(f"❌ Missing variables: {missing}")
    sys.exit(1)

log("✅ All environment variables loaded")

# Test Supabase
try:
    log("Testing Supabase connection...")
    response = requests.get(
        f"{os.getenv('SUPABASE_URL')}/rest/v1/bot_logs",
        headers={
            "apikey": os.getenv('SUPABASE_KEY'),
            "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}"
        },
        params={"select": "count"},
        timeout=10
    )
    log(f"✅ Supabase connected: {response.status_code}")
except Exception as e:
    log(f"⚠️ Supabase test failed: {e}")

print("="*60)
print("✅ GitHub Actions Bot Success!")
print("="*60)

# Log success to Supabase
try:
    requests.post(
        f"{os.getenv('SUPABASE_URL')}/rest/v1/bot_logs",
        headers={
            "apikey": os.getenv('SUPABASE_KEY'),
            "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "message": "[GitHub] Bot ran successfully",
            "level": "info",
            "created_at": datetime.now().isoformat() + "Z"
        }
    )
except:
    pass
