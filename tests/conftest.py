"""Pytest configuration and fixtures."""

import asyncio
from unittest.mock import AsyncMock, Mock
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from fakeredis import aioredis

from main import app
from evolution_client import EvolutionClient
from mcp_client import MCPClient
from cache import CacheManager
from config import settings


@pytest.fixture
def test_client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_evolution_client():
    """Mock Evolution client."""
    return AsyncMock(spec=EvolutionClient)


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client."""
    return AsyncMock(spec=MCPClient)


@pytest.fixture
def sample_webhook_payload():
    """Sample webhook payload from Evolution API."""
    return {
        "instance": "test_instance",
        "data": {
            "key": {
                "remoteJid": "5511999999999@s.whatsapp.net",
                "id": "test_message_id",
            },
            "message": {"conversation": "Hello, this is a test message"},
            "messageTimestamp": 1633046400,
        },
    }


@pytest.fixture
def sample_send_message_request():
    """Sample send message request."""
    return {
        "number": "5511999999999",
        "text": "Test message",
        "options": {"delay": 1000},
    }


@pytest.fixture
def sample_mcp_request():
    """Sample MCP request."""
    return {
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?",
                "timestamp": "2023-10-01T12:00:00",
            }
        ],
        "session_id": "test_session",
        "context": {"platform": "whatsapp"},
    }


@pytest.fixture
def sample_mcp_response():
    """Sample MCP response."""
    return {
        "response": "I'm doing well, thank you!",
        "session_id": "test_session",
        "context": {"platform": "whatsapp"},
    }


@pytest_asyncio.fixture
async def cache_manager():
    """Cache manager with fake Redis."""
    manager = CacheManager()
    manager.redis_client = aioredis.FakeRedis()
    manager.cache_enabled = True
    await manager.initialize()
    return manager


@pytest.fixture
def mock_redis_client():
    """Mock Redis client."""
    return Mock(spec=aioredis.FakeRedis)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
