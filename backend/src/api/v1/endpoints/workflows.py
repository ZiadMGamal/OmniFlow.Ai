from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowListResponse,
    WorkflowExecuteRequest,
    WorkflowExecutionResponse,
)
from src.services.workflow_service import workflow_service

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    data: WorkflowCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.create_workflow(session, UUID(current_user_id), data)


@router.get("", response_model=WorkflowListResponse)
async def list_user_workflows(
    page: int = 1,
    page_size: int = 20,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.list_user_workflows(session, UUID(current_user_id), page, page_size)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.get_workflow(session, workflow_id)


@router.patch("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: UUID,
    data: WorkflowUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.update_workflow(session, workflow_id, UUID(current_user_id), data)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    await workflow_service.delete_workflow(session, workflow_id, UUID(current_user_id))


@router.post("/{workflow_id}/execute", response_model=WorkflowExecutionResponse)
async def execute_workflow(
    workflow_id: UUID,
    data: WorkflowExecuteRequest,
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.execute_workflow(session, workflow_id, data)


@router.get("/{workflow_id}/executions")
async def get_executions(
    workflow_id: UUID,
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
):
    return await workflow_service.get_executions(session, workflow_id, page, page_size)
