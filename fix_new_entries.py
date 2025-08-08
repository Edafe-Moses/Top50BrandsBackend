#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand

print("=== FIXING NEW ENTRIES ===")

# Mark some brands as new entries
new_entry_brands = ['Flutterwave', 'Shoprite Nigeria', 'UBA Group']

for brand_name in new_entry_brands:
    try:
        brand = Brand.objects.get(title=brand_name)
        brand.is_new_entry = True
        brand.save()
        print(f"✅ Marked {brand_name} as new entry")
    except Brand.DoesNotExist:
        print(f"❌ Brand {brand_name} not found")

print(f"\nNew Entry Brands: {Brand.objects.filter(is_new_entry=True, is_published=True).count()}")

# List all new entry brands
print("\n=== NEW ENTRY BRANDS ===")
for brand in Brand.objects.filter(is_new_entry=True, is_published=True):
    print(f"- {brand.title} (Rank: {brand.current_rank})")