#!/usr/bin/env python
"""
Simple data population script that works with existing data
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand, Category
from blog.models import BlogPost, BlogCategory
from insights.models import Insight
from dashboard.models import YearlyRanking
from django.contrib.auth.models import User

def populate_brands():
    """Add more brands to existing categories"""
    try:
        year_2025 = YearlyRanking.objects.get(year=2025)
        
        # Get existing categories
        banking = Category.objects.filter(name__icontains='Banking').first()
        telecom = Category.objects.filter(name__icontains='Telecommunications').first()
        oil_gas = Category.objects.filter(name__icontains='Oil').first()
        tech = Category.objects.filter(name__icontains='Technology').first()
        manufacturing = Category.objects.filter(name__icontains='Manufacturing').first()
        
        print(f"Found categories: Banking={banking}, Telecom={telecom}, Oil&Gas={oil_gas}, Tech={tech}, Manufacturing={manufacturing}")
        
        # Additional brands data
        additional_brands = [
            {
                'title': 'Airtel Nigeria',
                'subtitle': 'Innovative Telecom Solutions',
                'description': 'Major telecommunications provider offering mobile, data, and digital financial services.',
                'full_description': 'Airtel Nigeria is a major telecommunications provider offering comprehensive mobile, data, and digital financial services across Nigeria.',
                'category': telecom,
                'current_rank': 6,
                'brand_value': '₦980B',
                'growth_rate': '+7.8%',
                'founded_year': '2010',
                'employees': '2,200',
                'year': 2025,
            },
            {
                'title': 'First Bank of Nigeria',
                'subtitle': 'Nigeria\'s Heritage Bank',
                'description': 'Nigeria\'s oldest bank and financial services group with over 160 years of banking excellence.',
                'full_description': 'First Bank of Nigeria is the oldest bank in Nigeria with over 160 years of banking excellence, providing comprehensive financial services.',
                'category': banking,
                'current_rank': 7,
                'brand_value': '₦850B',
                'growth_rate': '+3.9%',
                'founded_year': '1894',
                'employees': '8,500',
                'year': 2025,
            },
            {
                'title': 'Flutterwave',
                'subtitle': 'Fintech Innovation Leader',
                'description': 'Leading African fintech company providing payment infrastructure for global merchants.',
                'full_description': 'Flutterwave is a leading African fintech company providing payment infrastructure for global merchants and payment service providers.',
                'category': tech,
                'current_rank': 8,
                'brand_value': '₦680B',
                'growth_rate': '+15.2%',
                'founded_year': '2016',
                'employees': '800',
                'year': 2025,
            },
            {
                'title': 'Innoson Vehicle Manufacturing',
                'subtitle': 'Made in Nigeria Vehicles',
                'description': 'Nigeria\'s first indigenous automobile manufacturing company.',
                'full_description': 'Innoson Vehicle Manufacturing is Nigeria\'s first indigenous automobile manufacturing company producing quality vehicles.',
                'category': manufacturing,
                'current_rank': 9,
                'brand_value': '₦420B',
                'growth_rate': '+8.5%',
                'founded_year': '2007',
                'employees': '3,000',
                'year': 2025,
            },
            {
                'title': 'Access Bank',
                'subtitle': 'Africa\'s Gateway to the World',
                'description': 'Leading commercial bank with strong retail and corporate banking services.',
                'full_description': 'Access Bank is a leading commercial bank providing comprehensive retail and corporate banking services across Africa.',
                'category': banking,
                'current_rank': 10,
                'brand_value': '₦380B',
                'growth_rate': '+5.1%',
                'founded_year': '1989',
                'employees': '28,000',
                'year': 2025,
            },
        ]
        
        for brand_data in additional_brands:
            if brand_data['category']:  # Only create if category exists
                brand, created = Brand.objects.get_or_create(
                    title=brand_data['title'],
                    year=2025,
                    defaults=brand_data
                )
                if created:
                    print(f"✅ Created brand: {brand.title}")
                else:
                    print(f"📝 Brand already exists: {brand.title}")
            else:
                print(f"❌ Skipping {brand_data['title']} - no category found")
                
    except Exception as e:
        print(f"❌ Error creating brands: {e}")

def populate_blog_posts():
    """Create blog posts"""
    try:
        # Use existing categories for blog posts
        market_analysis = Category.objects.filter(name__icontains='Banking').first()
        brand_spotlight = Category.objects.filter(name__icontains='Technology').first()
        
        # Get or create user
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        
        # Create blog posts
        posts_data = [
            {
                'title': 'Nigeria\'s Top 10 Brands Show Resilient Growth in 2025',
                'excerpt': 'Despite economic challenges, Nigeria\'s leading brands demonstrate remarkable resilience and growth.',
                'content': 'Full analysis of how Nigeria\'s top brands are navigating the current economic landscape with innovative strategies and digital transformation initiatives.',
                'category': market_analysis,
                'author': user,
                'year': 2025,
                'is_featured': True,
                'read_time': 8,
                'status': 'published',
            },
            {
                'title': 'The Rise of Nigerian Fintech: Flutterwave\'s Success Story',
                'excerpt': 'How Flutterwave became one of Nigeria\'s most valuable tech companies.',
                'content': 'An in-depth look at Flutterwave\'s journey from startup to unicorn status, examining their innovative payment solutions and expansion across Africa.',
                'category': brand_spotlight,
                'author': user,
                'year': 2025,
                'is_featured': False,
                'read_time': 6,
                'status': 'published',
            },
            {
                'title': 'Banking Sector Transformation: Digital Innovation Leads the Way',
                'excerpt': 'Nigerian banks are embracing digital transformation to stay competitive.',
                'content': 'Analysis of how traditional banks like GTBank, Zenith, and First Bank are adapting to the digital age with mobile banking, AI, and fintech partnerships.',
                'category': market_analysis,
                'author': user,
                'year': 2025,
                'is_featured': False,
                'read_time': 7,
                'status': 'published',
            },
        ]
        
        for post_data in posts_data:
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults=post_data
            )
            if created:
                print(f"✅ Created blog post: {post.title}")
            else:
                print(f"📝 Blog post already exists: {post.title}")
                
    except Exception as e:
        print(f"❌ Error creating blog posts: {e}")

def populate_insights():
    """Create market insights"""
    try:
        # Get existing categories to use for insights
        banking_cat = Category.objects.filter(name__icontains='Banking').first()
        tech_cat = Category.objects.filter(name__icontains='Technology').first()
        telecom_cat = Category.objects.filter(name__icontains='Telecommunications').first()
        
        # Get or create user
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        
        # Create insights
        insights_data = [
            {
                'title': '2025 Nigerian Brand Valuation Report',
                'description': 'Comprehensive analysis of brand values across Nigerian markets with detailed methodology and market insights.',
                'content': 'Our annual brand valuation study reveals significant growth in Nigeria\'s top brands, with technology and fintech sectors leading the charge.',
                'insight_type': 'market_analysis',
                'category': tech_cat,
                'author': user,
                'year': 2025,
                'is_premium': False,
                'data_points': '150',
                'views_count': 2340,
                'download_count': 456,
            },
            {
                'title': 'Consumer Trust Index: Banking Sector Analysis',
                'description': 'How Nigerian consumers perceive and trust different banking brands based on comprehensive survey data.',
                'content': 'Survey results show that digital banking capabilities and customer service quality are the primary drivers of consumer trust in Nigerian banks.',
                'insight_type': 'consumer_behavior',
                'category': banking_cat,
                'author': user,
                'year': 2025,
                'is_premium': True,
                'data_points': '89',
                'views_count': 1890,
                'download_count': 234,
            },
            {
                'title': 'Telecom Brand Performance Metrics Q1 2025',
                'description': 'Quarterly performance analysis of major telecom brands including market share and customer satisfaction.',
                'content': 'MTN Nigeria continues to lead in market share while Airtel shows strong growth in data services and customer acquisition.',
                'insight_type': 'brand_performance',
                'category': telecom_cat,
                'author': user,
                'year': 2025,
                'is_premium': False,
                'data_points': '67',
                'views_count': 1456,
                'download_count': 189,
            },
        ]
        
        for insight_data in insights_data:
            if insight_data['category']:  # Only create if category exists
                insight, created = Insight.objects.get_or_create(
                    title=insight_data['title'],
                    defaults=insight_data
                )
                if created:
                    print(f"✅ Created insight: {insight.title}")
                else:
                    print(f"📝 Insight already exists: {insight.title}")
            else:
                print(f"❌ Skipping insight - no category found")
                
    except Exception as e:
        print(f"❌ Error creating insights: {e}")

def main():
    """Main function to populate data"""
    print("🚀 Starting simple data population...")
    
    try:
        print("\n📊 Populating brands...")
        populate_brands()
        
        print("\n📝 Populating blog posts...")
        populate_blog_posts()
        
        print("\n🔍 Populating insights...")
        populate_insights()
        
        print(f"\n✅ Data population completed!")
        print(f"📊 Total Brands: {Brand.objects.filter(year=2025).count()}")
        print(f"📝 Total Blog Posts: {BlogPost.objects.filter(year=2025).count()}")
        print(f"🔍 Total Insights: {Insight.objects.filter(year=2025).count()}")
        
    except Exception as e:
        print(f"❌ Error during data population: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
