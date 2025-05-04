from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

duration_choice_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="7 days", callback_data="duration:7"),
        InlineKeyboardButton(text="2 weeks", callback_data="duration:14"),
    ],
    [
        InlineKeyboardButton(text="1 month", callback_data="duration:30"),
        InlineKeyboardButton(text="3 months", callback_data="duration:90"),
    ],
    [
        InlineKeyboardButton(text="📅 Enter date (YYYY-MM-DD)", callback_data="duration_manual")
    ]
])