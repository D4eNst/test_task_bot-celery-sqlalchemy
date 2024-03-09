from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Keyboards can be created here (in the form of variables or functions)

# Example builder
def get_reply_kb(items: str | list):
    if isinstance(items, str):
        items = [items]

    builder = ReplyKeyboardBuilder()
    [builder.button(text=text) for text in items]

    return builder.as_markup(resize_keyboard=True)


# Remove keyboard
rkr = ReplyKeyboardRemove()


def main_menu_btn() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="Получить информацию по товару"),
            KeyboardButton(text="Получить информацию из БД")
        ],
        [
            KeyboardButton(text="Остановить уведомления")
        ]
    ],
        resize_keyboard=True
    )
    return keyboard


main_menu_btn = main_menu_btn()
