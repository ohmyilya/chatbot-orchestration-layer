from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ServiceBase(BaseModel):
    name: str
    endpoint: HttpUrl
    capabilities: List[str]
    description: Optional[str] = None
    max_concurrent_requests: Optional[int] = None
    timeout_seconds: Optional[float] = 30.0

class ServiceCreate(ServiceBase):
    api_key: Optional[str] = None
    headers: Optional[dict] = None

class ServiceUpdate(ServiceBase):
    name: Optional[str] = None
    endpoint: Optional[HttpUrl] = None
    capabilities: Optional[List[str]] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: str
    is_active: bool
    current_load: int = 0
    success_rate: float = 100.0
    average_response_time: float = 0.0

    class Config:
        orm_mode = True
