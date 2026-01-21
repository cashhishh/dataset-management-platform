-- Manual Database Setup and Test Data
-- Run this if you want to manually create tables or add test users

-- ============================================
-- 1. CREATE TABLES (if not auto-created)
-- ============================================

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_datasets_user_id 
ON datasets(user_id);

-- ============================================
-- 2. VERIFY TABLES
-- ============================================

-- List all tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check users table structure
\d users

-- Check datasets table structure
\d datasets

-- ============================================
-- 3. VIEW DATA
-- ============================================

-- View all users (without passwords)
SELECT id, email, username, role, created_at 
FROM users 
ORDER BY created_at DESC;

-- View all datasets with owner info
SELECT 
    d.id,
    d.name,
    d.description,
    u.username as owner,
    u.email as owner_email,
    d.created_at
FROM datasets d
JOIN users u ON d.user_id = u.id
ORDER BY d.created_at DESC;

-- Count datasets per user
SELECT 
    u.username,
    u.role,
    COUNT(d.id) as dataset_count
FROM users u
LEFT JOIN datasets d ON u.id = d.user_id
GROUP BY u.id, u.username, u.role;

-- ============================================
-- 4. CLEANUP (USE WITH CAUTION)
-- ============================================

-- Delete all datasets
-- DELETE FROM datasets;

-- Delete all users
-- DELETE FROM users;

-- Drop tables completely
-- DROP TABLE IF EXISTS datasets;
-- DROP TABLE IF EXISTS users;

-- ============================================
-- 5. USEFUL QUERIES
-- ============================================

-- Find user by email
SELECT id, email, username, role 
FROM users 
WHERE email = 'admin@test.com';

-- Find datasets by user ID
SELECT * 
FROM datasets 
WHERE user_id = 1;

-- Find datasets by username
SELECT d.* 
FROM datasets d
JOIN users u ON d.user_id = u.id
WHERE u.username = 'admin';

-- Check if email exists
SELECT EXISTS(
    SELECT 1 FROM users WHERE email = 'test@example.com'
) as email_exists;

-- ============================================
-- 6. PERFORMANCE CHECKS
-- ============================================

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans
FROM pg_stat_user_indexes
WHERE schemaname = 'public';

-- Check table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public';
