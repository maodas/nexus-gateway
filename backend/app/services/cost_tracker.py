"""
FinOps cost tracker, department token governance, and budget enforcement engine.
"""
import logging
from typing import Dict, Tuple, Any
from app.core.redis import redis_get, redis_incrby, redis_incrbyfloat

logger = logging.getLogger(__name__)

# Model pricing in USD per 1,000,000 tokens: (input_price_per_1M, output_price_per_1M)
MODEL_PRICING: Dict[str, Tuple[float, float]] = {
    "llama-3.3-70b-versatile": (0.59, 0.79),
    "llama-3.1-8b-instant": (0.05, 0.08),
    "meta-llama/llama-3.3-70b-instruct:free": (0.00, 0.00),
    "meta-llama/llama-3.1-70b-instruct": (0.40, 0.40),
    "gpt-4o": (2.50, 10.00),
}


def calculate_tokens_and_cost(
    prompt_tokens: int,
    completion_tokens: int,
    provider: str,
    model: str,
    benchmark_model: str = "gpt-4o"
) -> Dict[str, Any]:
    """
    Calculate token usage telemetry, estimated cost in USD, and FinOps dollars saved compared to benchmark.
    """
    total_tokens = prompt_tokens + completion_tokens

    pricing = MODEL_PRICING.get(model.lower(), (0.20, 0.20))
    input_cost = (prompt_tokens / 1_000_000.0) * pricing[0]
    output_cost = (completion_tokens / 1_000_000.0) * pricing[1]
    estimated_cost_usd = round(input_cost + output_cost, 6)

    bench_pricing = MODEL_PRICING.get(benchmark_model.lower(), (2.50, 10.00))
    bench_input_cost = (prompt_tokens / 1_000_000.0) * bench_pricing[0]
    bench_output_cost = (completion_tokens / 1_000_000.0) * bench_pricing[1]
    benchmark_cost_usd = bench_input_cost + bench_output_cost

    dollars_saved_usd = max(0.0, round(benchmark_cost_usd - estimated_cost_usd, 6))

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": estimated_cost_usd,
        "dollars_saved_usd": dollars_saved_usd,
    }


def record_department_usage(
    department: str,
    tokens_used: int,
    cost_usd: float,
    cost_saved_usd: float = 0.0,
    is_cached: bool = False
) -> None:
    """
    Record and increment granular token usage, spend, and request types (cached vs live) per department in Redis.

    Keys:
    - nexus:dept:{department}:cached_requests
    - nexus:dept:{department}:live_requests
    - nexus:dept:{department}:request_count
    - nexus:dept:{department}:tokens_total
    - nexus:dept:{department}:cost_total_usd
    - nexus:dept:{department}:cost_saved_usd
    """
    dept_clean = department.strip().lower() if department else "general"

    if is_cached:
        redis_incrby(f"nexus:dept:{dept_clean}:cached_requests", 1)
    else:
        redis_incrby(f"nexus:dept:{dept_clean}:live_requests", 1)

    redis_incrby(f"nexus:dept:{dept_clean}:tokens_total", tokens_used)
    redis_incrbyfloat(f"nexus:dept:{dept_clean}:cost_total_usd", round(cost_usd, 6))
    redis_incrbyfloat(f"nexus:dept:{dept_clean}:cost_saved_usd", round(cost_saved_usd, 6))
    redis_incrby(f"nexus:dept:{dept_clean}:request_count", 1)

    # Global level increments
    redis_incrby("nexus:telemetry:total_requests", 1)
    redis_incrby("nexus:telemetry:total_tokens", tokens_used)
    redis_incrbyfloat("nexus:telemetry:total_cost_usd", round(cost_usd, 6))
    redis_incrbyfloat("nexus:telemetry:total_saved_usd", round(cost_saved_usd, 6))

    logger.info(
        f"📊 FinOps Granular [{dept_clean}] {'(CACHED)' if is_cached else '(LIVE)'}: "
        f"+{tokens_used} tokens, +${cost_usd:.6f} spent."
    )


def check_department_budget(department: str, max_budget_usd: float = 100.0) -> bool:
    """
    Check current accumulated spend for department against budget cap.
    """
    dept_clean = department.strip().lower() if department else "general"
    key = f"nexus:dept:{dept_clean}:cost_total_usd"

    current_spend_raw = redis_get(key)
    if current_spend_raw is None:
        return True

    try:
        current_spend = float(current_spend_raw)
        if current_spend >= max_budget_usd:
            logger.warning(
                f"🚫 BUDGET EXCEEDED! Department '{dept_clean}' accumulated spend (${current_spend:.2f}) "
                f"exceeds max cap of ${max_budget_usd:.2f}."
            )
            return False
        return True
    except (ValueError, TypeError):
        return True


def record_cache_hit() -> None:
    """
    Increment global cache hits counter in Redis.
    """
    redis_incrby("nexus:telemetry:cache_hits", 1)


class CostTrackerService:
    """
    Service wrapper for cost tracking & budget governance.
    """

    @staticmethod
    def record_usage(department: str, tokens_used: int, cost_usd: float, cost_saved_usd: float = 0.0, is_cached: bool = False) -> None:
        record_department_usage(department, tokens_used, cost_usd, cost_saved_usd, is_cached)

    @staticmethod
    def is_within_budget(department: str, max_budget_usd: float = 100.0) -> bool:
        return check_department_budget(department, max_budget_usd)


cost_tracker = CostTrackerService()
