from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class ToolResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    category: Optional[str] = None
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    permission_level: str
    is_active: bool
    is_builtin: bool
    requires_api_key: bool
    icon: Optional[str] = None
    version: str
    total_executions: int
    avg_latency_ms: int
    success_rate: int
    created_at: datetime

    class Config:
        from_attributes = True


class ToolListResponse(BaseModel):
    tools: List[ToolResponse]
    total: int


class ToolExecutionLog(BaseModel):
    id: UUID
    tool_name: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: str
    error: Optional[str] = None
    duration_ms: int
    user_id: UUID
    created_at: datetime
