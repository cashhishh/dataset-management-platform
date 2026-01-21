# System Architecture Diagrams

## 1. High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     CLIENT (HTTP)                        │
│              (Browser, Postman, curl, etc.)              │
└────────────────────────┬─────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │
┌────────────────────────▼─────────────────────────────────┐
│                    FastAPI Server                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Routes (API Endpoints)             │    │
│  │  • /auth/register                               │    │
│  │  • /auth/login                                  │    │
│  │  • /datasets/ (CRUD)                            │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │                                    │
│  ┌──────────────────▼──────────────────────────────┐    │
│  │         Security Layer (Middleware)             │    │
│  │  • JWT Validation                               │    │
│  │  • Role-Based Access Control                    │    │
│  │  • Password Hashing                             │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │                                    │
│  ┌──────────────────▼──────────────────────────────┐    │
│  │          Models (Business Logic)                │    │
│  │  • UserModel                                    │    │
│  │  • DatasetModel                                 │    │
│  └──────────────────┬──────────────────────────────┘    │
│                     │                                    │
│  ┌──────────────────▼──────────────────────────────┐    │
│  │      Database Layer (Connection Pool)           │    │
│  │  • Context Managers                             │    │
│  │  • Raw SQL Queries                              │    │
│  └──────────────────┬──────────────────────────────┘    │
└─────────────────────┼────────────────────────────────────┘
                      │
                      │ SQL
                      │
┌─────────────────────▼────────────────────────────────────┐
│                PostgreSQL Database                       │
│  ┌──────────────┐         ┌──────────────┐             │
│  │    users     │─────────│   datasets   │             │
│  │              │ 1     ∞ │              │             │
│  │  id (PK)     │         │  id (PK)     │             │
│  │  email       │         │  name        │             │
│  │  username    │         │  description │             │
│  │  password    │         │  user_id(FK) │             │
│  │  role        │         │  file_path   │             │
│  └──────────────┘         └──────────────┘             │
└──────────────────────────────────────────────────────────┘
```

## 2. Authentication Flow

```
┌────────┐                                      ┌────────┐
│ Client │                                      │ Server │
└───┬────┘                                      └───┬────┘
    │                                               │
    │  1. POST /auth/register                       │
    │  { email, username, password, role }          │
    ├──────────────────────────────────────────────>│
    │                                               │
    │                           2. Hash password    │
    │                              (bcrypt)         │
    │                                          ┌────▼────┐
    │                           3. INSERT      │  Users  │
    │                              INTO users  │  Table  │
    │                                          └────┬────┘
    │                           4. Return user      │
    │                              (no password)    │
    │<──────────────────────────────────────────────┤
    │  { id, email, username, role }                │
    │                                               │
    │  5. POST /auth/login                          │
    │  { email, password }                          │
    ├──────────────────────────────────────────────>│
    │                                               │
    │                           6. Get user by      │
    │                              email            │
    │                                          ┌────▼────┐
    │                           7. Verify      │  Users  │
    │                              password    │  Table  │
    │                              (bcrypt)    └────┬────┘
    │                                               │
    │                           8. Generate JWT     │
    │                              token            │
    │<──────────────────────────────────────────────┤
    │  { access_token, token_type: "bearer" }       │
    │                                               │
```

## 3. Authorization Flow (Protected Routes)

```
┌────────┐                                      ┌────────┐
│ Client │                                      │ Server │
└───┬────┘                                      └───┬────┘
    │                                               │
    │  1. GET /datasets/                            │
    │  Header: Authorization: Bearer <JWT>          │
    ├──────────────────────────────────────────────>│
    │                                               │
    │                       2. Extract JWT from     │
    │                          Authorization header │
    │                                          ┌────▼──────┐
    │                       3. Decode JWT      │ Security  │
    │                          Validate sig.   │  Module   │
    │                                          └────┬──────┘
    │                       4. Extract:             │
    │                          - user_id            │
    │                          - role               │
    │                                               │
    │                       5. Query datasets  ┌────▼────┐
    │                          based on role   │Database │
    │                                          │         │
    │                          IF user:        │         │
    │                            WHERE user_id │         │
    │                          IF admin:       │         │
    │                            SELECT ALL    └────┬────┘
    │                                               │
    │<──────────────────────────────────────────────┤
    │  [ { id, name, description, ... } ]           │
    │                                               │
