#!/bin/bash

# Django Backend Setup Script for Top 50 Brands Nigeria
echo "🚀 Setting up Django Backend for Top 50 Brands Nigeria..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment (Linux/Mac)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
# Activate virtual environment (Windows)
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
fi

# Install Django and create project
echo "🔧 Installing Django..."
pip install Django==5.0.1

# Create Django project
echo "🏗️ Creating Django project..."
django-admin startproject top50brands .

# Navigate to project directory
cd top50brands

# Create Django apps
echo "📱 Creating Django apps..."

# Core app - for shared utilities and base models
python manage.py startapp core

# Brands app - for managing brand data, rankings, and profiles
python manage.py startapp brands

# Blog app - for blog posts and articles
python manage.py startapp blog

# Insights app - for brand insights and analytics reports
python manage.py startapp insights

# Rankings app - for managing different ranking categories
python manage.py startapp rankings

# Analytics app - for tracking and analytics
python manage.py startapp analytics

# Users app - for user management and authentication
python manage.py startapp users

# API app - for API endpoints and serializers
python manage.py startapp api

echo "✅ Django apps created successfully!"

# Install additional packages
echo "📦 Installing additional packages..."
pip install djangorestframework==3.14.0
pip install django-cors-headers==4.3.1
pip install django-filter==23.5
pip install Pillow==10.2.0
pip install python-decouple==3.8
pip install django-ckeditor==6.7.0
pip install django-taggit==5.0.1
pip install django-mptt==0.16.0
pip install django-extensions==3.2.3
pip install factory-boy==3.3.0
pip install pytest-django==4.8.0

# Create requirements.txt
echo "📝 Creating requirements.txt..."
pip freeze > requirements.txt

# Create directories
echo "📁 Creating project directories..."
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p media/brands
mkdir -p media/blog
mkdir -p media/insights
mkdir -p templates
mkdir -p logs

# Create initial migration
echo "🗄️ Creating initial migrations..."
python manage.py makemigrations

# Apply migrations
echo "⚡ Applying migrations..."
python manage.py migrate

# Create superuser (optional - will prompt for input)
echo "👤 Creating superuser..."
echo "You can create a superuser now or skip and do it later with: python manage.py createsuperuser"
read -p "Create superuser now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

echo "🎉 Django backend setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
echo "2. Navigate to project: cd top50brands"
echo "3. Run development server: python manage.py runserver"
echo "4. Access admin panel: http://127.0.0.1:8000/admin/"
echo "5. Access API: http://127.0.0.1:8000/api/"
