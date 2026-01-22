"""
Database migration script to safely add missing columns to existing tables.
This script checks for missing columns and adds them without losing data.
"""
import sqlite3
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_FILE = "./dataset_platform.db"


def get_table_columns(cursor, table_name):
    """Get list of column names for a table"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]


def column_exists(cursor, table_name, column_name):
    """Check if column exists in table"""
    columns = get_table_columns(cursor, table_name)
    return column_name in columns


def table_exists(cursor, table_name):
    """Check if table exists"""
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    return cursor.fetchone() is not None


def migrate_datasets_table(cursor):
    """Add missing columns to datasets table"""
    logger.info("Checking datasets table...")
    
    if not table_exists(cursor, 'datasets'):
        logger.info("datasets table doesn't exist, will be created by app")
        return
    
    columns_to_add = [
        ("file_name", "VARCHAR(255)"),
        ("file_size", "INTEGER"),
        ("row_count", "INTEGER"),
        ("column_count", "INTEGER"),
    ]
    
    for col_name, col_type in columns_to_add:
        if not column_exists(cursor, 'datasets', col_name):
            logger.info(f"Adding column '{col_name}' to datasets table")
            cursor.execute(f"ALTER TABLE datasets ADD COLUMN {col_name} {col_type}")
        else:
            logger.info(f"Column '{col_name}' already exists in datasets table")


def create_missing_tables(cursor):
    """Create dataset_columns and quality_reports tables if they don't exist"""
    
    # dataset_columns table
    if not table_exists(cursor, 'dataset_columns'):
        logger.info("Creating dataset_columns table...")
        cursor.execute("""
            CREATE TABLE dataset_columns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
                column_name VARCHAR(255) NOT NULL,
                column_type VARCHAR(50),
                column_index INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX idx_dataset_columns_dataset_id 
            ON dataset_columns(dataset_id);
        """)
        logger.info("dataset_columns table created")
    else:
        logger.info("dataset_columns table already exists")
    
    # quality_reports table
    if not table_exists(cursor, 'quality_reports'):
        logger.info("Creating quality_reports table...")
        cursor.execute("""
            CREATE TABLE quality_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
                total_rows INTEGER NOT NULL,
                total_columns INTEGER NOT NULL,
                duplicate_rows INTEGER DEFAULT 0,
                null_counts TEXT,
                completeness_score REAL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE INDEX idx_quality_reports_dataset_id 
            ON quality_reports(dataset_id);
        """)
        logger.info("quality_reports table created")
    else:
        logger.info("quality_reports table already exists")


def main():
    """Run migration"""
    logger.info("Starting database migration...")
    logger.info(f"Database file: {DB_FILE}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Migrate datasets table
        migrate_datasets_table(cursor)
        
        # Create missing tables
        create_missing_tables(cursor)
        
        # Commit changes
        conn.commit()
        
        logger.info("Migration completed successfully!")
        
        # Show final schema
        logger.info("\n=== Final datasets table schema ===")
        columns = get_table_columns(cursor, 'datasets')
        for col in columns:
            logger.info(f"  - {col}")
        
        cursor.close()
        conn.close()
        
        return 0
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
