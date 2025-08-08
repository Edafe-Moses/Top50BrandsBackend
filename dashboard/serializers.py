from rest_framework import serializers
from django.contrib.auth.models import User
from .models import YearlyRanking, DashboardUser, DataMigrationLog, SystemConfiguration


class LoginSerializer(serializers.Serializer):
    """Serializer for dashboard login."""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)


class DashboardUserSerializer(serializers.ModelSerializer):
    """Serializer for DashboardUser model."""
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    assigned_years_list = serializers.StringRelatedField(source='assigned_years', many=True, read_only=True)
    
    class Meta:
        model = DashboardUser
        fields = [
            'id', 'user', 'user_full_name', 'user_email', 'role',
            'can_create_years', 'can_edit_brands', 'can_publish_content', 'can_manage_users',
            'last_login_dashboard', 'login_count', 'assigned_years', 'assigned_years_list',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login_dashboard', 'login_count', 'created_at', 'updated_at']


class YearlyRankingSerializer(serializers.ModelSerializer):
    """Serializer for YearlyRanking model."""
    research_lead_name = serializers.CharField(source='research_lead.get_full_name', read_only=True)
    team_members_list = serializers.StringRelatedField(source='team_members', many=True, read_only=True)
    brands_count = serializers.ReadOnlyField()
    blog_posts_count = serializers.ReadOnlyField()
    insights_count = serializers.ReadOnlyField()
    
    class Meta:
        model = YearlyRanking
        fields = [
            'id', 'year', 'title', 'description', 'is_active', 'is_published', 'is_complete',
            'total_brands', 'research_methodology', 'data_collection_start', 'data_collection_end',
            'publication_date', 'research_lead', 'research_lead_name', 'team_members', 'team_members_list',
            'brands_count', 'blog_posts_count', 'insights_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['brands_count', 'blog_posts_count', 'insights_count', 'created_at', 'updated_at']
    
    def validate_year(self, value):
        """Validate year is reasonable."""
        if value < 2020 or value > 2050:
            raise serializers.ValidationError("Year must be between 2020 and 2050")
        return value
    
    def validate(self, data):
        """Validate that only one year can be active at a time."""
        if data.get('is_active', False):
            # Check if another year is already active (excluding current instance)
            existing_active = YearlyRanking.objects.filter(is_active=True)
            if self.instance:
                existing_active = existing_active.exclude(pk=self.instance.pk)
            
            if existing_active.exists():
                raise serializers.ValidationError({
                    'is_active': 'Only one year can be active at a time. Please deactivate the current active year first.'
                })
        
        return data


class DataMigrationLogSerializer(serializers.ModelSerializer):
    """Serializer for DataMigrationLog model."""
    initiated_by_name = serializers.CharField(source='initiated_by.get_full_name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = DataMigrationLog
        fields = [
            'id', 'migration_type', 'from_year', 'to_year', 'status', 'description',
            'items_processed', 'items_total', 'progress_percentage', 'error_message',
            'initiated_by', 'initiated_by_name', 'started_at', 'completed_at',
            'duration', 'created_at', 'updated_at'
        ]
        read_only_fields = ['progress_percentage', 'duration', 'created_at', 'updated_at']
    
    def get_duration(self, obj):
        """Calculate migration duration."""
        if obj.started_at and obj.completed_at:
            duration = obj.completed_at - obj.started_at
            return str(duration)
        return None


class SystemConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for SystemConfiguration model."""
    
    class Meta:
        model = SystemConfiguration
        fields = [
            'id', 'key', 'value', 'description', 'is_active', 'is_public', 'requires_admin',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_key(self, value):
        """Validate configuration key format."""
        if not value.replace('_', '').replace('-', '').isalnum():
            raise serializers.ValidationError("Key can only contain letters, numbers, underscores, and hyphens")
        return value.lower()


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    current_year = serializers.IntegerField()
    total_years = serializers.IntegerField()
    published_years = serializers.IntegerField()
    total_brands = serializers.IntegerField()
    total_blog_posts = serializers.IntegerField()
    total_insights = serializers.IntegerField()
    recent_migrations = serializers.IntegerField()
    user_role = serializers.CharField()
    user_permissions = serializers.DictField()
    assigned_years = serializers.ListField(child=serializers.IntegerField())


class BrandMigrationSerializer(serializers.Serializer):
    """Serializer for brand migration operations."""
    from_year = serializers.IntegerField()
    to_year = serializers.IntegerField()
    copy_brands = serializers.BooleanField(default=True)
    copy_metrics = serializers.BooleanField(default=True)
    copy_achievements = serializers.BooleanField(default=True)
    copy_timeline = serializers.BooleanField(default=False)
    update_ranks = serializers.BooleanField(default=True)
    selected_brands = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of brand IDs to migrate. If empty, all brands will be migrated."
    )
    
    def validate(self, data):
        """Validate migration parameters."""
        from_year = data['from_year']
        to_year = data['to_year']
        
        if from_year == to_year:
            raise serializers.ValidationError("From year and to year cannot be the same")
        
        # Check if years exist
        if not YearlyRanking.objects.filter(year=from_year).exists():
            raise serializers.ValidationError(f"Source year {from_year} does not exist")
        
        if not YearlyRanking.objects.filter(year=to_year).exists():
            raise serializers.ValidationError(f"Target year {to_year} does not exist")
        
        return data


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = __import__('blog.models', fromlist=['BlogTag']).BlogTag
        fields = ['id', 'name', 'slug', 'description']

class YearSetupSerializer(serializers.Serializer):
    """Serializer for setting up a new year."""
    year = serializers.IntegerField()
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    copy_from_year = serializers.IntegerField(required=False)
    copy_brands = serializers.BooleanField(default=False)
    copy_structure_only = serializers.BooleanField(default=True)
    
    def validate_year(self, value):
        """Validate year."""
        if value < 2020 or value > 2050:
            raise serializers.ValidationError("Year must be between 2020 and 2050")
        
        if YearlyRanking.objects.filter(year=value).exists():
            raise serializers.ValidationError(f"Year {value} already exists")
        
        return value
    
    def validate_copy_from_year(self, value):
        """Validate source year for copying."""
        if value and not YearlyRanking.objects.filter(year=value).exists():
            raise serializers.ValidationError(f"Source year {value} does not exist")
        return value
