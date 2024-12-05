import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import Settings

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def settings():
    return Settings()

@pytest.fixture
def test_message():
    return {
        "content": "test message",
        "user_id": "test_user",
        "metadata": {"source": "test"}
    }

@pytest.fixture
def test_headers():
    return {"Content-Type": "application/json"}
