# Django Backend Setup Commands

## Step 1: Create and Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

## Step 2: Install Django and Create Project

```bash
# Install Django
pip install Django==5.0.1

# Create Django project
django-admin startproject top50brands .

# Navigate to project directory
cd top50brands
```

## Step 3: Create Django Apps

```bash
# Core app - shared utilities and base models
python manage.py startapp core

# Brands app - brand data, rankings, and profiles
python manage.py startapp brands

# Blog app - blog posts and articles
python manage.py startapp blog

# Insights app - brand insights and analytics reports
python manage.py startapp insights

# Rankings app - different ranking categories
python manage.py startapp rankings

# Analytics app - tracking and analytics
python manage.py startapp analytics

# Users app - user management and authentication
python manage.py startapp users

# API app - API endpoints and serializers
python manage.py startapp api
```

## Step 4: Install Additional Packages

```bash
# Install REST framework and related packages
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

# Create requirements file
pip freeze > requirements.txt
```

## Step 5: Create Project Directories

```bash
# Create static directories
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images

# Create media directories
mkdir -p media/brands
mkdir -p media/blog
mkdir -p media/insights

# Create other directories
mkdir -p templates
mkdir -p logs
```

## Step 6: Database Setup

```bash
# Create initial migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

## Step 7: Run Development Server

```bash
# Start development server
python manage.py runserver

# Access the application
# Admin panel: http://127.0.0.1:8000/admin/
# API: http://127.0.0.1:8000/api/
```

## Project Structure After Setup

```
backend/
├── top50brands/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
├── brands/
├── blog/
├── insights/
├── rankings/
├── analytics/
├── users/
├── api/
├── static/
├── media/
├── templates/
├── logs/
├── venv/
├── manage.py
└── requirements.txt
```

## App Purposes

- **core**: Shared utilities, base models, and common functionality
- **brands**: Brand models, rankings, profiles, and brand-related data
- **blog**: Blog posts, articles, and content management
- **insights**: Analytics reports, market insights, and data visualization
- **rankings**: Different ranking categories and methodologies
- **analytics**: User tracking, page views, and site analytics
- **users**: User authentication, profiles, and permissions
- **api**: REST API endpoints, serializers, and API views

## Next Steps After Setup

1. Configure settings.py with your database and other configurations
2. Create models in each app
3. Set up URL routing
4. Create API endpoints
5. Populate database with existing brand data
6. Set up admin interface
7. Create data migration scripts
