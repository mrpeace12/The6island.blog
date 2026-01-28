#!/bin/bash
echo "========================================="
echo "🤖 24/7 BOT VERIFICATION SCRIPT"
echo "========================================="
echo "Checking at: $(date)"
echo ""

echo "1. CHECKING TERMUX PROCESSES..."
echo "--------------------------------"
ps aux | grep -E "(python|bot|news|schedule)" | grep -v grep | head -10
echo ""

echo "2. CHECKING GEO-NEWS-BOT FILES..."
echo "---------------------------------"
cd ~/geo-news-bot 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Active 24/7 bot candidates:"
    grep -l "24/7\|schedule\|every.*hour" *.py 2>/dev/null | head -5
    echo ""
    echo "Most recent bot files:"
    ls -lt *.py | head -5
else
    echo "geo-news-bot directory not found"
fi
echo ""

echo "3. CHECKING GITHUB REPO..."
echo "--------------------------"
cd ~/The6island.blog 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Workflow files:"
    ls -la .github/workflows/ 2>/dev/null || echo "No workflows directory"
    echo ""
    echo "Bot scripts:"
    ls -la *.py 2>/dev/null
else
    echo "The6island.blog directory not found"
fi
echo ""

echo "4. CHECKING SUPABASE LOGS..."
echo "----------------------------"
echo "Most recent 5 logs:"
curl -s "https://wewfkqshlyalwmjjiavc.supabase.co/rest/v1/bot_logs?select=message,created_at&order=created_at.desc&limit=5" \
  -H "apikey: sb_publishable_IM9gGo6aVbI2asSKlO69yw_5LEhL5TY" \
  -H "Authorization: Bearer sb_publishable_IM9gGo6aVbI2asSKlO69yw_5LEhL5TY" 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for log in data:
        print(f'{log[\"created_at\"][11:19]} - {log[\"message\"][:60]}...')
except:
    print('Could not fetch logs')
"
echo ""

echo "5. CHECKING WORDPRESS POSTS..."
echo "------------------------------"
echo "Manual check: Visit your WordPress site"
echo "Look for posts from:"
echo "  - GITHUB-BOT category"
echo "  - 24-7-NEWS category"
echo "  - Auto-generated posts"
echo ""

echo "6. RECOMMENDED ACTION PLAN:"
echo "---------------------------"
echo "A. STOP Termux bot if running"
echo "B. Add GitHub Secrets (MOST IMPORTANT)"
echo "C. Let GitHub run 24/7"
echo "D. Monitor for 4 hours"
echo "========================================="
