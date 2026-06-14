from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    triggers: List[Dict[str, Any]] = []
    category: Optional[str] = None
    tags: List[str] = []
    config: Dict[str, Any] = {}


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[Dict[str, Any]]] = None
    edges: Optional[List[Dict[str, Any]]] = None
    triggers: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    config: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    triggers: List[Dict[str, Any]]
    is_active: bool
    is_public: bool
    category: Optional[str] = None
    tags: List[str]
    config: Dict[str, Any]
    total_runs: int
    success_rate: float
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkflowListResponse(BaseModel):
    workflows: List[WorkflowResponse]
    total: int
    page: int
    page_size: int


class WorkflowExecuteRequest(BaseModel):
    input_data: Dict[str, Any] = {}
    trigger_type: str = "manual"


class WorkflowExecutionResponse(BaseModel):
    id: UUID
    workflow_id: UUID
    status: str
    trigger_type: Optional[str] = None
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None
    node_results: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


class WorkflowNodeSchema(BaseModel):
    id: str
    type: str
    label: str
    position: Dict[str, float]
    data: Dict[str, Any] = {}
    config: Dict[str, Any] = {}


class WorkflowEdgeSchema(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    condition: Optional[Dict[str, Any]] = None
