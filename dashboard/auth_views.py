"""
Authentication views for the dashboard
"""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """
    Handle dashboard login
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({
                'error': 'Username and password are required'
            }, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:  # Only staff users can access dashboard
                login(request, user)

                # Force session creation and save
                if not request.session.session_key:
                    request.session.create()

                # Store additional session data
                request.session['user_id'] = user.id
                request.session['is_authenticated'] = True
                request.session.save()

                print(f"🔧 Created session: {request.session.session_key}")
                print(f"🔧 Session data: {dict(request.session)}")

                response = JsonResponse({
                    'success': True,
                    'session_key': request.session.session_key,  # For debugging
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                    }
                })

                # Set multiple cookie formats to ensure compatibility
                session_key = request.session.session_key

                # Standard Django session cookie
                response.set_cookie(
                    'sessionid',
                    session_key,
                    max_age=86400,
                    httponly=False,
                    samesite=None,
                    secure=False,
                    domain=None
                )

                # Alternative cookie for cross-origin
                response.set_cookie(
                    'dashboard_session',
                    session_key,
                    max_age=86400,
                    httponly=False,
                    samesite=None,
                    secure=False,
                    domain=None
                )

                print(f"🍪 Set cookies: sessionid={session_key}")

                return response
            else:
                return JsonResponse({
                    'error': 'Access denied. Staff privileges required.'
                }, status=403)
        else:
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """
    Handle dashboard logout
    """
    logout(request)
    return JsonResponse({'success': True})


@require_http_methods(["GET"])
def user_view(request):
    """
    Get current user information
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Authentication required'
        }, status=401)

    if not request.user.is_staff:
        return JsonResponse({
            'error': 'Access denied'
        }, status=403)
    
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
    })


@require_http_methods(["GET"])
def dashboard_stats_view(request):
    """
    Get dashboard statistics (existing functionality)
    """
    # Debug session info
    print(f"🔍 Session key: {request.session.session_key}")
    print(f"🔍 Session data: {dict(request.session)}")
    print(f"🔍 User: {request.user}")
    print(f"🔍 Cookies: {request.COOKIES}")

    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Authentication required',
            'debug': {
                'session_key': request.session.session_key,
                'cookies': list(request.COOKIES.keys()),
                'user': str(request.user)
            }
        }, status=401)

    if not request.user.is_staff:
        return JsonResponse({
            'error': 'Access denied'
        }, status=403)
    
    # Import here to avoid circular imports
    from brands.models import Brand
    from blog.models import BlogPost
    from insights.models import Insight
    from dashboard.models import YearlyRanking
    
    try:
        current_year = 2025
        total_years = YearlyRanking.objects.count()
        published_years = YearlyRanking.objects.filter(is_published=True).count()
        total_brands = Brand.objects.count()
        total_blog_posts = BlogPost.objects.count()
        total_insights = Insight.objects.count()
        
        # User permissions based on staff status
        user_permissions = {
            'can_create_years': request.user.is_superuser,
            'can_edit_brands': request.user.is_staff,
            'can_publish_content': request.user.is_staff,
            'can_manage_users': request.user.is_superuser,
        }
        
        # Get assigned years (for now, all years for staff users)
        assigned_years = list(YearlyRanking.objects.values_list('year', flat=True))
        
        return JsonResponse({
            'current_year': current_year,
            'total_years': total_years,
            'published_years': published_years,
            'total_brands': total_brands,
            'total_blog_posts': total_blog_posts,
            'total_insights': total_insights,
            'recent_migrations': 0,  # Placeholder
            'user_role': 'superuser' if request.user.is_superuser else 'staff',
            'user_permissions': user_permissions,
            'assigned_years': assigned_years,
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to load dashboard statistics'
        }, status=500)
