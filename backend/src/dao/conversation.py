from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.conversation import Conversation, Message


class ConversationDAO(BaseDAO[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    async def get_user_conversations(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        return await self.get_all(session, page, page_size, filters={"user_id": user_id})

    async def get_with_messages(
        self, session: AsyncSession, conversation_id: UUID
    ) -> Optional[Conversation]:
        query = (
            select(Conversation)
            .options(selectinload(Conversation.messages))
            .where(
                Conversation.id == conversation_id,
                Conversation.is_deleted == False,
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def increment_message_count(
        self, session: AsyncSession, conversation_id: UUID, tokens: int = 0, cost: float = 0.0
    ):
        conv = await self.get_by_id(session, conversation_id)
        if conv:
            conv.total_messages += 1
            conv.total_tokens += tokens
            conv.total_cost += cost
            await session.flush()


class MessageDAO(BaseDAO[Message]):
    def __init__(self):
        super().__init__(Message)

    async def get_conversation_messages(
        self,
        session: AsyncSession,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Message]:
        query = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.is_deleted == False,
            )
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def get_recent_messages(
        self, session: AsyncSession, conversation_id: UUID, limit: int = 10
    ) -> List[Message]:
        query = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.is_deleted == False,
            )
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        messages = list(result.scalars().all())
        messages.reverse()
        return messages


conversation_dao = ConversationDAO()
message_dao = MessageDAO()
