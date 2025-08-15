"""
Custom middleware for dashboard authentication
"""
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin


class DashboardSessionMiddleware(MiddlewareMixin):
    """
    Custom middleware to handle dashboard session authentication
    """
    
    def process_request(self, request):
        """
        Process incoming request to check for dashboard session
        """
        # Only apply to dashboard API endpoints
        if not request.path.startswith('/api/dashboard/'):
            return None
        
        print(f"🔧 Dashboard middleware processing: {request.path}")
        print(f"🔧 Cookies received: {request.COOKIES}")
        print(f"🔧 Headers: {dict(request.headers)}")

        # Check for Authorization header first (more reliable for cross-origin)
        auth_header = request.headers.get('Authorization', '')
        session_key = None

        if auth_header.startswith('Bearer '):
            session_key = auth_header[7:]  # Remove 'Bearer ' prefix
            print(f"🔧 Found session key in Authorization header: {session_key}")
        else:
            # Fallback to cookies
            dashboard_session = request.COOKIES.get('dashboard_session')
            sessionid = request.COOKIES.get('sessionid')
            session_key = dashboard_session or sessionid
            if session_key:
                print(f"🔧 Found session key in cookies: {session_key}")
        
        if session_key:
            print(f"🔧 Found session key: {session_key}")
            
            try:
                # Try to get the session
                session = Session.objects.get(session_key=session_key)
                session_data = session.get_decoded()
                
                print(f"🔧 Session data: {session_data}")
                
                # If session has user_id, try to authenticate
                user_id = session_data.get('user_id')
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        if user.is_staff:
                            # Manually set the user on the request
                            request.user = user
                            print(f"🔧 Authenticated user: {user.username}")
                        else:
                            print(f"🔧 User {user.username} is not staff")
                    except User.DoesNotExist:
                        print(f"🔧 User {user_id} not found")
                else:
                    print(f"🔧 No user_id in session")
                    
            except Session.DoesNotExist:
                print(f"🔧 Session {session_key} not found")
        else:
            print(f"🔧 No session key found in cookies")
        
        return None
