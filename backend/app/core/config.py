"""
Application configuration management using pydantic-settings.
"""
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    NexusGateway Application Settings loaded from environment variables or .env file.
    """
    PROJECT_NAME: str = Field(default="NexusGateway", description="Name of the application project")
    VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    API_V1_STR: str = Field(default="/api/v1", description="API v1 route prefix")

    # Upstash Redis Configuration
    UPSTASH_REDIS_REST_URL: str = Field(
        default="",
        description="Upstash Redis REST API base URL"
    )
    UPSTASH_REDIS_REST_TOKEN: str = Field(
        default="",
        description="Upstash Redis REST API authorization token"
    )

    # LLM Provider API Keys
    GROQ_API_KEY: str = Field(
        default="",
        description="Groq API key for high-speed inference"
    )
    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key for fallback routing"
    )

    # Security Authentication Key
    GATEWAY_AUTH_KEY: str = Field(
        default="nexus-secret-auth-key-change-in-production",
        description="Secret key required for tenant authorization header"
    )

    # CORS Settings
    CORS_ORIGINS: List[str] = Field(
        default=["*"],
        description="Allowed origins for Cross-Origin Resource Sharing (CORS)"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Singleton settings instance
settings = Settings()
