from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListResponse,
    MessageResponse,
)
from src.services.conversation_service import conversation_service

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.create_conversation(session, UUID(current_user_id), data)


@router.get("", response_model=ConversationListResponse)
async def list_conversations(
    page: int = 1,
    page_size: int = 20,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.list_conversations(session, UUID(current_user_id), page, page_size)


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    include_messages: bool = False,
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.get_conversation(session, conversation_id, include_messages)


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: UUID,
    data: ConversationUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.update_conversation(session, conversation_id, data)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    await conversation_service.delete_conversation(session, conversation_id)


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
):
    return await conversation_service.get_messages(session, conversation_id, limit, offset)
