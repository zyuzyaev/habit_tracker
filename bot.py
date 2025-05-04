from dotenv import load_dotenv
import os

load_dotenv()  # <- this loads .env

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()