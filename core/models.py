from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract base model for SEO fields."""
    meta_title = models.CharField(max_length=200, blank=True, help_text="SEO title")
    meta_description = models.TextField(max_length=300, blank=True, help_text="SEO description")
    meta_keywords = models.CharField(max_length=500, blank=True, help_text="SEO keywords")
    
    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """Abstract base model for publishable content."""
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True


class SocialMediaModel(models.Model):
    """Abstract base model for social media links."""
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    class Meta:
        abstract = True


class ViewTrackingModel(models.Model):
    """Abstract base model for tracking views and engagement."""
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """Category model for organizing content."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007751', help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    """Tag model for content tagging."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Industry(TimeStampedModel):
    """Industry model for brand categorization."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name_plural = "Industries"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Location(TimeStampedModel):
    """Location model for geographical data."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    country = models.CharField(max_length=100, default='Nigeria')
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'country', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.country}"


class MediaFile(TimeStampedModel):
    """Model for managing uploaded media files."""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
    ]
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='media/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for images")
    caption = models.TextField(blank=True)
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size in bytes")
    width = models.PositiveIntegerField(null=True, blank=True, help_text="Image width in pixels")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="Image height in pixels")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def file_url(self):
        if self.file:
            return self.file.url
        return None


class SiteConfiguration(TimeStampedModel):
    """Model for site-wide configuration settings."""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['key']
    
    def __str__(self):
        return f"{self.key}: {self.value[:50]}"
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get a setting value by key."""
        try:
            setting = cls.objects.get(key=key, is_active=True)
            return setting.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_setting(cls, key, value, description=''):
        """Set a setting value."""
        setting, created = cls.objects.get_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        if not created:
            setting.value = value
            setting.description = description
            setting.save()
        return setting
