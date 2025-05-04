from datetime import datetime, date
import random
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot

from database import get_active_users

# Set up logging
logger = logging.getLogger(__name__)

# Motivational quotes (expanded and themed)
QUOTES = [
    # High-energy
    "You're on fire! 🔥 Keep pushing, you're getting closer every day!",
    "Discipline > motivation. You've got this. 💪",
    "This habit is shaping your future self — one day at a time. 🚀",
    "Winners are made on ordinary days like today. Keep going. 🏆",

    # Encouraging
    "Small wins build big momentum. You're doing great. 🌱",
    "Every day you show up, you get stronger. Keep it up! 💫",
    "Proud of you — you're honoring your commitment. 🙌",
    "Consistency is your superpower. 🦸‍♂️🦸‍♀️",

    # Reflective
    "Not every day is easy, but every day counts. ☀️",
    "It’s not about being perfect — it’s about being present. 🌊",
    "One good choice today can shape your week. 🧩",
    "Still going? That’s already a win. Keep walking. 🚶",
]

# Helper: progress emoji based on % complete
def get_progress_emoji(percent):
    if percent >= 100:
        return "🎉 Completed!"
    elif percent >= 75:
        return "✅ Almost there!"
    elif percent >= 50:
        return "🟡 Halfway through!"
    else:
        return "🔄 Just getting started!"

# Main job: send motivation message to each user
async def send_motivation(bot: Bot):
    today = date.today()

    try:
        users = get_active_users()
        logger.info(f"Sending motivation to {len(users)} users.")

        for user_id, habit_type, end_date, last_checkin, habit_name, start_date in users:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            total_days = (end - start).days + 1
            current_day = (today - start).days + 1
            current_day = max(1, min(current_day, total_days))

            percent_complete = round((current_day / total_days) * 100)
            progress_emoji = get_progress_emoji(percent_complete)

            verb = "doing" if habit_type == "good" else "avoiding"
            quote = random.choice(QUOTES)

            text = (
                f"🌟 *Day {current_day}* of your habit challenge!\n"
                f"You're {verb} *{habit_name}*.\n"
                f"Goal: {total_days} days ({percent_complete}% complete) {progress_emoji}\n\n"
                f"💬 {quote}"
            )

            try:
                await bot.send_message(user_id, text, parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"Could not send to user {user_id}: {e}")

    except Exception as e:
        logger.error(f"Error while sending motivation: {e}")

# Scheduler setup
def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    '''
    scheduler.add_job(
        send_motivation,
        trigger=CronTrigger(hour=12, minute=0),  # Adjust as needed
        args=[bot],
        id="send_motivation",
        replace_existing=True
    )
    '''
    scheduler.add_job(
        send_motivation,
        IntervalTrigger(minutes=1),
        kwargs={"bot": bot},
        id="test_motivation",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Scheduler started.")