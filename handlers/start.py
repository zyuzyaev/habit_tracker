from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.habit_type import habit_type_kb
from keyboards.date_picker import date_choice_kb
from keyboards.duration_picker import duration_choice_kb
from keyboards.habit_options import good_habit_kb, bad_habit_kb
from datetime import datetime, timedelta, date

# Import your DB insert function
from database import add_user_habit  # Make sure this is correctly imported

router = Router()

class HabitStates(StatesGroup):
    choosing_type = State()
    naming_habit = State()
    choosing_start_date = State()
    choosing_end_date = State()  # NEW state
    waiting_manual_date = State()
    waiting_manual_duration = State()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Hi! Let's begin.\nDo you want to track a good or bad habit?",
                         reply_markup=habit_type_kb)
    await state.set_state(HabitStates.choosing_type)


@router.message(HabitStates.choosing_type)
async def choose_type(message: Message, state: FSMContext):
    habit_type = message.text.strip().lower()
    if habit_type not in ["good", "bad"]:
        await message.answer("Please choose either 'Good' or 'Bad'.")
        return
    await state.update_data(habit_type=habit_type)
    if habit_type == "good":
        await message.answer("Great! Choose your good habit or type your own:", reply_markup=good_habit_kb)
    else:
        await message.answer("Okay! Choose your bad habit or type your own:", reply_markup=bad_habit_kb)


@router.callback_query(F.data.startswith("habit:"), HabitStates.choosing_type)
async def handle_habit_choice(callback: CallbackQuery, state: FSMContext):
    habit_value = callback.data.split(":")[1]
    if habit_value == "custom":
        await callback.message.answer("Okay, please type your habit:")
        await state.set_state(HabitStates.naming_habit)
    else:
        await state.update_data(habit_name=habit_value)
        data = await state.get_data()
        habit_type = data.get("habit_type")
        await callback.message.answer(
            f"You're tracking the {habit_type} habit: {habit_value}\nNow, when did you start (or stop) it?",
            reply_markup=date_choice_kb
        )
        await state.set_state(HabitStates.choosing_start_date)
    await callback.answer()


@router.message(HabitStates.naming_habit)
async def set_habit_name(message: Message, state: FSMContext):
    habit_name = message.text.strip()
    await state.update_data(habit_name=habit_name)
    data = await state.get_data()
    habit_type = data.get("habit_type")
    await message.answer(
        f"You're tracking the {habit_type} habit: {habit_name}\nNow, when did you start (or stop) it?",
        reply_markup=date_choice_kb
    )
    await state.set_state(HabitStates.choosing_start_date)


@router.callback_query(F.data.startswith("set_date:"))
async def set_date_today(callback: CallbackQuery, state: FSMContext):
    chosen_date = callback.data.split(":")[1]
    await state.update_data(start_date=chosen_date)
    await callback.message.answer(f"Got it! Start date: {chosen_date}.\nNow, until when do you want to stay consistent?",
                                  reply_markup=duration_choice_kb)
    await state.set_state(HabitStates.choosing_end_date)


@router.callback_query(F.data == "enter_date_manual")
async def prompt_manual_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Please type the date in YYYY-MM-DD format:")
    await state.set_state(HabitStates.waiting_manual_date)


@router.message(HabitStates.waiting_manual_date)
async def get_manual_date(message: Message, state: FSMContext):
    try:
        date_obj = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
        await state.update_data(start_date=str(date_obj))
        await message.answer(f"Saved! Start date: {date_obj}.\nNow, until when do you want to stay consistent?",
                             reply_markup=duration_choice_kb)
        await state.set_state(HabitStates.choosing_end_date)
    except ValueError:
        await message.answer("❌ Invalid date format. Please use YYYY-MM-DD.")


@router.callback_query(F.data.startswith("duration:"), HabitStates.choosing_end_date)
async def set_duration(callback: CallbackQuery, state: FSMContext):
    days = int(callback.data.split(":")[1])
    end_date = date.today() + timedelta(days=days)
    await state.update_data(end_date=end_date.isoformat())
    await finish_and_save(callback.message, state)


@router.callback_query(F.data == "duration_manual", HabitStates.choosing_end_date)
async def prompt_manual_duration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Please enter the goal date in format YYYY-MM-DD (e.g. 2025-07-01):")
    await state.set_state(HabitStates.waiting_manual_duration)


@router.message(HabitStates.waiting_manual_duration)
async def get_manual_duration(message: Message, state: FSMContext):
    try:
        end_date = datetime.strptime(message.text.strip(), "%Y-%m-%d").date()
        await state.update_data(end_date=end_date.isoformat())
        await finish_and_save(message, state)
    except ValueError:
        await message.answer("❌ Invalid format. Please use YYYY-MM-DD (e.g. 2025-07-01)")


# Final logic to insert to DB
async def finish_and_save(message_or_callback, state: FSMContext):
    data = await state.get_data()
    user_id = message_or_callback.from_user.id
    habit_type = data.get("habit_type")
    habit_name = data.get("habit_name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if all([habit_type, habit_name, start_date, end_date]):
        add_user_habit(
            user_id=user_id,
            habit_type=habit_type,
            habit_name=habit_name,
            start_date=start_date,
            end_date=end_date
        )
        await message_or_callback.answer(f"✅ Habit saved!\n"
                                         f"Type: {habit_type}\n"
                                         f"Habit: {habit_name}\n"
                                         f"From: {start_date}\n"
                                         f"To: {end_date}")
        await state.clear()
    else:
        await message_or_callback.answer("⚠️ Some data is missing. Please try again.")