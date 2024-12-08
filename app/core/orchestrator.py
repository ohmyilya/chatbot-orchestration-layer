from typing import Dict, List, Optional
from pydantic import BaseModel
import uuid
import asyncio
import time
from dataclasses import dataclass
from app.core.config import settings

class BotService(BaseModel):
    name: str
    endpoint: str
    capabilities: List[str]
    is_active: bool = True

@dataclass
class ServiceCreate:
    name: str
    endpoint: str
    capabilities: List[str]
    description: str

@dataclass
class ServiceResponse:
    id: str
    name: str
    endpoint: str
    capabilities: List[str]
    description: str
    is_active: bool

class ModelAuthorizationError(Exception):
    """Exception raised when a model is not authorized."""
    pass

class ChatbotOrchestrator:
    def __init__(self):
        self.services: Dict[str, BotService] = {}
        self._load_metrics: Dict[str, Dict] = {}
        self._last_health_check: Dict[str, float] = {}

    async def register_service(self, service: ServiceCreate) -> ServiceResponse:
        """Register a new bot service with the orchestrator."""
        if service.name in self.services:
            raise ValueError(f"Service {service.name} already exists")
        
        service_id = str(uuid.uuid4())
        service_response = ServiceResponse(
            id=service_id,
            name=service.name,
            endpoint=service.endpoint,
            capabilities=service.capabilities,
            description=service.description,
            is_active=True
        )
        
        self.services[service.name] = service_response
        self._load_metrics[service.name] = {
            "requests": 0,
            "success": 0,
            "total_time": 0
        }
        return service_response

    def deregister_service(self, service_name: str) -> None:
        """Remove a bot service from the orchestrator."""
        if service_name in self.services:
            del self.services[service_name]
            del self._load_metrics[service_name]

    def get_available_services(self) -> List[BotService]:
        """Get list of all active services."""
        return [service for service in self.services.values() if service.is_active]

    async def route_query(self, query: str) -> Optional[BotService]:
        """Route a query to the most appropriate bot service."""
        available_services = self.get_available_services()
        if not available_services:
            return None

        # Simple load balancing - choose service with least current load
        return min(
            available_services,
            key=lambda s: self._load_metrics[s.name]["requests"]
        )

    async def process_query(self, query: str) -> Dict:
        """Process a query through the appropriate bot service."""
        service = await self.route_query(query)
        if not service:
            return {"error": "No suitable service found for query"}
        
        try:
            self._load_metrics[service.name]["requests"] += 1
            start_time = time.time()
            
            # Simulate processing (replace with actual service call)
            await asyncio.sleep(0.1)
            response = {
                "service": service.name,
                "response": f"Processed by {service.name}: {query}"
            }
            
            # Update metrics
            self._load_metrics[service.name]["success"] += 1
            self._load_metrics[service.name]["total_time"] += time.time() - start_time
            
            return response
        except Exception as e:
            return {"error": f"Service error: {str(e)}"}
        finally:
            self._load_metrics[service.name]["requests"] -= 1

    def get_service_metrics(self, service_name: str) -> Dict:
        """Get performance metrics for a service."""
        if service_name not in self._load_metrics:
            raise KeyError(f"Service {service_name} not found")
        
        metrics = self._load_metrics[service_name]
        total_requests = metrics["success"]
        if total_requests > 0:
            avg_time = metrics["total_time"] / total_requests
            success_rate = (metrics["success"] / total_requests) * 100
        else:
            avg_time = 0
            success_rate = 100
            
        return {
            "current_load": metrics["requests"],
            "total_requests": total_requests,
            "success_rate": success_rate,
            "average_response_time": avg_time
        }

    def _check_model_authorization(self, model_name: str) -> None:
        """
        Check if the model is authorized for use.
        
        Args:
            model_name (str): Name of the model to check
        
        Raises:
            ModelAuthorizationError: If model is not authorized
        """
        if settings.MODEL_AUTHORIZATION_ENABLED:
            if model_name not in settings.AUTHORIZED_MODELS:
                raise ModelAuthorizationError(f"Model '{model_name}' is not authorized for use.")
