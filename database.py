import sqlite3
from datetime import date
import logging

# Set up logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_db_action(action, details):
    logger.info(f"DB Action: {action} - Details: {details}")

# Connect to DB
conn = sqlite3.connect("/Users/zyuzyaev/Coding/habit_tracker/habits.db")
cursor = conn.cursor()

# 1. Create the table (with habit_name column)
cursor.execute("""
CREATE TABLE IF NOT EXISTS habit_tracking (
    user_id INTEGER NOT NULL,
    habit_type TEXT,
    habit_name TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    last_checkin TEXT
)
""")
conn.commit()

# 2. Get active users whose habit is ongoing today
def get_active_users():
    today = date.today().isoformat()
    cursor.execute("""
    SELECT user_id, habit_type, end_date, last_checkin, habit_name, start_date
    FROM habit_tracking
    WHERE start_date <= ? AND end_date >= ?
    """, (today, today))
    return cursor.fetchall()

# 3. Update the last check-in date to avoid double messages
def update_last_checkin(user_id):
    today = date.today().isoformat()
    cursor.execute("UPDATE habit_tracking SET last_checkin = ? WHERE user_id = ?", (today, user_id))
    conn.commit()

# 4. Add new user habit
def add_user_habit(user_id, habit_type, habit_name, start_date, end_date):
    try:
        log_db_action("Add Habit", f"User ID: {user_id}, Habit Type: {habit_type}, Name: {habit_name}, Start: {start_date}, End: {end_date}")
        cursor.execute(
            "INSERT INTO habit_tracking (user_id, habit_type, habit_name, start_date, end_date, last_checkin) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, habit_type, habit_name, start_date, end_date, None)
        )
        conn.commit()

        cursor.execute("SELECT * FROM habit_tracking WHERE user_id = ? ORDER BY rowid DESC LIMIT 1", (user_id,))
        inserted_record = cursor.fetchone()

        if inserted_record:
            log_db_action("Add Habit", f"Successfully added habit for user {user_id}: {inserted_record}")
        else:
            log_db_action("Add Habit", f"Failed to add habit for user {user_id}. Record not found.")

    except Exception as e:
        logger.error(f"Error adding habit for user {user_id}: {e}")