#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from blog.models import BlogPost

def create_events():
    """Create event blog posts for the Memorable Events section"""
    print("=== CREATING EVENTS ===")
    
    events_data = [
        {
            'title': 'Nigeria Brand Awards 2024',
            'excerpt': 'Annual celebration of the most outstanding Nigerian brands across various industries.',
            'content': 'The Nigeria Brand Awards 2024 brought together industry leaders, innovators, and visionaries to celebrate excellence in branding and business innovation.',
            'is_featured': True,
            'category_name': 'Events'
        },
        {
            'title': 'Lagos Business Summit 2024',
            'excerpt': 'Premier business networking event bringing together top Nigerian entrepreneurs and executives.',
            'content': 'The Lagos Business Summit 2024 featured keynote speeches from leading CEOs and panel discussions on the future of Nigerian business.',
            'is_featured': True,
            'category_name': 'Events'
        },
        {
            'title': 'Fintech Innovation Conference',
            'excerpt': 'Exploring the future of financial technology in Nigeria and across Africa.',
            'content': 'This groundbreaking conference showcased the latest innovations in Nigerian fintech, featuring presentations from Flutterwave, Paystack, and other industry leaders.',
            'is_featured': True,
            'category_name': 'Events'
        },
        {
            'title': 'Brand Nigeria Expo 2024',
            'excerpt': 'Showcasing the best of Nigerian products and services to the world.',
            'content': 'Brand Nigeria Expo 2024 highlighted the excellence and innovation of Nigerian brands, attracting international attention and investment.',
            'is_featured': True,
            'category_name': 'Events'
        }
    ]
    
    # First, let's mark existing blog posts as not featured to make room for events
    BlogPost.objects.filter(is_featured=True).update(is_featured=False)
    
    from core.models import Category
    from django.contrib.auth.models import User
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Create Events category if it doesn't exist
    events_category, created = Category.objects.get_or_create(
        name='Events',
        defaults={
            'slug': 'events',
            'description': 'Company events and industry gatherings',
            'color': '#10B981'
        }
    )
    
    for i, event_data in enumerate(events_data, 1):
        # Create or update the event blog post
        blog_post, created = BlogPost.objects.update_or_create(
            title=event_data['title'],
            defaults={
                'excerpt': event_data['excerpt'],
                'content': event_data['content'],
                'category': events_category,
                'is_featured': True,
                'is_published': True,
                'status': 'published',
                'author': admin_user,
                'read_time': 5
            }
        )
        
        print(f"{'✅ Created' if created else '✅ Updated'} event: {event_data['title']}")
        print(f"   Expected image: /events/event-{blog_post.id}.png")

def create_activities():
    """Create activity blog posts for the Past Activities section"""
    print("\n=== CREATING ACTIVITIES ===")
    
    activities_data = [
        {
            'title': 'Digital Transformation Workshop',
            'excerpt': 'Helping Nigerian businesses embrace digital technologies for growth and efficiency.',
            'content': 'Our digital transformation workshop provided practical insights and tools for businesses looking to modernize their operations.',
            'category_name': 'Activities'
        },
        {
            'title': 'Brand Strategy Masterclass',
            'excerpt': 'Comprehensive training on building strong brand identity and market positioning.',
            'content': 'This masterclass covered essential brand strategy concepts, from brand positioning to customer engagement strategies.',
            'category_name': 'Activities'
        },
        {
            'title': 'Startup Mentorship Program',
            'excerpt': 'Connecting emerging Nigerian startups with experienced business leaders and mentors.',
            'content': 'Our mentorship program has helped over 50 Nigerian startups develop their business strategies and secure funding.',
            'category_name': 'Activities'
        },
        {
            'title': 'Corporate Social Responsibility Summit',
            'excerpt': 'Exploring how Nigerian brands can make positive impact in their communities.',
            'content': 'This summit brought together CSR leaders to discuss best practices and innovative approaches to community engagement.',
            'category_name': 'Activities'
        },
        {
            'title': 'Innovation Challenge 2024',
            'excerpt': 'Annual competition showcasing innovative solutions from Nigerian entrepreneurs.',
            'content': 'The Innovation Challenge 2024 featured groundbreaking solutions in fintech, healthtech, and agritech from Nigerian innovators.',
            'category_name': 'Activities'
        },
        {
            'title': 'Leadership Development Program',
            'excerpt': 'Developing the next generation of Nigerian business leaders through comprehensive training.',
            'content': 'Our leadership program focuses on developing strategic thinking, emotional intelligence, and effective communication skills.',
            'category_name': 'Activities'
        }
    ]
    
    from core.models import Category
    from django.contrib.auth.models import User
    
    # Get admin user
    admin_user = User.objects.get(username='admin')
    
    # Create Activities category if it doesn't exist
    activities_category, created = Category.objects.get_or_create(
        name='Activities',
        defaults={
            'slug': 'activities',
            'description': 'Company activities and programs',
            'color': '#8B5CF6'
        }
    )
    
    for i, activity_data in enumerate(activities_data, 1):
        # Create or update the activity blog post
        blog_post, created = BlogPost.objects.update_or_create(
            title=activity_data['title'],
            defaults={
                'excerpt': activity_data['excerpt'],
                'content': activity_data['content'],
                'category': activities_category,
                'is_featured': False,  # Activities are not featured, they're recent
                'is_published': True,
                'status': 'published',
                'author': admin_user,
                'read_time': 4
            }
        )
        
        print(f"{'✅ Created' if created else '✅ Updated'} activity: {activity_data['title']}")
        print(f"   Expected image: /activities/activity-{blog_post.id}.png")

if __name__ == "__main__":
    create_events()
    create_activities()
    
    print(f"\n=== SUMMARY ===")
    print(f"Featured blog posts (Events): {BlogPost.objects.filter(is_featured=True).count()}")
    print(f"Recent blog posts (Activities): {BlogPost.objects.filter(is_featured=False, is_published=True).count()}")