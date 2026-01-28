#!/usr/bin/env python3
print("="*60)
print("🌐 GITHUB BOT IS WORKING!")
print("="*60)

import os
print("Secrets loaded:")
for key in ['SUPABASE_URL', 'SUPABASE_KEY', 'NEWSDATA_KEY', 'WP_TOKEN', 'SITE_ID']:
    value = os.getenv(key)
    if value:
        print(f"✅ {key}: YES (length: {len(value)})")
    else:
        print(f"❌ {key}: NO")

print("="*60)
print("✅ SUCCESS! Workflow is working!")
print("="*60)
