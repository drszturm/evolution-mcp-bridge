from enum import Enum
from typing import Any

from pydantic import BaseModel


class ToolType(str, Enum):
    FUNCTION = "function"


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"


class TextContent(BaseModel):
    type: ContentType = ContentType.TEXT
    text: str


class ImageContent(BaseModel):
    type: ContentType = ContentType.IMAGE
    data: str | None = None
    mimeType: str | None = None


Content = TextContent | ImageContent


class ToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: dict[str, Any]


class CallToolRequest(BaseModel):
    name: str
    arguments: dict[str, Any]


class CallToolResult(BaseModel):
    content: list[Content]


class ListToolsResult(BaseModel):
    tools: list[ToolDefinition]


class PromptMessage(BaseModel):
    role: str
    content: Content


class GetPromptResult(BaseModel):
    messages: list[PromptMessage]


class ErrorResponse(BaseModel):
    error: str
    code: int
    message: str
