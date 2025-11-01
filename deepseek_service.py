import logging

import httpx

from config import settings
from deepseek_models import (
    ChatCompletion,
    DeepSeekChatRequest,
    DeepSeekMessage,
)

logger = logging.getLogger(__name__)


class DeepSeekService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = settings.DEEPSEEK_BASE_URL
        self.model = settings.DEEPSEEK_MODEL
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def chat_completion(
        self,
        messages: list[DeepSeekMessage],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> ChatCompletion:
        request_data = DeepSeekChatRequest(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream,
        )

        try:
            response = await self.client.post(
                "/chat/completions", json=request_data.model_dump()
            )

            if response.status_code != 200:
                error_msg = (
                    f"DeepSeek API error: {response.status_code} - {response.text}"
                )
                logger.error(error_msg)
                raise Exception(error_msg)

            data = response.json()

            return ChatCompletion(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
                usage=data["usage"],
            )

        except httpx.TimeoutException:
            logger.error("DeepSeek API request timeout")
            raise Exception("Request timeout. Please try again.")
        except httpx.RequestError as e:
            logger.error(f"DeepSeek API request error: {str(e)}")
            raise Exception("Service temporarily unavailable. Please try again.")
        except Exception as e:
            logger.error(f"Unexpected error in DeepSeek service: {str(e)}")
            raise

    async def close(self):
        await self.client.aclose()


deepseek_service = DeepSeekService()
