import logging
from typing import Any

import httpx

from config import settings
import messaging.evolution_client as evolution_client
from messaging.models import SendMediaRequest, SendMessageRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageService:
    def __init__(self) -> None:
        self.wpp_client = evolution_client.EvolutionClient()
        self.instagram_client = None

    @staticmethod
    def extract_message_data(webhook_data: dict[str, Any]) -> dict[str, Any]:
        """Extract message data from Evolution API webhook payload"""
        try:
            if not isinstance(webhook_data, dict):
                logger.error("Webhook data is not a dictionary")
                return {}

            # First structure validation
            if "key" in webhook_data and "message" in webhook_data:
                key_data = webhook_data.get("key", {})
                message_data = webhook_data.get("message", {})

                if not isinstance(key_data, dict) or not isinstance(message_data, dict):
                    logger.error("Invalid key or message structure")
                    return {}

                if "remoteJid" not in key_data:
                    logger.error("Missing remoteJid in key data")
                    return {}

                return {
                    "from": key_data["remoteJid"].replace("@s.whatsapp.net", ""),
                    "text": message_data.get("conversation", ""),
                    "timestamp": webhook_data.get("messageTimestamp"),
                    "id": key_data.get("id"),
                }

            # Second structure validation
            elif "messages" in webhook_data:
                messages = webhook_data.get("messages", [])

                if not isinstance(messages, list) or not messages:
                    logger.error("Messages field is not a list or is empty")
                    return {}

                message = messages[0]
                if not isinstance(message, dict):
                    logger.error("Message is not a dictionary")
                    return {}

                if "chatId" not in message:
                    logger.error("Missing chatId in message")
                    return {}

                return {
                    "from": message["chatId"].replace("@s.whatsapp.net", ""),
                    "text": message.get("body", ""),
                    "timestamp": message.get("timestamp"),
                    "id": message.get("id"),
                }
            else:
                logger.warning(f"Unknown webhook structure: {webhook_data}")
                return {}
        except Exception as e:
            logger.error(f"Error extracting message data: {str(e)}")
            return {}


message_service = MessageService()
