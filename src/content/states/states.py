from aiogram.fsm.state import StatesGroup, State


class GetProductInfo(StatesGroup):
    get_info = State()
