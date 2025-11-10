import ai.deepseek_web_service as deepseek_web_service
from config import settings

from ai.mcp_models import AgentMessage, CallToolResult, ContentType, TextContent
from messaging.models import MCPRequest, MCPResponse


class MCPClient:
    def __init__(self) -> None:
        self.base_url = settings.MCP_SERVER_URL
        self.headers = {
            "Authorization": f"Bearer {settings.MCP_API_KEY}",
            "Content-Type": "application/json",
        }

    async def send_message(self, request: MCPRequest) -> MCPResponse:
        """Send message to MCP server and get response"""
        try:
            messages = []
            for msg in request.messages:
                messages.append(
                    AgentMessage(
                        role="user",
                        content=f"<{request.session_id}>\n\n" + msg.content,
                    )
                )
            ds_service = deepseek_web_service.DeepSeekService()
            result = await ds_service.chat_completion(messages=messages)

            CallToolResult(
                content=[TextContent(type=ContentType.TEXT, text=result.content)]
            )

            return MCPResponse(response=result.content)

        except Exception as e:
            # return MCPResponse(response=str(e))
            raise Exception(f"MCP Client HTTP error: {str(e)}") from e
