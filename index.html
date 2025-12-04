import os
import sqlite3
import datetime
import qrcode
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

# === CONFIGURATION ===
BOT_TOKEN = os.getenv("BOT_TOKEN") or "7217849898:AAHRoxZLxdBVxcxXGhSYnUyPtsqxp5cxhWg"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "events", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
LANGUAGES = ["en", "am"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Messages ---
MESSAGES = {
    "start": {"en": "Welcome to Girgira Events Bot!",
              "am": "Girgira ኢቨንት ቦት እንኳን በደህና መጡ!"},
    "choose_language": {"en": "Choose your language:", "am": "ቋንቋዎን ይምረጡ:"},
    "no_events": {"en": "No events available.", "am": "ምንም ኢቨንት የለም።"},
    "event_created": {"en": "Event '{title}' created successfully!",
                      "am": "ኢቨንት '{title}' በሙሉ ተፈጥሯል!"},
    "photo_uploaded": {"en": "Invitation photo uploaded successfully!",
                       "am": "የኢቨንት ፎቶ ተጫነ!"},
    "incorrect_format": {"en": "Incorrect format, please follow instructions.",
                         "am": "ቅርጸ ቃል ትክክል አይደለም። መመሪያ ይከተሉ።"},
    "rsvp_received": {"en": "RSVP received! Now upload a photo/video using /upload_rsvp <RSVP_ID>",
                      "am": "RSVP ተቀባ! እባኮትን ፎቶ/ቪዲዮ ለማረጋገጥ /upload_rsvp <RSVP_ID> ይጠቀሙ።"}
}

# --- User Language ---
user_lang = {}  # {user_id: 'en'/'am'}

# --- DATABASE ---
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    gps_lat REAL,
    gps_long REAL,
    invitation_photo TEXT,
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

# --- HELPER FUNCTIONS ---
def generate_event_qr(event_id):
    event_url = f"https://t.me/YourBotUsername?start=event{event_id}"
    qr_img_path = os.path.join(UPLOAD_FOLDER, f"event_{event_id}_qr.png")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(event_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_img_path)
    return qr_img_path

# --- COMMANDS ---

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = MESSAGES["start"]["en"] + "\n" + MESSAGES["choose_language"]["en"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("English", "Amharic")
    await message.answer(text, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["English", "Amharic"])
async def choose_language(message: types.Message):
    lang = "en" if message.text == "English" else "am"
    user_lang[message.from_user.id] = lang
    await message.answer("Language set." if lang=="en" else "ቋንቋ ተለዋዋጭ ሆነ።", reply_markup=types.ReplyKeyboardRemove())

# Admin: create event
@dp.message_handler(commands=['create_event'])
async def create_event(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    await message.answer(
        "Send event details in format:\nTitle|Description|Date|Time|Location|GPS_Lat|GPS_Long|Schedule"
        if lang=="en" else
        "ዝርዝሩን በዚህ ቅርጽ ይላኩ፦\nርዕስ|መግለጫ|ቀን|ሰዓት|ቦታ|GPS_Lat|GPS_Long|Schedule"
    )

@dp.message_handler(lambda message: "|" in message.text)
async def save_event(message: types.Message):
    parts = message.text.split("|")
    lang = user_lang.get(message.from_user.id, "en")
    if len(parts) != 8:
        await message.answer(MESSAGES["incorrect_format"][lang])
        return
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO events(title,description,date,time,location,gps_lat,gps_long,schedule)
    VALUES(?,?,?,?,?,?,?,?)
    """, (parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6], parts[7]))
    conn.commit()
    event_id = cursor.lastrowid
    conn.close()
    # Generate QR code
    qr_path = generate_event_qr(event_id)
    await message.answer(MESSAGES["event_created"][lang].format(title=parts[0]))
    await message.answer_photo(open(qr_path, 'rb'), caption="Scan this QR code to join the event!")

# Admin: upload invitation photo
@dp.message_handler(commands=['upload_photo'])
async def upload_photo(message: types.Message):
    parts = message.text.split()
    lang = user_lang.get(message.from_user.id, "en")
    if len(parts)!=2 or not parts[1].isdigit():
        await message.answer("Usage: /upload_photo <event_id>" if lang=="en" else "/upload_photo <event_id> ይጠቀሙ")
        return
    event_id = int(parts[1])
    await message.answer("Send the invitation photo.")

    @dp.message_handler(content_types=['photo'])
    async def photo_handler(msg: types.Message):
        photo = msg.photo[-1]
        path = os.path.join(UPLOAD_FOLDER, f"event_{event_id}_invitation.jpg")
        await photo.download(destination_file=path)
        conn = sqlite3.connect("db.sqlite")
        cursor = conn.cursor()
        cursor.execute("UPDATE events SET invitation_photo=? WHERE id=?", (path, event_id))
        conn.commit()
        conn.close()
        await msg.answer(MESSAGES["photo_uploaded"][lang])

# List events
@dp.message_handler(commands=['events'])
async def list_events(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT id,title,date,time,location FROM events")
    events = cursor.fetchall()
    conn.close()
    if not events:
        await message.answer(MESSAGES["no_events"][lang])
    else:
        msg = ""
        for e in events:
            msg += f"{e[0]}. {e[1]} | {e[2]} {e[3]} | {e[4]}\n"
        await message.answer(msg)

# Guest: RSVP
@dp.message_handler(commands=['rsvp'])
async def start_rsvp(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    await message.answer(
        "Send RSVP in format:\n<Event_ID>|<Your Name>|<Number of attendees>|<Comments>\nThen upload a photo/video using /upload_rsvp <RSVP_ID>"
        if lang=="en" else
        "RSVP እንዲህ ይላኩ:\n<Event_ID>|<ስምዎ>|<ተሳታፊዎች ብዛት>|<አስተያየት>\nከዚያ ፎቶ/ቪዲዮ ለማረጋገጥ /upload_rsvp <RSVP_ID> ይጠቀሙ።"
    )

@dp.message_handler(lambda message: "|" in message.text)
async def save_rsvp(message: types.Message):
    parts = message.text.split("|")
    lang = user_lang.get(message.from_user.id, "en")
    if len(parts)!=4:
        await message.answer(MESSAGES["incorrect_format"][lang])
        return
    event_id, guest_name, attendees, comments = parts
    if not event_id.isdigit() or not attendees.isdigit():
        await message.answer("Event ID and attendees must be numbers." if lang=="en" else "Event ID እና ተሳታፊ ብዛት ቁጥር መሆን አለባቸው።")
        return
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO rsvps(event_id, guest_name, attendees, comments, user_id)
    VALUES(?,?,?,?,?)
    """, (int(event_id), guest_name, int(attendees), comments, message.from_user.id))
    conn.commit()
    rsvp_id = cursor.lastrowid
    conn.close()
    await message.answer(MESSAGES["rsvp_received"][lang].format(), reply=False)

# Upload RSVP file
@dp.message_handler(commands=['upload_rsvp'])
async def upload_rsvp(message: types.Message):
    parts = message.text.split()
    lang = user_lang.get(message.from_user.id, "en")
    if len(parts)!=2 or not parts[1].isdigit():
        await message.answer("Usage: /upload_rsvp <RSVP_ID>" if lang=="en" else "/upload_rsvp <RSVP_ID> ይጠቀሙ")
        return
    rsvp_id = int(parts[1])
    await message.answer("Please send the photo or video now." if lang=="en" else "እባኮትን ፎቶ/ቪዲዮ አሁን ይላኩ።")

    @dp.message_handler(content_types=['photo', 'video'])
    async def save_file(msg: types.Message):
        conn = sqlite3.connect("db.sqlite")
        cursor = conn.cursor()
        file_ext = "jpg" if msg.content_type=="photo" else "mp4"
        path = os.path.join(UPLOAD_FOLDER, f"rsvp_{rsvp_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}")
        await msg.download(destination_file=path)
        cursor.execute("UPDATE rsvps SET file_path=? WHERE id=?", (path, rsvp_id))
        conn.commit()
        conn.close()
        await msg.answer("RSVP file uploaded successfully!" if lang=="en" else "RSVP ፎቶ/ቪዲዮ ተጫነ።")

# Admin: List RSVPs
@dp.message_handler(commands=['list_rsvps'])
async def list_rsvps(message: types.Message):
    parts = message.text.split()
    lang = user_lang.get(message.from_user.id, "en")
    if len(parts)!=2 or not parts[1].isdigit():
        await message.answer("Usage: /list_rsvps <event_id>" if lang=="en" else "/list_rsvps <event_id> ይጠቀሙ")
        return
    event_id = int(parts[1])
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT guest_name, attendees, comments, file_path FROM rsvps WHERE event_id=?", (event_id,))
    rsvps = cursor.fetchall()
    conn.close()
    if not rsvps:
        await message.answer("No RSVPs yet." if lang=="en" else "RSVP አልተሰጠም።")
        return
    msg = ""
    for r in rsvps:
        guest_name, attendees, comments, file_path = r
        msg += f"Name: {guest_name}, Attendees: {attendees}, Comments: {comments}\n"
        if file_path:
            msg += f"File: {file_path}\n"
        msg += "-------------------\n"
    await message.answer(msg)

# QR event link from /start=event
@dp.message_handler(lambda message: message.text.startswith("/start=event"))
async def qr_event_start(message: types.Message):
    event_id = int(message.text.replace("/start=event", ""))
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT title, description, date, time, location FROM events WHERE id=?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    if not event:
        await message.answer("Event not found.")
        return
    title, desc, date, time, loc = event
    await message.answer(f"Event Details:\nTitle: {title}\nDescription: {desc}\nDate: {date} {time}\nLocation: {loc}\nSend /rsvp to RSVP!")

if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)