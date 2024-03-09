from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from .keyboards import kb

router = Router()


@router.callback_query(F.data.contains("subscribe"))
async def subscribe_handler(callback: types.CallbackQuery):
    article = callback.data.split()[1]
    await callback.answer(f"Вы подписались на получение уведомлений по товару с артикулом {article}")
