from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Inline keyboards can be created here (in the form of variables or functions)

# Example inline keyboard:
# def arrows() -> InlineKeyboardMarkup:
#     ikb_builder = InlineKeyboardBuilder()
#
#     ikb_builder.button(text="⬅", callback_data="arrow_back")
#     ikb_builder.button(text="➡", callback_data="arrow_next")
#
#     return ikb_builder.as_markup()

def get_reply_kb(items: dict):
    ikb_builder = InlineKeyboardBuilder()
    [ikb_builder.button(text=key, callback_data=value) for key, value in items.items()]

    return ikb_builder.as_markup()
