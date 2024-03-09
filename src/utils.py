import json
import logging
import aiohttp

from repository.database import async_db


async def start_with() -> None:
    logging.warning("Bot has been started!")


async def stop_with():
    await async_db.async_engine.dispose()
    logging.warning("Bot has been stopped!")


async def fetch_data_from_article(article: int | str):
    if isinstance(article, str) and not article.isdigit():
        raise ValueError("Article must be an integer")
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_product_info(article: int | str) -> str:
    product_data = await fetch_data_from_article(article)
    qts = {}

    products = product_data["data"]["products"]
    if not products:
        raise ValueError

    product = products[0]
    for size in product["sizes"]:
        qty = 0
        for stock in size["stocks"]:
            qty += stock["qty"]
        if len(product["sizes"]) > 1:
            qts[size["origName"]] = qty
        else:
            qts["one_size"] = qty

    ans = f"Вот информация о товаре с артикулом {article}: \n"
    ans += f'<b>Название</b>: {product["name"]}\n'
    ans += f'<b>Цена</b>: <s>{int(product["priceU"]) / 100} Руб</s> {int(product["salePriceU"]) / 100} Руб\n'
    ans += f'<b>Рейтинг</b>: {product["reviewRating"]}, на основе отзывов: {product["feedbacks"]}\n'
    ans += f'<b>Общее количество на складах</b>: '
    if len(qts) == 1:
        ans += str(qts.get("one_size"))
    else:
        ans += "\n - " + "\n - ".join([f'{key}: {value}' for key, value in qts.items()])
        ans += f"\nВсего: {sum((int(value) for key, value in qts.items()))}"

    return ans
