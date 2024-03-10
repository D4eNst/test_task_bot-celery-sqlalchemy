import asyncio
import json

from repository.database import redis_client
from src.bot import bot
from src.utils import get_product_info
from task.celery_worker import app


@app.task
def notify_task():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_notification())


async def send_notification():
    stored_value = await redis_client.get("subscribers")
    if stored_value:
        retrieved_dict = json.loads(stored_value.decode('utf-8'))
    else:
        retrieved_dict = {}
    for user, products in retrieved_dict.items():
        for product in products:
            product_info = await get_product_info(product)
            await bot.send_message(chat_id=int(user), text=product_info)
    # text = await get_product_info(article=article)
    # await bot.send_message(chat_id=user_id, text="Тестирую уведомление")
