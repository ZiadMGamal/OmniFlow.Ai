from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, Integer, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Workflow(BaseModel):
    __tablename__ = "workflows"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    nodes = Column(JSON, default=list)
    edges = Column(JSON, default=list)
    triggers = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)
    category = Column(String(100), nullable=True)
    tags = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    total_runs = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="workflows")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowExecution(BaseModel):
    __tablename__ = "workflow_executions"

    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    status = Column(String(50), default="pending")
    trigger_type = Column(String(50), nullable=True)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    node_results = Column(JSON, default=list)
    started_at = Column(String(50), nullable=True)
    completed_at = Column(String(50), nullable=True)

    workflow = relationship("Workflow", back_populates="executions")
