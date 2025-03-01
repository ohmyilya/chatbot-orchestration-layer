from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.core.orchestrator import ChatbotOrchestrator
from app.models.service import ServiceCreate, ServiceUpdate, ServiceResponse
from app.core.dependencies import get_orchestrator
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/", response_model=ServiceResponse)
async def register_service(
    service: ServiceCreate,
    orchestrator: ChatbotOrchestrator = Depends(get_orchestrator)
) -> ServiceResponse:
    """
    Register a new bot service with the orchestrator.

    Args:
        service (ServiceCreate): The service to be registered.
        orchestrator (ChatbotOrchestrator): The orchestrator dependency.

    Returns:
        ServiceResponse: The response after registering the service.
    """
    try:
        logger.info("Registering new service: %s", service.name)
        return await orchestrator.register_service(service)
    except ValueError as e:
        logger.error("Error registering service: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[ServiceResponse])
async def list_services(
    orchestrator: ChatbotOrchestrator = Depends(get_orchestrator)
):
    """List all registered bot services."""
    return orchestrator.get_available_services()

@router.post("/query", response_model=Dict[str, Any])
async def process_query(
    query: str,
    orchestrator: ChatbotOrchestrator = Depends(get_orchestrator)
):
    """Process a query through the appropriate bot service."""
    response = await orchestrator.process_query(query)
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])
    return response

@router.delete("/{service_name}")
async def deregister_service(
    service_name: str,
    orchestrator: ChatbotOrchestrator = Depends(get_orchestrator)
):
    """Remove a bot service from the orchestrator."""
    try:
        orchestrator.deregister_service(service_name)
        return {"message": f"Service {service_name} successfully deregistered"}
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Service {service_name} not found"
        )
