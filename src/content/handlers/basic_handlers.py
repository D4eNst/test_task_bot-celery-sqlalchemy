import random

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .keyboards import kb

router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer("Привет!", reply_markup=kb.main_menu_btn)


@router.message(F.text.in_(["Назад"]))
async def back(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Главное меню", reply_markup=kb.main_menu_btn)


@router.message()
async def other_messages(msg: types.Message):
    ans = ["Эм...", "Не понимаю(", "Попробуйте воспользоваться кнопками", "Я не знаю прогноз погоды!", "Я так и знал!"]
    await msg.answer(random.choice(ans))
