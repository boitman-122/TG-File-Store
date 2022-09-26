import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from database.database import *
from config import *


@Client.on_message(filters.private & filters.incoming)
async def forcesub(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "banned":
               await m.reply_text("**Hey you are banned 😜**", quote=True)
               return
        except UserNotParticipant:
            buttons = [[InlineKeyboardButton(text='Updates Channel 🔖', url=f"https://t.me/{UPDATE_CHANNEL}")]]
            if m.text:
                if (len(m.text.split()) > 1) & ('start' in m.text):
                    buttons.append([InlineKeyboardButton('🔄 Refresh', callback_data=f'refresh+{m.text.split()[1]}')])
            text = f"""Hello {m.from_user.mention()}
ಈ ಬಾಟ್ ಅನ್ನು ಬಳಸಲು ದಯವಿಟ್ಟು ನನ್ನ ಮುಕ್ಯ ಚಾನಲ್‌ಗೆ ಸೇರಿ!

ಓವರ್‌ಲೋಡ್‌ನಿಂದಾಗಿ, ಚಾನೆಲ್ ಚಂದಾದಾರರು ಮಾತ್ರ ಬಾಟ್ ಅನ್ನು ಬಳಸಬಹುದು!

Please Join My Updates Channel to use this Bot!

Due to Overload, Only Channel Subscribers can use the Bot!
You need to join in my Channel/Group to use me

Kindly Please join Channel"""
            await m.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(buttons),
                quote=True
            )
            return
        except Exception as e:
            print(e)
            await m.reply_text(f"Something Wrong. Please try again later or contact {owner.mention(style='md')}", quote=True)
            return
    await m.continue_propagation()


from plugins.commands import start
@Client.on_callback_query(filters.regex('^refresh'))
async def refresh_cb(c, m):
    owner = await c.get_users(int(OWNER_ID))
    if UPDATE_CHANNEL:
        try:
            user = await c.get_chat_member(UPDATE_CHANNEL, m.from_user.id)
            if user.status == "banned":
               try:
                   await m.message.edit("**Hey you are banned 😜**")
               except:
                   pass
               return
        except UserNotParticipant:
            await m.answer('You are not yet joined our channel. First join and then press refresh button 🤤', show_alert=True)
            return
        except Exception as e:
            print(e)
            await m.message.edit(f"Something Wrong. Please try again later or contact {owner.mention(style='md')}")
            return

    cmd, data = m.data.split("+")
    m = m.reply_to_message 
    await start(c, m)
