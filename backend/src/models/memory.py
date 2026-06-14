from sqlalchemy import Column, String, ForeignKey, JSON, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Memory(BaseModel):
    __tablename__ = "memories"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    memory_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    importance = Column(Float, default=0.5)
    embedding_id = Column(String(255), nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    source_conversation_id = Column(UUID(as_uuid=True), nullable=True)
    source_message_id = Column(UUID(as_uuid=True), nullable=True)

    user = relationship("User", back_populates="memories")
