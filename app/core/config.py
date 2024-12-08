from pydantic import BaseSettings, validator
from typing import List, Dict, Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot Orchestration Layer"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/chatbot_orchestration")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Configurations
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Service Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", 2000))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.7))
    
    # Model Authorization
    AUTHORIZED_MODELS: List[str] = os.getenv("AUTHORIZED_MODELS", "gpt-3.5-turbo,claude-2,llama2").split(",")
    MODEL_AUTHORIZATION_ENABLED: bool = os.getenv("MODEL_AUTHORIZATION_ENABLED", "True").lower() == "true"
    
    # Conversation Management
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", 10))
    CONVERSATION_TIMEOUT_MINUTES: int = int(os.getenv("CONVERSATION_TIMEOUT_MINUTES", 30))
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
