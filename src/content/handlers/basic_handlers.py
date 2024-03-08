import logging
from random import choice

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.user_request_repo import UserRequestsRepo
from repository.models import *
from .keyboards import kb, ikb

import src.content.states as st
from .schemas.user_request import UserRequest

router = Router()

btns = ["Получить информацию по товару", "Остановить уведомления", "получить информацию из БД"]


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("Привет!", reply_markup=kb.get_reply_kb(btns))


@router.message(F.text.in_(["Получить информацию по товару"]))
async def get_info(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(st.GetProductInfo.get_info)
    await msg.answer("Введите артикул: ", reply_markup=kb.get_reply_kb("Назад"))


@router.message(st.GetProductInfo.get_info, F.text.not_in("Назад"))
async def send_info(msg: types.Message, state: FSMContext, session: AsyncSession):
    if not msg.text.isdigit():
        await msg.answer("Похоже, это не артикул, попробуйте ещё: ")
        return
    repo = UserRequestsRepo(session)
    req = UserRequest(tg_id=msg.from_user.id, article=int(msg.text))
    await repo.create(req.model_dump())

    # логика получения ответа
    ans = f"Вот информация о товаре {msg.text}"

    await state.clear()
    await msg.answer(ans, reply_markup=kb.get_reply_kb(btns))


@router.message(F.text.in_(["получить информацию из БД"]))
async def get_requests_from_db(msg: types.Message, session: AsyncSession) -> None:
    repo = UserRequestsRepo(session)
    user_requests = await repo.find_last_5_records(tg_id=msg.from_user.id)
    ans_list = []
    for req in user_requests:
        ans_list.append(f"Article: {req.article}, date: {req.created_at}")

    await msg.answer("\n".join(ans_list))


@router.message(F.text.in_(["Назад"]))
async def back(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Главное меню", reply_markup=kb.get_reply_kb(btns))


@router.message()
async def other_messages(msg: types.Message):
    ans = ["Эм...", "Не понимаю(", "Попробуйте воспользоваться кнопками", "Я не знаю прогноз погоды!", "Я так и знал!"]
    await msg.answer(choice(ans))

# States can be set:
# async def set_state(msg: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
