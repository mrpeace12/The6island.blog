#!/usr/bin/env python3
print("="*60)
print("🌐 GITHUB ACTIONS BOT - RUNNING!")
print("="*60)

import os
import sys
from datetime import datetime

print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print()

# Check secrets
secrets = {
    'SUPABASE_URL': os.getenv('SUPABASE_URL'),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY'),
    'NEWSDATA_KEY': os.getenv('NEWSDATA_KEY'),
    'WP_TOKEN': os.getenv('WP_TOKEN'),
    'SITE_ID': os.getenv('SITE_ID')
}

all_good = True
for name, value in secrets.items():
    if value:
        print(f"✅ {name}: Set")
    else:
        print(f"❌ {name}: Missing")
        all_good = False

print()
print("="*60)
if all_good:
    print("🎉 SUCCESS! All secrets loaded correctly!")
    sys.exit(0)
else:
    print("⚠️ Some secrets are missing")
    sys.exit(1)
