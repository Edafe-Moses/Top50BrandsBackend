from django.contrib import admin
from .models import Category, Tag, Industry, Location, MediaFile, SiteConfiguration


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'is_active']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'state', 'city']
    list_filter = ['country', 'state']


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'file_size', 'uploaded_by', 'created_at']
    list_filter = ['media_type', 'created_at']
    readonly_fields = ['file_size', 'width', 'height']


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_active']
    list_filter = ['is_active']
