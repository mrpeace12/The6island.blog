#!/usr/bin/env python3
import os, requests
from datetime import datetime

# Get from GitHub Secrets
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')

print("GitHub Bot Test")

if all([SUPABASE_URL, SUPABASE_KEY]):
    requests.post(
        f"{SUPABASE_URL}/rest/v1/bot_logs",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "message": "[GitHub] Bot verification run",
            "level": "info",
            "created_at": datetime.now().isoformat() + "Z"
        }
    )
    print("✅ Logged to Supabase")
