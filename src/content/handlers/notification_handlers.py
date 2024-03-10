import json

from aiogram import types, Router, F
# import tasks.tasks as task

from repository.database import redis_client

router = Router()


@router.callback_query(F.data.contains("subscribe"))
async def subscribe_handler(callback: types.CallbackQuery):
    article = callback.data.split()[1]
    # task.notify_task.apply_async(args=[callback.from_user.id], countdown=None, eta=None, interval=10)

    stored_value = await redis_client.get("subscribers")
    if stored_value:
        retrieved_dict = json.loads(stored_value.decode('utf-8'))
    else:
        retrieved_dict = {}
    user_products = retrieved_dict.get(str(callback.from_user.id))
    user_id = callback.from_user.id
    if user_products is None:
        retrieved_dict[str(user_id)] = []
    if article not in retrieved_dict[str(user_id)]:
        retrieved_dict[str(user_id)].append(article)
        await redis_client.set("subscribers", json.dumps(retrieved_dict))
        await callback.answer(f"Вы подписались на получение уведомлений по товару с артикулом {article}")
    else:
        await callback.answer(f"Вы уже подписались на уведомления к этому товару")


@router.message(F.text.lower() == "остановить уведомления")
async def unsubscribe(msg: types.Message):
    user_id = msg.from_user.id
    stored_value = await redis_client.get("subscribers")
    if stored_value:
        retrieved_dict = json.loads(stored_value.decode('utf-8'))
    else:
        retrieved_dict = {}

    if retrieved_dict.get(str(user_id)):
        del retrieved_dict[str(user_id)]

    await redis_client.set("subscribers", json.dumps(retrieved_dict))
    await msg.answer("Вы отписались от уведомлений")
