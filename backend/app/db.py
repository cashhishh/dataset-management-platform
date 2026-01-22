"""
Database connection and initialization module.
Manages SQLite connection, schema creation, and safe migration.
"""

import sqlite3
from contextlib import contextmanager
import logging
import threading
import os

logger = logging.getLogger(__name__)

# ✅ SINGLE SQLite database file
DB_FILE = "./dataset_platform.db"

# Thread-local storage
_thread_local = threading.local()


def init_db_pool(min_conn=None, max_conn=None):
    """
    Initialize SQLite database.

    min_conn / max_conn are accepted ONLY for compatibility.
    SQLite does not use connection pools.
    """
    logger.info("=" * 60)
    logger.info("DATABASE INITIALIZATION")
    logger.info("=" * 60)
    logger.info("Database engine: SQLite")
    logger.info(f"Database file: {DB_FILE}")

    if os.path.exists(DB_FILE):
        logger.info("Database file exists")
    else:
        logger.info("Database file will be created")

    # Create base tables
    create_tables()

    # Run safe migration
    run_migration()

    logger.info("Database initialization complete")
    logger.info("=" * 60)


@contextmanager
def get_db_connection():
    """
    Thread-safe SQLite connection with foreign keys enabled.
    """
    if not hasattr(_thread_local, "connection") or _thread_local.connection is None:
        conn = sqlite3.connect(
            DB_FILE,
            check_same_thread=False,
            timeout=30
        )
        conn.row_factory = sqlite3.Row

        # 🔥 REQUIRED for SQLite
        conn.execute("PRAGMA foreign_keys = ON;")

        _thread_local.connection = conn

    try:
        yield _thread_local.connection
    except Exception as e:
        _thread_local.connection.rollback()
        logger.error(f"Database error: {e}")
        raise


@contextmanager
def get_db_cursor(commit: bool = False):
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
    logger.info("Creating/verifying database tables...")

    users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    datasets_table = """
    CREATE TABLE IF NOT EXISTS datasets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        user_id INTEGER NOT NULL,
        file_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    with get_db_cursor(commit=True) as cursor:
        cursor.execute(users_table)
        cursor.execute(datasets_table)

    logger.info("✓ Base tables ready")


# ============================
# SAFE AUTO MIGRATION
# ============================

def run_migration():
    logger.info("Running database migration...")

    with get_db_cursor(commit=True) as cursor:
        existing_columns = get_columns(cursor, "datasets")

        add_column(cursor, existing_columns, "datasets", "file_name", "TEXT")
        add_column(cursor, existing_columns, "datasets", "file_size", "INTEGER")
        add_column(cursor, existing_columns, "datasets", "row_count", "INTEGER")
        add_column(cursor, existing_columns, "datasets", "column_count", "INTEGER")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dataset_columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            column_name TEXT NOT NULL,
            column_type TEXT,
            column_index INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_id INTEGER NOT NULL,
            total_rows INTEGER,
            total_columns INTEGER,
            duplicate_rows INTEGER,
            null_counts TEXT,
            completeness_score REAL,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE CASCADE
        );
        """)

    logger.info("✓ Migration complete")


def get_columns(cursor, table_name: str) -> set:
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def add_column(cursor, existing_cols, table, column, col_type):
    if column not in existing_cols:
        logger.info(f"Adding column: {table}.{column}")
        cursor.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"
        )
    else:
        logger.info(f"Column exists: {table}.{column}")


def close_db_pool():
    if hasattr(_thread_local, "connection") and _thread_local.connection:
        _thread_local.connection.close()
        _thread_local.connection = None
        logger.info("Database connection closed")
