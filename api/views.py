from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q, Count, Avg, F
from django.db import models
from django.utils import timezone
from datetime import timedelta

from brands.models import Brand, BrandCategory
from blog.models import BlogPost, BlogCategory
from insights.models import Insight
from core.models import Category, Industry, Location
from dashboard.models import YearlyRanking, SystemConfiguration

from .serializers import (
    BrandListSerializer, BrandDetailSerializer,
    BlogPostListSerializer, BlogPostDetailSerializer, BlogCategorySerializer,
    InsightListSerializer, InsightDetailSerializer,
    CategorySerializer, IndustrySerializer, LocationSerializer,
    StatsSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination class."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Brand model."""
    queryset = Brand.objects.filter(is_published=True).select_related(
        'category', 'industry', 'headquarters'
    ).prefetch_related(
        'metrics', 'achievements', 'timeline', 'rankings'
    )
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'industry', 'is_featured', 'is_new_entry', 'year']
    search_fields = ['title', 'subtitle', 'description']
    ordering_fields = ['current_rank', 'brand_value', 'growth_rate', 'brand_recognition', 'created_at']
    ordering = ['year', 'current_rank']
    lookup_field = 'slug'

    def get_queryset(self):
        """Filter by year - default to current active year."""
        queryset = super().get_queryset()
        year = self.request.query_params.get('year')

        if not year:
            # Get current active year
            try:
                active_year = YearlyRanking.objects.get(is_active=True).year
                year = active_year
            except YearlyRanking.DoesNotExist:
                year = 2025  # Default fallback

        return queryset.filter(year=year)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BrandDetailSerializer
        return BrandListSerializer
    
    @action(detail=False, methods=['get'])
    def top_10(self, request):
        """Get top 10 brands."""
        top_brands = self.get_queryset().filter(current_rank__lte=10)
        serializer = self.get_serializer(top_brands, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured brands."""
        featured_brands = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(featured_brands, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_entries(self, request):
        """Get new entry brands."""
        new_brands = self.get_queryset().filter(is_new_entry=True)
        serializer = self.get_serializer(new_brands, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get brands grouped by category."""
        categories = Category.objects.all()
        result = {}
        for category in categories:
            brands = self.get_queryset().filter(category=category)[:5]  # Top 5 per category
            result[category.slug] = BrandListSerializer(brands, many=True).data
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def most_popular(self, request):
        """Get most popular brands based on views and customer rating."""
        try:
            # Calculate popularity score and get most popular brands
            popular_brands = self.get_queryset().annotate(
                popularity_score=F('views_count') * 0.3 + F('customer_rating') * 20
            ).order_by('-popularity_score')[:10]
            
            serializer = self.get_serializer(popular_brands, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Fallback to top 10 brands if calculation fails
            top_brands = self.get_queryset().order_by('-current_rank')[:10]
            serializer = self.get_serializer(top_brands, many=True)
            return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment brand views count."""
        brand = self.get_object()
        brand.views_count += 1
        brand.save(update_fields=['views_count'])
        return Response({'views_count': brand.views_count})


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BlogPost model."""
    queryset = BlogPost.objects.filter(
        status='published', is_published=True
    ).select_related('author', 'category').prefetch_related('tags')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'views_count', 'likes_count', 'created_at']
    ordering = ['-published_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured blog posts."""
        featured_posts = self.get_queryset().filter(is_featured=True)[:5]
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent blog posts."""
        recent_posts = self.get_queryset()[:8]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment blog post views count."""
        post = self.get_object()
        post.views_count += 1
        post.save(update_fields=['views_count'])
        return Response({'views_count': post.views_count})


class InsightViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Insight model."""
    queryset = Insight.objects.filter(is_published=True).select_related(
        'author', 'category'
    ).prefetch_related('metrics', 'key_findings')
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['insight_type', 'category', 'is_premium', 'is_featured']
    search_fields = ['title', 'description', 'content']
    ordering_fields = ['published_at', 'views_count', 'download_count', 'created_at']
    ordering = ['-published_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InsightDetailSerializer
        return InsightListSerializer
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured insights."""
        featured_insights = self.get_queryset().filter(is_featured=True)[:6]
        serializer = self.get_serializer(featured_insights, many=True)
        return Response(serializer.data)

    


    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get insights grouped by type."""
        insight_types = dict(Insight.INSIGHT_TYPES)
        result = {}
        for type_key, type_name in insight_types.items():
            insights = self.get_queryset().filter(insight_type=type_key)[:3]
            result[type_key] = {
                'name': type_name,
                'insights': InsightListSerializer(insights, many=True).data
            }
        return Response(result)
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, slug=None, pk=None):
        """Increment insight views count."""
        try:
            insight = self.get_object()
            insight.views_count += 1
            insight.save(update_fields=['views_count'])
            return Response({'views_count': insight.views_count})
        except Exception as e:
            return Response(
                {'error': f'Failed to increment views: {str(e)}'}, 
                status=400
            )
    
    @action(detail=True, methods=['post'])
    def increment_downloads(self, request, pk=None):
        """Increment insight downloads count."""
        insight = self.get_object()
        insight.download_count += 1
        insight.save(update_fields=['download_count'])
        return Response({'download_count': insight.download_count})


class CategoryListView(generics.ListAPIView):
    """List view for categories."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


class IndustryListView(generics.ListAPIView):
    """List view for industries."""
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    pagination_class = None


class LocationListView(generics.ListAPIView):
    """List view for locations."""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    pagination_class = None


class BlogCategoryListView(generics.ListAPIView):
    """List view for blog categories."""
    queryset = BlogCategory.objects.filter(is_active=True)
    serializer_class = BlogCategorySerializer
    pagination_class = None


class FeaturesListView(generics.ListAPIView):
    """List view for features (using categories as features)."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


@api_view(['GET'])
def available_years(request):
    """Get all available years with their status."""
    years = YearlyRanking.objects.all().values(
        'year', 'title', 'is_active', 'is_published', 'is_complete',
        'total_brands', 'publication_date'
    )

    # Add counts for each year
    for year_data in years:
        year = year_data['year']
        year_data['brands_count'] = Brand.objects.filter(year=year, is_published=True).count()
        year_data['blog_posts_count'] = BlogPost.objects.filter(year=year, is_published=True).count()
        year_data['insights_count'] = Insight.objects.filter(year=year, is_published=True).count()

    return Response({
        'years': list(years),
        'current_year': YearlyRanking.objects.filter(is_active=True).first().year if YearlyRanking.objects.filter(is_active=True).exists() else 2025
    })


@api_view(['GET'])
def site_stats(request):
    """Get site statistics."""
    # Get year parameter
    year = request.GET.get('year')
    if not year:
        try:
            year = YearlyRanking.objects.get(is_active=True).year
        except YearlyRanking.DoesNotExist:
            year = 2025

    # Calculate stats for specific year
    total_brands = Brand.objects.filter(is_published=True, year=year).count()
    total_blog_posts = BlogPost.objects.filter(status='published', is_published=True, year=year).count()
    total_insights = Insight.objects.filter(is_published=True, year=year).count()
    total_categories = Category.objects.filter(is_active=True).count()
    
    # Calculate combined brand value (simplified)
    combined_value = "₦25.8T"  # This would be calculated from actual brand values
    
    # Calculate average growth
    avg_growth = "+12.3%"  # This would be calculated from actual growth rates
    
    # Get top performing category
    top_category = Category.objects.annotate(
        brand_count=Count('brand')
    ).order_by('-brand_count').first()
    
    # Get latest update
    latest_brand_update = Brand.objects.filter(is_published=True).order_by('-updated_at').first()
    latest_blog_update = BlogPost.objects.filter(status='published').order_by('-updated_at').first()
    
    latest_update = max(
        latest_brand_update.updated_at if latest_brand_update else timezone.now(),
        latest_blog_update.updated_at if latest_blog_update else timezone.now()
    )
    
    stats_data = {
        'total_brands': total_brands,
        'total_blog_posts': total_blog_posts,
        'total_insights': total_insights,
        'total_categories': total_categories,
        'combined_brand_value': combined_value,
        'average_growth': avg_growth,
        'top_performing_category': top_category.name if top_category else 'N/A',
        'latest_update': latest_update,
    }
    
    serializer = StatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['GET'])
def search(request):
    """Global search endpoint."""
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Search brands
    brands = Brand.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query),
        is_published=True
    )[:5]
    
    # Search blog posts
    blog_posts = BlogPost.objects.filter(
        Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query),
        status='published', is_published=True
    )[:5]
    
    # Search insights
    insights = Insight.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(content__icontains=query),
        is_published=True
    )[:5]
    
    return Response({
        'query': query,
        'results': {
            'brands': BrandListSerializer(brands, many=True).data,
            'blog_posts': BlogPostListSerializer(blog_posts, many=True).data,
            'insights': InsightListSerializer(insights, many=True).data,
        },
        'total_results': brands.count() + blog_posts.count() + insights.count()
    })
