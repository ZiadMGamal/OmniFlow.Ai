from sqlalchemy import Column, String, Float, Boolean, ForeignKey, JSON, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Agent(BaseModel):
    __tablename__ = "agents"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    agent_type = Column(String(50), nullable=False, default="general")
    system_prompt = Column(Text, nullable=True)
    model = Column(String(100), default="gpt-4o")
    provider = Column(String(50), default="openai")
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=4096)
    tools = Column(JSON, default=list)
    is_public = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(500), nullable=True)
    category = Column(String(100), nullable=True)
    tags = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    total_runs = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    avg_latency = Column(Float, default=0.0)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="agents")
    conversations = relationship("Conversation", back_populates="agent")
