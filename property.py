from asyncio import run

from pymysql import IntegrityError
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery,ReplyKeyboardMarkup,KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command, StateFilter

from db2 import db


TOKEN="8622559912:AAE6QTGQCkIkShTnwBd3-XlLdrIy7piiaEQ"

bot=Bot(token=TOKEN)
dp=Dispatcher()
# ================= STATES =================

class UserState(StatesGroup):
    waiting_for_address=State()
    waiting_for_choise1=State()
    waiting_for_rooms=State()
    waiting_for_choise2=State()
    waiting_for_cost=State()



# ================= KEYBOARDS =================


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/add_datas")],
        [KeyboardButton(text="/saved_datas")],
        [KeyboardButton(text="/delete_datas")],
    ],
    resize_keyboard=True
)


add_datas_keyboard=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/Ma'lumotlarni to'ldirish")],
        [KeyboardButton(text="⬅️ Orqaga")],
    ],
    resize_keyboard=True
)








@dp.message(CommandStart())
async def start(message:Message):
    chat_id=message.from_user.id
    full_name=message.from_user.full_name

    await message.answer(
        text=f"Assalomu alaykum {full_name} 😊",
        reply_markup=keyboard)

    try:
        db.register_user(
            telegram_id=str(chat_id),
            fullname=full_name,
        )
        await message.answer(text="✅Muvaffaqiyatli ro'yxatga olindingiz")
    except IntegrityError:
        await message.answer(text="Qaytganingizdan xursandmiz")







@dp.message(Command(commands=["add_datas"],prefix="/"),)
async def datas(message):
    await message.answer(
        "Iltimos,barcha kategoriyalarni to'ldiring:",
        reply_markup=add_datas_keyboard
        )





    
@dp.message(lambda message:message.text=="/saved_datas")
async def showed_saved_data(message:Message):
    user_id=message.from_user.id

    datas=db.get_user_orders(user_id=user_id)

    if not datas:
        await message.answer(text="Sizda hali malumot mavjud emas")
        return
    

    Matn="Sizning saqlangan malumotlaringiz:\n\n"
    for index,d in enumerate(datas,1):
        Matn+=(
            f"{index}.\n\n"
            f"🗺️ Manzil: {d['address']}\n\n"
            f"🏠 Kvartira|Hovli: {d['choise1']}\n\n"
            f"🏙️ Xonalar soni: {d['rooms']}\n\n"
            f"🏠 Sotuvga|Ijaraga: {d['choise2']}\n\n"
            f"💲 Narxi: {d['cost']}\n\n")
    await message.answer(text=Matn)





@dp.message(Command(commands=["delete_datas"], prefix="/"))
async def delete_account(message: Message):
    user_id= message.from_user.id
    db.delete_user(user_id=user_id)
    await message.answer(
        text="Akkauntingiz ma'lumotlari muvaffaqiyatli o'chirildi"
    )








# ================= START FORM =================
@dp.message(lambda message: message.text == "/Ma'lumotlarni to'ldirish")
async def start_form(message: Message, state: FSMContext):
    await message.answer("Manzilni kiriting:")
    await state.set_state(UserState.waiting_for_address)

# ================= ADDRESS =================
@dp.message(UserState.waiting_for_address)
async def address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Kvartira/Hovli?")
    await state.set_state(UserState.waiting_for_choise1)


# ================= CHOISE1 =================
@dp.message(UserState.waiting_for_choise1)
async def choise1(message: Message, state: FSMContext):
    await state.update_data(choise1=message.text)
    await message.answer("Xonalar soni?")
    await state.set_state(UserState.waiting_for_rooms)


# ================= ROOMS =================
@dp.message(UserState.waiting_for_rooms)
async def rooms(message: Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await message.answer("Sotuv/Ijara?")
    await state.set_state(UserState.waiting_for_choise2)


# ================= CHOISE2 =================
@dp.message(UserState.waiting_for_choise2)
async def choise2(message: Message, state: FSMContext):
    await state.update_data(choise2=message.text)
    await message.answer("Narx?")
    await state.set_state(UserState.waiting_for_cost)


# ================= COST + SAVE =================
@dp.message(UserState.waiting_for_cost)
async def cost(message: Message, state: FSMContext):
    await state.update_data(cost=message.text)






    inline_markup=InlineKeyboardBuilder()
    inline_markup.button(text="Saqlab qo'yilsin",callback_data="save_to_db2")

    await message.answer(text="Malumotlarni saqlab qo'ymoqchimisiz?",reply_markup=inline_markup.as_markup())







@dp.message(lambda m: m.text == "⬅️ Orqaga")
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=keyboard)




@dp.callback_query(lambda call:call.data=="save_to_db2")
async def save_data_callback(call:CallbackQuery,state:FSMContext):
    data = await state.get_data()

    if not data:
        await call.message.answer("❗Ma'lumot topilmadi")
        return

    db.add_datas1(
        user_id=call.from_user.id,
        address=data["address"],
        choise1=data["choise1"],
        rooms=data["rooms"],
        choise2=data["choise2"],
        cost=data["cost"]
    )


    await call.message.answer(text="✅Muvaffaqiyatli saqlandi",reply_markup=keyboard)


    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    await call.answer()




@dp.message()
async def handler(message:Message,state: FSMContext):

    if message.text=="Uy manzili":
        await message.answer("Uy manzilini kiriting:")
        await state.set_state(UserState.waiting_for_address)

    elif message.text=="Kvartira/Hovli":
        await message.answer("Kvartirami yoki hovli")
        await state.set_state(UserState.waiting_for_choise1)

    elif message.text == "Xonalar soni":
        await message.answer("Xonalari soni nechta:")
        await state.set_state(UserState.waiting_for_rooms)

    elif message.text == "Sotuv/Ijara":
        await message.answer("Sotuvga yoki Ijaraga:")
        await state.set_state(UserState.waiting_for_choise2)

    elif message.text == "Narx":
        await message.answer("Narxi qancha")
        await state.set_state(UserState.waiting_for_cost)

@dp.message()
async def unknown_message(message: Message):
    await message.answer("❗Noma'lum xabar")







async def main():
    # Botni ishga tushirovchi funksiya
    db.create_users_table()
    db.create_address_table()
    await dp.start_polling(bot)

run( main() )


