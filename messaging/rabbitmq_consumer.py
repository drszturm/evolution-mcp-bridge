"""RabbitMQ consumer for Evolution API events."""

import json
from collections.abc import Callable

import aio_pika


class EvolutionRabbitMQConsumer:
    """Consumes events from Evolution API RabbitMQ queues."""

    def __init__(self, rabbitmq_url: str):
        """Initialize consumer with RabbitMQ URL and Redis cache."""
        self.rabbitmq_url = rabbitmq_url
        self.connection = None
        self.channel = None
        self.callbacks: dict[str, Callable] = {}

    async def connect(self):
        """Establish RabbitMQ connection."""
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

        exchange = await self.channel.declare_exchange(
            "evolution_exchange", aio_pika.ExchangeType.TOPIC, durable=True
        )
        return exchange

    async def consume_events(self, event_types: list):
        """Start consuming specified event types."""
        exchange = await self.connect()
        if self.channel is None:
            raise Exception("RabbitMQ channel is not established.")
        for event_type in event_types:
            queue = await self.channel.declare_queue(
                f"evolution_{event_type}", durable=True
            )

            await queue.bind(exchange, routing_key=f"event.{event_type}")
            await queue.consume(self._create_callback(event_type))

    def _create_callback(self, event_type: str):
        """Create callback handler for specific event type."""

        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    event_data = json.loads(message.body)

                    if event_type in self.callbacks:
                        await self.callbacks[event_type](event_data)

                except Exception as e:
                    print(f"Error processing event {event_type}: {e}")

        return callback

    def register_callback(self, event_type: str, handler: Callable):
        """Register callback for event type."""
        self.callbacks[event_type] = handler
