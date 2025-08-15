from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from core.models import (
    TimeStampedModel, SEOModel, PublishableModel, 
    ViewTrackingModel, Category
)


class BlogPost(TimeStampedModel, SEOModel, PublishableModel, ViewTrackingModel):
    """Blog post model for articles and insights."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Year-based tracking
    year = models.PositiveIntegerField(default=2025, help_text="Year this post was published")

    # Basic Information
    title = models.CharField(max_length=300, help_text="Blog post title")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.TextField(max_length=500, help_text="Short excerpt/summary")
    content = RichTextField(help_text="Full blog post content")
    
    # Media
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    featured_image_alt = models.CharField(max_length=200, blank=True, help_text="Alt text for featured image")
    
    # Author and Category
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status and Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Engagement
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    is_featured = models.BooleanField(default=False, help_text="Featured post")
    allow_comments = models.BooleanField(default=True)
    
    # Tags
    tags = TaggableManager(blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    
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
        
        # Use different image paths based on category
        if self.category and self.category.name == 'Events':
            # For events, use sequential numbering starting from 1
            event_posts = BlogPost.objects.filter(
                category__name='Events', 
                is_featured=True, 
                is_published=True
            ).order_by('id')
            try:
                event_index = list(event_posts.values_list('id', flat=True)).index(self.id) + 1
                return f'/events/event-{event_index}.png'
            except (ValueError, IndexError):
                return f'/events/event-1.png'
        
        elif self.category and self.category.name == 'Activities':
            # For activities, use sequential numbering starting from 1
            activity_posts = BlogPost.objects.filter(
                category__name='Activities', 
                is_published=True
            ).order_by('id')
            try:
                activity_index = list(activity_posts.values_list('id', flat=True)).index(self.id) + 1
                return f'/activities/activity-{activity_index}.png'
            except (ValueError, IndexError):
                return f'/activities/activity-1.png'
        
        # Default fallback for other blog posts
        return f'/blog/blog-{self.id}.png'
    
    @property
    def comments_count(self):
        """Get total comments count."""
        return self.comments.filter(is_approved=True).count()


class BlogComment(TimeStampedModel):
    """Blog comment model."""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100, help_text="Commenter name")
    email = models.EmailField(help_text="Commenter email")
    website = models.URLField(blank=True, help_text="Commenter website")
    content = models.TextField(help_text="Comment content")
    
    # Moderation
    is_approved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Threading (for replies)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Blog Comment"
        verbose_name_plural = "Blog Comments"
    
    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
    
    @property
    def is_reply(self):
        """Check if this is a reply to another comment."""
        return self.parent is not None


class BlogCategory(TimeStampedModel):
    """Blog-specific category model."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007751', help_text="Hex color code")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class name")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def posts_count(self):
        """Get count of published posts in this category."""
        return BlogPost.objects.filter(category=self, status='published', is_published=True).count()


class BlogTag(TimeStampedModel):
    """Blog tag model."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Newsletter(TimeStampedModel):
    """Newsletter subscription model."""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        default='weekly'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
    
    def __str__(self):
        return f"{self.email} ({self.frequency})"


class BlogStats(TimeStampedModel):
    """Blog statistics model."""
    post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='stats')
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    monthly_views = models.PositiveIntegerField(default=0)
    weekly_views = models.PositiveIntegerField(default=0)
    daily_views = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    total_likes = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)
    bounce_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0,
        help_text="Bounce rate percentage"
    )
    avg_time_on_page = models.PositiveIntegerField(default=0, help_text="Average time in seconds")
    
    class Meta:
        verbose_name_plural = "Blog Stats"
    
    def __str__(self):
        return f"{self.post.title} - Stats"
