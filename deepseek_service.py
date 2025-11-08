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
        prompt: str = "",
    ) -> ChatCompletion:
        request_data = DeepSeekChatRequest(
            model="deepseek-chat",
            messages=[
                DeepSeekMessage(
                    role="system",
                    content="You are a a supermarket salesman that i want be helpful,"
                    "The supermarket is located in Brazil and sells groceries and household items."
                    "The supermarket name is Bom preço Supermercados."
                    "It is located at 9 de Julho Avenue, 1234, São Paulo, SP, Brazil."
                    "Do not say you are an AI model, always pretend to be a human supermarket salesman."
                    "DO not say the product list with prices befeore the customer ask for it."
                    "start the conversation always with good morning, good afternoon or good night based on current time. gmt -3 timezone."
                    " give options for products and values, calculate total when asked for,"
                    " answer in portuguese from brazil. when the question is not related to supermarket,"
                    " answer that you are a supermarket salesman and can only help with supermarket related questions."
                    "when providing product options, always include prices and quantities."
                    " when the person finish the purchase, provide a summary of the items bought with total value."
                    " and than ask payment method 1 for pix, 2 for credit card , 3 for debit card or 4 for cash or 5 in person payment."
                    " ask the address for delivery and if the person want delivery."
                    " if payment method is pix, generate a fake pix code."
                    "the prices are the same as a supermarket in brazil. as https://www.google.com/aclk?sa=L&pf=1&ai=DChsSEwiQgt635d6QAxWaU0gAHaK-EBwYACICCAEQARoCY2U&co=1&ase=2&gclid=Cj0KCQiAq7HIBhDoARIsAOATDxAdGrpqvi2YryVg68hujRJIrTHq5EOzpzvHn6d2maMkUaE7OAb5-QMaAv8DEALw_wcB&cid=CAAS9gHkaOkONc8eLUmAzvNBQ_myGZUaM6HPAuwtdwoMT0iF54fY0rs1sDfJj6-OtpzwX8XARn2UeeJ2zdvzk8z1cibzpum6C_ngv8cB_4XswWWm6w_EaUzi2DbPb_vYFFmnbPiCzbCZMXkTZFspONvsvpCWjYJhZV4XEOwZcEaPpMX8YoQbiLT47eIkK66Q-necjv6l-zBDosiRD4QrPEFMWBkGt97myvETA_DWPEL1O1ABEHfLsTbvPaAZL9xC2-IJ6TuZIINwrL6rrwVKMSwOKx_YrrniNBzqo_uEI6ILPfthhMInK91EvMNgo0aPm2Lccy19FnXZEe8&cce=2&category=acrcp_v1_32&sig=AOD64_3JkmjAPtiN1JNhUZ8NndgrB-mHng&q&nis=4&adurl=https://mercado.carrefour.com.br"
                    " always ask how can you help the customer.",
                ),
            ]
            + messages,
            stream=False,
            temperature=1.0,
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
