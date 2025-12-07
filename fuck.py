# ======================================================================
#  © 2025 ʙᴏᴛᴍɪɴᴇ ᴛᴇᴄʜ & ꜱʜʀᴇᴇ ᴛᴇᴄʜ. ᴀʟʟ ʀɪɢʜᴛs ʀᴇꜱᴇʀᴠᴇᴅ.
#
#  ᴛʜɪs ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪꜱ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ᴜɴᴅᴇʀ ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ ᴘʀᴏᴘᴇʀᴛʏ ʟᴀᴡꜱ.
#  ᴍᴏᴅɪꜰɪᴄᴀᴛɪᴏɴ, ʀᴇꜱᴇʟʟɪɴɢ, ᴘᴜʙʟɪꜱʜɪɴɢ ᴏʀ ʀᴇᴅɪꜱᴛʀɪʙᴜᴛɪᴏɴ
#  ᴡɪᴛʜᴏᴜᴛ ᴘʀɪᴏʀ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ɪꜱ ꜱᴛʀɪᴄᴛʟʏ ᴘʀᴏʜɪʙɪᴛᴇᴅ.
#
#  ᴏᴡɴᴇʀꜱʜɪᴘ : @BOTMINE_TECH | @TheShreeTech
# ======================================================================

import os
import sys
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserAdminInvalid
from pymongo import MongoClient
import psutil
import platform
import time

load_dotenv()

# ================= ENV =================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
MONGO_URL = os.getenv("MONGO_URL")

mongo = MongoClient(MONGO_URL)
db = mongo["BANALL"]
users_db = db["users"]
groups_db = db["groups"]

SEMAPHORE = asyncio.Semaphore(400)   # heroku safe max speed
START_IMG = "https://files.catbox.moe/o7pv72.jpg"

app = Client(
    "BANALL-SESSION",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= SAVE =================
async def save_user(user):
    try:
        users_db.update_one({"_id": user.id}, {"$set": {"name": user.first_name}}, upsert=True)
    except:
        pass

async def save_group(chat):
    try:
        groups_db.update_one({"_id": chat.id}, {"$set": {"title": chat.title}}, upsert=True)
    except:
        pass

# ================= UI =================
def start_ui(name):
    return (
        f"**ʜᴇʏ {name}!**\n\n"
        "**ᴛʜᴇ ғᴀsᴛᴇsᴛ ʙᴀɴᴀʟʟ ʙᴏᴛ ɪɴ ᴛᴇʟᴇɢʀᴀᴍ 🚀**\n"
        "**ᴘᴏᴡᴇʀᴇᴅ ʙʏ ᴛʜᴇ ᴜɴᴋɴᴏᴡɴ ᴍɪɴᴅ 🜂 ⚙️**\n\n"
        "**❖ ʙᴀɴᴀʟʟ ᴊᴀsᴛ ᴀ ᴍᴀɢɪᴄ ʙᴀʙʏ**\n"
        "**❖ ᴜɴʙᴀɴᴀʟʟ (ʀᴇᴄᴏᴠᴇʀʏ ᴍᴏᴅᴇ)**\n"
        "**❖ ɪᴅ • ɪɴғᴏ • sᴛᴀᴛs**\n"
        "**❖ ʙʀᴏᴀᴅᴄᴀsᴛ • ʀᴇsᴛᴀʀᴛ • ᴘɪɴɢ**\n\n"
        "**🍀 ᴜʟᴛʀᴀ ғᴀsᴛ | ᴘᴜʀᴇ ɢʜᴏsᴛ👻 ᴍᴏᴅᴇ | ғᴜʟʟ ᴄᴏɴᴛʀᴏʟ**"
    )

def help_ui():
    return (
        "**📜 ᴄᴏᴍᴍᴀɴᴅ ᴍᴇɴᴜ**\n\n"
        "**❖ /banall  —  ғᴜʟʟ ᴍᴀss ʙᴀɴ**\n"
        "**❖ /unbanall  —  ᴀʟʟ ᴍᴇᴍʙᴇʀs ᴜɴʙᴀɴ**\n"
        "**❖ /id  —  ᴜsᴇʀ/ᴄʜᴀᴛ ɪᴅ**\n"
        "**❖ /info  —  ᴘʀᴏғɪʟᴇ ɪɴғᴏ**\n"
        "**❖ /stats  —  ᴅᴀᴛᴀʙᴀsᴇ ᴄᴏᴜɴᴛ**\n"
        "**❖ /ping  —  sᴇʀᴠᴇʀ ʟᴀᴛᴇɴᴄʏ**\n"
        "**❖ /broadcast  —  ᴍᴇssᴀɢᴇ ᴘᴜsʜ (ᴏᴡɴᴇʀ)**\n"
        "**❖ /restart  —  ʙᴏᴛ ʀᴇʙᴏᴏᴛ (ᴏᴡɴᴇʀ)**\n"
        "**❖ /update  —  sʏsᴛᴇᴍ sᴛᴀᴛᴜs (ᴏᴡɴᴇʀ)**"
    )
    
# ================= BUTTONS =================
async def start_buttons():
    me = await app.get_me()
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", url=f"https://t.me/{me.username}?startgroup=true")],
        [
            InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f"https://t.me/KaRn_Xd"),
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/BOTMINE_SUPPORT")
        ],
        [InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="help_menu")]
    ])

