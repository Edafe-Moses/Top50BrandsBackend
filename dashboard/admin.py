from django.contrib import admin
from .models import YearlyRanking, DashboardUser, DataMigrationLog, SystemConfiguration


@admin.register(YearlyRanking)
class YearlyRankingAdmin(admin.ModelAdmin):
    list_display = ['year', 'title', 'is_active', 'is_published', 'is_complete', 'total_brands', 'brands_count']
    list_filter = ['is_active', 'is_published', 'is_complete', 'year']
    search_fields = ['year', 'title', 'description']
    ordering = ['-year']
    readonly_fields = ['brands_count', 'blog_posts_count', 'insights_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('year', 'title', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'is_published', 'is_complete')
        }),
        ('Configuration', {
            'fields': ('total_brands', 'research_methodology')
        }),
        ('Timeline', {
            'fields': ('data_collection_start', 'data_collection_end', 'publication_date')
        }),
        ('Team', {
            'fields': ('research_lead', 'team_members')
        }),
        ('Statistics', {
            'fields': ('brands_count', 'blog_posts_count', 'insights_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['team_members']


@admin.register(DashboardUser)
class DashboardUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'can_create_years', 'can_edit_brands', 'can_publish_content', 'last_login_dashboard']
    list_filter = ['role', 'can_create_years', 'can_edit_brands', 'can_publish_content', 'can_manage_users']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['last_login_dashboard', 'login_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user', 'role')
        }),
        ('Permissions', {
            'fields': ('can_create_years', 'can_edit_brands', 'can_publish_content', 'can_manage_users')
        }),
        ('Assigned Years', {
            'fields': ('assigned_years',)
        }),
        ('Activity', {
            'fields': ('last_login_dashboard', 'login_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['assigned_years']


@admin.register(DataMigrationLog)
class DataMigrationLogAdmin(admin.ModelAdmin):
    list_display = ['migration_type', 'from_year', 'to_year', 'status', 'progress_percentage', 'initiated_by', 'created_at']
    list_filter = ['migration_type', 'status', 'from_year', 'to_year']
    search_fields = ['description', 'initiated_by__username']
    readonly_fields = ['progress_percentage', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Migration Details', {
            'fields': ('migration_type', 'from_year', 'to_year', 'description')
        }),
        ('Status', {
            'fields': ('status', 'items_processed', 'items_total', 'progress_percentage')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('initiated_by', 'started_at', 'completed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'is_active', 'is_public', 'requires_admin', 'updated_at']
    list_filter = ['is_active', 'is_public', 'requires_admin']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Configuration', {
            'fields': ('key', 'value', 'description')
        }),
        ('Access Control', {
            'fields': ('is_active', 'is_public', 'requires_admin')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
