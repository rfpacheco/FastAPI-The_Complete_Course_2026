"""
FastAPI TodoApp Test Suite

Tests are organized by functionality:
- test_auth.py - Authentication and registration tests
- test_todos.py - Todo CRUD operation tests
- test_users.py - User management tests
- test_admin.py - Admin-only operation tests

Run all tests:
    pytest

Run specific test file:
    pytest tests/test_auth.py

Run with coverage:
    pytest --cov=TodoApp tests/

Run specific test marker:
    pytest -m unit
    pytest -m integration
"""
