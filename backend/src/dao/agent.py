from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.agent import Agent


class AgentDAO(BaseDAO[Agent]):
    def __init__(self):
        super().__init__(Agent)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Optional[Agent]:
        query = select(Agent).where(Agent.slug == slug, Agent.is_deleted == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_agents(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        return await self.get_all(session, page, page_size, filters={"owner_id": user_id})

    async def get_public_agents(self, session: AsyncSession, page: int = 1, page_size: int = 20):
        return await self.get_all(session, page, page_size, filters={"is_public": True})

    async def get_by_type(
        self, session: AsyncSession, agent_type: str, user_id: UUID
    ) -> List[Agent]:
        query = select(Agent).where(
            Agent.agent_type == agent_type,
            Agent.owner_id == user_id,
            Agent.is_deleted == False,
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def increment_runs(self, session: AsyncSession, agent_id: UUID):
        agent = await self.get_by_id(session, agent_id)
        if agent:
            agent.total_runs += 1
            await session.flush()


agent_dao = AgentDAO()
