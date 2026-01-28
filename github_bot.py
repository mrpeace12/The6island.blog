#!/usr/bin/env python3
"""
THE6ISLAND.BLOG - 24/7 GitHub Actions Bot
"""
import os
import requests
from datetime import datetime
import sys

print("="*60)
print("🌐 THE6ISLAND.BLOG - GITHUB ACTIONS BOT")
print("="*60)
print(f"Run started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*60)

# Get environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')

def log(message):
    """Simple logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    
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
if not all([SUPABASE_URL, SUPABASE_KEY, NEWSDATA_KEY, WP_TOKEN, SITE_ID]):
    log("❌ Missing environment variables!")
    sys.exit(1)

log("✅ All environment variables present")

# Fetch news
try:
    log("📡 Fetching news...")
    url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&category=politics,world&size=2"
    response = requests.get(url, timeout=30)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get('results', [])
        log(f"Found {len(articles)} articles")
        
        # Process articles
        for article in articles:
            title = article.get('title', '').strip()
            if not title:
                continue
                
            # Clean title
            for prefix in ["World News | ", "Breaking News: ", "Latest: "]:
                if title.startswith(prefix):
                    title = title[len(prefix):]
            
            description = article.get('description', '') or article.get('content', 'No description available.')
            source = article.get('source_id', 'International News').upper()
            
            # Create HTML
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
                        Automated news aggregation • Updated every 4 hours • GitHub Actions
                    </p>
                </div>
            </div>
            """
            
            # Post to WordPress
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
                    "tags": ["auto-news", "24-7", "the6island"]
                },
                timeout=30
            )
            
            if wp_response.status_code in [200, 201]:
                log(f"✅ Posted: {title[:50]}...")
            else:
                log(f"❌ WordPress error: {wp_response.status_code}")
                
    else:
        log(f"❌ News API error: {response.status_code}")
        
except Exception as e:
    log(f"❌ Error: {str(e)}")

log("✅ Bot run completed")
print("="*60)
print(f"⏰ Next run scheduled in 4 hours")
print("="*60)
