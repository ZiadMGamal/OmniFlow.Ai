from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class MemoryCreate(BaseModel):
    content: str
    memory_type: str = "long_term"
    category: Optional[str] = None
    importance: float = 0.5
    metadata: Dict[str, Any] = {}


class MemoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    memory_type: str
    content: str
    summary: Optional[str] = None
    category: Optional[str] = None
    importance: float
    created_at: datetime

    class Config:
        from_attributes = True


class MemoryListResponse(BaseModel):
    memories: List[MemoryResponse]
    total: int
    page: int
    page_size: int


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 10
    memory_type: Optional[str] = None
    category: Optional[str] = None
