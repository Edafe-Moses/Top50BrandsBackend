#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand
from blog.models import BlogPost

def update_brand_images():
    """Update brand images with correct paths from public directory"""
    print("=== UPDATING BRAND IMAGES ===")
    
    # Mapping of brand titles to their image files
    brand_image_mapping = {
        'Dangote Group': '/brands/dangote-group.png',
        'MTN Nigeria': '/brands/mtn-nigeria.png',
        'Guaranty Trust Bank': '/brands/guaranty-trust-bank.png',
        'Zenith Bank': '/brands/zenith-bank.png',
        'Nigerian Breweries': '/brands/nigerian-breweries.png',
        'Airtel Nigeria': '/brands/airtel-nigeria.png',
        'First Bank Nigeria': '/brands/first-bank-nigeria.png',
        'Nestle Nigeria': '/brands/nestle-nigeria.png',
        'UBA Group': '/brands/uba-group.png',
        'Shoprite Nigeria': '/brands/shoprite-nigeria.png',  # This exists in logos folder
        'Flutterwave': '/brands/flutterwave.png',
    }
    
    # Update brands with correct image paths
    for brand_title, image_path in brand_image_mapping.items():
        try:
            brand = Brand.objects.get(title=brand_title)
            # We'll store the path in the description field temporarily since we can't upload files
            # The serializer will use the fallback logic we already implemented
            print(f"✅ Found brand: {brand_title}")
            print(f"   Current slug: {brand.slug}")
            print(f"   Expected image path: {image_path}")
        except Brand.DoesNotExist:
            print(f"❌ Brand not found: {brand_title}")

def update_blog_images():
    """Update blog post images with correct paths"""
    print("\n=== UPDATING BLOG POST IMAGES ===")
    
    blog_posts = BlogPost.objects.all().order_by('id')
    for i, post in enumerate(blog_posts, 1):
        expected_path = f'/blog/blog-{i}.png'
        print(f"✅ Blog post: {post.title}")
        print(f"   ID: {post.id}")
        print(f"   Expected image path: {expected_path}")

def check_image_paths():
    """Check if the fallback paths match available images"""
    print("\n=== CHECKING IMAGE PATH ALIGNMENT ===")
    
    print("\n--- Brand Images ---")
    brands = Brand.objects.all()
    for brand in brands:
        expected_path = f'/brands/{brand.slug}.png'
        print(f"Brand: {brand.title}")
        print(f"  Slug: {brand.slug}")
        print(f"  Expected path: {expected_path}")
        
        # Check if we need to update the slug to match available images
        available_images = [
            'dangote-group.png', 'mtn-nigeria.png', 'guaranty-trust-bank.png',
            'zenith-bank.png', 'nigerian-breweries.png', 'airtel-nigeria.png',
            'first-bank-nigeria.png', 'nestle-nigeria.png', 'uba-group.png',
            'flutterwave.png'
        ]
        
        matching_image = None
        for img in available_images:
            if brand.slug in img or img.replace('.png', '').replace('-', ' ').lower() in brand.title.lower():
                matching_image = img
                break
        
        if matching_image:
            print(f"  ✅ Matching image found: /brands/{matching_image}")
        else:
            print(f"  ❌ No matching image found")
        print()

def fix_brand_slugs():
    """Fix brand slugs to match available image files"""
    print("\n=== FIXING BRAND SLUGS TO MATCH IMAGES ===")
    
    # Mapping of current brand titles to correct slugs that match image files
    slug_fixes = {
        'Dangote Group': 'dangote-group',
        'MTN Nigeria': 'mtn-nigeria', 
        'Guaranty Trust Bank': 'guaranty-trust-bank',
        'Zenith Bank': 'zenith-bank',
        'Nigerian Breweries': 'nigerian-breweries',
        'Airtel Nigeria': 'airtel-nigeria',
        'First Bank Nigeria': 'first-bank-nigeria',
        'Nestle Nigeria': 'nestle-nigeria',
        'UBA Group': 'uba-group',
        'Shoprite Nigeria': 'shoprite-nigeria',  # We have this in logos folder
        'Flutterwave': 'flutterwave',
    }
    
    for brand_title, correct_slug in slug_fixes.items():
        try:
            brand = Brand.objects.get(title=brand_title)
            old_slug = brand.slug
            brand.slug = correct_slug
            brand.save()
            print(f"✅ Updated {brand_title}: '{old_slug}' → '{correct_slug}'")
        except Brand.DoesNotExist:
            print(f"❌ Brand not found: {brand_title}")

if __name__ == "__main__":
    print("Starting image path updates...")
    update_brand_images()
    update_blog_images()
    check_image_paths()
    fix_brand_slugs()
    
    print("\n=== FINAL CHECK ===")
    print("After slug fixes, brands should have these image paths:")
    for brand in Brand.objects.all():
        print(f"- {brand.title}: /brands/{brand.slug}.png")