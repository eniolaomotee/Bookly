from src.db.db import get_session
from src import app
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.auth.dependencies import RoleChecker,AccessTokenBearer,RefreshTokenBearer
import pytest

mock_session = AsyncMock()

mock_user_service = AsyncMock()


mock_book_service = AsyncMock()

def get_mock_session():
    yield mock_session
    
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])

    
app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = AsyncMock()
app.dependency_overrides['refresh_token_bearer'] = AsyncMock()

@pytest.fixture
def fake_session():
    """
    Fixture to provide a mock session for testing.
    """
    return mock_session

@pytest.fixture
def fake_user_service():
    """
    Fixture to provide a mock user service for testing.
    """
    return mock_user_service

@pytest.fixture
def test_client():
    """
    Fixture to provide a test client for the FastAPI app.
    """
    return TestClient(app)

@pytest.fixture
def fake_book_service():
    """
    Fixture to provide a mock book service for testing.
    """
    return mock_book_service