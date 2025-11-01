from pydantic import BaseModel, Field
from typing import Optional, Any


class DeepSeekMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")


class DeepSeekChatRequest(BaseModel):
    model: str = Field(default="deepseek-chat")
    messages: list[DeepSeekMessage]
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=4096)
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    stream: bool = Field(default=False)


class DeepSeekChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[dict[str, Any]]
    usage: dict[str, int]


class ChatCompletion(BaseModel):
    content: str
    model: str
    usage: dict[str, int]