```

## 4. Role-Based Access Matrix

```
┌─────────────────────┬──────────────┬─────────────┐
│     Endpoint        │  User Role   │ Admin Role  │
├─────────────────────┼──────────────┼─────────────┤
│ POST /auth/register │      ✓       │      ✓      │
│ POST /auth/login    │      ✓       │      ✓      │
│ GET /auth/me        │   ✓ (self)   │  ✓ (self)   │
├─────────────────────┼──────────────┼─────────────┤
│ POST /datasets/     │   ✓ (own)    │   ✓ (own)   │
│ GET /datasets/      │  ✓ (own only)│ ✓ (all+info)│
│ GET /datasets/{id}  │  ✓ (own only)│    ✓ (any)  │
│ DELETE /datasets/   │  ✓ (own only)│ ✓ (own only)│
└─────────────────────┴──────────────┴─────────────┘

Legend:
  ✓ = Allowed
  (own) = Only resources they created
  (all) = All resources from all users
  (self) = Only their own user info
```

## 5. Database Schema Relationship

```
┌────────────────────────────────────┐
│             users                  │
├────────────────────────────────────┤
│ id            SERIAL PRIMARY KEY   │◄───┐
│ email         VARCHAR(255) UNIQUE  │    │
│ username      VARCHAR(100) UNIQUE  │    │
│ hashed_pwd    VARCHAR(255)         │    │
│ role          VARCHAR(20)          │    │
│ created_at    TIMESTAMP            │    │
│ updated_at    TIMESTAMP            │    │
└────────────────────────────────────┘    │
                                          │
                                          │ Foreign Key
                                          │ ON DELETE CASCADE
                                          │
┌────────────────────────────────────┐    │
│           datasets                 │    │
├────────────────────────────────────┤    │
│ id            SERIAL PRIMARY KEY   │    │
│ name          VARCHAR(255)         │    │
│ description   TEXT                 │    │
│ user_id       INTEGER NOT NULL     │────┘
│ file_path     VARCHAR(500)         │
│ created_at    TIMESTAMP            │
│ updated_at    TIMESTAMP            │
└────────────────────────────────────┘

Indexes:
  • users.email (unique)
  • users.username (unique)
  • datasets.user_id (for fast lookups)
```

## 6. Request/Response Flow

```
Example: Creating a Dataset

1. Client Request
   ↓
   POST /datasets/
   Headers: {
     "Authorization": "Bearer eyJhbGc..."
     "Content-Type": "application/json"
   }
   Body: {
     "name": "Customer Data",
     "description": "Q1 2026 customer analytics",
     "file_path": "/uploads/customers.csv"
   }

2. FastAPI Router (dataset_routes.py)
   ↓
   @router.post("/")
   async def create_dataset(
     dataset_data: DatasetCreate,          ← Pydantic validation
     current_user: TokenData = Depends()   ← JWT validation
   )

3. Dependency Injection (auth_routes.py)
   ↓
   get_current_user(credentials)
   - Extract token from header
   - Decode JWT
   - Return TokenData(user_id, role)

4. Model Layer (dataset.py)
   ↓
   DatasetModel.create_dataset(
     name, description, user_id, file_path
   )

5. Database Layer (db.py)
   ↓
   with get_db_cursor(commit=True) as cursor:
     cursor.execute(
       "INSERT INTO datasets (...) VALUES (%s, %s, %s, %s)",
       (name, description, user_id, file_path)
     )

6. Response
   ↓
   201 Created
   {
     "id": 1,
     "name": "Customer Data",
     "description": "Q1 2026 customer analytics",
     "user_id": 5,
     "file_path": "/uploads/customers.csv",
     "created_at": "2026-01-21T10:30:00"
   }
