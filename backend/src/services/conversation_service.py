from uuid import UUID
from typing import Optional, List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError
from src.dao.conversation import conversation_dao, message_dao
from src.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)


class ConversationService:
    async def create_conversation(
        self, session: AsyncSession, user_id: UUID, data: ConversationCreate
    ) -> ConversationResponse:
        conv_data = data.model_dump()
        conv_data["user_id"] = user_id
        conv = await conversation_dao.create(session, conv_data)
        return ConversationResponse.model_validate(conv)

    async def get_conversation(
        self, session: AsyncSession, conversation_id: UUID, include_messages: bool = False
    ) -> ConversationResponse:
        if include_messages:
            conv = await conversation_dao.get_with_messages(session, conversation_id)
        else:
            conv = await conversation_dao.get_by_id(session, conversation_id)
        if not conv:
            raise NotFoundError("Conversation", str(conversation_id))
        return ConversationResponse.model_validate(conv)

    async def update_conversation(
        self, session: AsyncSession, conversation_id: UUID, data: ConversationUpdate
    ) -> ConversationResponse:
        update_data = data.model_dump(exclude_unset=True)
        conv = await conversation_dao.update(session, conversation_id, update_data)
        if not conv:
            raise NotFoundError("Conversation", str(conversation_id))
        return ConversationResponse.model_validate(conv)

    async def delete_conversation(self, session: AsyncSession, conversation_id: UUID):
        success = await conversation_dao.soft_delete(session, conversation_id)
        if not success:
            raise NotFoundError("Conversation", str(conversation_id))

    async def list_conversations(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        convs, total = await conversation_dao.get_user_conversations(
            session, user_id, page, page_size
        )
        return {
            "conversations": [ConversationResponse.model_validate(c) for c in convs],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def add_message(
        self, session: AsyncSession, conversation_id: UUID, data: dict
    ) -> MessageResponse:
        data["conversation_id"] = conversation_id
        message = await message_dao.create(session, data)
        await conversation_dao.increment_message_count(
            session,
            conversation_id,
            tokens=data.get("tokens_used", 0),
            cost=data.get("cost", 0.0),
        )
        return MessageResponse.model_validate(message)

    async def get_messages(
        self,
        session: AsyncSession,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> List[MessageResponse]:
        messages = await message_dao.get_conversation_messages(
            session, conversation_id, limit, offset
        )
        return [MessageResponse.model_validate(m) for m in messages]

    async def get_recent_context(
        self, session: AsyncSession, conversation_id: UUID, limit: int = 10
    ) -> List[dict]:
        messages = await message_dao.get_recent_messages(session, conversation_id, limit)
        return [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.content
        ]


conversation_service = ConversationService()
