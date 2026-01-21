# Architecture & Design Decisions

## System Overview

This is a **Multi-User Dataset Management Platform** - a RESTful API backend that demonstrates production-ready authentication, authorization, and data management.

## Core Design Principles

### 1. Clean Architecture
- **Separation of Concerns**: Routes → Models → Database
- **Single Responsibility**: Each module has one clear purpose
- **Dependency Direction**: High-level (routes) depend on low-level (models), not vice versa

### 2. Security-First Design
- All passwords hashed with bcrypt before storage
- JWT tokens for stateless authentication
- Role-based access control at the route level
- Parameterized SQL queries to prevent injection
- No sensitive data in responses (passwords excluded)

### 3. Database Design
- **Raw SQL**: Direct control, no ORM overhead, explicit queries
- **Connection Pooling**: Reuse connections for performance
- **Context Managers**: Automatic resource cleanup
- **Foreign Keys**: Referential integrity enforced at DB level
- **Indexes**: Performance optimization on frequently queried columns

## Technology Choices & Justifications

### FastAPI (vs Django/Flask)
**Why FastAPI?**
- Modern async support (though not used here - scalability ready)
- Automatic API documentation (OpenAPI/Swagger)
- Pydantic integration for validation
- Better performance than Flask/Django
- Type hints throughout

### Raw SQL (vs SQLAlchemy ORM)
**Why Raw SQL?**
- Direct control over queries
- No ORM abstraction overhead
- Easier to optimize for performance
- Clear understanding of what runs on DB
- Simpler for interviews to explain

### psycopg2 (vs asyncpg)
**Why psycopg2?**
- Synchronous, simpler to reason about
- Mature and stable
- Connection pooling built-in
- Sufficient for most use cases

### JWT (vs Session-based auth)
**Why JWT?**
- Stateless - scales horizontally
- No server-side session storage
- Works well with microservices
- Mobile-friendly

## Key Components Explained

### 1. Authentication Flow

```
┌──────────┐      POST /auth/register      ┌──────────┐
│  Client  │──────────────────────────────>│  Server  │
└──────────┘                                └──────────┘
                                                  │
                                                  ▼
                                            Hash password
                                                  │
                                                  ▼
                                            Store in DB
                                                  │
                                                  ▼
                                            Return user info


┌──────────┐      POST /auth/login         ┌──────────┐
│  Client  │──────────────────────────────>│  Server  │
└──────────┘                                └──────────┘
     ▲                                            │
     │                                            ▼
     │                                      Get user from DB
     │                                            │
     │                                            ▼
     │                                      Verify password
     │                                            │
     └────────────────────────────────────── Generate JWT
                  Return token
```

### 2. Authorization Flow

```
┌──────────┐    GET /datasets/    ┌──────────┐
│  Client  │───────────────────>│  Server  │
│  Header: │                      └────┬─────┘
│  Bearer  │                           │
│  TOKEN   │                           ▼
└──────────┘              Dependency: get_current_user()
     ▲                               │
     │                               ▼
     │                        Decode & validate JWT
     │                               │
     │                               ▼
     │                        Extract user_id & role
     │                               │
     │                               ▼
     │                        Check authorization
     │                               │
     │                               ▼
     └──────────────────────── Return datasets
              (filtered by role)
```

### 3. Database Connection Management

**Connection Pool Pattern**:
```python
# Initialize once at startup
connection_pool = psycopg2.pool.SimpleConnectionPool(min=2, max=10)

# Get connection from pool
@contextmanager
def get_db_connection():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)  # Return to pool
```

**Benefits**:
- Reuse connections (expensive to create)
- Automatic cleanup (context manager)
- Configurable pool size
- Thread-safe

### 4. Dependency Injection

FastAPI's dependency injection for authentication:

```python
# Dependency function
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validate token, return user data
    return TokenData(user_id=X, role="user")

# Use in routes
@router.get("/datasets/")
async def get_datasets(current_user: TokenData = Depends(get_current_user)):
    # current_user is automatically injected and validated
    pass
```

