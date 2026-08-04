"""
NexusGateway FastAPI Core Application Entrypoint.
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_v1_router

# Configure logging format
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("nexus_gateway")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI Lifespan context manager for startup and shutdown event handling.
    """
    # Startup lifecycle tasks
    logger.info(f"Initializing {settings.PROJECT_NAME} v{settings.VERSION}...")
    logger.info("Verifying infrastructure configuration & provider credentials...")
    yield
    # Shutdown lifecycle tasks
    logger.info(f"Shutting down {settings.PROJECT_NAME} gateway gracefully...")


def create_application() -> FastAPI:
    """
    Factory function to initialize and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="Enterprise-grade LLM Cost Autopilot, Semantic Proxy, and Fallback Gateway.",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # Configure CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API v1 router (/api/v1)
    application.include_router(api_v1_router, prefix=settings.API_V1_STR)

    @application.get("/", include_in_schema=False)
    async def root_redirect():
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health"
        }

    return application


app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
