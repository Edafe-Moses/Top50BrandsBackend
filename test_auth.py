#!/usr/bin/env python
"""
Test the dashboard authentication system
"""
import requests
import json

# Test credentials
USERNAME = 'user'
PASSWORD = 'admin'
BASE_URL = 'http://127.0.0.1:8000'

def test_authentication():
    """Test the complete authentication flow"""
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🔐 Testing Dashboard Authentication")
    print("=" * 50)
    
    # Test 1: Try to access stats without authentication
    print("\n1. Testing unauthenticated access to stats...")
    try:
        response = session.get(f'{BASE_URL}/api/dashboard/stats/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Login
    print("\n2. Testing login...")
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    try:
        response = session.post(
            f'{BASE_URL}/api/dashboard/auth/login/',
            json=login_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Login successful!")
        else:
            print("   ❌ Login failed!")
            return
            
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 3: Try to access stats after authentication
    print("\n3. Testing authenticated access to stats...")
    try:
        response = session.get(f'{BASE_URL}/api/dashboard/stats/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")  # Truncate long response
        
        if response.status_code == 200:
            print("   ✅ Stats access successful!")
        else:
            print("   ❌ Stats access failed!")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Test logout
    print("\n4. Testing logout...")
    try:
        response = session.post(f'{BASE_URL}/api/dashboard/auth/logout/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Logout successful!")
        else:
            print("   ❌ Logout failed!")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Try to access stats after logout
    print("\n5. Testing access after logout...")
    try:
        response = session.get(f'{BASE_URL}/api/dashboard/stats/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   ✅ Properly denied access after logout!")
        else:
            print("   ❌ Should be denied access after logout!")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Authentication test completed!")

if __name__ == '__main__':
    test_authentication()
