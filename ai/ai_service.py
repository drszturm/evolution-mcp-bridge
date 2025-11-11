import logging
from typing import Any
from ai.deepseek_models import ChatCompletion
from config import settings
from ai.mcp_service import DeepSeekService
from ai.mcp_client import MCPClient
from ai.mcp_models import AgentMessage


from messaging.models import MCPMessage, MCPRequest, MCPResponse


class AgentService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL
        self.model = settings.DEEPSEEK_MODEL
        self.logger = logging.getLogger(__name__)
        self.deepseek_service = DeepSeekService()
        self.mcp_client = MCPClient()  # Placeholder for MCP client if needed

    async def send(
        self,
        messages: list[AgentMessage],
        max_tokens: int = 2048,
        temperature: float = 0.4,
        stream: bool = False,
    ) -> MCPResponse:
        result = None
        try:
            # Fallback to DeepSeekService
            result = await self.deepseek_service.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
            )
            logging.debug(f"DeepSeekService result: {result}")
            content = (
                result.content if isinstance(result, ChatCompletion) else str(result)
            )
            return MCPResponse(response=content)
        except Exception as e:
            self.logger.error(f"Error in MCPClient send_message: {e}")
            raise

    async def close(self):
        # await self.client.aclose()
        pass


agent_service = AgentService()
