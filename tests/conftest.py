"""
Pytest configuration and fixtures for FastAPI TodoApp testing.

Provides:
- Test database setup and teardown
- Test client for API endpoints
- Authentication token fixtures
- Sample data fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Import app and models
import sys
from pathlib import Path

# Add parent directory to path to import TodoApp modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from TodoApp.main import app
from TodoApp.database import Base
from TodoApp.database import SessionLocal
from TodoApp.routers.auth import get_db


# ============================================================================
# Database Configuration
# ============================================================================

# Use in-memory SQLite for testing (faster, isolated)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def db():
    """Create a fresh test database for each test."""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with overridden database dependency."""
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db):
    """Create a test admin user in the database."""
    from TodoApp.models import Users
    from TodoApp.routers.auth import bcrypt_context

    user = Users(
        username="admintest",
        email="admin@test.com",
        first_name="Admin",
        last_name="User",
        hashed_password=bcrypt_context.hash("adminpass123"),
        is_active=True,
        role="admin",
        phone_number="+1-555-0001"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def regular_user(db):
    """Create a test regular user in the database."""
    from TodoApp.models import Users
    from TodoApp.routers.auth import bcrypt_context

    user = Users(
        username="usertest",
        email="user@test.com",
        first_name="Regular",
        last_name="User",
        hashed_password=bcrypt_context.hash("userpass123"),
        is_active=True,
        role="user",
        phone_number="+1-555-0002"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_token(client, admin_user):
    """Get JWT token for admin user."""
    response = client.post(
        "/auth/token",
        data={"username": "admintest", "password": "adminpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def user_token(client, regular_user):
    """Get JWT token for regular user."""
    response = client.post(
        "/auth/token",
        data={"username": "usertest", "password": "userpass123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def sample_todo_data(db, regular_user):
    """Create sample todos for testing."""
    from TodoApp.models import Todos

    todos = [
        Todos(
            title="Buy groceries",
            description="Milk, eggs, bread",
            priority=2,
            complete=False,
            owner_id=regular_user.id
        ),
        Todos(
            title="Complete project",
            description="Finish FastAPI project",
            priority=1,
            complete=False,
            owner_id=regular_user.id
        ),
        Todos(
            title="Call dentist",
            description="Schedule appointment",
            priority=3,
            complete=True,
            owner_id=regular_user.id
        ),
    ]

    for todo in todos:
        db.add(todo)
    db.commit()

    for todo in todos:
        db.refresh(todo)

    return todos
