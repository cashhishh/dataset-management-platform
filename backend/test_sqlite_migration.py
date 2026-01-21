"""
Quick test script to verify SQLite migration is working.
Run this before starting the server to catch any errors.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports work"""
    print("Testing imports...")
    try:
        from app.db import init_db_pool, create_tables, close_db_pool
        from app.models.user import UserModel
        from app.models.dataset import DatasetModel
        from app.core.security import hash_password, verify_password
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_database_init():
    """Test database initialization"""
    print("\nTesting database initialization...")
    try:
        from app.db import init_db_pool, create_tables
        
        # Remove old db file if exists
        if os.path.exists("dataset_platform.db"):
            os.remove("dataset_platform.db")
            print("  - Removed old database file")
        
        init_db_pool()
        print("✓ Database initialized")
        return True
    except Exception as e:
        print(f"✗ Database init error: {e}")
        return False

def test_user_operations():
    """Test user model operations"""
    print("\nTesting user operations...")
    try:
        from app.models.user import UserModel
        
        # Test create user
        user = UserModel.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",
            role="user"
        )
        
        if not user:
            print("✗ Failed to create user")
            return False
        print(f"✓ User created: {user['username']}")
        
        # Test get user by email
        found_user = UserModel.get_user_by_email("test@example.com")
        if not found_user:
            print("✗ Failed to get user by email")
            return False
        print(f"✓ User found by email: {found_user['email']}")
        
        # Test get user by username
        found_user2 = UserModel.get_user_by_username("testuser")
        if not found_user2:
            print("✗ Failed to get user by username")
            return False
        print(f"✓ User found by username: {found_user2['username']}")
        
        # Test user exists
        exists = UserModel.user_exists(email="test@example.com")
        if not exists:
            print("✗ User exists check failed")
            return False
        print("✓ User exists check passed")
        
        return True
    except Exception as e:
        print(f"✗ User operation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dataset_operations():
    """Test dataset model operations"""
    print("\nTesting dataset operations...")
    try:
        from app.models.dataset import DatasetModel
        from app.models.user import UserModel
        
        # Get user ID
        user = UserModel.get_user_by_email("test@example.com")
        user_id = user['id']
        
        # Test create dataset
        dataset = DatasetModel.create_dataset(
            name="Test Dataset",
            description="Test description",
            user_id=user_id,
            file_path="/test/path.csv"
        )
        
        if not dataset:
            print("✗ Failed to create dataset")
            return False
        print(f"✓ Dataset created: {dataset['name']}")
        
        # Test get datasets by user
        datasets = DatasetModel.get_datasets_by_user(user_id)
        if not datasets:
            print("✗ Failed to get datasets by user")
            return False
        print(f"✓ Found {len(datasets)} dataset(s) for user")
        
        # Test get dataset by id
        dataset_found = DatasetModel.get_dataset_by_id(dataset['id'])
        if not dataset_found:
            print("✗ Failed to get dataset by id")
            return False
        print(f"✓ Dataset found by ID: {dataset_found['name']}")
        
        # Test delete dataset
        success = DatasetModel.delete_dataset(dataset['id'], user_id)
        if not success:
            print("✗ Failed to delete dataset")
            return False
        print("✓ Dataset deleted successfully")
        
        return True
    except Exception as e:
        print(f"✗ Dataset operation error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SQLite Migration Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database_init,
        test_user_operations,
        test_dataset_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n✓ All tests passed! SQLite migration is working correctly.")
        print("You can now start the server with: uvicorn app.main:app --reload")
    else:
        print(f"\n✗ {failed} test(s) failed. Please fix the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
