from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id, require_admin
from src.schemas.user import UserResponse, UserUpdate, PasswordChangeRequest, UserListResponse
from src.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_user(session, UUID(current_user_id))


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    data: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await user_service.update_user(session, UUID(current_user_id), data)


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    data: PasswordChangeRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    await user_service.change_password(
        session, UUID(current_user_id), data.current_password, data.new_password
    )


@router.get("", response_model=UserListResponse, dependencies=[Depends(require_admin)])
async def list_users(
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.list_users(session, page, page_size)


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_admin)])
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await user_service.get_user(session, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    await user_service.delete_user(session, user_id)
