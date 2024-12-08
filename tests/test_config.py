import pytest
from app.core.config import Settings
from app.core.orchestrator import ModelAuthorizationError

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

def test_model_authorization_configuration():
    """Test model authorization configuration settings."""
    settings = Settings()
    
    # Test default authorized models
    assert "gpt-3.5-turbo" in settings.AUTHORIZED_MODELS
    assert "claude-2" in settings.AUTHORIZED_MODELS
    assert "llama2" in settings.AUTHORIZED_MODELS
    
    # Test authorization enabled by default
    assert settings.MODEL_AUTHORIZATION_ENABLED is True

def test_model_authorization_with_custom_env(monkeypatch):
    """Test custom model authorization configuration."""
    monkeypatch.setenv("AUTHORIZED_MODELS", "gpt-4,claude-3")
    monkeypatch.setenv("MODEL_AUTHORIZATION_ENABLED", "False")
    
    settings = Settings()
    
    assert settings.AUTHORIZED_MODELS == ["gpt-4", "claude-3"]
    assert settings.MODEL_AUTHORIZATION_ENABLED is False
