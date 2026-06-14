from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_session
from src.core.security import get_current_user_id
from src.schemas.tool import ToolResponse, ToolListResponse
from src.dao.tool import tool_dao

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("", response_model=ToolListResponse)
async def list_tools(
    category: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    if category:
        tools, total = await tool_dao.get_by_category(session, category)
    else:
        tools, total = await tool_dao.get_active_tools(session)
    
    return {
        "tools": [ToolResponse.model_validate(t) for t in tools],
        "total": total,
    }


@router.get("/{slug}", response_model=ToolResponse)
async def get_tool(
    slug: str,
    session: AsyncSession = Depends(get_session),
):
    tool = await tool_dao.get_by_slug(session, slug)
    if not tool:
        from src.core.exceptions import NotFoundError
        raise NotFoundError("Tool", slug)
    return ToolResponse.model_validate(tool)
