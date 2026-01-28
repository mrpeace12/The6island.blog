# THE6ISLAND.BLOG - 24/7 News Bot

This repository contains an automated news bot that runs on GitHub Actions.

## How It Works
1. Runs every 4 hours automatically
2. Fetches news from NewsData.io
3. Posts to WordPress automatically
4. Logs everything to Supabase
5. Runs even when your devices are off

## Setup
Add these secrets in GitHub:
- SUPABASE_URL
- SUPABASE_KEY
- NEWSDATA_KEY
- WP_TOKEN
- SITE_ID

## Manual Run
Go to Actions → 24/7 News Bot → Run workflow
