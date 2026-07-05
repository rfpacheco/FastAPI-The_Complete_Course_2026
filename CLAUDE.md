# FastAPI TodoApp - Complete Course 2026

## Project Overview

**FastAPI TodoApp** is a production-ready Todo management application built with FastAPI and PostgreSQL. The project demonstrates modern API development practices including authentication, authorization, database integration, containerization, and comprehensive CRUD operations.

### Current Capabilities

The TodoApp provides:

- **Todo Management**: Create, read, update, and delete todos with title, description, priority levels (1-5), and completion status
- **User Authentication**: Secure JWT-based token authentication using python-jose
- **User Management**: User registration, profile viewing, and password management
- **Role-Based Access Control**: Admin and regular user roles with differentiated permissions
- **Database Persistence**: PostgreSQL integration with SQLAlchemy ORM
- **Docker Containerization**: Full Docker Compose setup for easy deployment and development
- **Sample Data**: Pre-populated database with admin and regular users for testing

---

## Architecture

### Project Structure

```
FastAPI-The_Complete_Course_2026/
├── TodoApp/
│   ├── __init__.py
│   ├── main.py                 # Application entry point, router registration
│   ├── database.py             # SQLAlchemy engine and session configuration
│   ├── models.py               # SQLAlchemy ORM models (Users, Todos)
│   └── routers/
│       ├── __init__.py
│       ├── auth.py             # Authentication endpoints (register, login)
│       ├── todos.py            # Todo CRUD endpoints (user-scoped)
│       ├── users.py            # User profile and password management
│       └── admin.py            # Admin-only operations
├── docker/
│   └── init.sql                # Database initialization script with seed data
├── docker-compose.yml          # PostgreSQL container orchestration
├── .env.example                # Environment variable template
├── .env                        # Local environment configuration
├── pyproject.toml              # Project dependencies
└── requirements.txt            # pip-compatible dependency list
```

### Key Modules

#### **models.py** - Database Models
- **Users**: User account model with authentication fields
  - Fields: id, email, username, first_name, last_name, hashed_password, is_active, role, phone_number
  - Indexes on email and username for fast lookups
  - Supports role-based access (admin, user)

- **Todos**: Todo task model with user ownership
  - Fields: id, title, description, priority (1-5), complete status, owner_id
  - Foreign key relationship to Users (cascade delete)
  - Indexed on owner_id for efficient filtering

#### **database.py** - Database Configuration
- PostgreSQL connection setup using SQLAlchemy
- Session management with dependency injection
- Default connection: `postgresql://postgres:postgres@localhost/TodoApplicationServer`

#### **routers/auth.py** - Authentication
- User registration with validation
- JWT token-based login (20-minute expiration)
- Token generation with user context (username, id, role)
- Password hashing using bcrypt via passlib
- OAuth2 bearer token validation
- Dependencies: `get_current_user()` for protected routes

#### **routers/todos.py** - Todo Management
- Authenticated endpoints with user-scoped filtering
- Full CRUD operations (GET all, GET by id, POST, PUT, DELETE)
- Pydantic request validation with field constraints
- Priority validation (1-5 range)
- Automatically associated with authenticated user

#### **routers/users.py** - User Management
- Get current user profile
- Change password with current password verification
- Returns full user details (id, email, username, name, role, phone, status)

#### **routers/admin.py** - Admin Operations
- Admin-only endpoint to view all todos (across all users)
- Admin todo deletion capability (unrestricted by ownership)
- Role validation via JWT token claims

---

## Section 12 Accomplishments

### Full CRUD API Endpoints for Todos with Authentication

**Todos Router** (`routers/todos.py`):

- **GET `/`**: Fetch all todos for authenticated user
  - Returns: Array of user's todos
  - Authentication: Required (JWT token)

- **GET `/todo/{todo_id}`**: Fetch specific todo
  - Validates ownership before returning
  - Status: 200 (success) or 404 (not found)

- **POST `/todo`**: Create new todo
  - Request body: `{ title, description, priority (1-5), complete }`
  - Auto-associates with authenticated user
  - Status: 201 (created)

- **PUT `/todo/{todo_id}`**: Update existing todo
  - Validates ownership before modification
  - All fields can be updated
  - Status: 204 (no content)

- **DELETE `/todo/{todo_id}`**: Delete todo
  - Validates ownership before deletion
  - Status: 204 (no content)

### User Authentication System with JWT Tokens

**Authentication Details** (`routers/auth.py`):

- **Token Generation**: JWT tokens signed with HS256 algorithm
  - Token payload includes: username (sub), user id, role, expiration
  - 20-minute default expiration for security
  - Tokens use Bearer scheme (OAuth2 standard)

