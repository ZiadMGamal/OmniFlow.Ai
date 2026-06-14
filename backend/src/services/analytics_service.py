from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.analytics import analytics_dao
from src.schemas.analytics import AnalyticsDashboardResponse, AnalyticsOverview


class AnalyticsService:
    async def record_event(self, session: AsyncSession, event_data: dict):
        await analytics_dao.create(session, event_data)

    async def get_dashboard(
        self, session: AsyncSession, user_id: UUID, period: str = "7d"
    ) -> dict:
        total_tokens = await analytics_dao.get_total_tokens(session, user_id)
        total_cost = await analytics_dao.get_total_cost(session, user_id)
        avg_latency = await analytics_dao.get_avg_latency(session, user_id)
        events, total_events = await analytics_dao.get_user_events(session, user_id, limit=1000)

        success_count = sum(1 for e in events if e.status == "success")
        success_rate = (success_count / len(events) * 100) if events else 100.0

        overview = {
            "total_conversations": 0,
            "total_messages": 0,
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "total_agent_runs": total_events,
            "avg_latency_ms": avg_latency,
            "success_rate": success_rate,
            "active_users": 1,
        }

        return {
            "overview": overview,
            "token_usage": [],
            "agent_performance": [],
            "provider_usage": [],
            "recent_errors": [],
        }


analytics_service = AnalyticsService()
