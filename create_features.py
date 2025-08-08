#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from core.models import Category
from django.contrib.auth.models import User

# Create a simple Feature model using the existing Category model as a base
# We'll create "feature" categories that represent features

def create_features():
    """Create feature categories for the Latest Features section"""
    print("=== CREATING FEATURES ===")
    
    features_data = [
        {
            'name': 'Top 50 Brands 2024',
            'description': 'Comprehensive ranking of Nigeria\'s most valuable and influential brands for 2024.',
            'color': '#3B82F6'
        },
        {
            'name': 'New Market Entries',
            'description': 'Exciting new brands making their mark in the Nigerian market this year.',
            'color': '#10B981'
        },
        {
            'name': 'Most Popular Brands',
            'description': 'Consumer favorites that have captured the hearts of Nigerian customers.',
            'color': '#F59E0B'
        },
        {
            'name': 'Innovation Leaders',
            'description': 'Brands leading the way in technological innovation and digital transformation.',
            'color': '#8B5CF6'
        }
    ]
    
    created_features = []
    
    for i, feature_data in enumerate(features_data, 1):
        # Create or update the feature category
        feature, created = Category.objects.update_or_create(
            name=feature_data['name'],
            defaults={
                'slug': feature_data['name'].lower().replace(' ', '-'),
                'description': feature_data['description'],
                'color': feature_data['color']
            }
        )
        
        created_features.append(feature)
        print(f"{'✅ Created' if created else '✅ Updated'} feature: {feature_data['name']}")
        print(f"   Expected image: /features/feature-{i}.png")
    
    return created_features

if __name__ == "__main__":
    features = create_features()
    print(f"\n=== SUMMARY ===")
    print(f"Total features created: {len(features)}")