from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import init_db, close_db
from src.core.redis import RedisManager
from src.core.qdrant import QdrantManager
from src.core.middleware import (
    RequestIdMiddleware,
    RequestLoggingMiddleware,
    RateLimitMiddleware,
    ErrorHandlingMiddleware,
    SecurityHeadersMiddleware,
)
from src.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await init_db()
    await RedisManager.initialize()
    QdrantManager.initialize()
    yield
    # Shutdown logic
    await close_db()
    await RedisManager.close()
    QdrantManager.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="The Universal Multi-Tool AI Agent Platform API",
    lifespan=lifespan,
)

# Middleware (Order matters - inner to outer)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=settings.RATE_LIMIT_PER_MINUTE, window_seconds=60)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
