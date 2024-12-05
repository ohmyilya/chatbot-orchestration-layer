import pytest
from app.core.config import Settings

def test_settings():
    settings = Settings()
    assert hasattr(settings, "PROJECT_NAME")
    assert hasattr(settings, "API_V1_STR")
    assert settings.PROJECT_NAME == "Chatbot Orchestration"
    assert settings.API_V1_STR == "/api/v1"

def test_settings_environment_variables(monkeypatch):
    # Test that environment variables are properly loaded
    monkeypatch.setenv("PROJECT_NAME", "Test Project")
    monkeypatch.setenv("API_V1_STR", "/api/v2")
    
    settings = Settings()
    assert settings.PROJECT_NAME == "Test Project"
    assert settings.API_V1_STR == "/api/v2"
