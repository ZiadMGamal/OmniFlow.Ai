from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError
from src.core.security import hash_password, verify_password
from src.dao.user import user_dao
from src.schemas.user import UserUpdate, UserResponse


class UserService:
    async def get_user(self, session: AsyncSession, user_id: UUID) -> UserResponse:
        user = await user_dao.get_by_id(session, user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        return UserResponse.model_validate(user)

    async def update_user(
        self, session: AsyncSession, user_id: UUID, data: UserUpdate
    ) -> UserResponse:
        update_data = data.model_dump(exclude_unset=True)
        user = await user_dao.update(session, user_id, update_data)
        if not user:
            raise NotFoundError("User", str(user_id))
        return UserResponse.model_validate(user)

    async def change_password(
        self, session: AsyncSession, user_id: UUID, current_password: str, new_password: str
    ):
        user = await user_dao.get_by_id(session, user_id)
        if not user:
            raise NotFoundError("User", str(user_id))
        if not verify_password(current_password, user.hashed_password):
            from src.core.exceptions import AuthenticationError
            raise AuthenticationError("Current password is incorrect")
        await user_dao.update(session, user_id, {"hashed_password": hash_password(new_password)})

    async def list_users(self, session: AsyncSession, page: int = 1, page_size: int = 20):
        users, total = await user_dao.get_all(session, page, page_size)
        return {
            "users": [UserResponse.model_validate(u) for u in users],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def delete_user(self, session: AsyncSession, user_id: UUID):
        success = await user_dao.soft_delete(session, user_id)
        if not success:
            raise NotFoundError("User", str(user_id))


user_service = UserService()
