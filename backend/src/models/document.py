from sqlalchemy import Column, String, Boolean, ForeignKey, JSON, Integer, Text, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.models.base import BaseModel


class Document(BaseModel):
    __tablename__ = "documents"

    name = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_url = Column(String(1000), nullable=True)
    storage_path = Column(String(1000), nullable=True)
    status = Column(String(50), default="pending")
    total_chunks = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    collection_name = Column(String(255), nullable=True)
    processing_error = Column(Text, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    embedding_id = Column(String(255), nullable=True)
    page_number = Column(Integer, nullable=True)
    metadata_ = Column("metadata", JSON, default=dict)

    document = relationship("Document", back_populates="chunks")
