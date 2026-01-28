#!/usr/bin/env python3
"""
THE6ISLAND.BLOG - ULTIMATE GitHub Actions Bot
24/7 operation without Termux
"""
import os
import sys
import requests
import json
import time
from datetime import datetime
import re

print("="*70)
print("🌐 THE6ISLAND.BLOG - ULTIMATE 24/7 NEWS BOT")
print("="*70)
print(f"🚀 GitHub Actions Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*70)

# Get environment variables from GitHub Secrets
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')

# Logging function
def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")
    
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
                "level": level.lower(),
                "created_at": datetime.now().isoformat() + "Z"
            },
            timeout=5
        )
    except:
        pass

# Validate environment
log("Checking environment...")
if not all([SUPABASE_URL, SUPABASE_KEY, NEWSDATA_KEY, WP_TOKEN, SITE_ID]):
    log("❌ Missing environment variables!", "ERROR")
    sys.exit(1)

log("✅ Environment OK")

# Clean headline
def clean_headline(headline):
    prefixes = ["World News | ", "Breaking News: ", "Latest: ", "UPDATE: "]
    for prefix in prefixes:
        if headline.startswith(prefix):
            headline = headline[len(prefix):]
    return headline.strip()

# Fetch news
def fetch_news():
    try:
        log("📡 Fetching news...")
        
        # Primary geopolitical news (70%)
        geo_url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&category=politics,world&size=5"
        
        # Secondary other news (30%)
        other_url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&category=technology,business,sports&size=3"
        
        articles = []
        
        # Fetch geopolitical
        response = requests.get(geo_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                geo_articles = data.get('results', [])
                articles.extend(geo_articles[:4])  # Take 4 geopolitical
                log(f"Found {len(geo_articles)} geopolitical articles")
        
        # Fetch other categories
        response = requests.get(other_url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                other_articles = data.get('results', [])
                articles.extend(other_articles[:2])  # Take 2 others
                log(f"Found {len(other_articles)} other articles")
        
        # Remove duplicates
        unique_articles = []
        seen_titles = set()
        
        for article in articles:
            title = article.get('title', '').strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        log(f"✅ Total unique articles: {len(unique_articles)}")
        return unique_articles[:3]  # Process max 3
        
    except Exception as e:
        log(f"❌ Fetch error: {e}", "ERROR")
        return []

# Store in Supabase
def store_in_supabase(article):
    try:
        headline = clean_headline(article.get('title', ''))
        
        article_data = {
            "title": headline[:200],
            "description": article.get('description', '')[:1000] if article.get('description') else "",
            "content": article.get('content', '')[:2000] if article.get('content') else "",
            "category": "GEOPOLITICS",
            "source_url": article.get('link', ''),
            "image_url": article.get('image_url', ''),
            "published_at": article.get('pubDate', datetime.now().isoformat()),
            "created_at": datetime.now().isoformat()
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/news_articles",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            json=article_data,
            timeout=10
        )
        
        if response.status_code in [200, 201, 409]:
            log(f"💾 Stored: {headline[:50]}...")
            return True
        return False
        
    except Exception as e:
        log(f"❌ Store error: {e}", "ERROR")
        return False

# Post to WordPress
def post_to_wordpress(article):
    try:
        headline = clean_headline(article.get('title', ''))
        description = article.get('description', '') or article.get('content', 'No description available.')
        source = article.get('source_id', 'International News').upper()
        
        # Enhanced HTML
        html_content = f"""
        <div style="max-width:800px; margin:0 auto; font-family:Arial,sans-serif; line-height:1.6;">
            <div style="border-left:5px solid #8B0000; padding-left:20px; margin-bottom:25px;">
                <h1 style="color:#8B0000; margin:0 0 10px 0; font-size:1.8rem;">GEOPOLITICS</h1>
                <div style="color:#555;">
                    <strong>📰 {source} • {datetime.now().strftime('%B %d, %Y')}</strong>
                </div>
            </div>
            
            <h2 style="font-size:2.2rem; line-height:1.3; margin:0 0 25px 0; color:#111;">{headline}</h2>
            
            <div style="font-size:1.15rem; color:#222; line-height:1.7; margin-bottom:30px;">
                {description[:800] + '...' if len(description) > 800 else description}
            </div>
            
            <div style="margin-top:40px; padding:20px; background:#f8f9fa; border-radius:8px;">
                <p style="margin:0; color:#495057;">
                    <strong>🌐 THE6ISLAND.BLOG 24/7 NEWS NETWORK</strong><br>
                    Automated news aggregation • GitHub Actions • Updated every 4 hours
                </p>
            </div>
        </div>
        """
        
        response = requests.post(
            f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE_ID}/posts/new",
            headers={
                "Authorization": f"Bearer {WP_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "title": headline[:80],
                "content": html_content,
                "status": "publish",
                "categories": ["GEOPOLITICS", "24-7-NEWS"],
                "tags": ["github-actions", "auto-news", "geopolitics"]
            },
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            log(f"✅ Posted: {headline[:50]}...")
            return True
        else:
            log(f"❌ WordPress error: {response.status_code}", "ERROR")
            return False
            
    except Exception as e:
        log(f"❌ Post error: {e}", "ERROR")
        return False

# Main execution
def main():
    log("🚀 Starting bot cycle")
    
    # Fetch articles
    articles = fetch_news()
    
    if not articles:
        log("❌ No articles to process")
        return
    
    # Process articles
    stored = 0
    posted = 0
    
    for i, article in enumerate(articles):
        log(f"Processing article {i+1}/{len(articles)}...")
        
        # Store in Supabase
        if store_in_supabase(article):
            stored += 1
            
            # Post to WordPress
            if post_to_wordpress(article):
                posted += 1
            
            # Small delay
            if i < len(articles) - 1:
                time.sleep(5)
    
    # Summary
    log(f"✅ Cycle complete: {stored} stored, {posted} posted")
    
    print("\n" + "="*70)
    print(f"📊 SUMMARY: {len(articles)} fetched, {stored} stored, {posted} posted")
    print(f"⏰ Next run: 4 hours via GitHub Actions")
    print("="*70)

if __name__ == "__main__":
    main()
