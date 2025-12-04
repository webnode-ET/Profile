import os
import sqlite3
import datetime
from telebot import TeleBot, types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
bot = TeleBot(BOT_TOKEN)

# --- DATABASE setup ---
DB_FILE = "db.sqlite"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    schedule TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS rsvps(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    guest_name TEXT,
    attendees INTEGER,
    comments TEXT,
    file_path TEXT,
    user_id INTEGER
)
""")
conn.commit()
conn.close()

# --- Start command ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to Girgira Events Bot!\nUse /create_event to add an event or /events to list events.")

# --- Create event (Admin only) ---
@bot.message_handler(commands=['create_event'])
def create_event(message):
    try:
        # Format: /create_event Title|Description|Date|Time|Location|Schedule
        text = message.text[len("/create_event "):]
        parts = text.split("|")
        if len(parts) != 6:
            bot.reply_to(message, "Incorrect format. Use:\nTitle|Description|Date|Time|Location|Schedule")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO events(title, description, date, time, location, schedule)
        VALUES(?,?,?,?,?,?)
        """, tuple(parts))
        conn.commit()
        conn.close()
        bot.reply_to(message, f"Event '{parts[0]}' created successfully!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# --- List events ---
@bot.message_handler(commands=['events'])
def list_events(message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, date, time, location FROM events")
    events = cursor.fetchall()
    conn.close()
    if not events:
        bot.reply_to(message, "No events available.")
        return
    msg = ""
    for e in events:
        msg += f"{e[0]}. {e[1]} | {e[2]} {e[3]} | {e[4]}\n"
    bot.reply_to(message, msg)

# --- RSVP ---
@bot.message_handler(commands=['rsvp'])
def rsvp(message):
    try:
        # Format: /rsvp EventID|YourName|NumberAttendees|Comments
        text = message.text[len("/rsvp "):]
        parts = text.split("|")
        if len(parts) != 4:
            bot.reply_to(message, "Incorrect format. Use:\nEventID|YourName|NumberAttendees|Comments")
            return
        event_id, guest_name, attendees, comments = parts
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO rsvps(event_id, guest_name, attendees, comments, user_id)
        VALUES(?,?,?,?,?)
        """, (int(event_id), guest_name, int(attendees), comments, message.from_user.id))
        conn.commit()
        conn.close()
        bot.reply_to(message, "RSVP received successfully!")
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# --- Start polling ---
bot.polling()