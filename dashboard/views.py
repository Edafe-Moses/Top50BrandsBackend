from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from django.core.cache import cache
from django.core.management import call_command
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
import os

from .models import YearlyRanking, DashboardUser, DataMigrationLog, SystemConfiguration
from .serializers import (
    YearlyRankingSerializer, DashboardUserSerializer, 
    DataMigrationLogSerializer, SystemConfigurationSerializer,
    LoginSerializer, DashboardStatsSerializer
)
from brands.models import Brand
from blog.models import BlogPost
from insights.models import Insight
from api.serializers import BrandListSerializer, BlogPostListSerializer, InsightListSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admins to edit."""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_staff or request.user.is_superuser


@api_view(['POST'])
@permission_classes([])
def dashboard_login(request):
    """Login endpoint for dashboard users."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            # Check if user has dashboard access
            try:
                dashboard_profile = user.dashboard_profile
                if not user.is_active:
                    return Response(
                        {'error': 'Account is disabled'}, 
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                
                login(request, user)
                
                # Update login tracking
                dashboard_profile.last_login_dashboard = timezone.now()
                dashboard_profile.login_count += 1
                dashboard_profile.save()
                
                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                    },
                    'dashboard_profile': DashboardUserSerializer(dashboard_profile).data,
                    'message': 'Login successful'
                })
                
            except DashboardUser.DoesNotExist:
                return Response(
                    {'error': 'No dashboard access permissions'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dashboard_logout(request):
    """Logout endpoint for dashboard users."""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics."""
    try:
        dashboard_profile = request.user.dashboard_profile
    except DashboardUser.DoesNotExist:
        return Response(
            {'error': 'No dashboard access'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Get current year
    current_year = YearlyRanking.objects.filter(is_active=True).first()
    current_year_num = current_year.year if current_year else 2025
    
    # Calculate stats
    stats = {
        'current_year': current_year_num,
        'total_years': YearlyRanking.objects.count(),
        'published_years': YearlyRanking.objects.filter(is_published=True).count(),
        'total_brands': Brand.objects.filter(year=current_year_num).count(),
        'total_blog_posts': BlogPost.objects.filter(year=current_year_num).count(),
        'total_insights': Insight.objects.filter(year=current_year_num).count(),
        'recent_migrations': DataMigrationLog.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count(),
        'user_role': dashboard_profile.role,
        'user_permissions': {
            'can_create_years': dashboard_profile.can_create_years,
            'can_edit_brands': dashboard_profile.can_edit_brands,
            'can_publish_content': dashboard_profile.can_publish_content,
            'can_manage_users': dashboard_profile.can_manage_users,
        },
        'assigned_years': list(dashboard_profile.assigned_years.values_list('year', flat=True)),
    }
    
    serializer = DashboardStatsSerializer(stats)
    return Response(serializer.data)


class YearlyRankingViewSet(viewsets.ModelViewSet):
    """ViewSet for managing yearly rankings."""
    queryset = YearlyRanking.objects.all()
    serializer_class = YearlyRankingSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering = ['-year']
    
    def get_queryset(self):
        """Filter based on user permissions."""
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        
        try:
            dashboard_profile = user.dashboard_profile
            if dashboard_profile.role == 'admin':
                return self.queryset
            else:
                # Return only assigned years
                return self.queryset.filter(
                    id__in=dashboard_profile.assigned_years.values_list('id', flat=True)
                )
        except DashboardUser.DoesNotExist:
            return self.queryset.none()
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        """Set a year as the active year."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        year_ranking = self.get_object()
        
        # Deactivate all other years
        YearlyRanking.objects.filter(is_active=True).update(is_active=False)
        
        # Activate this year
        year_ranking.is_active = True
        year_ranking.save()
        
        return Response({
            'message': f'Year {year_ranking.year} is now active',
            'active_year': year_ranking.year
        })
    
    @action(detail=True, methods=['post'])
    def duplicate_year(self, request, pk=None):
        """Duplicate a year's structure for a new year."""
        if not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        source_year = self.get_object()
        new_year = request.data.get('new_year')
        
        if not new_year:
            return Response(
                {'error': 'new_year is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_year = int(new_year)
        except ValueError:
            return Response(
                {'error': 'new_year must be a valid year'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if year already exists
        if YearlyRanking.objects.filter(year=new_year).exists():
            return Response(
                {'error': f'Year {new_year} already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new year
        new_year_ranking = YearlyRanking.objects.create(
            year=new_year,
            title=f"Top 50 Most Valuable Brands in Nigeria {new_year}",
            description=f"The {new_year} edition of Nigeria's most comprehensive brand ranking.",
            is_active=False,
            is_published=False,
            is_complete=False,
            total_brands=source_year.total_brands,
            research_methodology=source_year.research_methodology,
            research_lead=request.user,
        )
        
        # Log the migration
        DataMigrationLog.objects.create(
            migration_type='new_year_setup',
            from_year=source_year.year,
            to_year=new_year,
            description=f'Created new year {new_year} based on {source_year.year}',
            initiated_by=request.user,
            status='completed',
            items_total=1,
            items_processed=1,
            started_at=timezone.now(),
            completed_at=timezone.now(),
        )
        
        return Response({
            'message': f'Year {new_year} created successfully',
            'year_data': YearlyRankingSerializer(new_year_ranking).data
        })


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing system configurations."""
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter configurations based on user permissions."""
        queryset = self.queryset.filter(is_active=True)
        
        # Non-admin users can only see public configurations
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_public=True)
        
        return queryset
    
    def update(self, request, *args, **kwargs):
        """Override update to check admin requirements."""
        instance = self.get_object()
        
        if instance.requires_admin and not request.user.is_staff:
            return Response(
                {'error': 'Admin access required to modify this configuration'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)


class DataMigrationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing data migration logs."""
    queryset = DataMigrationLog.objects.all()
    serializer_class = DataMigrationLogSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter logs based on user permissions."""
        if self.request.user.is_staff:
            return self.queryset
        
        # Regular users can only see their own migrations
        return self.queryset.filter(initiated_by=self.request.user)


class DashboardUserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing dashboard users."""
    queryset = User.objects.filter(dashboard_profile__isnull=False)
    serializer_class = DashboardUserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        """Filter users based on permissions."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_superuser:
            # Staff users can only see non-superuser accounts
            queryset = queryset.filter(is_superuser=False)
        
        return queryset

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset user password."""
        user = self.get_object()
        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response(
                {'error': 'new_password is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password reset successfully'})

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle user active status."""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        
        return Response({
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully',
            'is_active': user.is_active
        })


class DashboardBrandViewSet(viewsets.ModelViewSet):
    """ViewSet for managing brands through dashboard."""
    queryset = Brand.objects.all()
    serializer_class = BrandListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter brands based on user permissions."""
        queryset = super().get_queryset()
        user = self.request.user
        year = self.request.query_params.get('year')
        
        if year:
            queryset = queryset.filter(year=year)
        
        if not user.is_staff and hasattr(user, 'dashboard_profile'):
            # Non-staff users can only see brands for their assigned years
            assigned_years = user.dashboard_profile.assigned_years.values_list('year', flat=True)
            queryset = queryset.filter(year__in=assigned_years)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the creator when creating a brand."""
        # Default to current year if not specified
        if 'year' not in serializer.validated_data:
            current_year = YearlyRanking.objects.filter(is_active=True).first()
            if current_year:
                serializer.save(year=current_year.year)
            else:
                serializer.save(year=2025)
        else:
            serializer.save()


class DashboardBlogViewSet(viewsets.ModelViewSet):
    """ViewSet for managing blog posts through dashboard."""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostListSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter blog posts based on user permissions."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff and hasattr(user, 'dashboard_profile'):
            profile = user.dashboard_profile
            if not profile.can_publish_content:
                # Users without publish permission can only see their own posts
                queryset = queryset.filter(author=user.get_full_name() or user.username)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author when creating a blog post."""
        author_name = self.request.user.get_full_name() or self.request.user.username
        serializer.save(author=author_name)


class DashboardInsightViewSet(viewsets.ModelViewSet):
    """ViewSet for managing insights through dashboard."""
    queryset = Insight.objects.all()
    serializer_class = InsightListSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter insights based on user permissions."""
        queryset = super().get_queryset()
        user = self.request.user
        
        if not user.is_staff and hasattr(user, 'dashboard_profile'):
            profile = user.dashboard_profile
            if not profile.can_publish_content:
                # Users without publish permission can only see their own insights
                queryset = queryset.filter(author=user.get_full_name() or user.username)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author when creating an insight."""
        author_name = self.request.user.get_full_name() or self.request.user.username
        serializer.save(author=author_name)


from blog.models import BlogTag
from .serializers import BlogTagSerializer

class DashboardBlogTagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for listing all blog tags for dashboard use."""
    queryset = BlogTag.objects.all()
    serializer_class = BlogTagSerializer
    permission_classes = [IsAuthenticated]


# System Management Views
@api_view(['POST'])
@permission_classes([IsAdminUser])
def system_backup_view(request):
    """Create a system backup."""
    try:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create database backup using Django's dumpdata command
        call_command('dumpdata', '--output', f'/tmp/{backup_name}.json', '--indent', '2')
        
        return Response({
            'message': 'Backup created successfully',
            'backup_name': backup_name,
            'created_at': datetime.now().isoformat()
        })
    except Exception as e:
        return Response(
            {'error': f'Backup failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def system_restore_view(request):
    """Restore system from backup."""
    backup_file = request.data.get('backup_file')
    
    if not backup_file:
        return Response(
            {'error': 'backup_file is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Restore from backup using Django's loaddata command
        call_command('loaddata', backup_file)
        
        return Response({
            'message': 'System restored successfully',
            'restored_from': backup_file,
            'restored_at': datetime.now().isoformat()
        })
    except Exception as e:
        return Response(
            {'error': f'Restore failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_health_view(request):
    """Get system health status."""
    try:
        # Check database connectivity
        db_status = 'healthy'
        try:
            User.objects.count()
        except Exception:
            db_status = 'unhealthy'
        
        # Check cache connectivity
        cache_status = 'healthy'
        try:
            cache.set('health_check', 'ok', 10)
            if cache.get('health_check') != 'ok':
                cache_status = 'unhealthy'
        except Exception:
            cache_status = 'unhealthy'
        
        # Get system stats
        stats = {
            'database': db_status,
            'cache': cache_status,
            'total_users': User.objects.count(),
            'total_brands': Brand.objects.count(),
            'total_blog_posts': BlogPost.objects.count(),
            'total_insights': Insight.objects.count(),
            'active_years': YearlyRanking.objects.filter(is_active=True).count(),
            'published_years': YearlyRanking.objects.filter(is_published=True).count(),
            'recent_logins': User.objects.filter(
                last_login__gte=timezone.now() - timedelta(days=7)
            ).count(),
            'system_time': datetime.now().isoformat(),
        }
        
        overall_status = 'healthy' if db_status == 'healthy' and cache_status == 'healthy' else 'degraded'
        
        return Response({
            'status': overall_status,
            'components': {
                'database': db_status,
                'cache': cache_status
            },
            'stats': stats,
            'checked_at': datetime.now().isoformat()
        })
    except Exception as e:
        return Response(
            {'error': f'Health check failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_cache_view(request):
    """Clear system cache."""
    try:
        cache.clear()
        return Response({
            'message': 'Cache cleared successfully',
            'cleared_at': datetime.now().isoformat()
        })
    except Exception as e:
        return Response(
            {'error': f'Cache clear failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
