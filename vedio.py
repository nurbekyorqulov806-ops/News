
import asyncio
import os
import yt_dlp

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import CommandStart

TOKEN = "8632656609:AAHsLxm4JAJOM5dG_pt_rVnkMkGkzLsAAPM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_links = {}


# START
@dp.message(CommandStart())
async def start(message: Message):
    text = """
Assalomu alaykum. Men video yuklovchi botman.

Link yuboring:
- TikTok
- YouTube
- Shorts
- Instagram Reel
"""
    await message.answer(text)


# LINK
@dp.message(F.text)
async def get_link(message: Message):

    url = message.text.strip()

    if "http" not in url:
        return

    user_links[message.from_user.id] = url

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ FAST", callback_data="fast"),
                InlineKeyboardButton(text="🔥 HD", callback_data="hd")
            ],
            [
                InlineKeyboardButton(text="🎵 MUSIC", callback_data="music"),
                InlineKeyboardButton(text="🔥 TREND", callback_data="trend")
            ]
        ]
    )

    await message.answer("Nimani qilamiz?", reply_markup=keyboard)


# TREND
def get_trending():
    return [
        "🔥 TikTok Dance Trend",
        "🔥 Funny Video Trend",
        "🔥 Music Remix Trend",
        "🔥 Viral Challenge"
    ]


# DOWNLOAD
def download(url, mode):

    if mode == "fast":
        fmt = "worst[ext=mp4]/best[height<=360]"

    elif mode == "hd":
        fmt = "best[height<=480]/best"

    ydl_opts = {
        "format": fmt,
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "concurrent_fragment_downloads": 3
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename, info


# CALLBACK
@dp.callback_query(F.data.in_(["fast", "hd", "music", "trend"]))
async def process(callback: CallbackQuery):

    user_id = callback.from_user.id
    url = user_links.get(user_id)

    if not url:
        await callback.message.answer("Link topilmadi")
        await callback.answer()
        return

    await callback.message.answer("⏳ Yuklanmoqda...")

    # 🔥 TREND
    if callback.data == "trend":
        await callback.message.answer("\n".join(get_trending()))
        await callback.answer()
        return

    # 🎵 MUSIC
    if callback.data == "music":

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        title = info.get("title", "Noma'lum")
        uploader = info.get("uploader", "Noma'lum")

        audio = FSInputFile(filename)

        await callback.message.answer_audio(
            audio,
            caption=f"🎵 {title}\n👤 {uploader}"
        )

        os.remove(filename)
        await callback.answer()
        return

    # 📹 VIDEO (FAST / HD)
    file, info = download(url, callback.data)

    video = FSInputFile(file)

    await callback.message.answer_video(
        video,
        caption=f"📹 {info.get('title')}"
    )

    os.remove(file)

    await callback.answer()


# RUN
async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())





