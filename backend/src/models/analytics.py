from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from src.models.base import BaseModel


class AnalyticsEvent(BaseModel):
    __tablename__ = "analytics_events"

    event_type = Column(String(100), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=True)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=True)
    provider = Column(String(50), nullable=True)
    model = Column(String(100), nullable=True)
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    latency_ms = Column(Integer, default=0)
    status = Column(String(50), default="success")
    error_message = Column(String(1000), nullable=True)
    tool_name = Column(String(100), nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
