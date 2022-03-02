from aiokafka import AIOKafkaProducer

from config import config


async def send_one(username: str, message: str):
    producer = AIOKafkaProducer(bootstrap_servers=config.kafka_port)

    await producer.start()
    try:
        await producer.send_and_wait(username, message.encode())
    finally:
        await producer.stop()