help_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_home")]
])

# ================= START =================
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await save_user(message.from_user)
    if message.chat.type in (enums.ChatType.SUPERGROUP, enums.ChatType.GROUP):
        await save_group(message.chat)

    btn = await start_buttons()
    await message.reply_photo(
        START_IMG,
        caption=start_ui(message.from_user.mention),
        reply_markup=btn
    )

@app.on_callback_query(filters.regex("help_menu"))
async def help_cb(_, q: CallbackQuery):
    await q.message.edit_caption(help_ui(), reply_markup=help_buttons)

@app.on_callback_query(filters.regex("back_home"))
async def back_cb(_, q: CallbackQuery):
    btn = await start_buttons()
    await q.message.edit_caption(start_ui(q.from_user.mention), reply_markup=btn)

# ================= BAN ENGINE =================
async def ban_worker(chat_id, uid):
    async with SEMAPHORE:
        while True:
            try:
                await app.ban_chat_member(chat_id, uid)
                return True
            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except UserAdminInvalid:
                return False
            except:
                return False

@app.on_message(filters.command("banall") & filters.group)
async def banall_cmd(_, msg):
    chat_id = msg.chat.id
    try:
        await msg.delete()    
    except:
        pass

    tasks = []
    async for m in app.get_chat_members(chat_id):
        if m.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            continue
        tasks.append(asyncio.create_task(ban_worker(chat_id, m.user.id)))

    if tasks:
        await asyncio.gather(*tasks)
    # no reply, no logs, no trace

# ================= UNBAN =================
@app.on_message(filters.command("unbanall") & filters.group)
async def unban_cmd(_, msg):
    status = await msg.reply("unbanning…")
    count = 0

    async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.BANNED):
        try:
            await app.unban_chat_member(msg.chat.id, m.user.id)
            count += 1
        except:
            pass

    await status.edit(f"unbanned {count}")

# ================= ID =================
@app.on_message(filters.command("id"))
async def id_cmd(_, msg):
    if msg.reply_to_message:
        target = msg.reply_to_message.from_user
        return await msg.reply(
            f"🆔 ᴜsᴇʀ ɪᴅ: {target.id}"
        )

    await msg.reply(
        f"🆔 ʏᴏᴜʀ ɪᴅ: {msg.from_user.id}\n💬 ᴄʜᴀᴛ ɪᴅ: {msg.chat.id}"
    )

# ================= INFO =================
@app.on_message(filters.command("info"))
async def info_cmd(_, msg):
    u = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user

    username = f"@{u.username}" if u.username else "None"

    await msg.reply(
        f"👤 ɴᴀᴍᴇ: {u.first_name}\n"
        f"🆔 ɪᴅ: {u.id}\n"
        f"🏷 ᴜsᴇʀɴᴀᴍᴇ: {username}"
    )
