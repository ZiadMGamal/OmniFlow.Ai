import os
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.exceptions import NotFoundError, DocumentProcessingError, ValidationError
from src.core.config import settings
from src.dao.document import document_dao, document_chunk_dao
from src.schemas.document import DocumentResponse, DocumentUploadResponse


class DocumentService:
    async def upload_document(
        self, session: AsyncSession, user_id: UUID, filename: str, content: bytes, file_type: str
    ) -> DocumentUploadResponse:
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise ValidationError(f"File type {ext} is not supported")

        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"File size exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit")

        storage_path = f"documents/{user_id}/{uuid4().hex}{ext}"

        doc = await document_dao.create(session, {
            "name": filename,
            "file_type": file_type,
            "file_size": len(content),
            "storage_path": storage_path,
            "status": "pending",
            "owner_id": user_id,
            "collection_name": f"doc_{uuid4().hex[:8]}",
        })

        return DocumentUploadResponse.model_validate(doc)

    async def get_document(self, session: AsyncSession, document_id: UUID) -> DocumentResponse:
        doc = await document_dao.get_by_id(session, document_id)
        if not doc:
            raise NotFoundError("Document", str(document_id))
        return DocumentResponse.model_validate(doc)

    async def list_documents(
        self, session: AsyncSession, user_id: UUID, page: int = 1, page_size: int = 20
    ):
        docs, total = await document_dao.get_user_documents(session, user_id, page, page_size)
        return {
            "documents": [DocumentResponse.model_validate(d) for d in docs],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def delete_document(self, session: AsyncSession, document_id: UUID, user_id: UUID):
        doc = await document_dao.get_by_id(session, document_id)
        if not doc:
            raise NotFoundError("Document", str(document_id))
        if str(doc.owner_id) != str(user_id):
            from src.core.exceptions import AuthorizationError
            raise AuthorizationError("You don't own this document")
        await document_dao.soft_delete(session, document_id)

    async def process_document(self, session: AsyncSession, document_id: UUID):
        doc = await document_dao.get_by_id(session, document_id)
        if not doc:
            raise NotFoundError("Document", str(document_id))

        try:
            await document_dao.update(session, document_id, {"status": "processing"})
            await document_dao.update(session, document_id, {"status": "completed"})
        except Exception as e:
            await document_dao.update(session, document_id, {
                "status": "failed",
                "processing_error": str(e),
            })
            raise DocumentProcessingError(str(e))


document_service = DocumentService()
