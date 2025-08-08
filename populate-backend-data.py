#!/usr/bin/env python3
"""
Script to populate the Django backend with missing data for the frontend components.
This script will only add data that doesn't already exist in the database.
"""

import os
import sys
import django
import requests
from datetime import datetime

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(backend_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Now import Django models
from api.models import *

def populate_brand_header_cards():
    """Populate brand header cards if they don't exist"""
    print("🔄 Populating brand header cards...")
    
    cards_data = [
        {'title': 'Dangote Group', 'image': '/brands/dangote.png'},
        {'title': 'GTBank', 'image': '/brands/gtbank.png'},
        {'title': 'MTN Nigeria', 'image': '/brands/mtn.png'},
        {'title': 'Jumia', 'image': '/brands/jumia.png'},
        {'title': 'Flutterwave', 'image': '/brands/flutterwave.png'},
    ]
    
    # Check if we have a BrandHeaderCard model or similar
    # This is a placeholder - adjust based on actual model structure
    try:
        # Example: BrandHeaderCard.objects.get_or_create(...)
        print("✅ Brand header cards populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate brand header cards: {e}")

def populate_top10_brands():
    """Populate top 10 brands to watch if they don't exist"""
    print("🔄 Populating top 10 brands...")
    
    brands_data = [
        {
            'title': 'Paystack',
            'description': 'Leading payment processing platform revolutionizing online transactions in Nigeria.',
            'image': '/brands/paystack.png'
        },
        {
            'title': 'Konga',
            'description': 'Major e-commerce platform competing with international giants in the Nigerian market.',
            'image': '/brands/konga.png'
        },
        {
            'title': 'Interswitch',
            'description': 'Pioneer in digital payment solutions and financial technology infrastructure.',
            'image': '/brands/interswitch.png'
        },
        {
            'title': 'Andela',
            'description': 'Global technology talent accelerator training world-class software developers.',
            'image': '/brands/andela.png'
        },
        {
            'title': 'Cowrywise',
            'description': 'Digital savings and investment platform making wealth building accessible to all.',
            'image': '/brands/cowrywise.png'
        },
        {
            'title': 'Piggyvest',
            'description': 'Popular savings and investment app helping Nigerians achieve their financial goals.',
            'image': '/brands/piggyvest.png'
        },
        {
            'title': 'Opay',
            'description': 'Super app providing mobile payment, ride-hailing, and food delivery services.',
            'image': '/brands/opay.png'
        },
        {
            'title': 'Farmcrowdy',
            'description': 'Agricultural technology platform connecting farmers with investors and resources.',
            'image': '/brands/farmcrowdy.png'
        }
    ]
    
    try:
        # Example: Top10Brand.objects.get_or_create(...)
        print("✅ Top 10 brands populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate top 10 brands: {e}")

def populate_features():
    """Populate new features if they don't exist"""
    print("🔄 Populating new features...")
    
    features_data = [
        {'image': '/features/feature-1.png'},
        {'image': '/features/feature-2.png'},
        {'image': '/features/feature-3.png'},
        {'image': '/features/feature-4.png'},
    ]
    
    try:
        # Example: Feature.objects.get_or_create(...)
        print("✅ New features populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate new features: {e}")

def populate_events():
    """Populate past events if they don't exist"""
    print("🔄 Populating past events...")
    
    events_data = [
        {
            'title': 'Nigeria Brand Awards 2024',
            'description': 'Annual celebration of the most outstanding Nigerian brands across various industries.',
            'image': '/events/event-1.png'
        },
        {
            'title': 'Lagos Business Summit',
            'description': 'Premier business networking event bringing together top Nigerian entrepreneurs and executives.',
            'image': '/events/event-2.png'
        },
        {
            'title': 'Fintech Innovation Conference',
            'description': 'Exploring the future of financial technology in Nigeria and across Africa.',
            'image': '/events/event-3.png'
        },
        {
            'title': 'Brand Nigeria Expo',
            'description': 'Showcasing the best of Nigerian products and services to the world.',
            'image': '/events/event-4.png'
        }
    ]
    
    try:
        # Example: Event.objects.get_or_create(...)
        print("✅ Past events populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate past events: {e}")

def populate_activities():
    """Populate past activities if they don't exist"""
    print("🔄 Populating past activities...")
    
    activities_data = [
        {'image': '/activities/activity-1.png'},
        {'image': '/activities/activity-2.png'},
        {'image': '/activities/activity-3.png'},
        {'image': '/activities/activity-4.png'},
        {'image': '/activities/activity-5.png'},
        {'image': '/activities/activity-6.png'},
    ]
    
    try:
        # Example: Activity.objects.get_or_create(...)
        print("✅ Past activities populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate past activities: {e}")

def populate_insights():
    """Populate brand insights if they don't exist"""
    print("🔄 Populating brand insights...")
    
    insights_data = [
        {
            'title': 'Market Share Analysis',
            'description': 'Comprehensive analysis of market share distribution across Nigerian industries and key performance indicators.',
            'icon': 'PieChart',
            'metrics': {
                'total_brands': '250+',
                'market_coverage': '85%',
                'growth_rate': '+12.5%',
                'active_sectors': '15'
            }
        },
        {
            'title': 'Brand Performance Trends',
            'description': 'Real-time tracking of brand performance metrics including customer satisfaction, market penetration, and revenue growth.',
            'icon': 'TrendingUp',
            'metrics': {
                'avg_growth': '+8.3%',
                'top_performers': '25',
                'satisfaction_score': '4.2/5',
                'retention_rate': '78%'
            }
        },
        {
            'title': 'Consumer Behavior Insights',
            'description': 'Deep dive into Nigerian consumer preferences, purchasing patterns, and brand loyalty across different demographics.',
            'icon': 'Users',
            'metrics': {
                'survey_responses': '50K+',
                'age_groups': '6',
                'loyalty_index': '72%',
                'digital_adoption': '65%'
            }
        },
        {
            'title': 'Industry Benchmarking',
            'description': 'Comparative analysis of brand performance against industry standards and international benchmarks.',
            'icon': 'BarChart3',
            'metrics': {
                'benchmark_score': '7.8/10',
                'industry_rank': 'Top 3',
                'global_comparison': '+15%',
                'improvement_areas': '4'
            }
        },
        {
            'title': 'Digital Transformation Index',
            'description': 'Measuring how Nigerian brands are adapting to digital technologies and online customer engagement.',
            'icon': 'LineChart',
            'metrics': {
                'digital_maturity': '68%',
                'online_presence': '82%',
                'social_engagement': '+25%',
                'mobile_optimization': '74%'
            }
        },
        {
            'title': 'Brand Value Assessment',
            'description': 'Comprehensive evaluation of brand equity, financial performance, and market positioning strategies.',
            'icon': 'Target',
            'metrics': {
                'total_value': '₦2.5T',
                'avg_valuation': '₦10B',
                'value_growth': '+18%',
                'market_leaders': '12'
            }
        }
    ]
    
    try:
        # Example: Insight.objects.get_or_create(...)
        print("✅ Brand insights populated (placeholder)")
    except Exception as e:
        print(f"⚠️  Could not populate brand insights: {e}")

def check_django_backend():
    """Check if Django backend is running and accessible"""
    print("🔍 Checking Django backend...")
    
    try:
        # Try to make a request to the Django backend
        response = requests.get('http://localhost:8000/api/', timeout=5)
        if response.status_code == 200:
            print("✅ Django backend is running and accessible")
            return True
        else:
            print(f"⚠️  Django backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Django backend is not accessible: {e}")
        print("💡 Make sure to start the Django backend with: python manage.py runserver")
        return False

def main():
    """Main function to populate all missing data"""
    print("🚀 Starting backend data population...\n")
    
    # Check if Django backend is accessible
    backend_accessible = check_django_backend()
    
    if not backend_accessible:
        print("\n⚠️  Django backend is not accessible. Data will be prepared but not inserted.")
        print("   Start the Django backend and run this script again to insert data.")
    
    print("\n📊 Populating missing data...\n")
    
    # Populate all data types
    populate_brand_header_cards()
    populate_top10_brands()
    populate_features()
    populate_events()
    populate_activities()
    populate_insights()
    
    print("\n🎉 Data population completed!")
    print("\n📝 Note: This script contains placeholder implementations.")
    print("   Update the model imports and database operations based on your actual Django models.")
    print("\n💡 To make this script functional:")
    print("   1. Check your Django models in backend/api/models.py")
    print("   2. Update the import statements and model operations")
    print("   3. Run the script again to populate actual data")

if __name__ == "__main__":
    main()