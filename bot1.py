
from asyncio import run
from aiogram import Bot,Dispatcher
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,Message



TOKEN="8796230754:AAHOw_Dz7Vmpuish4DHdBtqZsx2iM_GxeXE"


bot=Bot(token=TOKEN)
dp=Dispatcher()




keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/help"),KeyboardButton(text="/info")],
        [KeyboardButton(text="/kinolar")]
    ],
    resize_keyboard=True
)

kinolar_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Merlin")],
        [KeyboardButton(text="Qasoskorlar")],
        [KeyboardButton(text="Spider man")]
    ],
    resize_keyboard=True
)



@dp.message(Command(commands=["start"],prefix="/"))
async def say_hello(message:Message):
    chat_id=message.from_user.id
    full_name=message.from_user.full_name

    await bot.send_message(
        chat_id=chat_id,
        text=f"Assalomu alaykum,{full_name}!",
        reply_markup=keyboard
    )



@dp.message(Command(commands=["help"],prefix="/"))
async def help(message):
    chat_id=message.from_user.id
    full_name=message.from_user.full_name

    await bot.send_message(
        chat_id=chat_id,
        text=f"Siz yordam olish buyrug'ini kiritdingiz,{full_name}",
        reply_markup=keyboard
    )





@dp.message(Command(commands=["info"],prefix="/"))
async def info(message):
    chat_id=message.from_user.id
    full_name=message.from_user.full_name

    await bot.send_message(
        chat_id=chat_id,
        text=f"Siz ma'lumot olish buyrug'ini kiritdingiz,{full_name}",
        reply_markup=keyboard
    )




@dp.message(Command(commands=["kinolar"],prefix="/"))
async def movies(message):
    await message.answer(
        "Qaysi kinoni tanlaysiz:",
        reply_markup=kinolar_keyboard
        )



@dp.message()
async def get_file_id(message):
    if message.video:
        await message.answer(message.video.file_id)
        return
    text=message.text.strip()

    if text=="Merlin":
        await message.answer_video(
            video="BAACAgIAAxkBAAMwafc-pjB_xnVefEIEbxRs8aBhWjkAAkeeAALckrhLsYzkdazzq347BA",
            caption="Merlin"
        )
    

    elif text=="Qasoskorlar":
        await message.answer_video(
            video="BAACAgIAAxkBAAMzafc_jW4aftYlwiTP2T9uqH2YHYcAAk6eAALckrhL7WoM5WpTa7A7BA",
            caption="Qasoskorlar"
        )


    elif text=="Spider man":
        await message.answer_video(
            video="BAACAgIAAxkBAAN3afmtS93xkgllJhiduAxZ-d8SzRsAAkSeAAJcFshLeal_7ONuWTU7BA",
            caption="Spider man"
        )


async def main():
    await dp.start_polling(bot)


run(main())





