from rest_framework import serializers
from brands.models import Brand, BrandMetric, BrandAchievement, BrandTimeline, BrandRanking
from blog.models import BlogPost, BlogComment, BlogCategory
from insights.models import Insight, InsightMetric, InsightKeyFinding
from core.models import Category, Industry, Location


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon']


class IndustrySerializer(serializers.ModelSerializer):
    """Serializer for Industry model."""
    class Meta:
        model = Industry
        fields = ['id', 'name', 'slug', 'description', 'icon']


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model."""
    class Meta:
        model = Location
        fields = ['id', 'name', 'slug', 'country', 'state', 'city']


class BrandMetricSerializer(serializers.ModelSerializer):
    """Serializer for BrandMetric model."""
    class Meta:
        model = BrandMetric
        fields = ['label', 'value', 'change', 'trend']


class BrandAchievementSerializer(serializers.ModelSerializer):
    """Serializer for BrandAchievement model."""
    class Meta:
        model = BrandAchievement
        fields = ['title', 'description', 'year', 'organization']


class BrandTimelineSerializer(serializers.ModelSerializer):
    """Serializer for BrandTimeline model."""
    class Meta:
        model = BrandTimeline
        fields = ['year', 'event', 'description']


class BrandRankingSerializer(serializers.ModelSerializer):
    """Serializer for BrandRanking model."""
    class Meta:
        model = BrandRanking
        fields = ['year', 'rank', 'brand_value', 'growth_rate', 'notes']


class BrandListSerializer(serializers.ModelSerializer):
    """Serializer for Brand list view (minimal data)."""
    category = CategorySerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    headquarters = LocationSerializer(read_only=True)
    rank_change = serializers.ReadOnlyField()
    rank_change_direction = serializers.ReadOnlyField()
    logo_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = [
            'id', 'title', 'subtitle', 'slug', 'description',
            'logo_url', 'image_url', 'current_rank', 'previous_rank',
            'brand_value', 'growth_rate', 'category', 'industry',
            'headquarters', 'brand_recognition', 'customer_rating',
            'is_featured', 'is_new_entry', 'rank_change', 'rank_change_direction',
            'views_count', 'likes_count', 'shares_count'
        ]

    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url)
        # Use the model's fallback property
        return obj.logo_url

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        # Use the model's fallback property
        return obj.image_url


class BrandDetailSerializer(serializers.ModelSerializer):
    """Serializer for Brand detail view (full data)."""
    category = CategorySerializer(read_only=True)
    industry = IndustrySerializer(read_only=True)
    headquarters = LocationSerializer(read_only=True)
    metrics = BrandMetricSerializer(many=True, read_only=True)
    achievements = BrandAchievementSerializer(many=True, read_only=True)
    timeline = BrandTimelineSerializer(many=True, read_only=True)
    rankings = BrandRankingSerializer(many=True, read_only=True)
    rank_change = serializers.ReadOnlyField()
    rank_change_direction = serializers.ReadOnlyField()
    logo_url = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()
    
    # Social media fields
    social_media = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = [
            'id', 'title', 'subtitle', 'slug', 'description', 'full_description',
            'logo_url', 'image_url', 'current_rank', 'previous_rank',
            'brand_value', 'market_cap', 'revenue', 'growth_rate',
            'founded_year', 'ceo', 'employees', 'headquarters',
            'category', 'industry', 'brand_recognition', 'customer_rating',
            'is_featured', 'is_new_entry', 'rank_change', 'rank_change_direction',
            'views_count', 'likes_count', 'shares_count',
            'metrics', 'achievements', 'timeline', 'rankings', 'social_media',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at'
        ]
    
    def get_social_media(self, obj):
        """Get social media links."""
        return {
            'twitter': obj.twitter,
            'facebook': obj.facebook,
            'instagram': obj.instagram,
            'linkedin': obj.linkedin,
            'youtube': obj.youtube,
            'website': obj.website,
        }


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for BlogCategory model."""
    posts_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'color', 'icon', 'posts_count']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost list view."""
    author = serializers.StringRelatedField()
    category = BlogCategorySerializer(read_only=True)
    featured_image_url = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image_url',
            'author', 'category', 'published_at', 'read_time',
            'views_count', 'likes_count', 'shares_count', 'comments_count',
            'is_featured'
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost detail view."""
    author = serializers.StringRelatedField()
    category = BlogCategorySerializer(read_only=True)
    featured_image_url = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image_url',
            'featured_image_alt', 'author', 'category', 'published_at',
            'read_time', 'views_count', 'likes_count', 'shares_count',
            'comments_count', 'is_featured', 'tags',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at'
        ]


class InsightMetricSerializer(serializers.ModelSerializer):
    """Serializer for InsightMetric model."""
    class Meta:
        model = InsightMetric
        fields = ['label', 'value', 'change', 'trend']


class InsightKeyFindingSerializer(serializers.ModelSerializer):
    """Serializer for InsightKeyFinding model."""
    class Meta:
        model = InsightKeyFinding
        fields = ['finding', 'description', 'impact_level']


class InsightListSerializer(serializers.ModelSerializer):
    """Serializer for Insight list view."""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    featured_image_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Insight
        fields = [
            'id', 'title', 'slug', 'description', 'featured_image_url',
            'insight_type', 'category', 'author', 'published_at',
            'data_points', 'accuracy', 'regions_covered',
            'views_count', 'likes_count', 'shares_count', 'download_count',
            'is_premium', 'is_featured'
        ]


class InsightDetailSerializer(serializers.ModelSerializer):
    """Serializer for Insight detail view."""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    metrics = InsightMetricSerializer(many=True, read_only=True)
    key_findings = InsightKeyFindingSerializer(many=True, read_only=True)
    featured_image_url = serializers.ReadOnlyField()
    report_file_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Insight
        fields = [
            'id', 'title', 'slug', 'description', 'content',
            'featured_image_url', 'report_file_url', 'insight_type',
            'category', 'author', 'research_team', 'published_at',
            'data_points', 'accuracy', 'sample_size', 'regions_covered',
            'views_count', 'likes_count', 'shares_count', 'download_count',
            'is_premium', 'is_featured', 'metrics', 'key_findings',
            'meta_title', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at'
        ]


class StatsSerializer(serializers.Serializer):
    """Serializer for site statistics."""
    total_brands = serializers.IntegerField()
    total_blog_posts = serializers.IntegerField()
    total_insights = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    combined_brand_value = serializers.CharField()
    average_growth = serializers.CharField()
    top_performing_category = serializers.CharField()
    latest_update = serializers.DateTimeField()