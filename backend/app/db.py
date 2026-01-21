"""
Database connection and initialization module.
Manages SQLite connection and schema creation.
"""
import sqlite3
from contextlib import contextmanager
import logging
import threading

logger = logging.getLogger(__name__)

# Database configuration - SQLite for local development
DB_PATH = "sqlite:///./dataset_platform.db"
DB_FILE = "./dataset_platform.db"

# Thread-local storage for SQLite connections
_thread_local = threading.local()


def init_db_pool(min_conn=1, max_conn=10):
    """
    Initialize database (SQLite doesn't need connection pool initialization).
    This function is kept for API compatibility.
    """
    logger.info("Using SQLite database (connection pool not needed)")
    # Create database file and tables if they don't exist
    create_tables()


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    SQLite uses thread-local connections for thread safety.
    """
    # Get or create connection for this thread
    if not hasattr(_thread_local, 'connection') or _thread_local.connection is None:
        _thread_local.connection = sqlite3.connect(
            DB_FILE,
            check_same_thread=False,
            timeout=30.0
        )
        _thread_local.connection.row_factory = sqlite3.Row
    
    conn = _thread_local.connection
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise


@contextmanager
def get_db_cursor(commit=False):
    """
    Context manager for database cursors with automatic commit/rollback.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()


def create_tables():
    """
    Create database tables if they don't exist.
    SQLite syntax: AUTOINCREMENT instead of SERIAL.
    """
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) UNIQUE NOT NULL,
        username VARCHAR(100) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    datasets_table = """
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        file_path VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    user_id_index = """
    CREATE INDEX IF NOT EXISTS idx_datasets_user_id 
    ON datasets(user_id);
    """

    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(users_table)
            cursor.execute(datasets_table)
            cursor.execute(user_id_index)
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


def close_db_pool():
    """
    Close database connection.
    """
    if hasattr(_thread_local, 'connection') and _thread_local.connection:
        _thread_local.connection.close()
        _thread_local.connection = None
        logger.info("Database connection closed")
