from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


# Evolution API Models
class EvolutionMessage(BaseModel):
    key: Optional[dict] = None
    message: Optional[dict] = None
    messageType: Optional[str] = None
    webhook_url: Optional[str] = None


class SendMessageRequest(BaseModel):
    number: str
    text: str
    options: Optional[Dict[str, Any]] = None


class SendMediaRequest(BaseModel):
    number: str
    media: str  # URL or base64
    caption: Optional[str] = None
    fileName: Optional[str] = None
    options: Optional[Dict[str, Any]] = None


# MCP Server Models
class MCPMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None


class MCPRequest(BaseModel):
    messages: List[MCPMessage]
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


# Webhook Models
class WebhookPayload(BaseModel):
    instance: str
    data: Dict[str, Any]