# ================= STATS =================
@app.on_message(filters.command("stats"))
async def stats_cmd(_, msg):
    users = users_db.count_documents({})
    groups = groups_db.count_documents({})

    await msg.reply(
        f"📊 ᴍᴏɴɢᴏ sᴛᴀᴛs\n"
        f"👤 ᴜsᴇʀs: {users}\n"
        f"👥 ɢʀᴏᴜᴘs: {groups}"
    )

# ================= BROADCAST =================
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def bc_cmd(_, msg):
    if not msg.reply_to_message:
        return await msg.reply("Reply to any message to broadcast.")

    sent = 0
    failed = 0

    for u in users_db.find({}, {"_id": 1}):
        try:
            await msg.reply_to_message.copy(u["_id"])
            sent += 1
        except:
            failed += 1
        await asyncio.sleep(0.03)  # anti spam

    await msg.reply(
        f"📣 ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇ\n"
        f"✅ sᴇɴᴛ: {sent}\n"
        f"❌ ғᴀɪʟᴇᴅ: {failed}"
    ) 
# ========================= RESTART =========================
@app.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart_cmd(_, msg):
    note = await msg.reply(
        "**♻ Restarting... Please wait**",
        quote=True,
        disable_web_page_preview=True
    )
    
    # delete command message too (ghost mode)
    try:
        await msg.delete()
    except:
        pass

    await asyncio.sleep(1.5)  # smooth exit, prevents crash logs
    os.execv(sys.executable, ["python3"] + sys.argv)

# ========================= UPDATE =========================
@app.on_message(filters.command("update") & filters.user(OWNER_ID))
async def update_cmd(_, msg):
    uptime = int(time.time() - psutil.boot_time())
    h = uptime // 3600
    m = (uptime % 3600) // 60

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    text = (
        "<b>📡 sʏsᴛᴇᴍ ᴜᴘᴅᴀᴛᴇ sᴛᴀᴛᴜs</b>\n\n"
        f"<b>🕒 ᴜᴘᴛɪᴍᴇ:</b> <code>{h}ʜ {m}ᴍ</code>\n"
        f"<b>⚙ ᴄᴘᴜ ʟᴏᴀᴅ:</b> <code>{cpu}%</code>\n"
        f"<b>💾 ʀᴀᴍ ᴜsᴀɢᴇ:</b> <code>{ram}%</code>\n"
        f"<b>🗄 ᴅɪsᴋ:</b> <code>{disk}%</code>\n\n"
        f"<b>📍 ᴘʏᴛʜᴏɴ:</b> <code>{platform.python_version()}</code>\n"
        f"<b>🤖 ʙᴏᴛ ᴠᴇʀsɪᴏɴ:</b> <code>ᴜʟᴛʀᴀ ʙᴀɴ ᴇɴɢɪɴᴇ</code>\n"
        f"<b>💠 ᴘʟᴀᴛғᴏʀᴍ:</b> <code>{platform.system()}</code>\n\n"
        "<b>🛠 ᴀʟʟ sʏsᴛᴇᴍs ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ</b>"
    )

    await msg.reply(text, disable_web_page_preview=True)


# ========================= PING =========================
@app.on_message(filters.command("ping"))
async def ping_cmd(_, msg):
    start = time.time()
    pong = await msg.reply("Pinging…")
    end = time.time()

    latency = round((end - start) * 1000)

    text = (
        "<b>🏓 ᴘɪɴɢ ʀᴇsᴘᴏɴsᴇ</b>\n\n"
        f"<b>⚡ ʟᴀᴛᴇɴᴄʏ:</b> <code>{latency} ᴍs</code>\n"
        "<b>📡 sʏsᴛᴇᴍ sᴛᴀᴛᴜs:</b> ᴏᴘᴇʀᴀᴛɪᴏɴᴀʟ"
    )

    await pong.edit(text)
# ================= RUN =================
print("🔥 BANALL RUNNING…")
app.run()

# © 2025 — Powered by @BOTMINE_TECH & @TheShreeTech
