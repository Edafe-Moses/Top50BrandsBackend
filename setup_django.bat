@echo off
REM Django Backend Setup Script for Top 50 Brands Nigeria (Windows)
echo 🚀 Setting up Django Backend for Top 50 Brands Nigeria...

REM Navigate to backend directory
cd backend

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate

REM Install Django and create project
echo 🔧 Installing Django...
pip install Django==5.0.1

REM Create Django project in current directory
echo 🏗️ Creating Django project...
django-admin startproject top50brands .

REM Create Django apps
echo 📱 Creating Django apps...

REM Core app - for shared utilities and base models
python manage.py startapp core

REM Brands app - for managing brand data, rankings, and profiles
python manage.py startapp brands

REM Blog app - for blog posts and articles
python manage.py startapp blog

REM Insights app - for brand insights and analytics reports
python manage.py startapp insights

REM Rankings app - for managing different ranking categories
python manage.py startapp rankings

REM Analytics app - for tracking and analytics
python manage.py startapp analytics

REM Users app - for user management and authentication
python manage.py startapp users

REM API app - for API endpoints and serializers
python manage.py startapp api

echo ✅ Django apps created successfully!

REM Install additional packages
echo 📦 Installing additional packages...
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

REM Create requirements.txt
echo 📝 Creating requirements.txt...
pip freeze > requirements.txt

REM Create directories
echo 📁 Creating project directories...
mkdir static\css
mkdir static\js
mkdir static\images
mkdir media\brands
mkdir media\blog
mkdir media\insights
mkdir templates
mkdir logs

REM Create initial migration
echo 🗄️ Creating initial migrations...
python manage.py makemigrations

REM Apply migrations
echo ⚡ Applying migrations...
python manage.py migrate

REM Create superuser prompt
echo 👤 You can create a superuser with: python manage.py createsuperuser

echo 🎉 Django backend setup complete!
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate
echo 2. Navigate to project: cd top50brands
echo 3. Run development server: python manage.py runserver
echo 4. Access admin panel: http://127.0.0.1:8000/admin/
echo 5. Access API: http://127.0.0.1:8000/api/

pause
