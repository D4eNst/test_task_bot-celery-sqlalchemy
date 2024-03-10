import logging

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import src.content.states as st
from repository.crud.user_request_repo import UserRequestsRepo
from src.utils import get_product_info
from .keyboards import kb, ikb

router = Router()


@router.message(F.text.lower() == "получить информацию по товару")
async def get_info(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(st.GetProductInfo.get_info)
    await msg.answer("Введите артикул: ", reply_markup=kb.get_reply_kb("Назад"))


@router.message(st.GetProductInfo.get_info, F.text.not_in("Назад"))
async def send_info(msg: types.Message, state: FSMContext, session: AsyncSession):
    if not msg.text.isdigit():
        await msg.answer("Похоже, это не артикул, попробуйте ещё: ")
        return

    try:
        ans = await get_product_info(msg.text)
    except ValueError:
        await msg.answer("По данному артикулу товар не найден")
        return
    except Exception as e:
        logging.error(e)
        await msg.answer("Произошла непредвиденная ошибка!", reply_markup=kb.main_menu_btn)
        return

    # Добавление записи в бд
    repo = UserRequestsRepo(session)
    req = dict(tg_id=msg.from_user.id, article=int(msg.text))
    await repo.create(req)

    await state.clear()
    await msg.answer(ans, reply_markup=ikb.get_reply_kb({"Подписаться": f"subscribe {msg.text}"}))
    await msg.answer("Главое меню   ", reply_markup=kb.main_menu_btn)


@router.message(F.text.lower() == "получить информацию из бд")
async def get_requests_from_db(msg: types.Message, session: AsyncSession) -> None:
    repo = UserRequestsRepo(session)
    user_requests = await repo.find_last_5_records(tg_id=msg.from_user.id)
    ans_list = []
    for req in user_requests:
        ans_list.append(f"📚 Артикул: {req.article}\n🗓 Дата запроса: {req.created_at:%Y-%m-%d %H:%M:%S}")
    sep = "\n" + "-"*55 + "\n"
    await msg.answer(sep.join(ans_list))
