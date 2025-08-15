from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import (
    TimeStampedModel, SEOModel, PublishableModel, 
    SocialMediaModel, ViewTrackingModel, Category, Industry, Location
)


class Brand(TimeStampedModel, SEOModel, PublishableModel, SocialMediaModel, ViewTrackingModel):
    """Main Brand model representing companies in the Top 50 ranking."""

    # Year-based tracking
    year = models.PositiveIntegerField(default=2025, help_text="Year this ranking data applies to")

    # Basic Information
    title = models.CharField(max_length=200, help_text="Brand name")
    subtitle = models.CharField(max_length=300, blank=True, help_text="Brand tagline or subtitle")
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(help_text="Short description")
    full_description = models.TextField(help_text="Detailed description")
    
    # Visual Assets
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    image = models.ImageField(upload_to='brands/images/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='brands/banners/', blank=True, null=True)
    
    # Ranking Information
    current_rank = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Current ranking position (1-50)"
    )
    previous_rank = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Previous year ranking position"
    )
    
    # Financial Data
    brand_value = models.CharField(max_length=20, help_text="Brand value (e.g., ₦4.2T)")
    market_cap = models.CharField(max_length=20, blank=True, help_text="Market capitalization")
    revenue = models.CharField(max_length=20, blank=True, help_text="Annual revenue")
    growth_rate = models.CharField(max_length=10, help_text="Growth rate (e.g., +12.5%)")
    
    # Company Details
    founded_year = models.CharField(max_length=4, blank=True, help_text="Year founded")
    ceo = models.CharField(max_length=200, blank=True, help_text="CEO name")
    employees = models.CharField(max_length=50, blank=True, help_text="Number of employees")
    headquarters = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metrics
    brand_recognition = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Brand recognition percentage (0-100)"
    )
    customer_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Customer rating (0.0-5.0)"
    )
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Featured brand")
    is_new_entry = models.BooleanField(default=False, help_text="New entry this year")
    
    class Meta:
        ordering = ['current_rank']
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
    
    class Meta:
        unique_together = [['slug', 'year']]
        ordering = ['year', 'current_rank']
        indexes = [
            models.Index(fields=['year', 'current_rank']),
            models.Index(fields=['year', 'slug']),
        ]

    def __str__(self):
        return f"#{self.current_rank} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def rank_change(self):
        """Calculate rank change from previous year."""
        if self.previous_rank:
            return self.previous_rank - self.current_rank
        return 0
    
    @property
    def rank_change_direction(self):
        """Get rank change direction."""
        change = self.rank_change
        if change > 0:
            return 'up'
        elif change < 0:
            return 'down'
        return 'stable'
    
    @property
    def logo_url(self):
        """Get logo URL with fallback."""
        if self.logo:
            return self.logo.url
        # Point to media directory
        return f'/media/brands/logos/{self.slug}.png'
    
    @property
    def image_url(self):
        """Get image URL with fallback."""
        if self.image:
            return self.image.url
        # Point to media directory
        return f'/media/brands/logos/{self.slug}.png'


class BrandMetric(TimeStampedModel):
    """Model for storing brand metrics and KPIs."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='metrics')
    label = models.CharField(max_length=100, help_text="Metric label (e.g., 'Total Assets')")
    value = models.CharField(max_length=50, help_text="Metric value (e.g., '₦9.2T')")
    change = models.CharField(max_length=20, blank=True, help_text="Change percentage (e.g., '+15%')")
    trend = models.CharField(
        max_length=10, 
        choices=[('up', 'Up'), ('down', 'Down'), ('stable', 'Stable')],
        default='stable'
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['brand', 'order', 'label']
        unique_together = ['brand', 'label']
    
    def __str__(self):
        return f"{self.brand.title} - {self.label}: {self.value}"


class BrandAchievement(TimeStampedModel):
    """Model for brand achievements and awards."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200, help_text="Achievement title")
    description = models.TextField(blank=True, help_text="Achievement description")
    year = models.CharField(max_length=4, blank=True, help_text="Year received")
    organization = models.CharField(max_length=200, blank=True, help_text="Awarding organization")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['brand', 'order', '-year']
    
    def __str__(self):
        return f"{self.brand.title} - {self.title}"


class BrandTimeline(TimeStampedModel):
    """Model for brand timeline events."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='timeline')
    year = models.CharField(max_length=4, help_text="Event year")
    event = models.CharField(max_length=300, help_text="Event description")
    description = models.TextField(blank=True, help_text="Detailed description")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['brand', 'year', 'order']
    
    def __str__(self):
        return f"{self.brand.title} - {self.year}: {self.event}"


class BrandRanking(TimeStampedModel):
    """Model for historical brand rankings."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='rankings')
    year = models.PositiveIntegerField(help_text="Ranking year")
    rank = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Ranking position"
    )
    brand_value = models.CharField(max_length=20, help_text="Brand value for that year")
    growth_rate = models.CharField(max_length=10, blank=True, help_text="Growth rate")
    notes = models.TextField(blank=True, help_text="Additional notes")
    
    class Meta:
        ordering = ['-year', 'rank']
        unique_together = ['brand', 'year']
    
    def __str__(self):
        return f"{self.brand.title} - {self.year}: #{self.rank}"


class BrandCategory(TimeStampedModel):
    """Model for brand categories specific to rankings."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007751', help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Brand Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BrandStats(TimeStampedModel):
    """Model for storing brand statistics and analytics."""
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name='stats')
    total_views = models.PositiveIntegerField(default=0)
    monthly_views = models.PositiveIntegerField(default=0)
    weekly_views = models.PositiveIntegerField(default=0)
    daily_views = models.PositiveIntegerField(default=0)
    total_likes = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    engagement_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text="Engagement rate percentage"
    )
    
    class Meta:
        verbose_name_plural = "Brand Stats"
    
    def __str__(self):
        return f"{self.brand.title} - Stats"
