import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'top50brands.settings')
django.setup()

from django.apps import apps

print("Listing all registered models:")
all_models = apps.get_models()

for model in all_models:
    print(f"App: {model._meta.app_label}, Model: {model.__name__}")
