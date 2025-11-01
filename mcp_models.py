from pydantic import BaseModel, Field
from typing import Optional, Any, Union
from enum import Enum


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
    data: Optional[str] = None
    mimeType: Optional[str] = None


Content = Union[TextContent, ImageContent]


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