- **Password Security**:
  - Bcrypt hashing with automatic salt generation
  - CryptContext from passlib for secure comparison
  - Prevents timing attacks during verification

- **Token Validation**:
  - `get_current_user()` dependency validates all protected routes
  - Extracts and validates JWT payload
  - Returns user context dict for route handlers
  - Rejects expired or malformed tokens with 401 errors

- **Login Endpoint** (`POST /auth/token`):
  - Accepts OAuth2 form data (username, password)
  - Returns access token with bearer type
  - Status: 200 on success, 401 on invalid credentials

### User Management

**Registration** (`POST /auth/`):
```python
{
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword",
  "role": "user",
  "phone_number": "+1-555-1234"
}
```

**User Profile** (`GET /user/`):
- Returns authenticated user's full profile
- Fields: id, email, username, names, is_active, role, phone_number
- Validates authentication, no user lookup parameters needed

**Password Management** (`PUT /user/password`):
- Updates password with current password verification
- Request: `{ current_password, new_password }`
- Prevents unauthorized password changes
- Uses bcrypt for new password hashing

### Admin Operations and Role-Based Access

**Admin Router** (`routers/admin.py`):

- **GET `/admin/todo`**: List all todos (admin only)
  - No user filtering applied
  - Requires `role == 'admin'` in JWT token
  - Returns: All todos in system

- **DELETE `/admin/todo/{todo_id}`**: Delete any todo (admin only)
  - No ownership validation
  - Useful for moderation and data cleanup
  - Requires admin role

**Access Control**:
- Role validation happens in route handlers
- Role claim extracted from JWT token during authentication
- Returns 401 if non-admin user attempts admin operations

### Database Integration with SQLAlchemy and PostgreSQL

**SQLAlchemy Setup**:
- ORM-based model definitions (Users, Todos)
- Declarative Base for schema definition
- Session management with automatic cleanup
- Query API for filtering and joining

**PostgreSQL Features**:
- ACID transactions for data consistency
- Foreign key constraints with CASCADE delete
- Indexes on frequently queried columns (email, username, owner_id)
- Password hashing stored as VARCHAR (bcrypt format)

**Connection Management**:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/TodoApplicationServer"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

### Docker Containerization with docker-compose

**docker-compose.yml** Configuration:

```yaml
services:
  postgres:
    image: postgres:15-alpine     # Lightweight PostgreSQL image
    container_name: todoapp-postgres
    environment:
      POSTGRES_USER: postgres      # Configurable via .env
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: TodoApplicationServer
    ports:
      - "5432:5432"               # Expose on standard port
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Data persistence
      - ./docker/init.sql:/docker-entrypoint-initdb.d/init.sql  # Auto-init
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Key Features**:
- PostgreSQL 15 Alpine (minimal footprint)
- Named volume for data persistence across container restarts
- Health checks to verify readiness
- Automatic initialization on first run with `init.sql`
- Configurable via `.env` file

**Quick Start**:
```bash
docker compose up -d      # Start database
docker compose ps         # Verify running
docker compose down       # Stop database
docker compose down -v    # Stop and reset data
```

### Sample Seed Data with Admin and Regular Users

**Seeded Users** (from `docker/init.sql`):

1. **John Doe** (johndoe) — Admin
   - Email: john.doe@example.com
   - Phone: +1-555-0101
   - Password: `secret` (hashed)
   - Role: admin

2. **Jane Smith** (janesmith) — User
   - Email: jane.smith@example.com
   - Phone: +1-555-0102
   - Password: `secret` (hashed)
   - Role: user

3. **Bob Wilson** (bobwilson) — User
   - Email: bob.wilson@example.com
   - Phone: +1-555-0103
   - Password: `secret` (hashed)
   - Role: user

4. **Eric Roby** (codingwithroby) — Admin
   - Email: codingwithroby@email.com
   - Phone: NULL
   - Password: `test1234` (hashed)
   - Role: admin

**Seeded Todos** (8 sample tasks):
- Distributed across users (John has 3, Jane and Bob have 2-3 each)
- Various priority levels (1-3)
- Mix of completed and incomplete tasks
- Real-world todo examples (learning, setup, deployment, documentation)

---

## Current Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | >= 0.136.1 |
| **Web Server** | Uvicorn | 0.47.0 |
| **ORM** | SQLAlchemy | >= 2.0.49 |
| **Database** | PostgreSQL | 15 (Alpine) |
| **Authentication** | python-jose | >= 3.5.0 |
| **JWT** | python-jose + jose | HS256 algorithm |
| **Password Hashing** | bcrypt via passlib | 4.0.1 / >= 1.7.4 |
| **Data Validation** | Pydantic | 2.13.4 |
| **Database Driver** | psycopg2-binary | >= 2.9.12 |
| **Environment Config** | python-dotenv | >= 1.0.0 |
| **Server Uploads** | python-multipart | 0.0.32 |
| **Python** | Python | >= 3.12 |

### Key Dependencies

```toml
bcrypt==4.0.1                    # Password hashing
fastapi>=0.136.1                 # API framework
passlib>=1.7.4                   # Password context manager
psycopg2-binary>=2.9.12          # PostgreSQL driver
pydantic==2.13.4                 # Data validation
python-dotenv>=1.0.0             # Environment variables
python-jose>=3.5.0               # JWT tokens
python-multipart==0.0.32         # Form data parsing
sqlalchemy>=2.0.49               # ORM
starlette>=1.0.0                 # ASGI framework
uvicorn==0.47.0                  # ASGI server
```

---

## Getting Started

### Prerequisites

- Docker Engine v20.10+ or Docker Desktop v4.0+
- Python 3.12+
- pip or uv package manager

### Installation and Setup

#### Step 1: Clone and Navigate

```bash
cd /path/to/FastAPI-The_Complete_Course_2026
```

#### Step 2: Start PostgreSQL Database

```bash
# Start the database container (includes auto-initialization)
docker compose up -d

