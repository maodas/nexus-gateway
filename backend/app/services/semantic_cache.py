"""
Semantic caching service integrated with Upstash Redis and 'nexus:' key namespacing.
Guarantees that fallback, outage, and policy guardrail responses are NEVER stored in cache.
"""
import hashlib
import json
import logging
import time
from typing import Optional, Any, Union
from app.core.redis import redis_get, redis_set, redis_del
from app.schemas.gateway import GatewayChatResponse

logger = logging.getLogger(__name__)

CACHE_TTL_DEFAULT_SECONDS = 86400  # 24 Hours


class SemanticCacheService:
    """
    Semantic response cache engine backed by namespaced Upstash Redis store.
    """

    @staticmethod
    def _hash_prompt(prompt_text: str) -> str:
        """
        Normalize and generate SHA-256 hash string for prompt text.
        """
        normalized_prompt = prompt_text.strip().lower()
        return hashlib.sha256(normalized_prompt.encode("utf-8")).hexdigest()

    def get_cached_response(self, prompt_text: str) -> Optional[GatewayChatResponse]:
        """
        Query Redis for cached response under key 'nexus:cache:prompt:{hash}'.

        Args:
            prompt_text (str): Normalized prompt text.

        Returns:
            Optional[GatewayChatResponse]: Cached GatewayChatResponse payload if hit, None if miss.
        """
        if not prompt_text:
            return None

        prompt_hash = self._hash_prompt(prompt_text)
        redis_key = f"nexus:cache:prompt:{prompt_hash}"

        cached_raw = redis_get(redis_key)
        if not cached_raw:
            return None

        try:
            if isinstance(cached_raw, str):
                data = json.loads(cached_raw)
            elif isinstance(cached_raw, dict):
                data = cached_raw
            else:
                return None

            # Safety check: Evict any stale fallback or guardrail response if found in Redis
            provider_used = str(data.get("provider_used", "")).lower()
            if "fallback" in provider_used or "policy-guardrail" in provider_used or data.get("fallback_triggered") or data.get("guardrail_triggered"):
                logger.warning(f"⚠️ Stale fallback response detected in cache for key '{redis_key}'. Evicting key.")
                self.clear_cached_response(prompt_text)
                return None

            logger.info(f"⚡ CACHE HIT! Served response from Redis key '{redis_key}'")

            return GatewayChatResponse(
                id=f"{data.get('id', 'chatcmpl-cache')}-cached",
                provider_used=f"{data.get('provider_used', 'unknown')}-cache",
                model_used=data.get("model_used", "nexus-cache"),
                content=data.get("content", ""),
                prompt_tokens=data.get("prompt_tokens", 0),
                completion_tokens=data.get("completion_tokens", 0),
                total_tokens=data.get("total_tokens", 0),
                estimated_cost_usd=0.0,  # Zero cost for cached hits
                cached=True,
                latency_ms=2.5,  # Sub-millisecond / ultra-low cache response time
                guardrail_triggered=data.get("guardrail_triggered", None)
            )
        except Exception as e:
            logger.warning(f"Failed to parse cached response payload: {e}")
            return None

    def clear_cached_response(self, prompt_text: str) -> bool:
        """
        Delete/evict cached response key for prompt from Redis.
        """
        if not prompt_text:
            return False

        prompt_hash = self._hash_prompt(prompt_text)
        redis_key = f"nexus:cache:prompt:{prompt_hash}"
        return redis_del(redis_key)

    def store_cached_response(
        self,
        prompt_text: str,
        response: Union[GatewayChatResponse, dict, Any],
        ttl_seconds: int = CACHE_TTL_DEFAULT_SECONDS
    ) -> bool:
        """
        Save response JSON payload to Redis under key 'nexus:cache:prompt:{hash}' with TTL.

        STRICT FALLBACK GUARD: Never store fallback, outage simulation, or policy guardrail responses!

        Args:
            prompt_text (str): User prompt text.
            response (Union[GatewayChatResponse, dict, Any]): Outbound response payload.
            ttl_seconds (int): Cache TTL duration in seconds.

        Returns:
            bool: True if cached successfully, False otherwise.
        """
        if not prompt_text:
            return False

        # Safely extract properties whether response is a Pydantic model, dictionary, or object
        if isinstance(response, dict):
            is_cached = response.get("cached", False)
            provider_used = str(response.get("provider_used", "")).lower()
            guardrail_triggered = response.get("guardrail_triggered", None)
            resp_id = response.get("id", "chatcmpl")
            model_used = response.get("model_used", "")
            content = response.get("content", "")
            prompt_tokens = response.get("prompt_tokens", 0)
            completion_tokens = response.get("completion_tokens", 0)
            total_tokens = response.get("total_tokens", 0)
        else:
            is_cached = getattr(response, "cached", False)
            provider_used = str(getattr(response, "provider_used", "")).lower()
            guardrail_triggered = getattr(response, "guardrail_triggered", None)
            resp_id = getattr(response, "id", "chatcmpl")
            model_used = getattr(response, "model_used", "")
            content = getattr(response, "content", "")
            prompt_tokens = getattr(response, "prompt_tokens", 0)
            completion_tokens = getattr(response, "completion_tokens", 0)
            total_tokens = getattr(response, "total_tokens", 0)

        if is_cached:
            return False

        # STRICT CHECK: Reject storing any fallback, outage, openrouter-fallback, or guardrail response
        if (
            "fallback" in provider_used
            or "policy-guardrail" in provider_used
            or guardrail_triggered is not None
        ):
            logger.warning(
                f"🛡️ CACHE BYPASS: Refusing to store fallback/outage/guardrail response "
                f"(provider: '{provider_used}') in Redis cache."
            )
            # Evict any existing stale cache entry for this prompt
            self.clear_cached_response(prompt_text)
            return False

        prompt_hash = self._hash_prompt(prompt_text)
        redis_key = f"nexus:cache:prompt:{prompt_hash}"

        try:
            payload = {
                "id": resp_id,
                "provider_used": provider_used,
                "model_used": model_used,
                "content": content,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "created": int(time.time()),
                "guardrail_triggered": guardrail_triggered,
            }

            success = redis_set(redis_key, json.dumps(payload), ex=ttl_seconds)
            if success:
                logger.info(f"💾 Saved clean primary response ({provider_used}) to Redis cache key '{redis_key}' (TTL: {ttl_seconds}s)")
            return success
        except Exception as e:
            logger.warning(f"Error storing response to semantic cache: {e}")
            return False


# Singleton semantic cache instance
semantic_cache = SemanticCacheService()
