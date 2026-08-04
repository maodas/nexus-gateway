"""
FinOps Analytics & Telemetry API endpoint with namespaced Redis aggregation.
"""
import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from app.core.security import verify_gateway_auth_key
from app.core.redis import redis_get, redis_keys

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/summary",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="FinOps Analytics Telemetry Summary",
    description="Retrieve real-time request counts, token consumption, total spend, department breakdown, and cache hit rate."
)
async def get_analytics_summary(
    auth_key: str = Depends(verify_gateway_auth_key)
) -> Dict[str, Any]:
    """
    Get consolidated telemetry and department usage metrics aggregated from Upstash Redis.
    """
    raw_total_requests = redis_get("nexus:telemetry:total_requests") or 0
    raw_total_tokens = redis_get("nexus:telemetry:total_tokens") or 0
    raw_total_cost = redis_get("nexus:telemetry:total_cost_usd") or 0.0
    raw_total_saved = redis_get("nexus:telemetry:total_saved_usd") or 0.0
    raw_cache_hits = redis_get("nexus:telemetry:cache_hits") or 0

    try:
        total_requests = int(raw_total_requests)
        total_tokens = int(raw_total_tokens)
        total_cost_usd = round(float(raw_total_cost), 4)
        total_saved_usd = round(float(raw_total_saved), 4)
        cache_hits = int(raw_cache_hits)
    except (ValueError, TypeError):
        total_requests = 0
        total_tokens = 0
        total_cost_usd = 0.0
        total_saved_usd = 0.0
        cache_hits = 0

    cache_hit_rate = round((cache_hits / total_requests * 100.0), 2) if total_requests > 0 else 0.0

    # Build Granular Department Breakdown Dictionary
    department_breakdown: Dict[str, Dict[str, Any]] = {}
    dept_keys = redis_keys("nexus:dept:*:request_count")

    for key in dept_keys:
        parts = key.split(":")
        if len(parts) >= 3:
            dept_name = parts[2]
            req_count = int(redis_get(f"nexus:dept:{dept_name}:request_count") or 0)
            cached_count = int(redis_get(f"nexus:dept:{dept_name}:cached_requests") or 0)
            live_count = int(redis_get(f"nexus:dept:{dept_name}:live_requests") or 0)
            tokens_total = int(redis_get(f"nexus:dept:{dept_name}:tokens_total") or 0)
            cost_raw = redis_get(f"nexus:dept:{dept_name}:cost_total_usd") or 0.0
            saved_raw = redis_get(f"nexus:dept:{dept_name}:cost_saved_usd") or 0.0

            cost_total = round(float(cost_raw), 4) if cost_raw else 0.0
            saved_total = round(float(saved_raw), 4) if saved_raw else 0.0

            department_breakdown[dept_name] = {
                "cached": cached_count,
                "live": live_count,
                "tokens": tokens_total,
                "requests_count": req_count,
                "request_count": req_count,
                "tokens_processed": tokens_total,
                "tokens_total": tokens_total,
                "cost_usd": cost_total,
                "cost_total_usd": cost_total,
                "cost_saved_usd": saved_total
            }

    if not department_breakdown:
        department_breakdown["general"] = {
            "cached": cache_hits,
            "live": max(0, total_requests - cache_hits),
            "tokens": total_tokens,
            "requests_count": total_requests,
            "request_count": total_requests,
            "tokens_processed": total_tokens,
            "tokens_total": total_tokens,
            "cost_usd": total_cost_usd,
            "cost_total_usd": total_cost_usd,
            "cost_saved_usd": total_saved_usd
        }

    return {
        "total_requests": total_requests,
        "total_tokens": total_tokens,
        "total_cost_usd": total_cost_usd,
        "total_saved_usd": total_saved_usd,
        "cache_hits": cache_hits,
        "cache_hit_rate_percentage": cache_hit_rate,
        "department_breakdown": department_breakdown
    }
