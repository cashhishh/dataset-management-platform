"""
User model for database operations.
Handles CRUD operations for users using raw SQL.
"""
from typing import Optional, List, Dict
from app.db import get_db_cursor
from app.core.security import hash_password
import logging

logger = logging.getLogger(__name__)


class UserModel:
    """User model for database operations"""
    
    @staticmethod
    def create_user(email: str, username: str, password: str, role: str = "user") -> Optional[Dict]:
        """
        Create a new user in the database.
        
        Args:
            email: User's email address
            username: User's username
            password: Plain text password (will be hashed)
            role: User role ('user' or 'admin')
        
        Returns:
            Dictionary with user data if successful, None if failed
        """
        hashed_pwd = hash_password(password)
        
        query = """
        INSERT INTO users (email, username, hashed_password, role)
        VALUES (?, ?, ?, ?);
        """
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (email, username, hashed_pwd, role))
                user_id = cursor.lastrowid
                
                # Fetch the created user
                cursor.execute(
                    "SELECT id, email, username, role, created_at FROM users WHERE id = ?",
                    (user_id,)
                )
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "email": result[1],
                        "username": result[2],
                        "role": result[3],
                        "created_at": result[4]
                    }
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """
        Retrieve user by email address.
        
        Args:
            email: User's email address
        
        Returns:
            Dictionary with user data including hashed password
        """
        query = """
        SELECT id, email, username, hashed_password, role, created_at
        FROM users
        WHERE email = ?;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (email,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "email": result[1],
                        "username": result[2],
                        "hashed_password": result[3],
                        "role": result[4],
                        "created_at": result[5]
                    }
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict]:
        """
        Retrieve user by username.
        
        Args:
            username: User's username
        
        Returns:
            Dictionary with user data including hashed password
        """
        query = """
        SELECT id, email, username, hashed_password, role, created_at
        FROM users
        WHERE username = ?;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "email": result[1],
                        "username": result[2],
                        "hashed_password": result[3],
                        "role": result[4],
                        "created_at": result[5]
                    }
        except Exception as e:
            logger.error(f"Error fetching user by username: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """
        Retrieve user by ID.
        
        Args:
            user_id: User's ID
        
        Returns:
            Dictionary with user data (without password)
        """
        query = """
        SELECT id, email, username, role, created_at
        FROM users
        WHERE id = ?;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "email": result[1],
                        "username": result[2],
                        "role": result[3],
                        "created_at": result[4]
                    }
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            return None
    
    @staticmethod
    def user_exists(email: str = None, username: str = None) -> bool:
        """
        Check if user exists by email or username.
        
        Args:
            email: User's email address
            username: User's username
        
        Returns:
            True if user exists, False otherwise
        """
        if email:
            query = "SELECT COUNT(*) FROM users WHERE email = ?;"
            param = (email,)
        elif username:
            query = "SELECT COUNT(*) FROM users WHERE username = ?;"
            param = (username,)
        else:
            return False
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, param)
                return cursor.fetchone()[0] > 0
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")
            return False
