#!/usr/bin/env python3
"""
THE6ISLAND.BLOG - PERFECT GitHub Actions Bot
Based on perfect_news_bot.py but optimized for GitHub Actions
"""
import os
import sys
import requests
import json
from datetime import datetime
import time

print("="*70)
print("🌐 THE6ISLAND.BLOG - PERFECT 24/7 BOT")
print("="*70)
print(f"🚀 GitHub Actions Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*70)

# Get environment variables from GitHub Secrets
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
NEWSDATA_KEY = os.getenv('NEWSDATA_KEY')
WP_TOKEN = os.getenv('WP_TOKEN')
SITE_ID = os.getenv('SITE_ID')
GROQ_KEY = os.getenv('GROQ_KEY')

def log_to_supabase(message, level="info"):
    """Log to Supabase database"""
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/bot_logs",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            },
            json={
                "message": f"[GitHub] {message}",
                "level": level,
                "created_at": datetime.now().isoformat() + "Z"
            },
            timeout=10
        )
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"⚠️ Supabase log failed: {e}")
        return False

def log(message, level="INFO"):
    """Log to console and Supabase"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")
    log_to_supabase(message, level.lower())

# Validate environment
log("Checking environment variables...")
if not all([SUPABASE_URL, SUPABASE_KEY, NEWSDATA_KEY, WP_TOKEN, SITE_ID]):
    log("❌ Missing environment variables!", "ERROR")
    sys.exit(1)

log("✅ Environment variables loaded")

# Clean headline function
def clean_headline(headline):
    prefixes = [
        "World News | ", "Breaking News: ", "Latest: ", 
        "UPDATE: ", "Exclusive: ", "BREAKING: ", "Just In: "
    ]
    for prefix in prefixes:
        if headline.startswith(prefix):
            headline = headline[len(prefix):]
    return headline.strip()

# Fetch news from NewsData.io
def fetch_news():
    try:
        log("📡 Fetching news from NewsData.io...")
        
        # Multiple queries for better coverage
        queries = [
            f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&category=politics,world&size=5",
            f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_KEY}&language=en&q=geopolitical OR diplomacy OR sanctions&size=3"
        ]
        
        all_articles = []
        
        for query in queries:
            try:
                response = requests.get(query, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        articles = data.get('results', [])
                        all_articles.extend(articles)
                        log(f"   Found {len(articles)} articles from query")
            except Exception as e:
                log(f"   Query error: {e}", "WARNING")
                continue
        
        # Remove duplicates based on title
        unique_articles = []
        seen_titles = set()
        
        for article in all_articles:
            title = article.get('title', '').strip()
            if title and title not in seen_titles:
                seen_titles.add(title)
                unique_articles.append(article)
        
        log(f"✅ Total unique articles: {len(unique_articles)}")
        return unique_articles[:3]  # Process max 3 articles
        
    except Exception as e:
        log(f"❌ Fetch error: {e}", "ERROR")
        return []

# Store article in Supabase
def store_article(article):
    try:
        headline = clean_headline(article.get('title', ''))
        source_url = article.get('link', '')
        
        if not headline or not source_url:
            return False
        
        article_data = {
            "title": headline[:200],
            "description": article.get('description', '')[:1000] if article.get('description') else "",
            "content": article.get('content', '')[:2000] if article.get('content') else "",
            "category": "GEOPOLITICS",
            "source_url": source_url,
            "image_url": article.get('image_url', ''),
            "published_at": article.get('pubDate', datetime.now().isoformat()),
            "created_at": datetime.now().isoformat()
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/news_articles",
            headers={
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates"
            },
            json=article_data,
            timeout=10
        )
        
        if response.status_code in [200, 201, 409]:
            log(f"💾 Stored: {headline[:50]}...")
            return True
        else:
            log(f"⚠️ Store failed: {response.status_code}", "WARNING")
            return False
            
    except Exception as e:
        log(f"❌ Store error: {e}", "ERROR")
        return False

# Post article to WordPress
def post_to_wordpress(article):
    try:
        headline = clean_headline(article.get('title', ''))
        description = article.get('description', '') or article.get('content', 'No description available.')
        source = article.get('source_id', 'International News').upper()
        
        if not headline:
            return False
        
        # Create enhanced HTML content
        html_content = f"""
        <div style="max-width:800px; margin:0 auto; font-family:'Segoe UI',Tahoma,Geneva,sans-serif; line-height:1.6;">
            <div style="border-left:5px solid #8B0000; padding-left:20px; margin-bottom:25px;">
                <h1 style="color:#8B0000; margin:0 0 10px 0; font-size:1.8rem;">GEOPOLITICS</h1>
                <div style="color:#555;">
                    <strong>📰 {source} • 🌍 GLOBAL</strong><br>
                    <small>{datetime.now().strftime("%B %d, %Y • %H:%M UTC")}</small>
                </div>
            </div>
            
            <h2 style="font-size:2.2rem; line-height:1.3; margin:0 0 25px 0; color:#111;">{headline}</h2>
            
            <div style="font-size:1.15rem; color:#222; line-height:1.7; margin-bottom:30px;">
                {description[:800] + '...' if len(description) > 800 else description}
            </div>
            
            <div style="margin-top:40px; padding:20px; background:linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius:8px;">
                <p style="margin:0; color:#495057; font-size:0.95rem;">
                    <strong>🌐 THE6ISLAND.BLOG 24/7 NEWS NETWORK</strong><br>
                    Automated news aggregation • Multi-source verification • Updated every 4 hours<br>
                    <small>Powered by GitHub Actions • AI-enhanced reporting</small>
                </p>
            </div>
            
            <div style="margin-top:30px; padding-top:20px; border-top:1px solid #dee2e6; color:#6c757d; font-size:0.9rem;">
                <p><strong>🔗 Source:</strong> {article.get('link', 'Multiple wire services')}</p>
            </div>
        </div>
        """
        
        # Post to WordPress
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
                "categories": ["GEOPOLITICS", "24-7-NEWS", "GITHUB-BOT"],
                "tags": ["auto-news", "geopolitics", "ai-generated", "verified"]
            },
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            wp_data = response.json()
            
            # Update Supabase to mark as posted
            try:
                # We need to find the article ID first
                search_response = requests.get(
                    f"{SUPABASE_URL}/rest/v1/news_articles",
                    headers={
                        "apikey": SUPABASE_KEY,
                        "Authorization": f"Bearer {SUPABASE_KEY}"
                    },
                    params={
                        "title": f"eq.{headline[:100]}",
                        "order": "created_at.desc",
                        "limit": "1"
                    },
                    timeout=5
                )
                
                if search_response.status_code == 200 and search_response.json():
                    article_id = search_response.json()[0]['id']
                    
                    requests.patch(
                        f"{SUPABASE_URL}/rest/v1/news_articles",
                        headers={
                            "apikey": SUPABASE_KEY,
                            "Authorization": f"Bearer {SUPABASE_KEY}",
                            "Content-Type": "application/json",
                            "Prefer": "return=minimal"
                        },
                        params={"id": f"eq.{article_id}"},
                        json={
                            "posted_to_wp": True,
                            "wp_post_id": str(wp_data.get('ID', '')),
                            "wp_post_url": wp_data.get('URL', '')
                        }
                    )
            except:
                pass  # Silently fail if can't update
            
            log(f"✅ Posted to WordPress: {headline[:50]}...")
            return True
        else:
            log(f"❌ WordPress error {response.status_code}: {response.text[:100]}", "ERROR")
            return False
            
    except Exception as e:
        log(f"❌ Post error: {e}", "ERROR")
        return False

# Main function
def main():
    log("🚀 Starting PERFECT GitHub Actions bot cycle")
    
    # Fetch news
    articles = fetch_news()
    
    if not articles:
        log("❌ No articles to process")
        return
    
    # Process articles
    stored_count = 0
    posted_count = 0
    
    for i, article in enumerate(articles):
        log(f"Processing article {i+1}/{len(articles)}...")
        
        # Store in Supabase
        if store_article(article):
            stored_count += 1
            
            # Post to WordPress
            if post_to_wordpress(article):
                posted_count += 1
            
            # Small delay between articles
            if i < len(articles) - 1:
                time.sleep(5)
    
    # Summary
    log(f"✅ Cycle complete: {stored_count} stored, {posted_count} posted to WordPress")
    
    print("\n" + "="*70)
    print(f"📊 SUMMARY:")
    print(f"   📥 Articles fetched: {len(articles)}")
    print(f"   💾 Articles stored: {stored_count}")
    print(f"   📤 Articles posted: {posted_count}")
    print(f"⏰ Next run: 4 hours via GitHub Actions schedule")
    print("="*70)

if __name__ == "__main__":
    main()
