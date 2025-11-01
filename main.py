import logging
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from evolution_client import EvolutionClient
from mcp_client import MCPClient
from models import (
    MCPMessage,
    MCPRequest,
    SendMediaRequest,
    SendMessageRequest,
    WebhookPayload,
    WppMessage,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    print("Application startup!")
    yield
    # Code to run on shutdown
    print("Application shutdown!")


app = FastAPI(
    title="Evolution API - MCP Bridge",
    description="Bridge between Whats App API and MCP Server",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client instances
evolution_client = EvolutionClient()
mcp_client = MCPClient()

# Store conversation sessions
conversation_sessions: dict[str, list[MCPMessage]] = {}


async def startup_event() -> None:
    """Initialize connections on startup"""
    logger.info("Starting Evolution API - MCP Bridge")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Evolution API - MCP Bridge is running"}


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Health check endpoint"""
    try:  # todo
        mcp_health = {"stable": True}  # await mcp_client.health_check()
        return {"status": "healthy", "mcp_server_available": mcp_health}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "mcp_server_available": False}


@app.post("/send-message")
async def send_message(request: SendMessageRequest):
    """Send message via Evolution API"""
    try:
        result = await evolution_client.send_message(request)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/send-media")
async def send_media(request: SendMediaRequest):
    """Send media via Evolution API"""
    try:
        result = await evolution_client.send_media(request)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error sending media: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def webhook_handler(
    payload: WebhookPayload, background_tasks: BackgroundTasks
) -> dict[str, str]:
    """Handle incoming webhook messages from Evolution API"""
    try:
        logger.info(f"Received webhook from instance: {payload.instance}")
        logger.info(f"Webhook data: {payload.data}")

        # Process webhook in background
        background_tasks.add_task(process_webhook_message, payload)

        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


async def process_webhook_message(payload: WebhookPayload) -> None:
    """Process incoming webhook message and forward to MCP"""
    try:
        # Extract message data from webhook payload
        message_data = extract_message_data(payload.data)

        if not message_data or not message_data.get("text"):
            logger.info("No text message found in webhook")
            return

        # Get phone number as session identifier
        phone_number = message_data.get("from")
        if not phone_number:
            logger.warning("No phone number found in message")
            return

        # Get or create conversation session
        session_id = f"whatsapp_{phone_number}"
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []

        # Add user message to session
        user_message = MCPMessage(role="user", content=message_data["text"])
        conversation_sessions[session_id].append(user_message)

        # Prepare MCP request
        mcp_request = MCPRequest(
            messages=conversation_sessions[session_id],
            session_id=session_id,
            context={"platform": "whatsapp", "phone_number": phone_number},
        )

        # Get response from MCP server
        mcp_response = await mcp_client.send_message(mcp_request)

        # Add assistant response to session
        assistant_message = MCPMessage(role="assistant", content=mcp_response.response)
        conversation_sessions[session_id].append(assistant_message)

        # Keep only last 10 messages to prevent memory issues
        if len(conversation_sessions[session_id]) > 10:
            conversation_sessions[session_id] = conversation_sessions[session_id][-10:]

        # Send response back via Evolution API
        send_request = SendMessageRequest(
            number=phone_number, text=mcp_response.response
        )

        await evolution_client.send_message(send_request)
        logger.info(f"Response sent to {phone_number}")

    except Exception as e:
        logger.error(f"Error processing webhook message: {str(e)}")
        phone_number = message_data.get("from")
        if phone_number:
            send_request = SendMessageRequest(
                number=str(phone_number), text="erro ao acessar o  agente"
            )
            await evolution_client.send_message(send_request)


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


@app.post("/chat-with-mcp")
async def chat_with_mcp(request: MCPRequest) -> dict[str, str]:
    """Direct chat endpoint with MCP server"""
    try:
        msg_response = await mcp_client.send_message(request)
        return {"status": "success", "data": msg_response.response}
    except Exception as e:
        logger.error(f"Error communicating with MCP: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def get_sessions() -> Any:
    """Get all active conversation sessions"""
    return {
        "sessions": {
            session_id: [msg.dict() for msg in messages]
            for session_id, messages in conversation_sessions.items()
        }
    }


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear a specific conversation session"""
    if session_id in conversation_sessions:
        del conversation_sessions[session_id]
        return {"status": "success", "message": f"Session {session_id} cleared"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.post("/setup-webhook/{instance}")
async def setup_webhook(instance: str):
    """Setup webhook for a specific Evolution API instance"""
    try:
        result = await evolution_client.set_webhook(instance)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error setting up webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
