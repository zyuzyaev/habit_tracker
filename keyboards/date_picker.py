from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date

today = date.today().isoformat()

date_choice_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📆 Today", callback_data=f"set_date:{today}")],
    [InlineKeyboardButton(text="📅 Enter date manually", callback_data="enter_date_manual")]
])
