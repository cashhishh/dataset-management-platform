"""
Dataset model for database operations.
Handles CRUD operations for datasets with role-based access control.
"""
from typing import Optional, List, Dict
from app.db import get_db_cursor
import logging

logger = logging.getLogger(__name__)


class DatasetModel:
    """Dataset model for database operations"""
    
    @staticmethod
    def create_dataset(name: str, description: str, user_id: int, file_path: str = None) -> Optional[Dict]:
        """
        Create a new dataset for a user.
        
        Args:
            name: Dataset name
            description: Dataset description
            user_id: Owner's user ID
            file_path: Optional file path
        
        Returns:
            Dictionary with dataset data if successful, None if failed
        """
        query = """
        INSERT INTO datasets (name, description, user_id, file_path)
        VALUES (?, ?, ?, ?);
        """
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (name, description, user_id, file_path))
                dataset_id = cursor.lastrowid
                
                # Fetch the created dataset
                cursor.execute(
                    "SELECT id, name, description, user_id, file_path, created_at FROM datasets WHERE id = ?",
                    (dataset_id,)
                )
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "name": result[1],
                        "description": result[2],
                        "user_id": result[3],
                        "file_path": result[4],
                        "created_at": result[5]
                    }
        except Exception as e:
            logger.error(f"Error creating dataset: {e}")
            return None
    
    @staticmethod
    def get_datasets_by_user(user_id: int) -> List[Dict]:
        """
        Get all datasets owned by a specific user.
        
        Args:
            user_id: Owner's user ID
        
        Returns:
            List of dataset dictionaries
        """
        query = """
        SELECT id, name, description, user_id, file_path, created_at
        FROM datasets
        WHERE user_id = ?
        ORDER BY created_at DESC;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                
                return [
                    {
                        "id": row[0],
                        "name": row[1],
                        "description": row[2],
                        "user_id": row[3],
                        "file_path": row[4],
                        "created_at": row[5]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error fetching datasets for user: {e}")
            return []
    
    @staticmethod
    def get_all_datasets() -> List[Dict]:
        """
        Get all datasets in the system (admin only).
        
        Returns:
            List of all dataset dictionaries with owner info
        """
        query = """
        SELECT d.id, d.name, d.description, d.user_id, d.file_path, d.created_at,
               u.username, u.email
        FROM datasets d
        JOIN users u ON d.user_id = u.id
        ORDER BY d.created_at DESC;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                
                return [
                    {
                        "id": row[0],
                        "name": row[1],
                        "description": row[2],
                        "user_id": row[3],
                        "file_path": row[4],
                        "created_at": row[5],
                        "owner_username": row[6],
                        "owner_email": row[7]
                    }
                    for row in results
                ]
        except Exception as e:
            logger.error(f"Error fetching all datasets: {e}")
            return []
    
    @staticmethod
    def get_dataset_by_id(dataset_id: int) -> Optional[Dict]:
        """
        Get a specific dataset by ID.
        
        Args:
            dataset_id: Dataset ID
        
        Returns:
            Dataset dictionary if found, None otherwise
        """
        query = """
        SELECT id, name, description, user_id, file_path, created_at
        FROM datasets
        WHERE id = ?;
        """
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, (dataset_id,))
                result = cursor.fetchone()
                
                if result:
                    return {
                        "id": result[0],
                        "name": result[1],
                        "description": result[2],
                        "user_id": result[3],
                        "file_path": result[4],
                        "created_at": result[5]
                    }
        except Exception as e:
            logger.error(f"Error fetching dataset by ID: {e}")
            return None
    
    @staticmethod
    def delete_dataset(dataset_id: int, user_id: int) -> bool:
        """
        Delete a dataset (only by owner).
        
        Args:
            dataset_id: Dataset ID to delete
            user_id: User ID requesting deletion
        
        Returns:
            True if deleted successfully, False otherwise
        """
        query = """
        DELETE FROM datasets
        WHERE id = ? AND user_id = ?;
        """
        
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (dataset_id, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting dataset: {e}")
            return False
