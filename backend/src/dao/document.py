from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.document import Document, DocumentChunk


class DocumentDAO(BaseDAO[Document]):
    def __init__(self):
        super().__init__(Document)

    async def get_user_documents(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        return await self.get_all(session, page, page_size, filters={"owner_id": user_id})

    async def get_pending_documents(self, session: AsyncSession):
        return await self.get_all(session, page=1, page_size=50, filters={"status": "pending"})


class DocumentChunkDAO(BaseDAO[DocumentChunk]):
    def __init__(self):
        super().__init__(DocumentChunk)

    async def get_document_chunks(
        self, session: AsyncSession, document_id: UUID, page: int = 1, page_size: int = 100
    ):
        return await self.get_all(
            session, page, page_size,
            filters={"document_id": document_id},
            order_by="chunk_index",
            order_desc=False,
        )


document_dao = DocumentDAO()
document_chunk_dao = DocumentChunkDAO()
