from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from core.models import (
    TimeStampedModel, SEOModel, PublishableModel, 
    ViewTrackingModel, Category
)


class Insight(TimeStampedModel, SEOModel, PublishableModel, ViewTrackingModel):
    """Model for brand insights and market research reports."""
    
    INSIGHT_TYPES = [
        ('market_analysis', 'Market Analysis'),
        ('consumer_behavior', 'Consumer Behavior'),
        ('brand_performance', 'Brand Performance'),
        ('industry_trends', 'Industry Trends'),
        ('methodology', 'Methodology'),
        ('forecast', 'Forecast'),
    ]

    # Year-based tracking
    year = models.PositiveIntegerField(default=2025, help_text="Year this insight applies to")

    # Basic Information
    title = models.CharField(max_length=300, help_text="Insight title")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(max_length=500, help_text="Short description")
    content = RichTextField(help_text="Full insight content")
    
    # Classification
    insight_type = models.CharField(max_length=30, choices=INSIGHT_TYPES, default='market_analysis')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Media
    featured_image = models.ImageField(upload_to='insights/images/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True)
    report_file = models.FileField(upload_to='insights/reports/', blank=True, null=True, help_text="PDF report file")
    
    # Author and Attribution
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insights')
    research_team = models.CharField(max_length=200, blank=True, help_text="Research team members")
    
    # Metrics and Data
    data_points = models.CharField(max_length=20, blank=True, help_text="Number of data points (e.g., '50K+')")
    accuracy = models.CharField(max_length=10, blank=True, help_text="Accuracy percentage (e.g., '94%')")
    sample_size = models.CharField(max_length=20, blank=True, help_text="Sample size (e.g., '10,000')")
    regions_covered = models.CharField(max_length=50, blank=True, help_text="Regions covered (e.g., '36 States')")
    
    # Status
    is_premium = models.BooleanField(default=False, help_text="Premium content requiring subscription")
    is_featured = models.BooleanField(default=False, help_text="Featured insight")
    download_count = models.PositiveIntegerField(default=0, help_text="Number of downloads")
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Insight"
        verbose_name_plural = "Insights"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def featured_image_url(self):
        """Get featured image URL with fallback."""
        if self.featured_image:
            return self.featured_image.url
        return f'/static/images/insights/insight-{self.id}.png'
    
    @property
    def report_file_url(self):
        """Get report file URL."""
        if self.report_file:
            return self.report_file.url
        return None


class InsightMetric(TimeStampedModel):
    """Model for insight metrics and key findings."""
    insight = models.ForeignKey(Insight, on_delete=models.CASCADE, related_name='metrics')
    label = models.CharField(max_length=100, help_text="Metric label")
    value = models.CharField(max_length=50, help_text="Metric value")
    change = models.CharField(max_length=20, blank=True, help_text="Change from previous period")
    trend = models.CharField(
        max_length=10,
        choices=[('up', 'Up'), ('down', 'Down'), ('stable', 'Stable')],
        default='stable'
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['insight', 'order', 'label']
        unique_together = ['insight', 'label']
    
    def __str__(self):
        return f"{self.insight.title} - {self.label}: {self.value}"


class InsightKeyFinding(TimeStampedModel):
    """Model for key findings in insights."""
    insight = models.ForeignKey(Insight, on_delete=models.CASCADE, related_name='key_findings')
    finding = models.CharField(max_length=300, help_text="Key finding statement")
    description = models.TextField(blank=True, help_text="Detailed explanation")
    impact_level = models.CharField(
        max_length=10,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ],
        default='medium'
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    
    class Meta:
        ordering = ['insight', 'order']
    
    def __str__(self):
        return f"{self.insight.title} - {self.finding[:50]}"


class MarketData(TimeStampedModel):
    """Model for storing market data and statistics."""
    title = models.CharField(max_length=200, help_text="Data title")
    description = models.TextField(blank=True)
    
    # Data categorization
    data_type = models.CharField(
        max_length=30,
        choices=[
            ('market_size', 'Market Size'),
            ('growth_rate', 'Growth Rate'),
            ('market_share', 'Market Share'),
            ('consumer_spending', 'Consumer Spending'),
            ('brand_awareness', 'Brand Awareness'),
            ('customer_satisfaction', 'Customer Satisfaction'),
        ]
    )
    
    # Data values
    value = models.CharField(max_length=50, help_text="Data value")
    unit = models.CharField(max_length=20, blank=True, help_text="Unit of measurement")
    period = models.CharField(max_length=50, help_text="Time period (e.g., '2024 Q1')")
    source = models.CharField(max_length=200, blank=True, help_text="Data source")
    
    # Geographical scope
    country = models.CharField(max_length=100, default='Nigeria')
    region = models.CharField(max_length=100, blank=True)
    
    # Status
    is_verified = models.BooleanField(default=False, help_text="Data verified by research team")
    confidence_level = models.CharField(
        max_length=10,
        choices=[
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
        ],
        default='medium'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Market Data"
        verbose_name_plural = "Market Data"
    
    def __str__(self):
        return f"{self.title}: {self.value} ({self.period})"


class ResearchMethodology(TimeStampedModel):
    """Model for research methodologies used in insights."""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    methodology_type = models.CharField(
        max_length=30,
        choices=[
            ('quantitative', 'Quantitative'),
            ('qualitative', 'Qualitative'),
            ('mixed', 'Mixed Methods'),
        ]
    )
    
    # Methodology details
    sample_size_min = models.PositiveIntegerField(null=True, blank=True)
    sample_size_max = models.PositiveIntegerField(null=True, blank=True)
    data_collection_methods = models.TextField(blank=True)
    analysis_techniques = models.TextField(blank=True)
    limitations = models.TextField(blank=True)
    
    # Validation
    peer_reviewed = models.BooleanField(default=False)
    industry_standard = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Research Methodology"
        verbose_name_plural = "Research Methodologies"
    
    def __str__(self):
        return self.name


class InsightDownload(TimeStampedModel):
    """Model for tracking insight downloads."""
    insight = models.ForeignKey(Insight, on_delete=models.CASCADE, related_name='downloads')
    user_email = models.EmailField(blank=True, help_text="User email for tracking")
    user_name = models.CharField(max_length=100, blank=True)
    user_company = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    download_type = models.CharField(
        max_length=20,
        choices=[
            ('pdf', 'PDF Report'),
            ('data', 'Raw Data'),
            ('summary', 'Executive Summary'),
        ],
        default='pdf'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Insight Download"
        verbose_name_plural = "Insight Downloads"
    
    def __str__(self):
        return f"{self.insight.title} - {self.download_type} ({self.created_at.date()})"