# Verify it's running
docker compose ps

# Optional: Check logs
docker compose logs -f postgres
```

The first run will:
- Pull the PostgreSQL 15 Alpine image
- Create and start the `todoapp-postgres` container
- Initialize schema and seed data from `docker/init.sql`

#### Step 3: Install Python Dependencies

```bash
# Using pip
pip install -e .

# OR using uv (faster, more reliable)
uv sync
```

This installs all dependencies including FastAPI, SQLAlchemy, psycopg2, and JWT libraries.

#### Step 4: Run the Application

```bash
uvicorn TodoApp.main:app --reload
```

The app will start at `http://localhost:8000`

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)

#### Step 5: Test Authentication

**Get a Token**:
```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secret"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Use Token to Access Protected Routes**:
```bash
curl -X GET "http://localhost:8000/" \
  -H "Authorization: Bearer <token_from_above>"
```

### Environment Configuration

The `.env.example` shows available settings:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=TodoApplicationServer
DB_PORT=5432
DB_HOST=localhost

# Application Configuration
DEBUG=True
```

Copy to `.env` and customize as needed. The application reads these values for docker-compose startup.

### Stopping and Resetting

```bash
# Stop the database (data persists)
docker compose down

# Stop and delete all data (fresh start)
docker compose down -v

# Restart after stopping
docker compose restart postgres
```

---

## Key Endpoints and Their Requirements

### Authentication Endpoints

| Method | Endpoint | Authentication | Purpose |
|--------|----------|-----------------|---------|
| POST | `/auth/` | None | Register new user |
| POST | `/auth/token` | None (OAuth2 form) | Login and get JWT token |

### Todo Endpoints

| Method | Endpoint | Authentication | Scope | Purpose |
|--------|----------|-----------------|-------|---------|
| GET | `/` | Required | Own todos | Fetch all user's todos |
| GET | `/todo/{id}` | Required | Own todos | Fetch single todo |
| POST | `/todo` | Required | Own todos | Create new todo |
| PUT | `/todo/{id}` | Required | Own todos | Update todo |
| DELETE | `/todo/{id}` | Required | Own todos | Delete todo |

### User Endpoints

| Method | Endpoint | Authentication | Purpose |
|--------|----------|-----------------|---------|
| GET | `/user/` | Required | Fetch current user profile |
| PUT | `/user/password` | Required | Change password |

### Admin Endpoints

| Method | Endpoint | Authentication | Role Required | Purpose |
|--------|----------|-----------------|---------------|---------|
| GET | `/admin/todo` | Required | admin | View all todos (all users) |
| DELETE | `/admin/todo/{id}` | Required | admin | Delete any todo |

### Request/Response Examples

#### Register User
```bash
curl -X POST "http://localhost:8000/auth/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "new@example.com",
    "first_name": "New",
    "last_name": "User",
    "password": "securepass123",
    "role": "user",
    "phone_number": "+1-555-9999"
  }'
```

#### Create Todo (with token)
```bash
curl -X POST "http://localhost:8000/todo" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": 2,
    "complete": false
  }'
```

#### Update Todo
```bash
curl -X PUT "http://localhost:8000/todo/1" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, butter",
    "priority": 3,
    "complete": true
  }'
```

#### Change Password
```bash
curl -X PUT "http://localhost:8000/user/password" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "secret",
    "new_password": "newpassword123"
  }'
```