**Benefits**:
- DRY (Don't Repeat Yourself)
- Testable (can mock dependencies)
- Clean route handlers
- Automatic validation

## Role-Based Access Control (RBAC)

### Access Matrix

| Endpoint | Regular User | Admin |
|----------|-------------|-------|
| POST /datasets/ | ✅ Create own | ✅ Create own |
| GET /datasets/ | ✅ See own only | ✅ See ALL + owners |
| GET /datasets/{id} | ✅ Own only | ✅ Any dataset |
| DELETE /datasets/{id} | ✅ Own only | ❌ Own only (ownership protection) |

### Implementation

**User Access**:
```python
if current_user.role == "user":
    datasets = DatasetModel.get_datasets_by_user(current_user.user_id)
```

**Admin Access**:
```python
if current_user.role == "admin":
    datasets = DatasetModel.get_all_datasets()  # Includes owner info
```

**Ownership Check**:
```python
dataset = DatasetModel.get_dataset_by_id(dataset_id)
if current_user.role != "admin" and dataset["user_id"] != current_user.user_id:
    raise HTTPException(status_code=403, detail="Access denied")
```

## Security Considerations

### Implemented ✅
1. **Password Security**: Bcrypt hashing with salt
2. **SQL Injection Prevention**: Parameterized queries
3. **Token Validation**: JWT signature verification
4. **Role Enforcement**: Dependencies check roles
5. **Ownership Validation**: Users can't access others' data
6. **HTTPS-Ready**: Works with reverse proxy

### Production Enhancements 🔧
1. **Environment Variables**: Move secrets out of code
2. **Rate Limiting**: Prevent brute force attacks
3. **Token Refresh**: Long-lived refresh tokens
4. **Token Revocation**: Blacklist for logout
5. **CORS**: Restrict to specific origins
6. **Logging**: Audit trail for security events
7. **Password Policy**: Min length, complexity rules
8. **Account Lockout**: After failed attempts

## Scalability Considerations

### Current Design Supports:
- **Horizontal Scaling**: Stateless JWT auth
- **Connection Pooling**: Efficient DB usage
- **Indexed Queries**: Fast lookups

### Future Enhancements:
- **Caching**: Redis for session data
- **Background Tasks**: Celery for async processing
- **Load Balancing**: Multiple app instances
- **Database Replication**: Read replicas

## Testing Strategy

### Unit Tests
- Model methods (CRUD operations)
- Security functions (hash, verify, token)
- Schema validation

### Integration Tests
- Full auth flow (register → login → access)
- Authorization checks (user vs admin)
- Database operations (create → read → delete)

### Test Cases
1. ✅ User registration with valid data
2. ❌ Registration with duplicate email
3. ✅ Login with correct credentials
4. ❌ Login with wrong password
5. ✅ Access protected route with valid token
6. ❌ Access without token
7. ✅ User creates dataset
8. ✅ User views own datasets
9. ❌ User views other user's dataset
10. ✅ Admin views all datasets

## Interview Talking Points

### Architecture
- "Implemented clean architecture with separated layers"
- "Used dependency injection for auth validation"
- "Applied SOLID principles throughout"

### Security
- "JWT-based stateless authentication for scalability"
- "Bcrypt password hashing with automatic salting"
- "Role-based access control with granular permissions"
- "Parameterized SQL queries to prevent injection"

### Database
- "PostgreSQL with connection pooling for performance"
- "Raw SQL for direct control and optimization"
- "Context managers for safe resource management"
- "Foreign keys and indexes for data integrity and speed"

### Best Practices
- "Pydantic schemas for request/response validation"
- "Proper HTTP status codes (201, 401, 403, 404, 500)"
- "Comprehensive logging for debugging and auditing"
- "Environment-ready for dev/staging/prod deployment"

## Code Quality Highlights

1. **Type Hints**: Throughout for IDE support and clarity
2. **Documentation**: Docstrings for all functions
3. **Error Handling**: Try-except blocks with logging
4. **Consistent Naming**: PEP 8 compliance
5. **Comments**: Explaining "why", not "what"
6. **No Dead Code**: Every line has purpose

## Deployment Considerations

### Development
```bash
uvicorn app.main:app --reload
```

### Production
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (Future)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
- DB credentials
- JWT secret key
- CORS origins
- Debug mode

## Conclusion

This project demonstrates:
- ✅ Production-ready backend architecture
- ✅ Security best practices
- ✅ Clean, maintainable code
- ✅ Scalable design patterns
- ✅ RESTful API principles
- ✅ Interview-ready implementation

**Perfect for resume as a second backend project** - shows depth beyond basic CRUD, with real-world auth/authz complexity.
