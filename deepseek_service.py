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
            timeout=120.0,
        )

    async def chat_completion(
        self,
        messages: list[DeepSeekMessage],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        stream: bool = False,
    ) -> ChatCompletion:
        request_data = DeepSeekChatRequest(
            model="deepseek-chat",
            messages=[
                DeepSeekMessage(
                    role="system",
                    content="You are a a supermarket salesman that i want be helpful,"
                    " give options for products and values, calculate total when asked for,"
                    " answer in portuguese from brazil. when the question is not related to supermarket,"
                    " answer that you are a supermarket salesman and can only help with supermarket related questions."
                    "when providing product options, always include prices and quantities."
                    " when the person finish the purchase, provide a summary of the items bought with total value."
                    " and than ask payment method pix, credit card or debit card or in person payment."
                    " ask the address for delivery and if the person want delivery."
                    " if payment method is pix, generate a fake pix code.",
                ),
            ]
            + messages,
            stream=False,
        )
        logger.debug(f"DeepSeek API request data: {request_data.model_dump()}")
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
            logger.debug(f"DeepSeek API response data: {data}")
            return ChatCompletion(
                content=data["choices"][0]["message"]["content"],
                model=data["model"],
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
