from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends
from src.services.marketplace_service import marketplace_service

router = APIRouter(prefix="/marketplace", tags=["Marketplace"])


@router.get("/integrations", response_model=List[Dict[str, Any]])
async def list_integrations(
    category: Optional[str] = None,
    status: Optional[str] = None,
):
    return await marketplace_service.list_integrations(category, status)


@router.get("/integrations/{integration_id}", response_model=Dict[str, Any])
async def get_integration(integration_id: str):
    integration = await marketplace_service.get_integration(integration_id)
    if not integration:
        from src.core.exceptions import NotFoundError
        raise NotFoundError("Integration", integration_id)
    return integration
