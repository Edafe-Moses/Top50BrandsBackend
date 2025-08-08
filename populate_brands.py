#!/usr/bin/env python
"""
Script to populate the database with sample brand data.
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from brands.models import Brand, BrandMetric, BrandAchievement, BrandTimeline
from core.models import Category, Industry, Location
from dashboard.models import YearlyRanking

def create_sample_data():
    """Create sample brand data."""
    
    # Create or get YearlyRanking for 2025
    yearly_ranking, created = YearlyRanking.objects.get_or_create(
        year=2025,
        defaults={
            'title': 'Top 50 Nigerian Brands 2025',
            'is_active': True,
            'is_published': True,
            'is_complete': True,
            'total_brands': 50,
            'description': 'The definitive ranking of Nigeria\'s most valuable brands for 2025.'
        }
    )
    
    # Create categories
    categories_data = [
        {'name': 'Banking & Financial Services', 'slug': 'banking-financial', 'color': '#1e40af'},
        {'name': 'Telecommunications', 'slug': 'telecommunications', 'color': '#dc2626'},
        {'name': 'Oil & Gas', 'slug': 'oil-gas', 'color': '#059669'},
        {'name': 'Manufacturing', 'slug': 'manufacturing', 'color': '#7c3aed'},
        {'name': 'Consumer Goods', 'slug': 'consumer-goods', 'color': '#ea580c'},
    ]
    
    for cat_data in categories_data:
        Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'color': cat_data['color'],
                'is_active': True
            }
        )
    
    # Create industries
    industries_data = [
        {'name': 'Banking', 'slug': 'banking'},
        {'name': 'Telecommunications', 'slug': 'telecommunications'},
        {'name': 'Oil & Gas', 'slug': 'oil-gas'},
        {'name': 'Cement', 'slug': 'cement'},
        {'name': 'Beverages', 'slug': 'beverages'},
        {'name': 'Food Processing', 'slug': 'food-processing'},
    ]
    
    for ind_data in industries_data:
        Industry.objects.get_or_create(
            slug=ind_data['slug'],
            defaults={'name': ind_data['name']}
        )
    
    # Create locations
    locations_data = [
        {'name': 'Lagos', 'slug': 'lagos', 'state': 'Lagos State'},
        {'name': 'Abuja', 'slug': 'abuja', 'state': 'FCT'},
        {'name': 'Port Harcourt', 'slug': 'port-harcourt', 'state': 'Rivers State'},
        {'name': 'Kano', 'slug': 'kano', 'state': 'Kano State'},
    ]
    
    for loc_data in locations_data:
        Location.objects.get_or_create(
            slug=loc_data['slug'],
            defaults={
                'name': loc_data['name'],
                'state': loc_data['state'],
                'country': 'Nigeria'
            }
        )
    
    # Get created objects
    banking_cat = Category.objects.get(slug='banking-financial')
    telecom_cat = Category.objects.get(slug='telecommunications')
    oil_gas_cat = Category.objects.get(slug='oil-gas')
    manufacturing_cat = Category.objects.get(slug='manufacturing')
    consumer_cat = Category.objects.get(slug='consumer-goods')
    
    banking_ind = Industry.objects.get(slug='banking')
    telecom_ind = Industry.objects.get(slug='telecommunications')
    oil_gas_ind = Industry.objects.get(slug='oil-gas')
    cement_ind = Industry.objects.get(slug='cement')
    beverages_ind = Industry.objects.get(slug='beverages')
    
    lagos = Location.objects.get(slug='lagos')
    abuja = Location.objects.get(slug='abuja')
    
    # Create sample brands
    brands_data = [
        {
            'title': 'Dangote Group',
            'slug': 'dangote-group',
            'description': 'Africa\'s leading conglomerate with interests in cement, sugar, salt, flour, and oil refining.',
            'full_description': 'Dangote Group is Africa\'s largest conglomerate, founded by Aliko Dangote. The company has diversified interests spanning cement production, sugar refining, salt processing, flour milling, and oil refining. With operations across multiple African countries, Dangote Group is a major contributor to Nigeria\'s GDP and one of the continent\'s most valuable companies.',
            'current_rank': 1,
            'previous_rank': 1,
            'brand_value': '₦2.5T',
            'market_cap': '₦3.2T',
            'revenue': '₦4.1T',
            'growth_rate': '+15.2%',
            'founded_year': '1981',
            'ceo': 'Aliko Dangote',
            'employees': '30,000+',
            'category': manufacturing_cat,
            'industry': cement_ind,
            'headquarters': lagos,
            'brand_recognition': 95,
            'customer_rating': 4.8,
            'is_featured': True,
            'year': 2025,
            'is_published': True,
        },
        {
            'title': 'MTN Nigeria',
            'slug': 'mtn-nigeria',
            'description': 'Nigeria\'s largest telecommunications company providing mobile and digital services.',
            'full_description': 'MTN Nigeria is the country\'s largest mobile network operator, serving over 77 million subscribers. The company provides voice, data, digital services, and mobile money solutions. MTN has been at the forefront of Nigeria\'s digital transformation, investing heavily in 4G and 5G infrastructure.',
            'current_rank': 2,
            'previous_rank': 3,
            'brand_value': '₦1.8T',
            'market_cap': '₦2.1T',
            'revenue': '₦1.9T',
            'growth_rate': '+12.8%',
            'founded_year': '2001',
            'ceo': 'Karl Toriola',
            'employees': '3,000+',
            'category': telecom_cat,
            'industry': telecom_ind,
            'headquarters': lagos,
            'brand_recognition': 92,
            'customer_rating': 4.6,
            'is_featured': True,
            'year': 2025,
            'is_published': True,
        },
        {
            'title': 'Guaranty Trust Bank',
            'slug': 'guaranty-trust-bank',
            'description': 'Leading Nigerian bank providing innovative financial services and solutions.',
            'full_description': 'Guaranty Trust Bank (GTBank) is one of Nigeria\'s leading financial institutions, known for its innovative banking solutions and excellent customer service. The bank offers a wide range of financial services including retail banking, corporate banking, investment banking, and digital payment solutions.',
            'current_rank': 3,
            'previous_rank': 2,
            'brand_value': '₦1.2T',
            'market_cap': '₦1.5T',
            'revenue': '₦890B',
            'growth_rate': '+8.5%',
            'founded_year': '1990',
            'ceo': 'Segun Agbaje',
            'employees': '5,000+',
            'category': banking_cat,
            'industry': banking_ind,
            'headquarters': lagos,
            'brand_recognition': 88,
            'customer_rating': 4.7,
            'is_featured': True,
            'year': 2025,
            'is_published': True,
        },
        {
            'title': 'Nigerian Breweries',
            'slug': 'nigerian-breweries',
            'description': 'Nigeria\'s largest brewing company with a portfolio of premium beer brands.',
            'full_description': 'Nigerian Breweries Plc is the largest brewing company in Nigeria and one of the largest in Africa. The company produces and markets a wide range of high-quality beer, stout, and non-alcoholic beverages. With brands like Star, Gulder, Heineken, and Legend, Nigerian Breweries has been a household name for decades.',
            'current_rank': 4,
            'previous_rank': 4,
            'brand_value': '₦980B',
            'market_cap': '₦1.1T',
            'revenue': '₦650B',
            'growth_rate': '+6.2%',
            'founded_year': '1946',
            'ceo': 'Hans Essaadi',
            'employees': '2,500+',
            'category': consumer_cat,
            'industry': beverages_ind,
            'headquarters': lagos,
            'brand_recognition': 85,
            'customer_rating': 4.5,
            'is_featured': False,
            'year': 2025,
            'is_published': True,
        },
        {
            'title': 'Zenith Bank',
            'slug': 'zenith-bank',
            'description': 'Premier Nigerian bank known for excellence in retail and corporate banking.',
            'full_description': 'Zenith Bank Plc is one of Nigeria\'s largest financial services providers, offering a comprehensive range of banking and financial services to corporate and individual customers. The bank is known for its strong financial performance, innovative products, and excellent customer service.',
            'current_rank': 5,
            'previous_rank': 5,
            'brand_value': '₦850B',
            'market_cap': '₦1.0T',
            'revenue': '₦720B',
            'growth_rate': '+9.1%',
            'founded_year': '1990',
            'ceo': 'Ebenezer Onyeagwu',
            'employees': '4,500+',
            'category': banking_cat,
            'industry': banking_ind,
            'headquarters': lagos,
            'brand_recognition': 87,
            'customer_rating': 4.6,
            'is_featured': False,
            'year': 2025,
            'is_published': True,
        }
    ]
    
    created_brands = []
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            slug=brand_data['slug'],
            year=brand_data['year'],
            defaults=brand_data
        )
        created_brands.append(brand)
        
        if created:
            print(f"Created brand: {brand.title}")
            
            # Add sample metrics
            metrics_data = [
                {'label': 'Total Assets', 'value': brand_data['market_cap'], 'change': '+12%', 'trend': 'up'},
                {'label': 'Annual Revenue', 'value': brand_data['revenue'], 'change': brand_data['growth_rate'], 'trend': 'up'},
                {'label': 'Market Share', 'value': '15.2%', 'change': '+2.1%', 'trend': 'up'},
                {'label': 'Employee Count', 'value': brand_data['employees'], 'change': '+8%', 'trend': 'up'},
            ]
            
            for i, metric_data in enumerate(metrics_data):
                BrandMetric.objects.create(
                    brand=brand,
                    order=i,
                    **metric_data
                )
            
            # Add sample achievements
            achievements_data = [
                {
                    'title': 'Best Nigerian Brand 2024',
                    'description': 'Recognized as the most valuable Nigerian brand',
                    'year': '2024',
                    'organization': 'Brand Finance Nigeria',
                    'order': 0
                },
                {
                    'title': 'Excellence in Corporate Governance',
                    'description': 'Award for outstanding corporate governance practices',
                    'year': '2023',
                    'organization': 'Nigerian Stock Exchange',
                    'order': 1
                }
            ]
            
            for achievement_data in achievements_data:
                BrandAchievement.objects.create(
                    brand=brand,
                    **achievement_data
                )
            
            # Add sample timeline
            timeline_data = [
                {
                    'year': brand_data['founded_year'],
                    'event': 'Company Founded',
                    'description': f'{brand.title} was established',
                    'order': 0
                },
                {
                    'year': '2020',
                    'event': 'Digital Transformation',
                    'description': 'Launched comprehensive digital transformation initiative',
                    'order': 1
                },
                {
                    'year': '2024',
                    'event': 'Market Leadership',
                    'description': 'Achieved market leadership position in key segments',
                    'order': 2
                }
            ]
            
            for timeline_item in timeline_data:
                BrandTimeline.objects.create(
                    brand=brand,
                    **timeline_item
                )
        else:
            print(f"Brand already exists: {brand.title}")
    
    print(f"\nCreated {len(created_brands)} brands successfully!")
    print("Sample data population completed.")

if __name__ == '__main__':
    create_sample_data()