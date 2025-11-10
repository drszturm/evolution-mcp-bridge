import logging
from typing import Any

from ai.deepseek_web_service import DeepSeekService
from ai.mcp_client import MCPClient
from ai.mcp_models import AgentMessage
from config import settings
from deepseek_models import (
    ChatCompletion,
)
from messaging.models import MCPMessage, MCPRequest


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
        temperature: float = 0.7,
        stream: bool = False,
        prompt: str = "",
    ) -> ChatCompletion:
        result = None
        try:
            request_data = MCPRequest(
                messages=[MCPMessage(**msg.dict()) for msg in messages],
            )
            agent_result = await self.mcp_client.send_message(request_data)
            if not agent_result.response:
                raise Exception("Empty response from MCP Client")
            result = ChatCompletion(content=agent_result.response, model=self.model)
            return result
        except Exception as e:
            self.logger.error(f"Error in MCPClient send_message: {e}")
            # Fallback to DeepSeekService
            result = await self.deepseek_service.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream,
                prompt=prompt,
            )
            return result
        finally:
            self.logger.error("Error in  chat_completion:")
            raise

    async def close(self):
        # await self.client.aclose()
        pass


agent_service = ()
