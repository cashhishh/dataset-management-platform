# Multi-User Dataset Management Platform

A production-ready backend API for managing datasets with JWT authentication and role-based access control.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **psycopg2** - PostgreSQL adapter (raw SQL, no ORM)
- **JWT** - Token-based authentication
- **passlib** - Password hashing with bcrypt

## Features

### Authentication & Authorization
- User registration with email validation
- Secure login with JWT access tokens
- Password hashing using bcrypt
- Role-based access control (user/admin)

### Dataset Management
- Authenticated users can create datasets
- Users can ONLY view/delete their own datasets
- Admins can view ALL datasets with owner information
- Clean separation of user and admin capabilities

### Security
- JWT-based authentication on protected routes
- Dependency injection for auth validation
- Proper HTTP status codes and error handling
- CORS configuration for API access

### Database
- PostgreSQL with connection pooling
- Auto-creation of tables on startup
- Context managers for safe connection handling
- Indexed queries for performance

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # Application entry point
│   ├── db.py                   # Database connection & initialization
│   ├── core/
│   │   └── security.py         # JWT & password utilities
│   ├── models/
│   │   ├── user.py             # User database operations
│   │   └── dataset.py          # Dataset database operations
│   ├── schemas/
│   │   ├── auth.py             # Auth request/response schemas
│   │   └── user.py             # User & dataset schemas
│   └── routes/
│       ├── auth_routes.py      # Authentication endpoints
│       └── dataset_routes.py   # Dataset management endpoints
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL 12+

### 1. Database Setup

Create a PostgreSQL database:
```bash
psql -U postgres
CREATE DATABASE dataset_platform;
\q
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Database

Update database credentials in `app/db.py`:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "dataset_platform",
    "user": "postgres",
    "password": "your_password"
}
```

**Production**: Use environment variables instead of hardcoded values.

### 4. Run the Application

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Or directly:
```bash
python app/main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/auth/me` | Get current user info | Yes |

### Datasets

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/datasets/` | Create new dataset | Yes | user/admin |
| GET | `/datasets/` | Get user's datasets (or all for admin) | Yes | user/admin |
| GET | `/datasets/{id}` | Get specific dataset | Yes | owner/admin |
| DELETE | `/datasets/{id}` | Delete dataset | Yes | owner only |
| GET | `/datasets/admin/all` | Get all datasets (admin) | Yes | admin |

## Example Usage

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "role": "user"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create a Dataset (Authenticated)

```bash
curl -X POST "http://localhost:8000/datasets/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Analysis",
    "description": "Q1 2026 customer behavior data",
    "file_path": "/uploads/customers.csv"
  }'
```

### 4. Get Your Datasets

```bash
curl -X GET "http://localhost:8000/datasets/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

### users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### datasets
```sql
CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Security Considerations

### Current Implementation
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Role-based access control
- ✅ Input validation with Pydantic
- ✅ SQL injection prevention (parameterized queries)
- ✅ Connection pooling for database

### Production Recommendations
- 🔧 Move secrets to environment variables
- 🔧 Use HTTPS only
- 🔧 Implement rate limiting
- 🔧 Add refresh tokens
- 🔧 Configure proper CORS origins
- 🔧 Add request logging and monitoring
- 🔧 Implement token revocation
- 🔧 Add password complexity requirements

## Development

### Code Structure Principles
- **Clean Architecture**: Separation of concerns (routes → models → database)
- **Dependency Injection**: Auth dependencies in FastAPI
- **Context Managers**: Safe database connection handling
- **Raw SQL**: Direct PostgreSQL queries without ORM overhead
- **Pydantic Validation**: Type-safe request/response schemas
- **Comprehensive Logging**: Tracking all important operations

### Adding New Features
1. Define schema in `schemas/`
2. Create model methods in `models/`
3. Add route handlers in `routes/`
4. Register router in `main.py`

## Testing

Example test scenarios:
- Register user with duplicate email (should fail)
- Login with wrong password (should fail)
- Access protected route without token (should fail)
- User tries to view another user's dataset (should fail)
- Admin views all datasets (should succeed)

## Interview Talking Points

1. **Authentication**: JWT-based stateless authentication
2. **Authorization**: Role-based access with dependency injection
3. **Database**: Connection pooling, context managers, raw SQL
4. **Security**: Password hashing, parameterized queries, token validation
5. **Architecture**: Clean separation of routes, models, and schemas
6. **Error Handling**: Proper HTTP status codes and descriptive messages
7. **Scalability**: Connection pooling, indexed queries

## License

This is a portfolio project for demonstration purposes.
