"""
Database connection and initialization module.
Manages PostgreSQL connection pool and schema creation.
"""
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

# Database configuration - DEV ONLY
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "dataset_platform",
    "user": "postgres",
    "password": "postgres"  # DEV ONLY – move to env var in production
}

# Connection pool
connection_pool = None


def init_db_pool(min_conn=1, max_conn=10):
    """
    Initialize PostgreSQL connection pool.
    """
    global connection_pool
    try:
        connection_pool = SimpleConnectionPool(
            min_conn,
            max_conn,
            **DB_CONFIG
        )
        logger.info("Database connection pool created successfully")
    except Exception as e:
        logger.error(f"Error creating connection pool: {e}")
        raise


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    """
    if connection_pool is None:
        raise RuntimeError("Database connection pool is not initialized")

    conn = None
    try:
        conn = connection_pool.getconn()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)


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
    """
    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
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
        id SERIAL PRIMARY KEY,
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
    Close all connections in the pool.
    """
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        logger.info("Database connection pool closed")
