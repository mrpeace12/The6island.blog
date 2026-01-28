#!/usr/bin/env python3
import os
import sys
import requests

print("="*60)
print("🌐 TEST BOT - GitHub Actions")
print("="*60)

# Debug: Show what's available
print("Environment check:")
for key in ['SUPABASE_URL', 'SUPABASE_KEY', 'NEWSDATA_KEY', 'WP_TOKEN', 'SITE_ID', 'GROQ_KEY']:
    value = os.getenv(key)
    if value:
        print(f"✅ {key}: Set (length: {len(value)})")
    else:
        print(f"❌ {key}: Missing")

# Test Supabase connection
print("\n📡 Testing Supabase connection...")
try:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        response = requests.get(
            f"{supabase_url}/rest/v1/bot_logs",
            headers={"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}"},
            params={"select": "count"},
            timeout=10
        )
        print(f"✅ Supabase connected: Status {response.status_code}")
    else:
        print("❌ Missing Supabase credentials")
except Exception as e:
    print(f"⚠️ Supabase test failed: {e}")

print("\n" + "="*60)
print("✅ GitHub Actions Bot Test Complete!")
print("="*60)
