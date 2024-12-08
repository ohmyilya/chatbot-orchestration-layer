import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings
from typing import Dict, Any

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def settings():
    return Settings()

@pytest.fixture
def test_message() -> Dict[str, Any]:
    return {
        "content": "test message",
        "user_id": "test_user",
        "metadata": {
            "source": "test",
            "timestamp": "2024-01-01T00:00:00Z",
            "priority": "normal"
        }
    }

@pytest.fixture
def test_headers() -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer test_token"
    }

@pytest.fixture
def invalid_test_message() -> Dict[str, Any]:
    return {
        "content": "",
        "user_id": None,
        "metadata": {}
    }
