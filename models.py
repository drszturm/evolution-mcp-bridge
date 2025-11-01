from datetime import datetime
from typing import Any

from pydantic import BaseModel


# Evolution API Models
class WppMessage(BaseModel):
    key: dict | None
    message: dict
    messageType: str
    webhook_url: str | None = None


class SendMessageRequest(BaseModel):
    number: str
    text: str
    options: dict[str, Any] | None = None


class SendMediaRequest(BaseModel):
    number: str
    media: str  # URL or base64
    caption: str | None = None
    fileName: str | None = None
    options: dict[str, Any] | None = None


# MCP Server Models
class MCPMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime | None = None


class MCPRequest(BaseModel):
    messages: list[MCPMessage]
    session_id: str | None = None
    context: dict[str, Any] | None = None


class MCPResponse(BaseModel):
    response: str
    session_id: str | None = None
    context: dict[str, Any] | None = None


# Webhook Models
class WebhookPayload(BaseModel):
    instance: str
    data: dict[str, Any]
