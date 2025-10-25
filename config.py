"""Configuration settings for the Evolution API - MCP Bridge."""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    # Evolution API Configuration
    EVOLUTION_API_BASE_URL = os.getenv(
        "EVOLUTION_API_BASE_URL", "http://localhost:8080"
    )
    EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")

    # MCP Server Configuration
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
    MCP_API_KEY = os.getenv("MCP_API_KEY", "")

    # FastAPI Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # Webhook Configuration
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", f"http://localhost:{PORT}/webhook")

    # Redis Cache Configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default
    CACHE_PREFIX = os.getenv("CACHE_PREFIX", "evolution_mcp")

    # Cache Strategy Configuration
    CACHE_MAX_ENTRIES = int(os.getenv("CACHE_MAX_ENTRIES", "1000"))
    CACHE_POPULAR_THRESHOLD = int(os.getenv("CACHE_POPULAR_THRESHOLD", "5"))


settings = Settings()
