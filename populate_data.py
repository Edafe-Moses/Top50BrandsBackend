#!/usr/bin/env python
"""
Script to populate the database with initial brand data.
Run this after setting up the Django project and running migrations.

Usage: python populate_data.py
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand, BrandMetric, BrandAchievement, BrandTimeline, BrandCategory
from blog.models import BlogPost, BlogCategory
from insights.models import Insight, InsightMetric, InsightKeyFinding
from core.models import Category, Industry, Location
from django.contrib.auth.models import User


def create_categories():
    """Create brand categories."""
    categories_data = [
        {'name': 'Banking', 'slug': 'banking', 'description': 'Financial services and banking institutions', 'color': '#1e40af'},
        {'name': 'Telecommunications', 'slug': 'telecommunications', 'description': 'Mobile networks and telecom services', 'color': '#7c3aed'},
        {'name': 'Consumer Goods', 'slug': 'consumer-goods', 'description': 'Fast-moving consumer goods and retail', 'color': '#dc2626'},
        {'name': 'Manufacturing', 'slug': 'manufacturing', 'description': 'Industrial manufacturing and production', 'color': '#ea580c'},
        {'name': 'Agribusiness', 'slug': 'agribusiness', 'description': 'Agriculture and food processing', 'color': '#16a34a'},
        {'name': 'Oil & Gas', 'slug': 'oil-gas', 'description': 'Energy and petroleum industry', 'color': '#0891b2'},
        {'name': 'Technology', 'slug': 'technology', 'description': 'Technology and digital services', 'color': '#4f46e5'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")


def create_industries():
    """Create industries."""
    industries_data = [
        {'name': 'Financial Services', 'slug': 'financial-services'},
        {'name': 'Telecommunications', 'slug': 'telecommunications'},
        {'name': 'Food & Beverages', 'slug': 'food-beverages'},
        {'name': 'Building Materials', 'slug': 'building-materials'},
        {'name': 'Agribusiness', 'slug': 'agribusiness'},
        {'name': 'Oil & Gas', 'slug': 'oil-gas'},
        {'name': 'Technology', 'slug': 'technology'},
    ]
    
    for ind_data in industries_data:
        industry, created = Industry.objects.get_or_create(
            slug=ind_data['slug'],
            defaults=ind_data
        )
        if created:
            print(f"Created industry: {industry.name}")


def create_locations():
    """Create locations."""
    locations_data = [
        {'name': 'Lagos', 'slug': 'lagos', 'country': 'Nigeria', 'state': 'Lagos'},
        {'name': 'Abuja', 'slug': 'abuja', 'country': 'Nigeria', 'state': 'FCT'},
        {'name': 'Port Harcourt', 'slug': 'port-harcourt', 'country': 'Nigeria', 'state': 'Rivers'},
        {'name': 'Kano', 'slug': 'kano', 'country': 'Nigeria', 'state': 'Kano'},
    ]
    
    for loc_data in locations_data:
        location, created = Location.objects.get_or_create(
            slug=loc_data['slug'],
            defaults=loc_data
        )
        if created:
            print(f"Created location: {location.name}")


def create_brands():
    """Create brand data."""
    # Get categories and locations
    banking_cat = Category.objects.get(slug='banking')
    telecom_cat = Category.objects.get(slug='telecommunications')
    consumer_cat = Category.objects.get(slug='consumer-goods')
    manufacturing_cat = Category.objects.get(slug='manufacturing')
    agribusiness_cat = Category.objects.get(slug='agribusiness')
    
    financial_ind = Industry.objects.get(slug='financial-services')
    telecom_ind = Industry.objects.get(slug='telecommunications')
    food_ind = Industry.objects.get(slug='food-beverages')
    building_ind = Industry.objects.get(slug='building-materials')
    agri_ind = Industry.objects.get(slug='agribusiness')
    
    lagos = Location.objects.get(slug='lagos')
    
    brands_data = [
        {
            'title': 'Dangote Group',
            'subtitle': 'Africa\'s Leading Industrial Conglomerate',
            'slug': 'dangote-group',
            'description': 'Africa\'s largest industrial conglomerate with interests in cement, sugar, salt, and oil refining.',
            'full_description': 'Dangote Group is Africa\'s leading industrial conglomerate, founded by Aliko Dangote. The company has diversified interests across cement production, sugar refining, salt manufacturing, and oil refining, making it one of the most valuable brands in Nigeria.',
            'current_rank': 1,
            'brand_value': '₦4.2T',
            'market_cap': '₦4.2 Trillion',
            'revenue': '₦3.97 Trillion',
            'growth_rate': '+12.5%',
            'founded_year': '1981',
            'ceo': 'Aliko Dangote',
            'employees': '11,000+',
            'headquarters': lagos,
            'category': manufacturing_cat,
            'industry': building_ind,
            'brand_recognition': 95,
            'customer_rating': Decimal('4.8'),
            'is_featured': True,
            'website': 'https://dangote.com',
        },
        {
            'title': 'MTN Nigeria',
            'subtitle': 'Leading Telecommunications Network',
            'slug': 'mtn-nigeria',
            'description': 'Nigeria\'s largest mobile network operator providing voice, data, and digital services.',
            'full_description': 'MTN Nigeria is the country\'s largest telecommunications company, providing mobile voice, data, and digital services to over 77 million subscribers across Nigeria.',
            'current_rank': 2,
            'brand_value': '₦2.8T',
            'market_cap': '₦2.8 Trillion',
            'revenue': '₦1.7 Trillion',
            'growth_rate': '+8.3%',
            'founded_year': '2001',
            'ceo': 'Karl Toriola',
            'employees': '2,500+',
            'headquarters': lagos,
            'category': telecom_cat,
            'industry': telecom_ind,
            'brand_recognition': 92,
            'customer_rating': Decimal('4.5'),
            'is_featured': True,
            'website': 'https://mtnonline.com',
        },
        {
            'title': 'Guaranty Trust Bank',
            'subtitle': 'Nigeria\'s Most Trusted Bank',
            'slug': 'guaranty-trust-bank',
            'description': 'Leading commercial bank known for innovation and excellent customer service.',
            'full_description': 'Guaranty Trust Bank (GTBank) is one of Nigeria\'s leading financial institutions, renowned for its innovative banking solutions and exceptional customer service.',
            'current_rank': 3,
            'brand_value': '₦1.8T',
            'market_cap': '₦1.8 Trillion',
            'revenue': '₦684 Billion',
            'growth_rate': '+15.2%',
            'founded_year': '1990',
            'ceo': 'Segun Agbaje',
            'employees': '5,000+',
            'headquarters': lagos,
            'category': banking_cat,
            'industry': financial_ind,
            'brand_recognition': 88,
            'customer_rating': Decimal('4.7'),
            'is_featured': True,
            'website': 'https://gtbank.com',
        },
        {
            'title': 'Zenith Bank',
            'subtitle': 'Leading Commercial Bank',
            'slug': 'zenith-bank',
            'description': 'One of Nigeria\'s premier financial institutions providing comprehensive banking services.',
            'full_description': 'Zenith Bank Plc is one of Nigeria\'s leading financial institutions, known for its innovative banking solutions and excellent customer service.',
            'current_rank': 4,
            'brand_value': '₦1.5T',
            'growth_rate': '+10.2%',
            'founded_year': '1990',
            'ceo': 'Ebenezer Onyeagwu',
            'employees': '10,000+',
            'headquarters': lagos,
            'category': banking_cat,
            'industry': financial_ind,
            'brand_recognition': 85,
            'customer_rating': Decimal('4.6'),
            'website': 'https://zenithbank.com',
        },
        {
            'title': 'Nigerian Breweries',
            'subtitle': 'Leading Beverage Company',
            'slug': 'nigerian-breweries',
            'description': 'Nigeria\'s pioneer and largest brewing company with iconic beer brands.',
            'full_description': 'Nigerian Breweries Plc is the pioneer and largest brewing company in Nigeria with popular brands like Star, Gulder, Heineken, and Legend.',
            'current_rank': 5,
            'brand_value': '₦1.2T',
            'growth_rate': '+6.8%',
            'founded_year': '1946',
            'ceo': 'Hans Essaadi',
            'employees': '7,500+',
            'headquarters': lagos,
            'category': consumer_cat,
            'industry': food_ind,
            'brand_recognition': 92,
            'customer_rating': Decimal('4.4'),
            'website': 'https://nbplc.com',
        },
    ]
    
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            slug=brand_data['slug'],
            defaults=brand_data
        )
        if created:
            print(f"Created brand: {brand.title}")
            
            # Create sample metrics for each brand
            create_brand_metrics(brand)
            create_brand_achievements(brand)
            create_brand_timeline(brand)


def create_brand_metrics(brand):
    """Create sample metrics for a brand."""
    if brand.slug == 'dangote-group':
        metrics_data = [
            {'label': 'Market Share', 'value': '65%', 'change': '+3%', 'trend': 'up'},
            {'label': 'Countries', 'value': '18', 'change': '+2', 'trend': 'up'},
            {'label': 'Production Capacity', 'value': '48Mt', 'change': '+8%', 'trend': 'up'},
            {'label': 'Revenue Growth', 'value': '12.5%', 'change': '+2.1%', 'trend': 'up'},
        ]
    elif brand.slug == 'mtn-nigeria':
        metrics_data = [
            {'label': 'Subscribers', 'value': '77M+', 'change': '+8%', 'trend': 'up'},
            {'label': '4G Coverage', 'value': '75%', 'change': '+15%', 'trend': 'up'},
            {'label': 'Network Quality', 'value': '95%', 'change': '+2%', 'trend': 'up'},
            {'label': 'Data Revenue', 'value': '45%', 'change': '+5%', 'trend': 'up'},
        ]
    else:
        metrics_data = [
            {'label': 'Customer Base', 'value': '4.2M', 'change': '+8%', 'trend': 'up'},
            {'label': 'Branch Network', 'value': '500+', 'change': '+5%', 'trend': 'up'},
        ]
    
    for i, metric_data in enumerate(metrics_data):
        BrandMetric.objects.get_or_create(
            brand=brand,
            label=metric_data['label'],
            defaults={**metric_data, 'order': i}
        )


def create_brand_achievements(brand):
    """Create sample achievements for a brand."""
    achievements_data = [
        {'title': 'Brand of the Year 2023', 'year': '2023'},
        {'title': 'Excellence in Innovation', 'year': '2022'},
        {'title': 'Customer Service Award', 'year': '2021'},
    ]
    
    for i, achievement_data in enumerate(achievements_data):
        BrandAchievement.objects.get_or_create(
            brand=brand,
            title=achievement_data['title'],
            defaults={**achievement_data, 'order': i}
        )


def create_brand_timeline(brand):
    """Create sample timeline for a brand."""
    timeline_data = [
        {'year': brand.founded_year, 'event': f'Founded {brand.title}'},
        {'year': '2020', 'event': 'Digital transformation initiative'},
        {'year': '2023', 'event': 'Expansion into new markets'},
    ]
    
    for i, timeline_data in enumerate(timeline_data):
        BrandTimeline.objects.get_or_create(
            brand=brand,
            year=timeline_data['year'],
            event=timeline_data['event'],
            defaults={'order': i}
        )


def create_sample_blog_posts():
    """Create sample blog posts."""
    # Create admin user if doesn't exist
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@top50brands.ng',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    
    # Create blog categories
    blog_categories = [
        {'name': 'Fintech', 'slug': 'fintech', 'color': '#3b82f6'},
        {'name': 'Energy', 'slug': 'energy', 'color': '#f59e0b'},
        {'name': 'Technology', 'slug': 'technology', 'color': '#8b5cf6'},
        {'name': 'Banking', 'slug': 'banking', 'color': '#10b981'},
    ]
    
    for cat_data in blog_categories:
        BlogCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
    
    print("Sample data population completed!")


def main():
    """Main function to populate all data."""
    print("Starting data population...")
    
    create_categories()
    create_industries()
    create_locations()
    create_brands()
    create_sample_blog_posts()
    
    print("Data population completed successfully!")


if __name__ == '__main__':
    main()
