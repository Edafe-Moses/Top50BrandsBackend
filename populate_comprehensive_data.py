#!/usr/bin/env python
"""
Comprehensive data population script for Top 50 Brands Nigeria
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand, Category, Industry, Location, BrandMetric, BrandAchievement
from blog.models import BlogPost, BlogCategory
from insights.models import Insight
from dashboard.models import YearlyRanking
from django.contrib.auth.models import User

def create_categories():
    """Create brand categories"""
    categories = [
        {'name': 'Banking & Finance', 'color': '#1E40AF', 'description': 'Financial services and banking institutions'},
        {'name': 'Telecommunications', 'color': '#059669', 'description': 'Mobile networks and communication services'},
        {'name': 'Oil & Gas', 'color': '#DC2626', 'description': 'Energy and petroleum companies'},
        {'name': 'Food & Beverages', 'color': '#D97706', 'description': 'Food production and beverage companies'},
        {'name': 'Retail & Consumer Goods', 'color': '#7C3AED', 'description': 'Retail chains and consumer products'},
        {'name': 'Technology', 'color': '#0891B2', 'description': 'Technology and software companies'},
        {'name': 'Manufacturing', 'color': '#65A30D', 'description': 'Industrial and manufacturing companies'},
        {'name': 'Healthcare', 'color': '#BE185D', 'description': 'Healthcare and pharmaceutical companies'},
    ]

    for cat_data in categories:
        # Use name as the unique lookup, and provide other fields in defaults
        # This will update existing entries or create new ones without conflict.
        defaults = {
            'slug': slugify(cat_data['name']),
            'color': cat_data['color'],
            'description': cat_data['description']
        }
        category, created = Category.objects.update_or_create(
            name=cat_data['name'],
            defaults=defaults
        )
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Updated category: {category.name}")

def create_industries():
    """Create industries"""
    industries = [
        'Banking', 'Telecommunications', 'Oil & Gas', 'Food Processing',
        'Retail', 'Technology', 'Manufacturing', 'Healthcare',
        'Insurance', 'Real Estate', 'Transportation', 'Media'
    ]
    
    for industry_name in industries:
        # Use name as the unique lookup to prevent conflicts.
        industry, created = Industry.objects.update_or_create(
            name=industry_name,
            defaults={'slug': slugify(industry_name)}
        )
        if created:
            print(f"Created industry: {industry.name}")
        else:
            print(f"Updated industry: {industry.name}")

def create_locations():
    """Create locations"""
    locations = [
        {'name': 'Lagos', 'state': 'Lagos'},
        {'name': 'Abuja', 'state': 'FCT'},
        {'name': 'Port Harcourt', 'state': 'Rivers'},
        {'name': 'Kano', 'state': 'Kano'},
        {'name': 'Ibadan', 'state': 'Oyo'},
    ]
    
    for loc_data in locations:
        location, created = Location.objects.update_or_create(
            name=loc_data['name'],
            defaults={'state': loc_data['state']}
        )
        if created:
            print(f"Created location: {location.name}")
        else:
            print(f"Updated location: {location.name}")

def create_comprehensive_brands():
    """Create comprehensive brand data"""
    year_2025 = YearlyRanking.objects.get(year=2025)
    
    # Get categories
    banking = Category.objects.get(name='Banking & Finance')
    telecom = Category.objects.get(name='Telecommunications')
    oil_gas = Category.objects.get(name='Oil & Gas')
    food_bev = Category.objects.get(name='Food & Beverages')
    retail = Category.objects.get(name='Retail & Consumer Goods')
    tech = Category.objects.get(name='Technology')
    manufacturing = Category.objects.get(name='Manufacturing')

    # Get locations
    lagos = Location.objects.get(name='Lagos')
    abuja = Location.objects.get(name='Abuja')
    
    brands_data = [
        {
            'title': 'Dangote Group',
            'subtitle': 'Africa\'s Leading Conglomerate',
            'description': 'Nigeria\'s largest industrial conglomerate with interests in cement, sugar, salt, and oil refining.',
            'category': oil_gas,
            'current_rank': 1,
            'brand_value': '₦4.2T',
            'growth_rate': '+12.5%',
            'headquarters': lagos,
            'founded_year': '1981',
            'employees': '41000',
            'website': 'https://www.dangote.com',
        },
        {
            'title': 'MTN Nigeria',
            'subtitle': 'Leading Telecommunications Provider',
            'description': 'Nigeria\'s largest mobile network operator providing voice, data, and digital services.',
            'category': telecom,
            'current_rank': 2,
            'brand_value': '₦2.8T',
            'growth_rate': '+8.3%',
            'headquarters': lagos,
            'founded_year': '2001',
            'employees': '3500',
            'website': 'https://www.mtnonline.com',
        },
        {
            'title': 'Guaranty Trust Bank',
            'subtitle': 'Premier Financial Institution',
            'description': 'One of Nigeria\'s leading commercial banks offering retail and corporate banking services.',
            'category': banking,
            'current_rank': 3,
            'brand_value': '₦1.8T',
            'growth_rate': '+6.7%',
            'headquarters': lagos,
            'founded_year': '1990',
            'employees': '5200',
            'website': 'https://www.gtbank.com',
        },
        {
            'title': 'Zenith Bank',
            'subtitle': 'International Commercial Bank',
            'description': 'Leading Nigerian commercial bank with strong international presence and digital banking solutions.',
            'category': banking,
            'current_rank': 4,
            'brand_value': '₦1.5T',
            'growth_rate': '+5.2%',
            'headquarters': lagos,
            'founded_year': '1990',
            'employees': '6800',
            'website': 'https://www.zenithbank.com',
        },
        {
            'title': 'Nigerian Breweries',
            'subtitle': 'Premium Beverage Company',
            'description': 'Nigeria\'s pioneer and largest brewing company producing premium beer and malt drinks.',
            'category': food_bev,
            'current_rank': 5,
            'brand_value': '₦1.2T',
            'growth_rate': '+4.1%',
            'headquarters': lagos,
            'founded_year': '1946',
            'employees': '2800',
            'website': 'https://www.nbplc.com',
        },
        {
            'title': 'Airtel Nigeria',
            'subtitle': 'Innovative Telecom Solutions',
            'description': 'Major telecommunications provider offering mobile, data, and digital financial services.',
            'category': telecom,
            'current_rank': 6,
            'brand_value': '₦980B',
            'growth_rate': '+7.8%',
            'headquarters': lagos,
            'founded_year': '2010',
            'employees': '2200',
            'website': 'https://www.airtel.com.ng',
        },
        {
            'title': 'First Bank Nigeria',
            'subtitle': 'Nigeria\'s Heritage Bank',
            'description': 'Nigeria\'s oldest bank and financial services group with over 160 years of banking excellence.',
            'category': banking,
            'current_rank': 7,
            'brand_value': '₦850B',
            'growth_rate': '+3.9%',
            'headquarters': lagos,
            'founded_year': '1894',
            'employees': '8500',
            'website': 'https://www.firstbanknigeria.com',
        },
        {
            'title': 'Nestle Nigeria',
            'subtitle': 'Good Food, Good Life',
            'description': 'Leading nutrition, health, and wellness company with iconic brands like Maggi and Milo.',
            'category': food_bev,
            'current_rank': 9,
            'brand_value': '₦720B',
            'growth_rate': '+5.1%',
            'headquarters': lagos,
            'founded_year': '1961',
            'employees': '2300',
            'website': 'https://www.nestle-cwa.com/en/nestle-nigeria',
        },
        {
            'title': 'UBA Group',
            'subtitle': 'Pan-African Financial Institution',
            'description': 'United Bank for Africa is a leading pan-African financial services group headquartered in Nigeria.',
            'category': banking,
            'current_rank': 10,
            'brand_value': '₦680B',
            'growth_rate': '+6.2%',
            'headquarters': lagos,
            'founded_year': '1949',
            'employees': '10000',
            'website': 'https://www.ubagroup.com',
        },
        # {
        #     'title': 'Flutterwave',
        #     'subtitle': 'Powering Digital Payments',
        #     'description': 'A leading technology company that enables businesses to make and accept payments across Africa.',
        #     'category': tech,
        #     'current_rank': 11,
        #     'brand_value': '₦650B',
        #     'growth_rate': '+25.0%',
        #     'headquarters': lagos,
        #     'founded_year': '2016',
        #     'employees': '500',
        #     'website': 'https://www.flutterwave.com',
        # },
        # {
        #     'title': 'Access Bank',
        #     'subtitle': 'More Than Banking',
        #     'description': 'A full-service commercial bank operating through a network of more than 600 branches and service outlets.',
        #     'category': banking,
        #     'current_rank': 8,
        #     'brand_value': '₦780B',
        #     'growth_rate': '+7.2%',
        #     'headquarters': lagos,
        #     'founded_year': '1989',
        #     'employees': '6000',
        #     'website': 'https://www.accessbankplc.com',
        # },
        # {
        #     'title': 'Innoson Vehicle Manufacturing',
        #     'subtitle': 'The African Pride',
        #     'description': 'Nigeria\'s first indigenous automobile manufacturing company.',
        #     'category': manufacturing,
        #     'current_rank': 15,
        #     'brand_value': '₦400B',
        #     'growth_rate': '+18.5%',
        #     'headquarters': lagos, # Assuming Lagos for consistency
        #     'founded_year': '2007',
        #     'employees': '1500',
        #     'website': 'https://www.innosonvehicles.com',
        # },
        {
            'title': 'Shoprite Nigeria',
            'subtitle': 'Leading Retail Chain',
            'description': 'Major retail supermarket chain offering quality products and exceptional shopping experience.',
            'category': retail,
            'current_rank': 8,
            'brand_value': '₦750B',
            'growth_rate': '+3.5%',
            'headquarters': lagos,
            'founded_year': '2005',
            'employees': '2000',
            'website': 'https://www.shoprite.com.ng',
        },
        {
            'title': 'Flutterwave',
            'subtitle': 'Fintech Innovation Leader',
            'description': 'Leading African fintech company providing payment infrastructure for global merchants and payment service providers.',
            'category': tech,
            'current_rank': 9,
            'brand_value': '₦680B',
            'growth_rate': '+15.2%',
            'headquarters': lagos,
            'founded_year': 2016,
            'employees': '800',
            'website': 'https://flutterwave.com',
        },
        {
            'title': 'Andela',
            'subtitle': 'Building Tomorrow\'s Tech Talent',
            'description': 'Global talent network connecting companies with vetted, remote software developers from Africa.',
            'category': tech,
            'current_rank': 11,
            'brand_value': '₦450B',
            'growth_rate': '+28.5%',
            'headquarters': lagos,
            'founded_year': '2014',
            'employees': '2000',
            'website': 'https://andela.com',
        },
        {
            'title': 'Paystack',
            'subtitle': 'Modern Online Payments',
            'description': 'Leading payment processing platform enabling businesses to accept payments online and offline.',
            'category': tech,
            'current_rank': 12,
            'brand_value': '₦420B',
            'growth_rate': '+22.3%',
            'headquarters': lagos,
            'founded_year': '2015',
            'employees': '300',
            'website': 'https://paystack.com',
        },
        {
            'title': 'Jumia',
            'subtitle': 'Africa\'s Leading E-commerce Platform',
            'description': 'Pan-African e-commerce platform connecting millions of consumers and sellers across Africa.',
            'category': tech,
            'current_rank': 13,
            'brand_value': '₦380B',
            'growth_rate': '+18.7%',
            'headquarters': lagos,
            'founded_year': '2012',
            'employees': '5000',
            'website': 'https://jumia.com.ng',
        },
        {
            'title': 'Interswitch',
            'subtitle': 'Digital Payment Solutions',
            'description': 'Leading African integrated digital payments and commerce company.',
            'category': tech,
            'current_rank': 14,
            'brand_value': '₦350B',
            'growth_rate': '+16.4%',
            'headquarters': lagos,
            'founded_year': '2002',
            'employees': '1200',
            'website': 'https://interswitch.com',
        },
        {
            'title': 'Konga',
            'subtitle': 'Nigeria\'s Premier E-commerce Destination',
            'description': 'Leading Nigerian e-commerce platform offering diverse products and services.',
            'category': tech,
            'current_rank': 15,
            'brand_value': '₦320B',
            'growth_rate': '+14.2%',
            'headquarters': lagos,
            'founded_year': '2012',
            'employees': '800',
            'website': 'https://konga.com',
        },
        {
            'title': 'OPay',
            'subtitle': 'Super App for Everything',
            'description': 'Leading fintech company providing mobile payment, ride-hailing, and food delivery services.',
            'category': tech,
            'current_rank': 16,
            'brand_value': '₦300B',
            'growth_rate': '+35.8%',
            'headquarters': lagos,
            'founded_year': '2018',
            'employees': '3000',
            'website': 'https://opayweb.com',
        },
        {
            'title': 'PiggyVest',
            'subtitle': 'Smart Savings & Investment',
            'description': 'Leading savings and investment platform helping Nigerians achieve their financial goals.',
            'category': tech,
            'current_rank': 17,
            'brand_value': '₦280B',
            'growth_rate': '+42.1%',
            'headquarters': lagos,
            'founded_year': '2016',
            'employees': '200',
            'website': 'https://piggyvest.com',
        },
        {
            'title': 'Cowrywise',
            'subtitle': 'Automated Wealth Management',
            'description': 'Digital wealth management platform offering automated savings and investment solutions.',
            'category': tech,
            'current_rank': 18,
            'brand_value': '₦250B',
            'growth_rate': '+38.9%',
            'headquarters': lagos,
            'founded_year': '2017',
            'employees': '150',
            'website': 'https://cowrywise.com',
        },
        {
            'title': 'Farmcrowdy',
            'subtitle': 'Digital Agriculture Platform',
            'description': 'Leading agtech platform connecting farmers with sponsors and providing agricultural solutions.',
            'category': tech,
            'current_rank': 19,
            'brand_value': '₦220B',
            'growth_rate': '+26.7%',
            'headquarters': lagos,
            'founded_year': '2016',
            'employees': '180',
            'website': 'https://farmcrowdy.com',
        },
    ]
    for brand_data in brands_data:
        # Use update_or_create to prevent duplicates and make the script idempotent
        brand, created = Brand.objects.update_or_create(
            title=brand_data['title'], 
            year=2025,
            defaults={
                'subtitle': brand_data['subtitle'],
                'description': brand_data['description'],
                'full_description': brand_data.get('full_description', brand_data['description']),
                'category': brand_data['category'],
                'current_rank': brand_data['current_rank'],
                'brand_value': brand_data['brand_value'],
                'growth_rate': brand_data['growth_rate'],
                'headquarters': brand_data['headquarters'],
                'founded_year': brand_data['founded_year'],
                'employees': brand_data['employees'],
                'website': brand_data['website'],
            }
        )
        if created:
            print(f"Created brand: {brand.title}")
        else:
            print(f"Updated brand: {brand.title}")

def create_blog_posts():
    """Create blog posts"""
    # Create blog categories
    categories_data = [
        {'name': 'Market Analysis', 'color': '#3B82F6'},
        {'name': 'Brand Spotlight', 'color': '#10B981'},
        {'name': 'Industry Trends', 'color': '#F59E0B'},
        {'name': 'Research Reports', 'color': '#8B5CF6'},
    ]
    
    for cat_data in categories_data:
        category, created = BlogCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'color': cat_data['color']}
        )
        if created:
            print(f"Created blog category: {category.name}")
    
    # Get user for author
    user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    
    # Create blog posts
    posts_data = [
        {
            'title': 'Nigeria\'s Top 10 Brands Show Resilient Growth in 2025',
            'excerpt': 'Despite economic challenges, Nigeria\'s leading brands demonstrate remarkable resilience and growth.',
            'content': 'Full analysis of how Nigeria\'s top brands are navigating the current economic landscape...',
            'category': BlogCategory.objects.get(name='Market Analysis'),
            'author': user,
            'year': 2025,
            'is_featured': True,
            'read_time': 8,
        },
        {
            'title': 'The Rise of Nigerian Fintech: Flutterwave\'s Success Story',
            'excerpt': 'How Flutterwave became one of Nigeria\'s most valuable tech companies.',
            'content': 'An in-depth look at Flutterwave\'s journey from startup to unicorn status...',
            'category': BlogCategory.objects.get(name='Brand Spotlight'),
            'author': user,
            'year': 2025,
            'is_featured': False,
            'read_time': 6,
        },
        {
            'title': 'Banking Sector Transformation: Digital Innovation Leads the Way',
            'excerpt': 'Nigerian banks are embracing digital transformation to stay competitive.',
            'content': 'Analysis of how traditional banks are adapting to the digital age...',
            'category': BlogCategory.objects.get(name='Industry Trends'),
            'author': user,
            'year': 2025,
            'is_featured': False,
            'read_time': 7,
        },
    ]
    
    for post_data in posts_data:
        post, created = BlogPost.objects.get_or_create(
            title=post_data['title'],
            defaults=post_data
        )
        if created:
            print(f"Created blog post: {post.title}")

def create_insights():
    """Create market insights"""
    # Use existing categories for insights
    market_research = Category.objects.filter(name__icontains='Banking').first()
    consumer_behavior = Category.objects.filter(name__icontains='Telecommunications').first()
    brand_performance = Category.objects.filter(name__icontains='Technology').first()
    
    # Get user for author
    user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    
    # Create insights
    insights_data = [
        {
            'title': '2025 Nigerian Brand Valuation Report',
            'description': 'Comprehensive analysis of brand values across Nigerian markets.',
            'content': 'Detailed methodology and findings from our annual brand valuation study...',
            'insight_type': 'market_analysis',
            'category': market_research,
            'author': user,
            'year': 2025,
            'is_premium': False,
            'data_points': '150',
        },
        {
            'title': 'Consumer Trust Index: Banking Sector Analysis',
            'description': 'How Nigerian consumers perceive and trust different banking brands.',
            'content': 'Survey results and analysis of consumer trust in banking institutions...',
            'insight_type': 'consumer_behavior',
            'category': consumer_behavior,
            'author': user,
            'year': 2025,
            'is_premium': True,
            'data_points': '89',
        },
        {
            'title': 'Telecom Brand Performance Metrics Q1 2025',
            'description': 'Quarterly performance analysis of major telecom brands.',
            'content': 'Performance metrics and market share analysis for telecom sector...',
            'insight_type': 'brand_performance',
            'category': brand_performance,
            'author': user,
            'year': 2025,
            'is_premium': False,
            'data_points': '67',
        },
    ]
    
    for insight_data in insights_data:
        insight, created = Insight.objects.get_or_create(
            title=insight_data['title'],
            defaults=insight_data
        )
        if created:
            print(f"Created insight: {insight.title}")

def main():
    """Main function to populate all data"""
    print("Starting comprehensive data population...")
    
    try:
        create_categories()
        create_industries()
        create_locations()
        create_comprehensive_brands()
        create_blog_posts()
        create_insights()
        
        print("\n✅ Comprehensive data population completed successfully!")
        print(f"📊 Brands: {Brand.objects.count()}")
        print(f"📝 Blog Posts: {BlogPost.objects.count()}")
        print(f"🔍 Insights: {Insight.objects.count()}")
        print(f"🏷️ Categories: {Category.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error during data population: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
