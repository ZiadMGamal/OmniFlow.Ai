from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    agent_type: str = "general"
    system_prompt: Optional[str] = None
    model: str = "gpt-4o"
    provider: str = "openai"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=100, le=128000)
    tools: List[str] = []
    is_public: bool = False
    avatar_url: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    config: Dict[str, Any] = {}


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    tools: Optional[List[str]] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None
    avatar_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class AgentResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    agent_type: str
    system_prompt: Optional[str] = None
    model: str
    provider: str
    temperature: float
    max_tokens: int
    tools: List[str]
    is_public: bool
    is_active: bool
    avatar_url: Optional[str] = None
    category: Optional[str] = None
    tags: List[str]
    config: Dict[str, Any]
    total_runs: int
    success_rate: float
    avg_latency: float
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    agents: List[AgentResponse]
    total: int
    page: int
    page_size: int


class AgentExecuteRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    attachments: Optional[List[str]] = None
    stream: bool = True
