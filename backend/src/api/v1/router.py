from fastapi import APIRouter
from src.api.v1.endpoints import (
    auth,
    users,
    agents,
    conversations,
    chat,
    workflows,
    tools,
    documents,
    analytics,
    marketplace,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(agents.router)
api_router.include_router(conversations.router)
api_router.include_router(chat.router)
api_router.include_router(workflows.router)
api_router.include_router(tools.router)
api_router.include_router(documents.router)
api_router.include_router(analytics.router)
api_router.include_router(marketplace.router)
