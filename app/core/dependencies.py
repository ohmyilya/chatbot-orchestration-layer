from typing import AsyncGenerator
from fastapi import Depends
from app.core.orchestrator import ChatbotOrchestrator
from app.core.config import settings
import redis.asyncio as redis

# Global instances
_redis_client = None
_orchestrator = None

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """Get Redis connection."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
    try:
        yield _redis_client
    finally:
        pass  # Connection will be handled by the global client

async def get_orchestrator(
    redis: redis.Redis = Depends(get_redis)
) -> ChatbotOrchestrator:
    """Get ChatbotOrchestrator instance."""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ChatbotOrchestrator()
        # Initialize orchestrator with any persisted services
        services = await redis.hgetall("services")
        for service_data in services.values():
            await _orchestrator.register_service(service_data)
    return _orchestrator
