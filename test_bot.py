#!/usr/bin/env python3
import os
import sys

print("=== TEST BOT ===")
print(f"SUPABASE_URL: {'✅ Set' if os.getenv('SUPABASE_URL') else '❌ Not set'}")
print(f"SUPABASE_KEY: {'✅ Set' if os.getenv('SUPABASE_KEY') else '❌ Not set'}")
print(f"NEWSDATA_KEY: {'✅ Set' if os.getenv('NEWSDATA_KEY') else '❌ Not set'}")
print(f"WP_TOKEN: {'✅ Set' if os.getenv('WP_TOKEN') else '❌ Not set'}")
print(f"SITE_ID: {'✅ Set' if os.getenv('SITE_ID') else '❌ Not set'}")

# Check if all are set
all_set = all([
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY'), 
    os.getenv('NEWSDATA_KEY'),
    os.getenv('WP_TOKEN'),
    os.getenv('SITE_ID')
])

if all_set:
    print("\n✅ All environment variables are set!")
    sys.exit(0)
else:
    print("\n❌ Missing environment variables!")
    sys.exit(1)
