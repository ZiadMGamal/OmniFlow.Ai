from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.tool import Tool


class ToolDAO(BaseDAO[Tool]):
    def __init__(self):
        super().__init__(Tool)

    async def get_by_slug(self, session: AsyncSession, slug: str) -> Optional[Tool]:
        query = select(Tool).where(Tool.slug == slug, Tool.is_deleted == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, session: AsyncSession, name: str) -> Optional[Tool]:
        query = select(Tool).where(Tool.name == name, Tool.is_deleted == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_active_tools(self, session: AsyncSession):
        return await self.get_all(session, page=1, page_size=100, filters={"is_active": True})

    async def get_by_category(self, session: AsyncSession, category: str):
        return await self.get_all(session, page=1, page_size=100, filters={"category": category})


tool_dao = ToolDAO()
