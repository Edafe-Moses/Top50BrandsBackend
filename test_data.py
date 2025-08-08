#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from blog.models import BlogPost
from brands.models import Brand

print("=== DATABASE CHECK ===")
print(f"Total Blog Posts: {BlogPost.objects.count()}")
print(f"Published Blog Posts: {BlogPost.objects.filter(status='published', is_published=True).count()}")
print(f"Featured Blog Posts: {BlogPost.objects.filter(is_featured=True, status='published', is_published=True).count()}")

print(f"\nTotal Brands: {Brand.objects.count()}")
print(f"Published Brands: {Brand.objects.filter(is_published=True).count()}")
print(f"New Entry Brands: {Brand.objects.filter(is_new_entry=True, is_published=True).count()}")
print(f"Featured Brands: {Brand.objects.filter(is_featured=True, is_published=True).count()}")
print(f"Top 10 Brands: {Brand.objects.filter(current_rank__lte=10, is_published=True).count()}")

# Check if there are any blog posts at all
if BlogPost.objects.exists():
    print("\n=== SAMPLE BLOG POSTS ===")
    for post in BlogPost.objects.all()[:3]:
        print(f"- {post.title} (Status: {post.status}, Published: {post.is_published}, Featured: {post.is_featured})")

# Check if there are any brands at all
if Brand.objects.exists():
    print("\n=== SAMPLE BRANDS ===")
    for brand in Brand.objects.all()[:5]:
        print(f"- {brand.title} (Published: {brand.is_published}, Featured: {brand.is_featured}, New Entry: {brand.is_new_entry}, Rank: {brand.current_rank})")