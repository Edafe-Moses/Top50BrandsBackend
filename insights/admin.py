from django.contrib import admin
from .models import Insight, InsightMetric, InsightKeyFinding, MarketData, ResearchMethodology, InsightDownload


@admin.register(InsightMetric)
class InsightMetricAdmin(admin.ModelAdmin):
    list_display = ['insight', 'label', 'value', 'trend']
    list_filter = ['trend']

@admin.register(InsightKeyFinding)
class InsightKeyFindingAdmin(admin.ModelAdmin):
    list_display = ['insight', 'finding', 'impact_level']
    search_fields = ['finding', 'description']




from .models import (
    Insight, InsightMetric, InsightKeyFinding, MarketData, 
    ResearchMethodology, InsightDownload
)


class InsightMetricInline(admin.TabularInline):
    model = InsightMetric
    extra = 1


class InsightKeyFindingInline(admin.TabularInline):
    model = InsightKeyFinding
    extra = 1


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'insight_type', 'category', 'author', 'is_premium', 'is_featured', 'published_at']
    list_filter = ['insight_type', 'category', 'is_premium', 'is_featured', 'author']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at']
    inlines = [InsightMetricInline, InsightKeyFindingInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'content')
        }),
        ('Classification', {
            'fields': ('insight_type', 'category', 'author', 'research_team')
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_alt', 'report_file')
        }),
        ('Metrics', {
            'fields': ('data_points', 'accuracy', 'sample_size', 'regions_covered')
        }),
        ('Status', {
            'fields': ('is_premium', 'is_featured', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        })
    )


@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ['title', 'data_type', 'value', 'period', 'country', 'is_verified']
    list_filter = ['data_type', 'country', 'is_verified', 'confidence_level']
    search_fields = ['title', 'description']


@admin.register(ResearchMethodology)
class ResearchMethodologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'methodology_type', 'peer_reviewed', 'industry_standard']
    list_filter = ['methodology_type', 'peer_reviewed', 'industry_standard']


@admin.register(InsightDownload)
class InsightDownloadAdmin(admin.ModelAdmin):
    list_display = ['insight', 'user_email', 'download_type', 'created_at']
    list_filter = ['download_type', 'created_at']
    readonly_fields = ['created_at']
