from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[ModelType]:
        query = select(self.model).where(
            self.model.id == id,
            self.model.is_deleted == False,
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: str = "created_at",
        order_desc: bool = True,
    ) -> tuple[List[ModelType], int]:
        query = select(self.model).where(self.model.is_deleted == False)
        count_query = select(func.count()).select_from(self.model).where(self.model.is_deleted == False)

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.where(getattr(self.model, key) == value)
                    count_query = count_query.where(getattr(self.model, key) == value)

        total_result = await session.execute(count_query)
        total = total_result.scalar()

        if hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column.asc())

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        result = await session.execute(query)
        items = list(result.scalars().all())
        return items, total

    async def create(self, session: AsyncSession, data: Dict[str, Any]) -> ModelType:
        instance = self.model(**data)
        session.add(instance)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def update(self, session: AsyncSession, id: UUID, data: Dict[str, Any]) -> Optional[ModelType]:
        instance = await self.get_by_id(session, id)
        if not instance:
            return None
        for key, value in data.items():
            if hasattr(instance, key) and value is not None:
                setattr(instance, key, value)
        await session.flush()
        await session.refresh(instance)
        return instance

    async def soft_delete(self, session: AsyncSession, id: UUID) -> bool:
        instance = await self.get_by_id(session, id)
        if not instance:
            return False
        instance.is_deleted = True
        await session.flush()
        return True

    async def hard_delete(self, session: AsyncSession, id: UUID) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await session.execute(query)
        return result.rowcount > 0

    async def count(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count()).select_from(self.model).where(self.model.is_deleted == False)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.where(getattr(self.model, key) == value)
        result = await session.execute(query)
        return result.scalar()

    async def exists(self, session: AsyncSession, id: UUID) -> bool:
        query = select(func.count()).select_from(self.model).where(
            self.model.id == id,
            self.model.is_deleted == False,
        )
        result = await session.execute(query)
        return result.scalar() > 0
