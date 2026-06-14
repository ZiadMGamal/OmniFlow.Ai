from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    id: UUID
    name: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    file_type: str
    file_size: int
    status: str
    total_chunks: int
    total_tokens: int
    collection_name: Optional[str] = None
    processing_error: Optional[str] = None
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    page_size: int


class DocumentChunkResponse(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    content: str
    token_count: int
    page_number: Optional[int] = None

    class Config:
        from_attributes = True


class RAGQueryRequest(BaseModel):
    query: str
    collection_name: Optional[str] = None
    limit: int = 5
    score_threshold: float = 0.7


class RAGQueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    total_results: int
