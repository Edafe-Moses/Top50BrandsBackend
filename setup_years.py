#!/usr/bin/env python
"""
Script to set up initial year data and create the 2025 ranking.
Run this after running migrations.

Usage: python setup_years.py
"""

import os
import sys
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from dashboard.models import YearlyRanking, SystemConfiguration, DashboardUser
from django.contrib.auth.models import User


def create_yearly_rankings():
    """Create yearly ranking entries."""
    
    # Create 2025 ranking (current active year)
    ranking_2025, created = YearlyRanking.objects.get_or_create(
        year=2025,
        defaults={
            'title': 'Top 50 Most Valuable Brands in Nigeria 2025',
            'description': 'The definitive ranking of Nigeria\'s most valuable and influential brands for 2025, based on comprehensive market research and brand valuation.',
            'is_active': True,
            'is_published': True,
            'is_complete': False,
            'total_brands': 50,
            'research_methodology': 'Our methodology combines financial performance, brand recognition, market share, customer loyalty, and digital presence to create a comprehensive brand valuation.',
            'data_collection_start': date(2024, 10, 1),
            'data_collection_end': date(2025, 3, 31),
            'publication_date': date(2025, 6, 1),
        }
    )
    
    if created:
        print(f"Created 2025 ranking: {ranking_2025.title}")
    else:
        print(f"2025 ranking already exists: {ranking_2025.title}")
    
    # Create 2024 ranking (previous year for comparison)
    ranking_2024, created = YearlyRanking.objects.get_or_create(
        year=2024,
        defaults={
            'title': 'Top 50 Most Valuable Brands in Nigeria 2024',
            'description': 'The 2024 edition of Nigeria\'s most comprehensive brand ranking.',
            'is_active': False,
            'is_published': True,
            'is_complete': True,
            'total_brands': 50,
            'research_methodology': 'Comprehensive brand valuation methodology covering financial metrics, market presence, and brand equity.',
            'data_collection_start': date(2023, 10, 1),
            'data_collection_end': date(2024, 3, 31),
            'publication_date': date(2024, 6, 1),
        }
    )
    
    if created:
        print(f"Created 2024 ranking: {ranking_2024.title}")
    else:
        print(f"2024 ranking already exists: {ranking_2024.title}")
    
    # Create 2023 ranking (historical data)
    ranking_2023, created = YearlyRanking.objects.get_or_create(
        year=2023,
        defaults={
            'title': 'Top 50 Most Valuable Brands in Nigeria 2023',
            'description': 'The 2023 edition showcasing Nigeria\'s brand landscape.',
            'is_active': False,
            'is_published': True,
            'is_complete': True,
            'total_brands': 50,
            'research_methodology': 'Multi-factor brand valuation approach.',
            'data_collection_start': date(2022, 10, 1),
            'data_collection_end': date(2023, 3, 31),
            'publication_date': date(2023, 6, 1),
        }
    )
    
    if created:
        print(f"Created 2023 ranking: {ranking_2023.title}")
    else:
        print(f"2023 ranking already exists: {ranking_2023.title}")


def create_system_configurations():
    """Create initial system configurations."""
    
    configs = [
        {
            'key': 'current_year',
            'value': '2025',
            'description': 'Current active ranking year',
            'is_public': True,
            'requires_admin': True,
        },
        {
            'key': 'site_title',
            'value': 'Top 50 Brands Nigeria',
            'description': 'Main site title',
            'is_public': True,
            'requires_admin': False,
        },
        {
            'key': 'site_description',
            'value': 'Nigeria\'s most comprehensive ranking of valuable and influential brands',
            'description': 'Site description for SEO',
            'is_public': True,
            'requires_admin': False,
        },
        {
            'key': 'default_redirect_year',
            'value': '2025',
            'description': 'Default year to redirect to when accessing home page',
            'is_public': True,
            'requires_admin': True,
        },
        {
            'key': 'enable_year_switching',
            'value': 'true',
            'description': 'Allow users to switch between different years',
            'is_public': True,
            'requires_admin': False,
        },
        {
            'key': 'show_historical_data',
            'value': 'true',
            'description': 'Show historical data and comparisons',
            'is_public': True,
            'requires_admin': False,
        },
        {
            'key': 'api_version',
            'value': 'v1',
            'description': 'Current API version',
            'is_public': True,
            'requires_admin': True,
        },
        {
            'key': 'maintenance_mode',
            'value': 'false',
            'description': 'Enable maintenance mode',
            'is_public': False,
            'requires_admin': True,
        },
    ]
    
    for config_data in configs:
        config, created = SystemConfiguration.objects.get_or_create(
            key=config_data['key'],
            defaults=config_data
        )
        if created:
            print(f"Created configuration: {config.key}")
        else:
            print(f"Configuration already exists: {config.key}")


def setup_admin_user():
    """Set up dashboard profile for existing admin user."""
    try:
        admin_user = User.objects.get(username='user')  # The superuser we created
        
        dashboard_profile, created = DashboardUser.objects.get_or_create(
            user=admin_user,
            defaults={
                'role': 'admin',
                'can_create_years': True,
                'can_edit_brands': True,
                'can_publish_content': True,
                'can_manage_users': True,
            }
        )
        
        if created:
            # Assign all years to admin
            dashboard_profile.assigned_years.set(YearlyRanking.objects.all())
            print(f"Created dashboard profile for admin user: {admin_user.username}")
        else:
            print(f"Dashboard profile already exists for: {admin_user.username}")
            
    except User.DoesNotExist:
        print("Admin user not found. Please create a superuser first.")


def main():
    """Main function to set up all initial data."""
    print("Setting up initial year data...")
    
    create_yearly_rankings()
    create_system_configurations()
    setup_admin_user()
    
    print("\nYear setup completed successfully!")
    print("\nAvailable years:")
    for ranking in YearlyRanking.objects.all():
        status = "ACTIVE" if ranking.is_active else "INACTIVE"
        print(f"  - {ranking.year}: {ranking.title} ({status})")
    
    print(f"\nCurrent active year: {YearlyRanking.objects.get(is_active=True).year}")
    print("Dashboard is ready for use!")


if __name__ == '__main__':
    main()
