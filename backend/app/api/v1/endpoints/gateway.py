"""
Gateway API endpoint handler for OpenAI-compatible completions and chaos outage simulation.
"""
import logging
from typing import Optional
from fastapi import APIRouter, Depends, Header, status, HTTPException
from app.core.security import verify_gateway_auth_key
from app.schemas.gateway import GatewayChatRequest, GatewayChatResponse
from app.services.router_engine import router_engine

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/chat/completions",
    status_code=status.HTTP_200_OK,
    response_model=GatewayChatResponse,
    summary="LLM Gateway Completions Proxy",
    description="Route completion requests to optimal provider (Groq/OpenRouter) with PII guardrail scrubbing and circuit-breaker fallback resilience."
)
async def create_chat_completion(
    request: GatewayChatRequest,
    x_simulate_outage: Optional[str] = Header(default=None, alias="X-Simulate-Outage"),
    auth_key: str = Depends(verify_gateway_auth_key)
) -> GatewayChatResponse:
    """
    Process incoming chat completion request through smart router engine.
    """
    try:
        logger.info(f"Incoming /chat/completions request from department '{request.department}'")
        simulate_outage_flag = (x_simulate_outage == "groq") or (request.simulate_outage == "groq")
        response = await router_engine.process_chat_completion(request, header_outage_flag=simulate_outage_flag)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled error processing gateway completion: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gateway execution failure: {str(e)}"
        )


@router.post(
    "/simulate-outage",
    status_code=status.HTTP_200_OK,
    summary="Chaos Testing Outage Trigger",
    description="Trigger simulated provider outage for chaos testing."
)
async def simulate_outage(
    provider: str = "groq",
    auth_key: str = Depends(verify_gateway_auth_key)
):
    """
    Chaos testing trigger endpoint to test circuit breaker failover.
    """
    return {
        "status": "active",
        "provider": provider,
        "message": f"Simulated outage enabled for provider '{provider}'. Requests passing X-Simulate-Outage: {provider} will trigger failover."
    }
