"""
Pydantic schemas for FinOps analytics, metrics, and monitoring telemetry.
"""
from typing import List, Dict
from pydantic import BaseModel, Field


class CostBreakdownByProvider(BaseModel):
    """
    Cost breakdown summarized per provider.
    """
    provider: str = Field(..., description="Provider identifier (groq, openrouter, etc.)")
    total_cost_usd: float = Field(..., description="Total spent in USD")
    request_count: int = Field(..., description="Total request count")


class CachePerformanceMetrics(BaseModel):
    """
    Semantic cache telemetry.
    """
    total_queries: int = Field(..., description="Total gateway requests evaluated")
    cache_hits: int = Field(..., description="Total cache hits")
    cache_misses: int = Field(..., description="Total cache misses")
    hit_rate_percentage: float = Field(..., description="Cache hit percentage")
    total_saved_usd: float = Field(..., description="Total cost saved by caching")


class AnalyticsSummaryResponse(BaseModel):
    """
    Overall FinOps & Performance telemetry payload for Frontend Chart.js dashboard.
    """
    total_requests: int = Field(..., description="Total requests processed")
    total_spent_usd: float = Field(..., description="Total expenditure across all providers")
    total_saved_usd: float = Field(..., description="Total saved via autopilot routing & semantic cache")
    average_latency_ms: float = Field(..., description="Average latency in ms")
    cache_metrics: CachePerformanceMetrics = Field(..., description="Semantic cache breakdown")
    provider_breakdown: List[CostBreakdownByProvider] = Field(..., description="Per-provider spend breakdown")
    cost_trend_timeline: List[Dict[str, Any]] = Field(..., description="Timeline chart data series")
