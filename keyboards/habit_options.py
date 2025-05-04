from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bad_habit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Alcohol", callback_data="habit:Alcohol")],
    [InlineKeyboardButton(text="Smoking", callback_data="habit:Smoking")],
    [InlineKeyboardButton(text="Fast food", callback_data="habit:Fast food")],
    [InlineKeyboardButton(text="✍️ Type my own", callback_data="habit:custom")]
])

good_habit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Running", callback_data="habit:Running")],
    [InlineKeyboardButton(text="Reading", callback_data="habit:Reading")],
    [InlineKeyboardButton(text="Sports", callback_data="habit:Sports")],
    [InlineKeyboardButton(text="✍️ Type my own", callback_data="habit:custom")]
])