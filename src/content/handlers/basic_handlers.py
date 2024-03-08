import logging
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from repository.crud.user_request_repo import UserRequestsRepo
from repository.models import *
from .keyboards import kb, ikb

import src.content.states as st

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message) -> None:
    ans = "Привет!"
    btns = ["Получить информацию по товару", "Остановить уведомления", "получить информацию из БД"]
    await msg.answer(ans, reply_markup=kb.get_reply_kb(btns))


@router.message(F.is_("Получить информацию по товару"))
async def get_info(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(st.GetProductInfo.get_info)

    await msg.answer("Введите артикул", reply_markup=kb.rkr)


@router.message(st.GetProductInfo.get_info)
async def send_info(msg: types.Message, state: FSMContext, session: AsyncSession):
    if not msg.text.isdigit():
        # await msg.answer()
        ...

# States can be set:
# async def set_state(msg: types.Message, state: FSMContext) -> None:
#     await state.set_state(st.SomeState.state1)
