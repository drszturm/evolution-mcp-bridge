from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


# Evolution API Models
class WppMessage(BaseModel):
    key: Optional[dict]
    message: dict
    messageType: str
    webhook_url: Optional[str] = None


class SendMessageRequest(BaseModel):
    number: str
    text: str
    options: Optional[dict[str, Any]] = None


class SendMediaRequest(BaseModel):
    number: str
    media: str  # URL or base64
    caption: Optional[str] = None
    fileName: Optional[str] = None
    options: Optional[dict[str, Any]] = None


# MCP Server Models
class MCPMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class MCPRequest(BaseModel):
    messages: List[MCPMessage]
    session_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None


class MCPResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None


# Webhook Models
class WebhookPayload(BaseModel):
    instance: str
    data: dict[str, Any]
