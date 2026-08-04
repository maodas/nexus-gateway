from fastapi import Header, HTTPException, status
from app.core.config import settings

async def verify_gateway_auth_key(
    x_gateway_api_key: str = Header(None, alias="X-Gateway-API-Key"),
    authorization: str = Header(None)
):
    """
    Validates incoming request authentication.
    Supports either 'X-Gateway-API-Key' header or 'Authorization: Bearer <key>'.
    Allows empty key in local development if GATEWAY_AUTH_KEY is not configured.
    """
    # If no key is configured in .env, bypass for easy local dev
    if not settings.GATEWAY_AUTH_KEY:
        return "dev-tenant"

    token = x_gateway_api_key
    if not token and authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    if token != settings.GATEWAY_AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Gateway Authentication Key"
        )
    
    return "authorized-tenant"