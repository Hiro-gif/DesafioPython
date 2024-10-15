import asyncio
import json

import aio_pika
import aioredis
from core.scrapping import scrape_cnpj_data  # Certifique-se de adaptar este import ao seu módulo de scrapping

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        cnpj = data['cnpj']
        task_id = data['task_id']

        # Realizar o scrapping
        result = await scrape_cnpj_data(cnpj)

        # Conexão com Redis
        redis = await aioredis.create_redis_pool('redis://localhost')

        # Atualizar o status da tarefa no Redis
        await redis.set(task_id, json.dumps(result))



async def main():
    # Conexão ao RabbitMQ usando aio_pika
    connection = await aio_pika.connect_robust(
        "amqp://meu_usuario:minha_senha@localhost/"
    )

    async with connection:
        channel = await connection.channel()

        # Declarar a fila
        queue = await channel.declare_queue('scrape_tasks', durable=True)

        # Consumir mensagens da fila
        await queue.consume(process_message)

        # Manter o serviço rodando
        print("Worker está em execução. To exit press CTRL+C")
        await asyncio.Future()  # Mantém o worker rodando indefinidamente

if __name__ == "__main__":
    asyncio.run(main())