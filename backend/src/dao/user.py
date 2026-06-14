from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.user import User


class UserDAO(BaseDAO[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        query = select(User).where(User.email == email, User.is_deleted == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def email_exists(self, session: AsyncSession, email: str) -> bool:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        return result.scalar_one_or_none() is not None

    async def get_active_users(self, session: AsyncSession, page: int = 1, page_size: int = 20):
        return await self.get_all(
            session, page, page_size, filters={"is_active": True}
        )

    async def update_token_usage(self, session: AsyncSession, user_id, tokens: int, cost: float):
        user = await self.get_by_id(session, user_id)
        if user:
            user.total_tokens_used += tokens
            user.total_cost += int(cost * 100)
            await session.flush()


user_dao = UserDAO()
