import httpx
from typing import Dict, Any, Optional
from models import SendMessageRequest, SendMediaRequest
from config import settings


class EvolutionClient:
    def __init__(self) -> None:
        self.base_url = settings.EVOLUTION_API_BASE_URL
        self.headers = {
            "apikey": settings.EVOLUTION_API_KEY,
            "Content-Type": "application/json",
        }

    async def send_message(self, request: SendMessageRequest) -> Any:
        """Send text message via Evolution API"""
        async with httpx.AsyncClient() as client:
            payload = {
                "number": request.number,
                "text": request.text,
                **({"options": request.options} if request.options else {}),
            }

            response = await client.post(
                f"{self.base_url}/message/sendText/{request.number}",
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def send_media(self, request: SendMediaRequest) -> Any:
        """Send media message via Evolution API"""
        async with httpx.AsyncClient() as client:
            payload = {
                "number": request.number,
                "media": request.media,
                "fileName": request.fileName,
                "caption": request.caption,
                **({"options": request.options} if request.options else {}),
            }

            response = await client.post(
                f"{self.base_url}/message/sendMedia/{request.number}",
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_instance_info(self, instance: str) -> Any:
        """Get information about a specific instance"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/instance/info/{instance}", headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def set_webhook(self, instance: str) -> Any:
        """Set webhook for receiving messages"""
        async with httpx.AsyncClient() as client:
            payload = {
                "webhook": settings.WEBHOOK_URL,
                "enabled": True,
                "webhook_by_events": False,
            }

            response = await client.post(
                f"{self.base_url}/instance/setWebhook/{instance}",
                json=payload,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
