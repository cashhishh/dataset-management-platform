# Quick Start Guide

## Setup Steps (5 minutes)

### 1. Create PostgreSQL Database
```bash
# Start PostgreSQL (if not running)
# Then create database:
psql -U postgres
CREATE DATABASE dataset_platform;
\q
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Update Database Config
Edit `backend/app/db.py` and update the password:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "dataset_platform",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD"  # Change this
}
```

### 4. Run the Server
```bash
cd backend
python app/main.py
```

Server will start at: http://localhost:8000

### 5. View API Documentation
Open browser: http://localhost:8000/docs

## Test the API (Using Interactive Docs)

### Step 1: Register a User
1. Go to http://localhost:8000/docs
2. Expand `POST /auth/register`
3. Click "Try it out"
4. Use this JSON:
```json
{
  "email": "admin@test.com",
  "username": "admin",
  "password": "admin123",
  "role": "admin"
}
```
5. Click "Execute"

### Step 2: Login
1. Expand `POST /auth/login`
2. Click "Try it out"
3. Use:
```json
{
  "email": "admin@test.com",
  "password": "admin123"
}
```
4. Copy the `access_token` from the response

### Step 3: Authorize
1. Click the green "Authorize" button at the top
2. Paste: `Bearer YOUR_ACCESS_TOKEN`
3. Click "Authorize"

### Step 4: Create a Dataset
1. Expand `POST /datasets/`
2. Click "Try it out"
3. Use:
```json
{
  "name": "Test Dataset",
  "description": "My first dataset",
  "file_path": "/uploads/test.csv"
}
```
4. Click "Execute"

### Step 5: View Your Datasets
1. Expand `GET /datasets/`
2. Click "Try it out"
3. Click "Execute"
4. See your dataset!

## Architecture Overview

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Routes  │ (auth_routes, dataset_routes)
    └────┬────┘
         │
    ┌────┴────┐
    │ Models  │ (UserModel, DatasetModel)
    └────┬────┘
         │
    ┌────┴────────┐
    │ PostgreSQL  │
    └─────────────┘
```

## Key Features Demonstrated

✅ JWT Authentication
✅ Password Hashing (bcrypt)
✅ Role-Based Access Control
✅ Database Connection Pooling
✅ Raw SQL Queries
✅ Dependency Injection
✅ Context Managers
✅ Clean Architecture
✅ API Documentation
✅ Error Handling

## Common Issues

### Issue: "relation 'users' does not exist"
**Solution**: Tables are auto-created on startup. Restart the server.

### Issue: "could not connect to server"
**Solution**: Ensure PostgreSQL is running and credentials are correct.

### Issue: "401 Unauthorized"
**Solution**: Your token expired. Login again and get a new token.

### Issue: "403 Forbidden"
**Solution**: You're trying to access a resource you don't own (users can only see their own datasets).

## Next Steps

1. Create multiple users (regular and admin)
2. Test user isolation (users can't see each other's datasets)
3. Test admin privileges (admin can see all datasets)
4. Try to delete another user's dataset (should fail)
5. Explore the auto-generated API docs

## Resume Talking Points

- "Built a production-ready FastAPI backend with JWT authentication"
- "Implemented role-based access control with dependency injection"
- "Used PostgreSQL with connection pooling and raw SQL for performance"
- "Applied clean architecture principles with separated layers"
- "Handled security concerns: password hashing, token validation, parameterized queries"
- "Demonstrated RESTful API design with proper HTTP status codes"
