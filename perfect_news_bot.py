#!/usr/bin/env python3
"""
PERFECT NEWS BOT - CLEAN VERSION
For GitHub Actions (uses environment variables)
"""
import os
import sys
import requests
import time
from datetime import datetime
import re
import random
import hashlib
from bs4 import BeautifulSoup

print("="*70)
print("🌐 THE6ISLAND.BLOG - PERFECT NEWS BOT (GitHub Actions)")
print("="*70)

# Get environment variables from GitHub Secrets
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
GROQ_KEY = os.getenv('GROQ_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def log(message):
    """Log to console and Supabase"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
    # Log to Supabase if available
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            requests.post(
                f"{SUPABASE_URL}/rest/v1/bot_logs",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "message": f"[GitHub] {message}",
                    "level": "info",
                    "created_at": datetime.now().isoformat() + "Z"
                },
                timeout=5
            )
        except:
            pass

# Check environment
log("Checking environment variables...")
if not all([NEWSDATA_KEY, WP_TOKEN, SITE_ID]):
    log("❌ Missing required environment variables!")
    sys.exit(1)

log("✅ Environment OK")

# Your bot logic here (simplified version)
def fetch_and_process():
    try:
        log("📡 Fetching news...")
        url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&category=politics,world&size=2"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('results', [])
            log(f"Found {len(articles)} articles")
            
            for article in articles:
                title = article.get('title', '').strip()
                if not title:
                    continue
                
                # Clean title
                for prefix in ["World News | ", "Breaking News: ", "Latest: "]:
                    if title.startswith(prefix):
                        title = title[len(prefix):]
                
                description = article.get('description', '') or article.get('content', '')
                source = article.get('source_id', 'International News').upper()
                
                # Post to WordPress
                html_content = f"""
                <div style="max-width:800px; margin:0 auto; font-family:Arial,sans-serif; line-height:1.6;">
                    <h1 style="color:#333; border-bottom:2px solid #8B0000; padding-bottom:10px;">
                        {title}
                    </h1>
                    
                    <div style="color:#555; margin-bottom:20px;">
                        <strong>📰 {source} • {datetime.now().strftime('%B %d, %Y')}</strong>
                    </div>
                    
                    <div style="font-size:1.1rem; color:#222; line-height:1.7;">
                        {description[:500] + '...' if len(description) > 500 else description}
                    </div>
                    
                    <div style="margin-top:30px; padding:15px; background:#f8f9fa; border-radius:5px;">
                        <p style="margin:0; color:#666;">
                            <strong>🌐 THE6ISLAND.BLOG 24/7 NEWS NETWORK</strong><br>
                            Automated news aggregation • GitHub Actions
                        </p>
                    </div>
                </div>
                """
                
                wp_response = requests.post(
                    f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE_ID}/posts/new",
                    headers={
                        "Authorization": f"Bearer {WP_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "title": title[:80],
                        "content": html_content,
                        "status": "publish",
                        "categories": ["GEOPOLITICS", "GITHUB-BOT"],
                        "tags": ["auto-news", "24-7"]
                    },
                    timeout=30
                )
                
                if wp_response.status_code in [200, 201]:
                    log(f"✅ Posted: {title[:50]}...")
                else:
                    log(f"❌ WordPress error: {wp_response.status_code}")
        
        log("✅ Bot run completed")
        
    except Exception as e:
        log(f"❌ Error: {e}")

if __name__ == "__main__":
    fetch_and_process()
