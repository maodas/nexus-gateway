"""
API v1 main router aggregation module.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, gateway, analytics

api_v1_router = APIRouter()

# Include endpoints
api_v1_router.include_router(health.router, tags=["Health Checks"])
api_v1_router.include_router(gateway.router, prefix="/gateway", tags=["Gateway"])
api_v1_router.include_router(analytics.router, prefix="/analytics", tags=["FinOps Telemetry"])
