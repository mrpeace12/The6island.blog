#!/usr/bin/env python3
print("="*60)
print("🌐 THE6ISLAND.BLOG - REAL GITHUB BOT")
print("="*60)

import os
import sys
import requests
import json
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

# Check environment
log("Checking environment...")
secrets = {
    'SUPABASE_URL': os.getenv('SUPABASE_URL'),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
    'NEWSDATA_KEY': os.getenv('NEWSDATA_KEY'),
    'WP_TOKEN': os.getenv('WP_TOKEN'),
    'SITE_ID': os.getenv('SITE_ID'),
    'GROQ_KEY': os.getenv('GROQ_KEY')
}

for name, value in secrets.items():
    if value:
        log(f"✅ {name}: Set")
    else:
        log(f"❌ {name}: Missing")

# Test Supabase
try:
    log("Testing Supabase...")
    response = requests.get(
        f"{secrets['SUPABASE_URL']}/rest/v1/bot_logs",
        headers={"apikey": secrets['SUPABASE_KEY'], "Authorization": f"Bearer {secrets['SUPABASE_KEY']}"},
        params={"select": "count"},
        timeout=10
    )
    log(f"✅ Supabase: {response.json()[0]['count']} logs")
except Exception as e:
    log(f"⚠️ Supabase error: {e}")

# Fetch news
try:
    log("Fetching news...")
    news_url = f"https://newsdata.io/api/1/latest?apikey={secrets['NEWSDATA_KEY']}&language=en&category=politics&size=1"
    news_response = requests.get(news_url, timeout=30)
    
    if news_response.status_code == 200:
        articles = news_response.json().get('results', [])
        log(f"✅ Found {len(articles)} news articles")
        
        # Post to WordPress
        for article in articles:
            title = article.get('title', 'News Update')
            content = article.get('description', 'Latest news update.')
            
            wp_data = {
                "title": title[:80],
                "content": f"<h1>{title}</h1><p>{content}</p><p>📰 Automated via GitHub Actions</p>",
                "status": "publish",
                "categories": ["GITHUB-ACTIONS"]
            }
            
            wp_response = requests.post(
                f"https://public-api.wordpress.com/rest/v1.1/sites/{secrets['SITE_ID']}/posts/new",
                headers={"Authorization": f"Bearer {secrets['WP_TOKEN']}", "Content-Type": "application/json"},
                json=wp_data,
                timeout=30
            )
            
            if wp_response.status_code in [200, 201]:
                log(f"✅ Posted: {title[:50]}...")
            else:
                log(f"❌ WordPress error: {wp_response.status_code}")
                
    else:
        log(f"❌ News API error: {news_response.status_code}")
        
except Exception as e:
    log(f"⚠️ News error: {e}")

# Log success to Supabase
try:
    log("Logging to Supabase...")
    requests.post(
        f"{secrets['SUPABASE_URL']}/rest/v1/bot_logs",
        headers={
            "apikey": secrets['SUPABASE_KEY'],
            "Authorization": f"Bearer {secrets['SUPABASE_KEY']}",
            "Content-Type": "application/json"
        },
        json={
            "message": "[GitHub] Bot ran successfully with news fetch",
            "level": "info",
            "created_at": datetime.now().isoformat() + "Z"
        }
    )
    log("✅ Logged to Supabase")
except Exception as e:
    log(f"⚠️ Logging error: {e}")

print("="*60)
print("✅ GITHUB ACTIONS BOT COMPLETE!")
print("="*60)
