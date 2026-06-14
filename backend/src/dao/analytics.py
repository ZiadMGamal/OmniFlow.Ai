from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.analytics import AnalyticsEvent


class AnalyticsDAO(BaseDAO[AnalyticsEvent]):
    def __init__(self):
        super().__init__(AnalyticsEvent)

    async def get_user_events(
        self, session: AsyncSession, user_id: UUID, event_type: Optional[str] = None, limit: int = 100
    ):
        filters = {"user_id": user_id}
        if event_type:
            filters["event_type"] = event_type
        return await self.get_all(session, page=1, page_size=limit, filters=filters)

    async def get_total_tokens(self, session: AsyncSession, user_id: UUID) -> int:
        query = (
            select(func.sum(AnalyticsEvent.total_tokens))
            .where(AnalyticsEvent.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalar() or 0

    async def get_total_cost(self, session: AsyncSession, user_id: UUID) -> float:
        query = (
            select(func.sum(AnalyticsEvent.cost))
            .where(AnalyticsEvent.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalar() or 0.0

    async def get_avg_latency(self, session: AsyncSession, user_id: UUID) -> float:
        query = (
            select(func.avg(AnalyticsEvent.latency_ms))
            .where(AnalyticsEvent.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalar() or 0.0


analytics_dao = AnalyticsDAO()
