"""
Authentication Tests - Unit and Integration Tests

Tests for:
- User registration
- Login and JWT token generation
- Token validation
- Password hashing
"""

import pytest
from starlette import status


class TestUserRegistration:
    """Integration tests for user registration."""

    @pytest.mark.integration
    def test_register_user_success(self, client):
        """Test successful user registration with valid data."""
        response = client.post(
            "/auth/",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepass123",
                "role": "user",
                "phone_number": "+1-555-1234"
            }
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.integration
    def test_register_user_missing_phone(self, client):
        """Test registration fails when phone_number is missing."""
        response = client.post(
            "/auth/",
            json={
                "username": "newuser2",
                "email": "new2@example.com",
                "first_name": "Jane",
                "last_name": "Doe",
                "password": "securepass123",
                "role": "user"
                # Missing phone_number
            }
        )

        # Should fail validation (422 Unprocessable Entity)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.integration
    def test_register_duplicate_username(self, client, regular_user):
        """Test registration fails with duplicate username."""
        response = client.post(
            "/auth/",
            json={
                "username": "usertest",  # Same as regular_user
                "email": "different@example.com",
                "first_name": "Different",
                "last_name": "User",
                "password": "pass123",
                "role": "user",
                "phone_number": "+1-555-9999"
            }
        )

        # Should fail (likely 400 Bad Request or 409 Conflict)
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_409_CONFLICT,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]

    @pytest.mark.integration
    def test_register_duplicate_email(self, client, regular_user):
        """Test registration fails with duplicate email."""
        response = client.post(
            "/auth/",
            json={
                "username": "differentuser",
                "email": "user@test.com",  # Same as regular_user
                "first_name": "Different",
                "last_name": "Name",
                "password": "pass123",
                "role": "user",
                "phone_number": "+1-555-9999"
            }
        )

        # Should fail
        assert response.status_code in [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_409_CONFLICT,
            status.HTTP_422_UNPROCESSABLE_ENTITY
        ]


class TestLogin:
    """Integration tests for login and token generation."""

    @pytest.mark.integration
    def test_login_success(self, client, regular_user):
        """Test successful login returns JWT token."""
        response = client.post(
            "/auth/token",
            data={"username": "usertest", "password": "userpass123"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.integration
    def test_login_invalid_password(self, client, regular_user):
        """Test login fails with incorrect password."""
        response = client.post(
            "/auth/token",
            data={"username": "usertest", "password": "wrongpassword"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.integration
    def test_login_user_not_found(self, client):
        """Test login fails with non-existent username."""
        response = client.post(
            "/auth/token",
            data={"username": "nonexistent", "password": "anypass"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.integration
    def test_token_format(self, client, user_token):
        """Test that token is a valid JWT format."""
        # Token should have 3 parts separated by dots (header.payload.signature)
        parts = user_token.split(".")
        assert len(parts) == 3


class TestTokenValidation:
    """Integration tests for token validation."""

    @pytest.mark.integration
    def test_access_protected_route_with_valid_token(self, client, user_token):
        """Test accessing protected route with valid token."""
        response = client.get(
            "/user/",
            headers={"Authorization": f"Bearer {user_token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "usertest"
        assert data["email"] == "user@test.com"

    @pytest.mark.integration
    def test_access_protected_route_without_token(self, client):
        """Test accessing protected route without token."""
        response = client.get("/user/")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.integration
    def test_access_protected_route_with_invalid_token(self, client):
        """Test accessing protected route with invalid token."""
        response = client.get(
            "/user/",
            headers={"Authorization": "Bearer invalid.token.here"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.integration
    def test_access_protected_route_with_malformed_auth_header(self, client):
        """Test with malformed Authorization header."""
        response = client.get(
            "/user/",
            headers={"Authorization": "InvalidFormat"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
