import pika
import json

import uuid
import pika
import aioredis
import asyncio
import aio_pika


async def send_scrape_task(cnpj):
    task_id = str(uuid.uuid4())

    # Conexão com Redis para armazenar o status da tarefa
    redis = await aioredis.create_redis_pool('redis://redis:6379')
    # Armazenar no Redis o status inicial da tarefa
    await redis.set(task_id, "processando...")
    value = await redis.get(task_id)
    print("Redis Test task_id:", value.decode())


    # Conexão com RabbitMQ usando aio_pika
    connection = await aio_pika.connect_robust(
        "amqp://meu_usuario:minha_senha@rabbitmq/"
    )

    async with connection:
        channel = await connection.channel()  # Cria um canal
        await channel.default_exchange.publish(
            aio_pika.Message(body=cnpj.encode(), correlation_id=task_id),
            routing_key='scrape_queue',
        )

    return task_id