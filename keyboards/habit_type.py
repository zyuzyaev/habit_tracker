from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

habit_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Good"), KeyboardButton(text="Bad")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)