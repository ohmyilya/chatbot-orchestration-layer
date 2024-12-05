from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseBotService(ABC):
    """Base class for all bot service integrations."""
    
    @abstractmethod
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query and return the response."""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the service is healthy and available."""
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> list:
        """Return a list of service capabilities."""
        pass
