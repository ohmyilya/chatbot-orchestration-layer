from typing import Dict, Any, List
from app.services.base import BaseBotService
import asyncio

class EchoBotService(BaseBotService):
    """A simple echo bot service for testing."""
    
    def __init__(self, name: str = "echo_bot"):
        self.name = name
        self._response_time = 0.1  # simulated response time in seconds
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Echo back the query with a simulated delay."""
        await asyncio.sleep(self._response_time)
        return {
            "service": self.name,
            "query": query,
            "response": f"Echo: {query}",
            "confidence": 1.0
        }
    
    async def health_check(self) -> bool:
        """Always healthy for this demo service."""
        return True
    
    @property
    def capabilities(self) -> List[str]:
        """List of bot capabilities."""
        return [
            "echo",
            "repeat",
            "mirror"
        ]
    
    def set_response_time(self, seconds: float) -> None:
        """Set the simulated response time."""
        self._response_time = max(0.0, seconds)
