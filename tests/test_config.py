import pytest
from app.core.config import Settings

def test_settings_default_values():
    settings = Settings()
    assert settings.PROJECT_NAME == "Chatbot Orchestration"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.DEBUG is False

def test_settings_environment_variables(monkeypatch):
    # Test that environment variables are properly loaded
    monkeypatch.setenv("PROJECT_NAME", "Test Project")
    monkeypatch.setenv("API_V1_STR", "/api/v2")
    monkeypatch.setenv("DEBUG", "True")
    
    settings = Settings()
    assert settings.PROJECT_NAME == "Test Project"
    assert settings.API_V1_STR == "/api/v2"
    assert settings.DEBUG is True

def test_settings_invalid_environment_variables(monkeypatch):
    # Test handling of invalid environment variables
    monkeypatch.setenv("PROJECT_NAME", "")
    monkeypatch.setenv("API_V1_STR", "invalid_api_path")
    
    settings = Settings()
    assert settings.PROJECT_NAME == "Chatbot Orchestration"  # Fallback to default
    assert settings.API_V1_STR == "/api/v1"  # Fallback to default
