#!/usr/bin/env python
"""
Create a superuser for dashboard access
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create a superuser if it doesn't exist"""
    username = 'admin'
    email = 'admin@top50brands.ng'
    password = 'admin123'  # Change this in production!
    
    if User.objects.filter(username=username).exists():
        print(f"✅ Superuser '{username}' already exists")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        print(f"✅ Created superuser '{username}' with password '{password}'")
    
    print(f"📧 Email: {user.email}")
    print(f"👤 Name: {user.first_name} {user.last_name}")
    print(f"🔑 Staff: {user.is_staff}")
    print(f"🔑 Superuser: {user.is_superuser}")
    print(f"\n🚀 You can now login to the dashboard at: http://localhost:3000/dashboard/login")
    print(f"   Username: {username}")
    print(f"   Password: {password}")

if __name__ == '__main__':
    create_superuser()
