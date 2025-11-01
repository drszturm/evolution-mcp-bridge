from ast import arguments
import httpx
from typing import Dict, Any, Optional
from deepseek_models import DeepSeekMessage
import deepseek_service
from mcp_models import CallToolResult, TextContent, ContentType
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
        messages = []
        for msg in request.messages:
            messages.append(DeepSeekMessage(role="user", content=msg.content))
        ds_service = deepseek_service.DeepSeekService()
        result = await ds_service.chat_completion(messages=messages)

        CallToolResult(
            content=[TextContent(type=ContentType.TEXT, text=result.content)]
        )

        return MCPResponse(response=result.content)
