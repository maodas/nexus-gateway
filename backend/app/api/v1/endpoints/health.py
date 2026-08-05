"""
Health check and diagnostics endpoint.
"""
from typing import Dict, Any
from fastapi import APIRouter, status
from app.core.config import settings
from app.core.redis import get_redis_client

router = APIRouter()


@router.api_route(
    "/health",
    methods=["GET", "HEAD"],
    status_code=status.HTTP_200_OK,
    summary="System Health & Diagnostics",
    description="Check backend operational status, Redis connection, and service metadata. Accepts GET and HEAD requests."
)
async def check_health() -> Dict[str, Any]:
    """
    Perform system health checks across infrastructure services.

    Returns:
        Dict[str, Any]: Service health status payload.
    """
    redis_client = get_redis_client()
    redis_status = "connected" if redis_client is not None else "unconfigured"

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "dependencies": {
            "redis": redis_status,
            "groq_configured": bool(settings.GROQ_API_KEY),
            "openrouter_configured": bool(settings.OPENROUTER_API_KEY)
        }
    }
