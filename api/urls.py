from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'blog', views.BlogPostViewSet, basename='blogpost')
router.register(r'insights', views.InsightViewSet, basename='insight')

app_name = 'api'

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Additional list views
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('industries/', views.IndustryListView.as_view(), name='industries'),
    path('locations/', views.LocationListView.as_view(), name='locations'),
    path('blog-categories/', views.BlogCategoryListView.as_view(), name='blog-categories'),
    path('features/', views.FeaturesListView.as_view(), name='features'),

    # Utility endpoints
    path('years/', views.available_years, name='available-years'),
    path('stats/', views.site_stats, name='site-stats'),
    path('search/', views.search, name='search'),

    # Dashboard endpoints
    path('dashboard/', include('dashboard.urls')),
]
