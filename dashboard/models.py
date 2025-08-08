from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimeStampedModel


class YearlyRanking(TimeStampedModel):
    """Model to manage yearly rankings and their status."""
    
    year = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(2020), MaxValueValidator(2050)],
        help_text="Ranking year"
    )
    title = models.CharField(max_length=200, help_text="Title for this year's ranking")
    description = models.TextField(blank=True, help_text="Description of this year's ranking")
    
    # Status
    is_active = models.BooleanField(default=False, help_text="Is this the current active year?")
    is_published = models.BooleanField(default=False, help_text="Is this year's ranking published?")
    is_complete = models.BooleanField(default=False, help_text="Is data collection complete for this year?")
    
    # Metadata
    total_brands = models.PositiveIntegerField(default=50, help_text="Total number of brands in this year's ranking")
    research_methodology = models.TextField(blank=True, help_text="Research methodology used for this year")
    data_collection_start = models.DateField(null=True, blank=True)
    data_collection_end = models.DateField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    
    # Team
    research_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_rankings')
    team_members = models.ManyToManyField(User, blank=True, related_name='ranking_teams')
    
    class Meta:
        ordering = ['-year']
        verbose_name = "Yearly Ranking"
        verbose_name_plural = "Yearly Rankings"
    
    def __str__(self):
        return f"{self.year} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active year at a time
        if self.is_active:
            YearlyRanking.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    @property
    def brands_count(self):
        """Get the actual number of brands for this year."""
        from brands.models import Brand
        return Brand.objects.filter(year=self.year).count()
    
    @property
    def blog_posts_count(self):
        """Get the number of blog posts for this year."""
        from blog.models import BlogPost
        return BlogPost.objects.filter(year=self.year).count()
    
    @property
    def insights_count(self):
        """Get the number of insights for this year."""
        from insights.models import Insight
        return Insight.objects.filter(year=self.year).count()


class DashboardUser(TimeStampedModel):
    """Extended user profile for dashboard access."""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('editor', 'Editor'),
        ('researcher', 'Researcher'),
        ('viewer', 'Viewer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    
    # Permissions
    can_create_years = models.BooleanField(default=False)
    can_edit_brands = models.BooleanField(default=False)
    can_publish_content = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    
    # Access tracking
    last_login_dashboard = models.DateTimeField(null=True, blank=True)
    login_count = models.PositiveIntegerField(default=0)
    
    # Assigned years
    assigned_years = models.ManyToManyField(YearlyRanking, blank=True, help_text="Years this user can manage")
    
    class Meta:
        verbose_name = "Dashboard User"
        verbose_name_plural = "Dashboard Users"
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"
    
    @property
    def can_access_year(self, year):
        """Check if user can access a specific year."""
        if self.role == 'admin':
            return True
        return self.assigned_years.filter(year=year).exists()


class DataMigrationLog(TimeStampedModel):
    """Log data migrations between years."""
    
    MIGRATION_TYPES = [
        ('brand_copy', 'Brand Copy'),
        ('brand_update', 'Brand Update'),
        ('new_year_setup', 'New Year Setup'),
        ('data_cleanup', 'Data Cleanup'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    migration_type = models.CharField(max_length=20, choices=MIGRATION_TYPES)
    from_year = models.PositiveIntegerField(null=True, blank=True)
    to_year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Details
    description = models.TextField(help_text="Description of the migration")
    items_processed = models.PositiveIntegerField(default=0)
    items_total = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    # User tracking
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_migrations')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Data Migration Log"
        verbose_name_plural = "Data Migration Logs"
    
    def __str__(self):
        return f"{self.migration_type} - {self.from_year} to {self.to_year} ({self.status})"
    
    @property
    def progress_percentage(self):
        """Calculate migration progress percentage."""
        if self.items_total == 0:
            return 0
        return (self.items_processed / self.items_total) * 100


class SystemConfiguration(TimeStampedModel):
    """System-wide configuration settings."""
    
    key = models.CharField(max_length=100, unique=True, help_text="Configuration key")
    value = models.TextField(help_text="Configuration value (JSON format)")
    description = models.TextField(blank=True, help_text="Description of this configuration")
    is_active = models.BooleanField(default=True)
    
    # Access control
    is_public = models.BooleanField(default=False, help_text="Can be accessed via public API")
    requires_admin = models.BooleanField(default=True, help_text="Requires admin access to modify")
    
    class Meta:
        ordering = ['key']
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configurations"
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}..."
    
    @classmethod
    def get_value(cls, key, default=None):
        """Get configuration value by key."""
        try:
            config = cls.objects.get(key=key, is_active=True)
            return config.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_value(cls, key, value, description="", user=None):
        """Set configuration value."""
        config, created = cls.objects.get_or_create(
            key=key,
            defaults={
                'value': value,
                'description': description,
            }
        )
        if not created:
            config.value = value
            config.description = description
            config.save()
        return config
