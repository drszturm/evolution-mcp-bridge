"""Redis cache implementation for message caching with popularity tracking."""

import hashlib
import json
from datetime import datetime
from typing import Any, dict, Optional, Tuple

import redis.asyncio as redis

from config import settings


class CacheManager:
    """Manage Redis caching for messages and responses."""

    def __init__(self):
        """Initialize cache manager."""
        self.redis_client: Optional[redis.Redis] = None
        self.cache_enabled = settings.CACHE_ENABLED

    async def initialize(self):
        """Initialize Redis connection."""
        if not self.cache_enabled:
            return

        try:
            self.redis_client = redis.from_url(
                settings.REDIS_URL, encoding="utf-8", decode_responses=True
            )
            # Test connection
            await self.redis_client.ping()
            print("✅ Redis cache connected successfully")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            self.cache_enabled = False

    def _generate_cache_key(
        self, message: str, session_id: Optional[str] = None
    ) -> str:
        """Generate a cache key from message content and optional session ID."""
        # Normalize message by removing extra whitespace and converting to lowercase
        normalized_msg = " ".join(message.strip().lower().split())

        # Create content hash
        content_to_hash = normalized_msg
        if session_id:
            content_to_hash += f"_{session_id}"

        content_hash = hashlib.md5(content_to_hash.encode()).hexdigest()
        return f"{settings.CACHE_PREFIX}:response:{content_hash}"

    def _generate_popularity_key(self, message: str) -> str:
        """Generate key for tracking message popularity."""
        normalized_msg = " ".join(message.strip().lower().split())
        content_hash = hashlib.md5(normalized_msg.encode()).hexdigest()
        return f"{settings.CACHE_PREFIX}:popularity:{content_hash}"

    def _generate_session_key(self, session_id: str) -> str:
        """Generate key for session-based caching."""
        return f"{settings.CACHE_PREFIX}:session:{session_id}"

    async def get_cached_response(
        self, message: str, session_id: Optional[str] = None
    ) -> Optional[Any]:
        """Get cached response for a message."""
        if not self.cache_enabled or not self.redis_client:
            return None

        try:
            cache_key = self._generate_cache_key(message, session_id)
            cached_data = await self.redis_client.get(cache_key)

            if cached_data:
                # Update popularity score
                await self._increment_popularity(message)
                return json.loads(cached_data)

        except Exception as e:
            print(f"Error reading from cache: {e}")

        return None

    async def set_cached_response(
        self, message: str, response: dict[str, Any], session_id: Optional[str] = None
    ) -> None:
        """Cache a response for a message."""
        if not self.cache_enabled or not self.redis_client:
            return

        try:
            cache_key = self._generate_cache_key(message, session_id)
            popularity_key = self._generate_popularity_key(message)

            # Prepare cache data
            cache_data = {
                "response": response,
                "message": message,
                "session_id": session_id,
                "cached_at": datetime.now().isoformat(),
                "popularity": 0,
            }

            # Store in cache with TTL
            await self.redis_client.setex(
                cache_key, settings.CACHE_TTL, json.dumps(cache_data)
            )

            # Initialize popularity if not exists
            if not await self.redis_client.exists(popularity_key):
                await self.redis_client.setex(
                    popularity_key,
                    settings.CACHE_TTL * 2,  # Longer TTL for popularity
                    1,
                )

            # Clean up if we have too many entries
            await self._cleanup_old_entries()

        except Exception as e:
            print(f"Error writing to cache: {e}")

    async def _increment_popularity(self, message: str) -> None:
        """Increment popularity counter for a message."""
        if not self.cache_enabled or not self.redis_client:
            return

        try:
            popularity_key = self._generate_popularity_key(message)
            await self.redis_client.incr(popularity_key)
        except Exception as e:
            print(f"Error incrementing popularity: {e}")
