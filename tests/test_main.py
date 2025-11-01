"""Tests for main FastAPI application."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app, conversation_sessions


class TestMainEndpoints:
    """Test main API endpoints."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test fixtures."""
        self.client = TestClient(app)
        # Clear conversation sessions before each test
        conversation_sessions.clear()

    def test_root_endpoint(self):
        """Test root endpoint returns correct message."""
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Evolution API - MCP Bridge is running"}

    def test_health_check_success(self):
        """Test health check endpoint when MCP server is available."""
        with patch(
            "main.mcp_client.health_check", new_callable=AsyncMock
        ) as mock_health:
            mock_health.return_value = True
            response = self.client.get("/health")
            assert response.status_code == 200
            assert response.json() == {
                "status": "healthy",
                "mcp_server_available": True,
            }

    def test_health_check_failure(self):
        """Test health check endpoint when MCP server is unavailable."""
        with patch(
            "main.mcp_client.health_check", new_callable=AsyncMock
        ) as mock_health:
            mock_health.return_value = False
            response = self.client.get("/health")
            assert response.status_code == 200
            assert response.json() == {
                "status": "healthy",
                "mcp_server_available": False,
            }

    @pytest.mark.asyncio
    async def test_send_message_success(self, mock_evolution_client):
        """Test successful message sending."""
        with patch("main.evolution_client", mock_evolution_client):
            mock_evolution_client.send_message.return_value = {"status": "sent"}

            request_data = {
                "number": "5511999999999",
                "text": "Test message",
                "options": {"delay": 1000},
            }

            response = self.client.post("/send-message", json=request_data)
            assert response.status_code == 200
            assert response.json() == {"status": "success", "data": {"status": "sent"}}
            mock_evolution_client.send_message.assert_called_once()
