from typing import AsyncGenerator

from aiokafka import AIOKafkaConsumer

from config import config


async def consume(user_id: str) -> AsyncGenerator:
    consumer = AIOKafkaConsumer(
        "notifications",
        user_id,
        bootstrap_servers=config.kafka_port,
        group_id="notifications",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            yield {
                "topic": msg.topic,
                "partition": msg.partition,
                "offset": msg.offset,
                "key": msg.key,
                "value": msg.value,
                "timestamp": msg.timestamp,
            }
    finally:
        await consumer.stop()
