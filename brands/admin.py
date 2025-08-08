from django.contrib import admin
from .models import (
    Brand, BrandMetric, BrandAchievement, BrandTimeline, 
    BrandRanking, BrandCategory, BrandStats
)


class BrandMetricInline(admin.TabularInline):
    model = BrandMetric
    extra = 1


class BrandAchievementInline(admin.TabularInline):
    model = BrandAchievement
    extra = 1


class BrandTimelineInline(admin.TabularInline):
    model = BrandTimeline
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['current_rank', 'title', 'category', 'brand_value', 'growth_rate', 'is_featured', 'is_published']
    list_filter = ['category', 'industry', 'is_featured', 'is_new_entry', 'is_published']
    search_fields = ['title', 'subtitle', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['current_rank']
    inlines = [BrandMetricInline, BrandAchievementInline, BrandTimelineInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'slug', 'description', 'full_description')
        }),
        ('Media', {
            'fields': ('logo', 'image', 'banner_image')
        }),
        ('Ranking', {
            'fields': ('current_rank', 'previous_rank', 'brand_value', 'market_cap', 'revenue', 'growth_rate')
        }),
        ('Company Details', {
            'fields': ('founded_year', 'ceo', 'employees', 'headquarters', 'category', 'industry')
        }),
        ('Metrics', {
            'fields': ('brand_recognition', 'customer_rating')
        }),
        ('Social Media', {
            'fields': ('website', 'twitter', 'facebook', 'instagram', 'linkedin', 'youtube')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_new_entry', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        })
    )


@admin.register(BrandCategory)
class BrandCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


admin.register(BrandRanking)
admin.register(BrandStats)
