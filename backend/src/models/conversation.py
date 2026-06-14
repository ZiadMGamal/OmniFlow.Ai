from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Conversation(BaseModel):
    __tablename__ = "conversations"

    title = Column(String(500), nullable=True, default="New Conversation")
    summary = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    model = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)
    total_messages = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    metadata_ = Column("metadata", JSON, default=dict)
    pinned = Column(Integer, default=0)

    user = relationship("User", back_populates="conversations")
    agent = relationship("Agent", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(BaseModel):
    __tablename__ = "messages"

    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=True)
    message_type = Column(String(50), default="text")
    tool_calls = Column(JSON, nullable=True)
    tool_results = Column(JSON, nullable=True)
    reasoning = Column(Text, nullable=True)
    sources = Column(JSON, nullable=True)
    attachments = Column(JSON, nullable=True)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    latency_ms = Column(Integer, default=0)
    model = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)
    parent_message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    conversation = relationship("Conversation", back_populates="messages")
    parent = relationship("Message", remote_side="Message.id")
