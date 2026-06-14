from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    agent_id: Optional[UUID] = None
    model: Optional[str] = None
    provider: Optional[str] = None


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    pinned: Optional[int] = None


class MessageCreate(BaseModel):
    content: str
    role: str = "user"
    attachments: Optional[List[str]] = None


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: Optional[str] = None
    message_type: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[str] = None
    sources: Optional[List[Dict[str, Any]]] = None
    attachments: Optional[List[str]] = None
    tokens_used: int
    cost: float
    latency_ms: int
    model: Optional[str] = None
    provider: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: UUID
    title: Optional[str] = None
    summary: Optional[str] = None
    user_id: UUID
    agent_id: Optional[UUID] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    total_messages: int
    total_tokens: int
    total_cost: float
    pinned: int
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    conversations: List[ConversationResponse]
    total: int
    page: int
    page_size: int


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    stream: bool = True
    attachments: Optional[List[str]] = None
    tools_enabled: bool = True
    memory_enabled: bool = True
    rag_enabled: bool = True


class ChatStreamEvent(BaseModel):
    event: str
    data: Dict[str, Any]
    timestamp: datetime


class AgentThought(BaseModel):
    step: int
    thought: str
    action: Optional[str] = None
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    reasoning: Optional[str] = None
