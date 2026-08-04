"""
Resilience layer providing Circuit Breaker state management and provider failure tracking.
"""
import logging
import time
from enum import Enum
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    """
    Circuit breaker state enum.
    """
    HEALTHY = "HEALTHY"      # Normal operation - closed circuit
    OPEN = "OPEN"            # Tripped - failing provider isolated
    HALF_OPEN = "HALF_OPEN"  # Probe mode - testing recovery


class CircuitBreakerException(Exception):
    """Raised when attempting to execute a request through an open circuit breaker."""
    pass


class CircuitBreaker:
    """
    Circuit Breaker implementation for isolating failing upstream LLM providers.
    """

    def __init__(self, failure_threshold: int = 3, recovery_timeout_sec: float = 30.0) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self.state = CircuitState.HEALTHY
        self.failure_count = 0
        self.last_failure_time = 0.0

    def is_available(self) -> bool:
        """
        Check if the provider circuit is available for traffic.
        """
        now = time.time()
        if self.state == CircuitState.OPEN:
            if now - self.last_failure_time >= self.recovery_timeout_sec:
                logger.info("Circuit breaker entering HALF_OPEN state; testing provider recovery.")
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True

    def record_success(self) -> None:
        """
        Record a successful execution; resets state to HEALTHY.
        """
        if self.state != CircuitState.HEALTHY:
            logger.info("Circuit breaker recovered! Resetting state to HEALTHY.")
        self.state = CircuitState.HEALTHY
        self.failure_count = 0

    def record_failure(self) -> None:
        """
        Record an execution failure; trips circuit breaker to OPEN if threshold reached.
        """
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning(
                f"🚨 CIRCUIT BREAKER TRIPPED to OPEN! {self.failure_count} consecutive failures recorded. "
                f"Isolating provider for {self.recovery_timeout_sec}s."
            )


class ResilienceEngine:
    """
    Resilience manager tracking circuit breaker states across multiple LLM providers.
    """

    def __init__(self) -> None:
        self._breakers: Dict[str, CircuitBreaker] = {
            "groq": CircuitBreaker(failure_threshold=2, recovery_timeout_sec=20.0),
            "openrouter": CircuitBreaker(failure_threshold=3, recovery_timeout_sec=30.0),
        }

    def _get_breaker(self, provider: str) -> CircuitBreaker:
        provider_key = provider.lower()
        if provider_key not in self._breakers:
            self._breakers[provider_key] = CircuitBreaker()
        return self._breakers[provider_key]

    def is_provider_healthy(self, provider: str) -> bool:
        """
        Check if a given provider's circuit is operational.
        """
        return self._get_breaker(provider).is_available()

    def record_success(self, provider: str) -> None:
        """
        Record success for provider.
        """
        self._get_breaker(provider).record_success()

    def record_failure(self, provider: str) -> None:
        """
        Record failure for provider.
        """
        self._get_breaker(provider).record_failure()

    def get_provider_status(self) -> Dict[str, Any]:
        """
        Get operational status overview of all registered provider breakers.
        """
        return {
            provider: {
                "state": breaker.state.value,
                "failures": breaker.failure_count,
            }
            for provider, breaker in self._breakers.items()
        }


# Singleton resilience engine instance
resilience_engine = ResilienceEngine()
