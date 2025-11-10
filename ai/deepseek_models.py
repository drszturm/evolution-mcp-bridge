from typing import Any

from pydantic import BaseModel


class DeepSeekChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[dict[str, Any]]


class ChatCompletion(BaseModel):
    content: str
    model: str
