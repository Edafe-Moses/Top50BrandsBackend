#!/usr/bin/env python
"""
Test session handling with credentials: 'include'
"""
import requests
import json

# Test credentials
USERNAME = 'user'
PASSWORD = 'admin'
BASE_URL = 'http://127.0.0.1:8000'

def test_session_with_credentials():
    """Test session handling like the frontend does"""
    
    print("🔐 Testing Session with credentials: 'include'")
    print("=" * 60)
    
    # Test 1: Login and get session cookie
    print("\n1. Testing login to get session cookie...")
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    try:
        # Login request
        login_response = requests.post(
            f'{BASE_URL}/api/dashboard/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Login Status: {login_response.status_code}")
        print(f"   Login Response: {login_response.text}")
        
        if login_response.status_code != 200:
            print("   ❌ Login failed!")
            return
        
        # Get session cookie
        session_cookie = login_response.cookies.get('sessionid')
        print(f"   Session Cookie: {session_cookie}")
        
        if not session_cookie:
            print("   ❌ No session cookie received!")
            return
        
        print("   ✅ Login successful with session cookie!")
        
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Use session cookie for stats request
    print("\n2. Testing stats request with session cookie...")
    try:
        # Stats request with session cookie
        stats_response = requests.get(
            f'{BASE_URL}/api/dashboard/stats/',
            cookies={'sessionid': session_cookie}
        )
        
        print(f"   Stats Status: {stats_response.status_code}")
        print(f"   Stats Response: {stats_response.text[:200]}...")
        
        if stats_response.status_code == 200:
            print("   ✅ Stats access successful with session cookie!")
        else:
            print("   ❌ Stats access failed even with session cookie!")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Session test completed!")

if __name__ == '__main__':
    test_session_with_credentials()
