from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth_views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'years', views.YearlyRankingViewSet, basename='yearly-ranking')
router.register(r'configurations', views.SystemConfigurationViewSet, basename='system-configuration')
router.register(r'migrations', views.DataMigrationLogViewSet, basename='data-migration-log')
router.register(r'users', views.DashboardUserViewSet, basename='dashboard-user')
router.register(r'brands', views.DashboardBrandViewSet, basename='dashboard-brand')
router.register(r'blog', views.DashboardBlogViewSet, basename='dashboard-blog')
router.register(r'blog-tags', views.DashboardBlogTagViewSet, basename='dashboard-blogtag')
router.register(r'insights', views.DashboardInsightViewSet, basename='dashboard-insight')

app_name = 'dashboard'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', auth_views.login_view, name='dashboard-login'),
    path('auth/logout/', auth_views.logout_view, name='dashboard-logout'),
    path('auth/user/', auth_views.user_view, name='dashboard-user'),

    # Dashboard stats
    path('stats/', auth_views.dashboard_stats_view, name='dashboard-stats'),

    # System management endpoints
    path('system/backup/', views.system_backup_view, name='system-backup'),
    path('system/restore/', views.system_restore_view, name='system-restore'),
    path('system/health/', views.system_health_view, name='system-health'),
    path('system/cache/clear/', views.clear_cache_view, name='clear-cache'),

    # Router URLs
    path('', include(router.urls)),
]
