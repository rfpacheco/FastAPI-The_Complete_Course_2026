# FastAPI TodoApp - Testing Guide

## Overview

This directory contains unit and integration tests for the FastAPI TodoApp application using pytest.

### Test Types

- **Unit Tests**: Test individual functions and components in isolation
- **Integration Tests**: Test multiple components working together end-to-end

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures and pytest configuration
├── test_auth.py          # Authentication and registration tests
├── test_todos.py         # Todo CRUD operations tests
├── test_users.py         # User management and profile tests
├── test_admin.py         # Admin-only operations tests
└── README.md             # This file
```

## Quick Start

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_auth.py
```

### Run Specific Test Function
```bash
pytest tests/test_auth.py::test_register_user
```

### Run Tests by Marker
```bash
pytest -m unit           # Run only unit tests
pytest -m integration    # Run only integration tests
pytest -m auth           # Run only auth tests
```

### Run with Coverage Report
```bash
pytest --cov=TodoApp tests/
pytest --cov=TodoApp --cov-report=html tests/  # Generate HTML report
```

### Run Tests in Parallel (faster)
```bash
pip install pytest-xdist
pytest -n auto
```

## Available Fixtures

All fixtures are defined in `conftest.py`:

### Database
- `db` - Fresh test database for each test (SQLite in-memory)
- `client` - FastAPI TestClient with overridden database

### Users
- `admin_user` - Pre-created admin user (username: admintest, password: adminpass123)
- `regular_user` - Pre-created regular user (username: usertest, password: userpass123)

### Authentication
- `admin_token` - JWT token for admin user
- `user_token` - JWT token for regular user

### Data
- `sample_todo_data` - 3 sample todos for testing (belongs to regular_user)

## Example Test

```python
import pytest
from starlette import status

@pytest.mark.integration
def test_create_todo(client, user_token):
    """Integration test: Create a todo with authentication."""
    response = client.post(
        "/todo",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "title": "Buy milk",
            "description": "Whole milk",
            "priority": 2,
            "complete": False
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Buy milk"
    assert data["priority"] == 2
```

## Test Coverage

Target coverage metrics:
- Overall: > 80%
- Authentication: > 90%
- CRUD operations: > 85%
- Admin operations: > 85%

Check coverage:
```bash
pytest --cov=TodoApp --cov-report=term-missing tests/
```

## Best Practices

1. **One assertion per test (when possible)** - Makes failures clear
2. **Use descriptive names** - `test_create_todo_with_valid_data` not `test_create`
3. **Use markers** - Tag tests with @pytest.mark.unit or @pytest.mark.integration
4. **Use fixtures** - Don't create test data manually in tests
5. **Test edge cases** - Empty values, duplicates, permissions
6. **Test error cases** - 401, 404, 400 status codes
7. **Keep tests fast** - Use in-memory SQLite, avoid sleep()

## CI/CD Integration

These tests are designed to run in CI/CD pipelines:

```bash
# GitHub Actions example
pytest --cov=TodoApp --cov-report=xml tests/
```

## Debugging Tests

### Run single test with output
```bash
pytest tests/test_auth.py::test_register_user -v -s
```

### Drop into debugger on failure
```bash
pytest --pdb
```

### Show print statements
```bash
pytest -s
```

### Stop on first failure
```bash
pytest -x
```

## Common Issues

### Import Errors
Make sure you're running pytest from project root:
```bash
cd /path/to/FastAPI-The_Complete_Course_2026
pytest
```

### Database Connection Issues
Tests use SQLite in-memory. If you see connection errors, verify conftest.py is in the tests directory.

### Async Test Issues
Tests are configured with `asyncio_mode = auto` in pytest.ini. Ensure pytest-asyncio is installed:
```bash
pip install pytest-asyncio
```

## Next Steps

- [ ] Write unit tests for authentication
- [ ] Write integration tests for todo CRUD
- [ ] Write tests for admin operations
- [ ] Achieve 80%+ code coverage
- [ ] Set up CI/CD pipeline with pytest
