"""Tests for Redis cache manager."""

import pytest
import json
from unittest.mock import AsyncMock, patch
from datetime import datetime

from cache import CacheManager
from config import settings


class TestCacheManager:
    """Test Redis cache manager functionality."""

    @pytest.mark.asyncio
    async def test_initialize_success(self):
        """Test successful cache initialization."""
        with patch("redis.asyncio.from_url") as mock_redis:
            mock_client = AsyncMock()
            mock_client.ping = AsyncMock()
            mock_redis.return_value = mock_client

            cache_manager = CacheManager()
            await cache_manager.initialize()

            assert cache_manager.cache_enabled is True
            mock_redis.assert_called_once_with(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
