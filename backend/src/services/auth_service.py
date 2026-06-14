from datetime import timedelta
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from src.core.config import settings
from src.core.exceptions import AuthenticationError, ValidationError
from src.dao.user import user_dao
from src.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse


class AuthService:
    async def register(self, session: AsyncSession, data: UserCreate) -> TokenResponse:
        if await user_dao.email_exists(session, data.email):
            raise ValidationError("Email already registered")

        user = await user_dao.create(session, {
            "email": data.email,
            "hashed_password": hash_password(data.password),
            "full_name": data.full_name,
            "role": "user",
        })

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role, "email": user.email},
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )

    async def login(self, session: AsyncSession, data: UserLogin) -> TokenResponse:
        user = await user_dao.get_by_email(session, data.email)
        if not user:
            raise AuthenticationError("Invalid email or password")

        if not verify_password(data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("Account is disabled")

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role, "email": user.email},
        )
        refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )

    async def refresh_token(self, session: AsyncSession, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid refresh token")

        user_id = payload.get("sub")
        user = await user_dao.get_by_id(session, UUID(user_id))
        if not user or not user.is_active:
            raise AuthenticationError("User not found or disabled")

        new_access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"role": user.role, "email": user.email},
        )
        new_refresh_token = create_refresh_token(subject=str(user.id))

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )


auth_service = AuthService()
