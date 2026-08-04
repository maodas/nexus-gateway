"""
Pydantic schemas for Gateway completion requests and responses.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """
    Standard OpenAI-style chat message format.
    """
    role: str = Field(..., description="Message role (system, user, assistant)")
    content: str = Field(..., description="Message content text")


class GatewayChatRequest(BaseModel):
    """
    Incoming gateway completion request schema compatible with OpenAI protocol.
    """
    messages: List[ChatMessage] = Field(..., description="List of conversation messages")
    model: Optional[str] = Field(default=None, description="Requested model or None for autopilot routing")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=1000, gt=0, description="Maximum completion tokens limit")
    department: Optional[str] = Field(default="general", description="Tenant or department identifier for FinOps tracking")
    simulate_outage: Optional[str] = Field(default=None, description="Optional parameter to simulate provider outage ('groq')")


class GatewayChatResponse(BaseModel):
    """
    Gateway completion response metadata and payload.
    """
    id: str = Field(..., description="Unique completion request ID")
    provider_used: str = Field(..., description="Actual LLM provider executing request (groq, openrouter, etc.)")
    model_used: str = Field(..., description="Actual model selected and executed")
    content: str = Field(..., description="Assistant response text")
    prompt_tokens: int = Field(default=0, description="Input prompt token count")
    completion_tokens: int = Field(default=0, description="Output completion token count")
    total_tokens: int = Field(default=0, description="Total tokens consumed")
    estimated_cost_usd: float = Field(default=0.0, description="Calculated request cost in USD")
    cached: bool = Field(default=False, description="True if served from semantic cache")
    latency_ms: float = Field(..., description="Total execution latency in milliseconds")
    pii_redacted: bool = Field(default=False, description="True if PII/sensitive tokens were sanitized")
    redacted_items_count: int = Field(default=0, description="Count of redacted sensitive data matches")
