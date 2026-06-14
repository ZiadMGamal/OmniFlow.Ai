from uuid import UUID
from typing import List, Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.memory import Memory
from src.dao.base import BaseDAO


class LongTermMemory(BaseDAO[Memory]):
    """Manages persistent core memories in PostgreSQL"""
    
    def __init__(self):
        super().__init__(Memory)
        
    async def add_core_memory(
        self, session: AsyncSession, user_id: UUID, content: str, category: str = "general"
    ) -> Memory:
        data = {
            "user_id": user_id,
            "memory_type": "core",
            "content": content,
            "category": category,
            "importance": 1.0, # Core memories are always highly important
        }
        return await self.create(session, data)
        
    async def get_core_memories(
        self, session: AsyncSession, user_id: UUID
    ) -> List[Memory]:
        query = select(Memory).where(
            Memory.user_id == user_id,
            Memory.memory_type == "core",
            Memory.is_deleted == False
        )
        result = await session.execute(query)
        return list(result.scalars().all())


long_term_memory = LongTermMemory()
