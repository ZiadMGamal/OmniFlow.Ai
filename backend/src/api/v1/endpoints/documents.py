from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.document import DocumentUploadResponse, DocumentResponse, DocumentListResponse
from src.services.document_service import document_service

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    content = await file.read()
    response = await document_service.upload_document(
        session, UUID(current_user_id), file.filename, content, file.content_type
    )
    
    background_tasks.add_task(document_service.process_document, session, response.id)
    return response


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    return await document_service.list_documents(session, UUID(current_user_id), page, page_size)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    return await document_service.get_document(session, document_id)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    await document_service.delete_document(session, document_id, UUID(current_user_id))
