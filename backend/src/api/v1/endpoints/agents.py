from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.agent import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
from src.services.agent_service import agent_service

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    data: AgentCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.create_agent(session, UUID(current_user_id), data)


@router.get("", response_model=AgentListResponse)
async def list_user_agents(
    page: int = 1,
    page_size: int = 20,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.list_user_agents(session, UUID(current_user_id), page, page_size)


@router.get("/public", response_model=AgentListResponse)
async def list_public_agents(
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.list_public_agents(session, page, page_size)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.get_agent(session, agent_id)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    data: AgentUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.update_agent(session, agent_id, UUID(current_user_id), data)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    await agent_service.delete_agent(session, agent_id, UUID(current_user_id))


@router.post("/{agent_id}/clone", response_model=AgentResponse)
async def clone_agent(
    agent_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await agent_service.clone_agent(session, agent_id, UUID(current_user_id))
