"""
Dataset model for database operations.
Handles CRUD operations for datasets.
"""

from typing import Optional, List, Dict
import json
import logging
from app.db import get_db_cursor

logger = logging.getLogger(__name__)


class DatasetModel:
    """Dataset model for database operations"""

    @staticmethod
    def create_dataset(
        name: str,
        description: Optional[str],
        user_id: int,
        file_path: Optional[str] = None,
        file_name: Optional[str] = None,
        file_size: Optional[int] = None,
        row_count: Optional[int] = None,
        column_count: Optional[int] = None,
    ) -> Optional[Dict]:
        """
        Create dataset and return created row.
        """
        query = """
        INSERT INTO datasets
        (name, description, user_id, file_path, file_name, file_size, row_count, column_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """

        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    query,
                    (
                        name,
                        description,
                        user_id,
                        file_path,
                        file_name,
                        file_size,
                        row_count,
                        column_count,
                    ),
                )
                dataset_id = cursor.lastrowid

                cursor.execute(
                    """
                    SELECT id, name, description, user_id, file_path,
                           file_name, file_size, row_count, column_count,
                           created_at
                    FROM datasets
                    WHERE id = ?
                    """,
                    (dataset_id,),
                )

                row = cursor.fetchone()
                return dict(row) if row else None

        except Exception as e:
            logger.error(f"Create dataset failed: {e}", exc_info=True)
            return None

    @staticmethod
    def get_datasets_by_user(user_id: int) -> List[Dict]:
        query = """
        SELECT id, name, description, user_id, file_path,
               file_name, file_size, row_count, column_count,
               created_at
        FROM datasets
        WHERE user_id = ?
        ORDER BY created_at DESC;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_all_datasets() -> List[Dict]:
        query = """
        SELECT d.id, d.name, d.description, d.user_id, d.file_path,
               d.file_name, d.file_size, d.row_count, d.column_count,
               d.created_at, u.username AS owner_username, u.email AS owner_email
        FROM datasets d
        JOIN users u ON d.user_id = u.id
        ORDER BY d.created_at DESC;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_dataset_by_id(dataset_id: int) -> Optional[Dict]:
        query = """
        SELECT id, name, description, user_id, file_path,
               file_name, file_size, row_count, column_count,
               created_at
        FROM datasets
        WHERE id = ?;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (dataset_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def delete_dataset(dataset_id: int, user_id: int) -> bool:
        query = "DELETE FROM datasets WHERE id = ? AND user_id = ?;"
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(query, (dataset_id, user_id))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Delete dataset failed: {e}", exc_info=True)
            return False

    @staticmethod
    def save_column_metadata(dataset_id: int, columns: List[Dict]) -> bool:
        query = """
        INSERT INTO dataset_columns
        (dataset_id, column_name, column_type, column_index)
        VALUES (?, ?, ?, ?);
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                for col in columns:
                    cursor.execute(
                        query,
                        (dataset_id, col["name"], col["type"], col["index"]),
                    )
            return True
        except Exception as e:
            logger.error(f"Save column metadata failed: {e}", exc_info=True)
            return False

    @staticmethod
    def get_column_metadata(dataset_id: int) -> List[Dict]:
        query = """
        SELECT id, column_name, column_type, column_index
        FROM dataset_columns
        WHERE dataset_id = ?
        ORDER BY column_index;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (dataset_id,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def save_quality_report(
        dataset_id: int,
        total_rows: int,
        total_columns: int,
        duplicate_rows: int,
        null_counts: Dict,
        completeness_score: float,
    ) -> Optional[int]:
        query = """
        INSERT INTO quality_reports
        (dataset_id, total_rows, total_columns, duplicate_rows, null_counts, completeness_score)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        try:
            with get_db_cursor(commit=True) as cursor:
                cursor.execute(
                    query,
                    (
                        dataset_id,
                        total_rows,
                        total_columns,
                        duplicate_rows,
                        json.dumps(null_counts),
                        completeness_score,
                    ),
                )
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Save quality report failed: {e}", exc_info=True)
            return None

    @staticmethod
    def get_quality_report(dataset_id: int) -> Optional[Dict]:
        query = """
        SELECT id, total_rows, total_columns, duplicate_rows,
               null_counts, completeness_score, generated_at
        FROM quality_reports
        WHERE dataset_id = ?
        ORDER BY generated_at DESC
        LIMIT 1;
        """
        with get_db_cursor() as cursor:
            cursor.execute(query, (dataset_id,))
            row = cursor.fetchone()
            if not row:
                return None

            data = dict(row)
            data["null_counts"] = json.loads(data["null_counts"]) if data["null_counts"] else {}
            return data
