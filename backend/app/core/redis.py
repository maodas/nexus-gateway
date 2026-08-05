"""
Upstash Redis client wrapper with robust exception handling and namespaced key helpers.
"""
import logging
from typing import Optional, Any
from upstash_redis import Redis
from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: Optional[Redis] = None


def get_redis_client() -> Optional[Redis]:
    """
    Get or initialize the global Upstash Redis client singleton instance.

    Returns:
        Optional[Redis]: Initialized Upstash Redis instance, or None if unconfigured.
    """
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    if not settings.UPSTASH_REDIS_REST_URL or not settings.UPSTASH_REDIS_REST_TOKEN:
        logger.info("Upstash Redis credentials unconfigured. Operating in memory-only / pass-through mode.")
        return None

    try:
        _redis_client = Redis(
            url=settings.UPSTASH_REDIS_REST_URL,
            token=settings.UPSTASH_REDIS_REST_TOKEN
        )
        logger.info("Successfully connected to Upstash Redis REST API.")
        return _redis_client
    except Exception as e:
        logger.error(f"Failed to connect to Upstash Redis: {e}")
        return None


def redis_get(key: str) -> Optional[Any]:
    """
    Safely get value from Redis key without throwing exceptions.
    """
    client = get_redis_client()
    if not client:
        return None
    try:
        return client.get(key)
    except Exception as e:
        logger.warning(f"Redis GET failed for key '{key}': {e}")
        return None


def redis_set(key: str, value: Any, ex: Optional[int] = None) -> bool:
    """
    Safely set value in Redis key with optional expiration (TTL in seconds).
    """
    client = get_redis_client()
    if not client:
        return False
    try:
        if ex:
            client.set(key, value, ex=ex)
        else:
            client.set(key, value)
        return True
    except Exception as e:
        logger.warning(f"Redis SET failed for key '{key}': {e}")
        return False


def redis_del(key: str) -> bool:
    """
    Safely delete key from Redis without throwing exceptions.
    """
    client = get_redis_client()
    if not client:
        return False
    try:
        client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Redis DEL failed for key '{key}': {e}")
        return False


def redis_incrby(key: str, amount: int) -> Optional[int]:
    """
    Safely increment integer value in Redis key.
    """
    client = get_redis_client()
    if not client:
        return None
    try:
        return client.incrby(key, amount)
    except Exception as e:
        logger.warning(f"Redis INCRBY failed for key '{key}': {e}")
        return None


def redis_incrbyfloat(key: str, amount: float) -> Optional[float]:
    """
    Safely increment float value in Redis key.
    """
    client = get_redis_client()
    if not client:
        return None
    try:
        return client.incrbyfloat(key, amount)
    except Exception as e:
        logger.warning(f"Redis INCRBYFLOAT failed for key '{key}': {e}")
        return None


def redis_keys(pattern: str = "nexus:*") -> list:
    """
    Safely fetch keys matching namespaced pattern.
    """
    client = get_redis_client()
    if not client:
        return []
    try:
        res = client.keys(pattern)
        return res if res else []
    except Exception as e:
        logger.warning(f"Redis KEYS failed for pattern '{pattern}': {e}")
        return []