### Validation Rules

**Todo Creation/Update**:
- `title`: Required, minimum 3 characters
- `description`: Required, 3-100 characters
- `priority`: Integer between 1-5 (inclusive)
- `complete`: Boolean

**User Registration**:
- `username`: Unique across system
- `email`: Unique, must be valid email format
- `password`: Any non-empty string (consider enforcing strength in production)
- `role`: "user" or "admin"

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    phone_number VARCHAR(20)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

### Todos Table

```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    complete BOOLEAN DEFAULT FALSE,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_todos_owner_id ON todos(owner_id);
```

---

## Future Sections Roadmap

### Section 13+ Potential Topics

While the exact roadmap hasn't been documented, likely future enhancements based on typical FastAPI course progression include:

- **Testing & Quality Assurance**
  - Unit tests with pytest
  - Integration tests for endpoints
  - Test database setup and teardown
  - Coverage reporting

- **API Documentation Enhancements**
  - OpenAPI/Swagger customization
  - Endpoint descriptions and examples
  - Response schema documentation
  - Request/response examples in docs

- **Frontend Integration**
  - React/Vue.js frontend scaffolding
  - API client SDK generation
  - CORS configuration
  - WebSocket support for real-time updates

- **Advanced Features**
  - Email notifications
  - File uploads for todos
  - Todo categories/tags
  - Recurring todos
  - Sharing todos between users
  - Activity logging and audit trails

- **Production Deployment**
  - Kubernetes configuration (YAML manifests)
  - CI/CD pipeline setup (GitHub Actions, GitLab CI)
  - Environment-specific configurations
  - Database migrations with Alembic
  - Monitoring and logging

- **Security Enhancements**
  - Rate limiting
  - CORS configuration
  - SQL injection prevention review
  - HTTPS/TLS setup
  - API key authentication option
  - Two-factor authentication (2FA)

- **Performance Optimization**
  - Query optimization and caching
  - Database connection pooling
  - Response compression
  - Pagination for large result sets
  - Database migration strategies

---

## Useful Commands

### Development

```bash
# Start database
docker compose up -d

# Install dependencies
uv sync
# or
pip install -e .

# Run application
uvicorn TodoApp.main:app --reload

# Access API documentation
# Browser: http://localhost:8000/docs
```

### Database Management

```bash
# Connect to database CLI
docker compose exec postgres psql -U postgres -d TodoApplicationServer

# Check seeded users
docker compose exec postgres psql -U postgres -d TodoApplicationServer -c \
  "SELECT id, username, email, role FROM users;"

# Reset database
docker compose down -v
docker compose up -d

# Re-seed existing database
docker compose exec -T postgres psql -U postgres -d TodoApplicationServer < docker/init.sql
```

### Testing Credentials

- **Admin User**: johndoe / secret (or codingwithroby / test1234)
- **Regular User**: janesmith / secret (or bobwilson / secret)

---

## Security Notes

### Current Implementation

- Passwords hashed with bcrypt (salt rounds: 12)
- JWT tokens with 20-minute expiration
- Role-based access control for admin operations
- User-scoped todo filtering (users can't access others' todos)

### Production Recommendations

- Move `SECRET_KEY` to environment variable
- Increase JWT token expiration consideration (refresh tokens)
- Implement rate limiting on auth endpoints
- Add request validation for password strength
- Use HTTPS/TLS in production
- Enable database connection SSL
- Configure CORS properly for frontend domain
- Add request logging and monitoring
- Implement database backup strategy

---

## Troubleshooting

**Database Connection Refused**
- Ensure Docker is running: `docker compose ps`
- Wait 10-15 seconds after starting for database to be ready
- Verify `.env` settings match connection string in `database.py`

**Port Already in Use**
- Change `DB_PORT` in `.env` (e.g., 5433)
- Update port mapping in `docker-compose.yml`

**Authentication Fails**
- Verify JWT token is being passed with `Authorization: Bearer <token>`
- Check token hasn't expired (20 minute default)
- Verify username/password spelling for login

**Admin Endpoints Return 401**
- Verify user has `role: 'admin'` in database
- Check JWT token contains role claim
- Test with johndoe or codingwithroby credentials

---

## Contributing Notes

When making changes:
1. Update database schema in both `models.py` and `docker/init.sql`
2. Test with Docker database for consistency
3. Verify all endpoints work with new schema changes
4. Consider adding sample data to `docker/init.sql` for testing

---

## License

Part of the FastAPI Complete Course 2026 educational project.

---

**Last Updated**: Section 12 Complete  
**Next**: Section 13+ (Testing, Deployment, Frontend, Advanced Features)
