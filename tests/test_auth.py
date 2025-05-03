import pytest
from unittest.mock import patch, MagicMock
from app.schemas.auth import Token
from .conftest import client


@pytest.fixture
def mock_create_new_user():
    with patch("app.crud.user.create_new_user") as mock:
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.name = "Test User"
        mock_user.hashed_password = "$2b$12$TpwjKRUgJy7yXYETKt6ule7lUiqGgJS.dZ7fUg8XEymRUemfrqjKK"
        mock.return_value = mock_user
        yield mock


@pytest.fixture
def mock_authenticate_user():
    with patch("app.crud.user.authenticate_user") as mock:
        mock.return_value = Token(
            access="mocked_access_token",
            refresh="mocked_refresh_token"
        )
        yield mock


@pytest.fixture
def mock_refresh_access_token():
    with patch("app.core.security.refresh_access_token") as mock:
        mock.return_value = {"access": "new_mocked_access_token"}
        yield mock


@pytest.fixture
def mock_verify_token():
    with patch("app.core.security.verify_token") as mock:
        mock.return_value = {"sub": "1", "type": "refresh"}
        yield mock


class TestAuthEndpoints:
    @patch("app.api.auth.create_new_user")
    def test_register_endpoint(self, mock_create_api, mock_create_new_user):
        mock_create_api.return_value = {"message": "User created successfully"}

        user_data = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }

        response = client.post("/register", json=user_data)

        assert response.status_code == 200
        assert response.json() == {"message": "User created successfully"}


    @patch("app.api.auth.authenticate_user")
    def test_login_endpoint(self, mock_login_api, mock_authenticate_user):
        mock_login_api.return_value = {
            "access": "mocked_access_token",
            "refresh": "mocked_refresh_token"
        }

        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = client.post("/login", json=login_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "access" in response_data
        assert "refresh" in response_data

    @patch("app.api.auth.refresh_access_token")
    def test_refresh_token_endpoint(self, mock_refresh_api, mock_refresh_access_token, mock_verify_token):
        mock_refresh_api.return_value = {"access": "new_mocked_access_token"}

        refresh_data = {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidHlwZSI6InJlZnJlc2gifQ.mock_signature"
        }

        response = client.post("/refresh", json=refresh_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "access" in response_data


class TestAuthEndpointsFailure:
    def test_register_endpoint_failure(self):
        with patch("app.api.auth.create_new_user") as mock_create_new_user:
            from fastapi import HTTPException
            mock_create_new_user.side_effect = HTTPException(status_code=400, detail="Email already registered")

            user_data = {
                "email": "existing@example.com",
                "name": "Existing User",
                "password": "password123"
            }

            response = client.post("/register", json=user_data)

            assert response.status_code == 400
            assert response.json() == {"detail": "Email already registered"}

    def test_login_endpoint_failure(self):
        with patch("app.api.auth.authenticate_user") as mock_authenticate_user:
            from fastapi import HTTPException
            mock_authenticate_user.side_effect = HTTPException(status_code=400, detail="Incorrect password")

            login_data = {
                "email": "test@example.com",
                "password": "wrong_password"
            }

            response = client.post("/login", json=login_data)

            assert response.status_code == 400
            assert response.json() == {"detail": "Incorrect password"}

    def test_refresh_token_endpoint_failure(self):
        with patch("app.api.auth.refresh_access_token") as mock_refresh_access_token:
            from fastapi import HTTPException
            mock_refresh_access_token.side_effect = HTTPException(status_code=401, detail="Invalid refresh token")

            refresh_data = {
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidHlwZSI6ImludmFsaWQifQ.mock_signature"
            }

            response = client.post("/refresh", json=refresh_data)

            assert response.status_code == 401
            assert response.json() == {"detail": "Invalid refresh token"}