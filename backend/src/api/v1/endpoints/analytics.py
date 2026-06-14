from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.analytics import AnalyticsDashboardResponse
from src.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=AnalyticsDashboardResponse)
async def get_dashboard(
    period: str = "7d",
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await analytics_service.get_dashboard(session, UUID(current_user_id), period)
