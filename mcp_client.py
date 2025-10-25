import httpx
from typing import Dict, Any, Optional
from models import MCPRequest, MCPResponse
from config import settings


class MCPClient:
    def __init__(self) -> None:
        self.base_url = settings.MCP_SERVER_URL
        self.headers = {
            "Authorization": f"Bearer {settings.MCP_API_KEY}",
            "Content-Type": "application/json",
        }

    async def send_message(self, request: MCPRequest) -> MCPResponse:
        """Send message to MCP server and get response"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat",
                json=request.dict(),
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            return MCPResponse(**response.json())
