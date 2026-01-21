#!/usr/bin/env python3
"""
API Test Script
Tests all endpoints of the Multi-User Dataset Management Platform
Run this after starting the server to verify everything works.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(test_name):
    print(f"\n{BLUE}[TEST]{RESET} {test_name}")

def print_success(message):
    print(f"{GREEN}✓{RESET} {message}")

def print_error(message):
    print(f"{RED}✗{RESET} {message}")

def print_info(message):
    print(f"{YELLOW}ℹ{RESET} {message}")

def test_health_check():
    """Test if server is running"""
    print_test("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success(f"Server is running: {response.json()}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server. Is it running on http://localhost:8000?")
        return False

def test_register_user():
    """Test user registration"""
    print_test("User Registration")
    
    # Test regular user
    user_data = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass123",
        "role": "user"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    
    if response.status_code == 201:
        print_success("Regular user registered successfully")
        print_info(f"User ID: {response.json()['id']}")
        return True
    elif response.status_code == 400:
        print_info("User already exists (OK if running test multiple times)")
        return True
    else:
        print_error(f"Failed to register: {response.text}")
        return False

def test_register_admin():
    """Test admin registration"""
    print_test("Admin Registration")
    
    admin_data = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=admin_data)
    
    if response.status_code == 201:
        print_success("Admin user registered successfully")
        return True
    elif response.status_code == 400:
        print_info("Admin already exists (OK if running test multiple times)")
        return True
    else:
        print_error(f"Failed to register admin: {response.text}")
        return False

def test_login_user():
    """Test user login and get token"""
    print_test("User Login")
    
    login_data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print_success("User logged in successfully")
        print_info(f"Token: {token[:30]}...")
        return token
    else:
        print_error(f"Failed to login: {response.text}")
        return None

def test_login_admin():
    """Test admin login and get token"""
    print_test("Admin Login")
    
    login_data = {
        "email": "admin@example.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print_success("Admin logged in successfully")
        return token
    else:
        print_error(f"Failed to login admin: {response.text}")
        return None

def test_get_current_user(token):
    """Test getting current user info"""
    print_test("Get Current User Info")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print_success(f"Retrieved user: {user['username']} ({user['email']})")
        print_info(f"Role: {user['role']}")
        return True
    else:
        print_error(f"Failed to get user info: {response.text}")
        return False

def test_create_dataset(token):
    """Test creating a dataset"""
    print_test("Create Dataset")
    
    dataset_data = {
        "name": "Test Dataset 1",
        "description": "This is a test dataset created by automated test",
        "file_path": "/uploads/test1.csv"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/datasets/", json=dataset_data, headers=headers)
    
    if response.status_code == 201:
        dataset = response.json()
        print_success(f"Dataset created: {dataset['name']} (ID: {dataset['id']})")
        return dataset['id']
    else:
        print_error(f"Failed to create dataset: {response.text}")
        return None

def test_get_user_datasets(token):
    """Test getting user's datasets"""
    print_test("Get User Datasets")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/datasets/", headers=headers)
    
    if response.status_code == 200:
        datasets = response.json()
        print_success(f"Retrieved {len(datasets)} dataset(s)")
        for ds in datasets:
            print_info(f"  - {ds['name']} (ID: {ds['id']})")
        return True
    else:
        print_error(f"Failed to get datasets: {response.text}")
        return False

def test_admin_view_all(admin_token):
    """Test admin viewing all datasets"""
    print_test("Admin View All Datasets")
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/datasets/", headers=headers)
    
    if response.status_code == 200:
        datasets = response.json()
        print_success(f"Admin retrieved {len(datasets)} dataset(s) from all users")
        for ds in datasets:
            owner = ds.get('owner_username', 'unknown')
            print_info(f"  - {ds['name']} (Owner: {owner})")
        return True
    else:
        print_error(f"Failed to get all datasets: {response.text}")
        return False

def test_unauthorized_access():
    """Test accessing protected route without token"""
    print_test("Unauthorized Access (Should Fail)")
    
    response = requests.get(f"{BASE_URL}/datasets/")
    
    if response.status_code == 401 or response.status_code == 403:
        print_success("Correctly rejected request without token")
        return True
    else:
        print_error(f"Should have rejected, but got: {response.status_code}")
        return False

def test_invalid_login():
    """Test login with wrong password"""
    print_test("Invalid Login (Should Fail)")
    
    login_data = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 401:
        print_success("Correctly rejected invalid credentials")
        return True
    else:
        print_error(f"Should have rejected, but got: {response.status_code}")
        return False

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Multi-User Dataset Management Platform - API Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Run tests
    tests_passed = 0
    tests_failed = 0
    
    # 1. Health check
    if not test_health_check():
        print_error("\nServer is not running. Start it with: python app/main.py")
        sys.exit(1)
    tests_passed += 1
    
    # 2. Register users
    if test_register_user():
        tests_passed += 1
    else:
        tests_failed += 1
    
    if test_register_admin():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 3. Test invalid login
    if test_invalid_login():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 4. Login users
    user_token = test_login_user()
    if user_token:
        tests_passed += 1
    else:
        tests_failed += 1
        print_error("\nCannot continue without user token")
        sys.exit(1)
    
    admin_token = test_login_admin()
    if admin_token:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 5. Get user info
    if test_get_current_user(user_token):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 6. Test unauthorized access
    if test_unauthorized_access():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 7. Create dataset
    dataset_id = test_create_dataset(user_token)
    if dataset_id:
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 8. Get user datasets
    if test_get_user_datasets(user_token):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # 9. Admin view all
    if admin_token and test_admin_view_all(admin_token):
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}Passed:{RESET} {tests_passed}")
    print(f"{RED}Failed:{RESET} {tests_failed}")
    
    if tests_failed == 0:
        print(f"\n{GREEN}✓ All tests passed! Your API is working correctly.{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}✗ Some tests failed. Check the output above.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
