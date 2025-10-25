"""Tests for Evolution API client."""

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from evolution_client import EvolutionClient
from models import SendMessageRequest, SendMediaRequest


class TestEvolutionClient:
    """Test Evolution API client functionality."""

    @pytest.fixture
    def evolution_client(self):
        """Create Evolution client instance."""
        return EvolutionClient()

    @pytest.mark.asyncio
    async def test_send_message_success(self, evolution_client):
        """Test successful message sending."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "sent", "messageId": "123"}

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response

            request = SendMessageRequest(number="5511999999999", text="Test message")

            result = await evolution_client.send_message(request)

            assert result == {"status": "sent", "messageId": "123"}
            mock_post.assert_called_once()