```

## 7. Security Layers

```
┌─────────────────────────────────────────────────────┐
│              External Request                       │
└──────────────────────┬──────────────────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   1. CORS Middleware        │
        │   Check origin allowed      │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   2. Pydantic Validation    │
        │   Validate request schema   │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   3. JWT Authentication     │
        │   Verify token signature    │
        │   Check expiration          │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   4. Role Authorization     │
        │   Check user role           │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   5. Ownership Check        │
        │   Verify resource owner     │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   6. SQL Parameterization   │
        │   Prevent injection         │
        └──────────────┬──────────────┘
                       │
                ┌──────▼──────┐
                │  Database   │
                └─────────────┘
```

## 8. Connection Pool Architecture

```
┌────────────────────────────────────────┐
│        Application Startup             │
└──────────────────┬─────────────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │  Initialize Connection Pool  │
    │  Min: 2, Max: 10 connections │
    └──────────────┬───────────────┘
                   │
        ┌──────────▼──────────┐
        │  Connection Pool    │
        ├─────────────────────┤
        │ [Conn1] [Conn2]     │
        │ [Conn3] [Conn4]     │
        │ [Conn5] ...         │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌───────┐      ┌───────┐      ┌───────┐
│Request│      │Request│      │Request│
│   1   │      │   2   │      │   3   │
└───┬───┘      └───┬───┘      └───┬───┘
    │              │              │
    │ getconn()    │ getconn()    │ getconn()
    ▼              ▼              ▼
┌───────┐      ┌───────┐      ┌───────┐
│ Conn1 │      │ Conn2 │      │ Conn3 │
└───┬───┘      └───┬───┘      └───┬───┘
    │              │              │
    │ Execute SQL  │ Execute SQL  │ Execute SQL
    │              │              │
    │ putconn()    │ putconn()    │ putconn()
    ▼              ▼              ▼
    └──────────────┴──────────────┘
            Return to pool
```

## 9. Code Organization

```
FastAPI Application Structure

app/
│
├── main.py ─────────────┐
│   • FastAPI instance   │
│   • Router registration│
│   • CORS config        │
│   • Lifespan events    │
│                        │
├── db.py ───────────────┤
│   • Connection pool    │
│   • Context managers   │
│   • Table creation     │
│                        │
├── core/ ───────────────┤
│   └── security.py      │
│       • JWT encode/decode
│       • Password hash/verify
│                        │
├── models/ ─────────────┤
│   ├── user.py          │
│   │   • create_user()  │
│   │   • get_user_by_*()│
│   └── dataset.py       │
│       • create_dataset()│
│       • get_datasets_*()│
│                        │
├── schemas/ ────────────┤
│   ├── auth.py          │
│   │   • UserRegister   │
│   │   • UserLogin      │
│   │   • Token          │
│   └── user.py          │
│       • UserResponse   │
│       • DatasetCreate  │
│       • DatasetResponse│
│                        │
└── routes/ ─────────────┘
    ├── auth_routes.py
    │   • POST /register
    │   • POST /login
    │   • GET /me
    │   • Dependency: get_current_user
    └── dataset_routes.py
        • POST /datasets/
        • GET /datasets/
        • GET /datasets/{id}
        • DELETE /datasets/{id}
```

## 10. Data Flow Example

```
User Registration Flow:

Client                    Server                   Database
  │                         │                         │
  │ POST /auth/register     │                         │
  ├────────────────────────>│                         │
  │ {email, username, pwd}  │                         │
  │                         │                         │
  │                    Pydantic                       │
  │                    validates                      │
  │                    schema ✓                       │
  │                         │                         │
  │                   Hash password                   │
  │                   (bcrypt) ✓                      │
  │                         │                         │
  │                         │ INSERT INTO users       │
  │                         ├────────────────────────>│
  │                         │ (email, username,       │
  │                         │  hashed_pwd, role)      │
  │                         │                         │
  │                         │    Return new user      │
  │                         │<────────────────────────┤
  │                         │    (id, email, etc)     │
  │                         │                         │
  │  201 Created            │                         │
  │<────────────────────────┤                         │
  │  {id, email, username}  │                         │
  │  (no password!)         │                         │
  │                         │                         │
```

---

These diagrams provide visual representation of the system's architecture, making it easier to explain during interviews or to understand the codebase structure.
