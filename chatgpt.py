

# Bu bot telegramda ai dan foydalanish imkoniyatini beradi.
# Bu bot faqatgina xabarlaringizda Nurbek so'zini ko'rsagina ushbu gapni oladi va ai ga yuboradi,
# ai esa bunga mos javob qaytarishga harakat qiladi.Buni istalgan guruhga admin sifatida qo'shishingiz mumkin.
# Bu bot guruhdagi insonlar yozuviga ham men Nurbekning aqlli yordamchisiman deb javob qaytara oladi.
# IStalgan savolni bersangiz jacob berishi mumkin faqat Nurbek so'zi albatta qatnashishi lozim!!!





import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
import google.generativeai as genai

# --- SOZLAMALAR ---
TELEGRAM_TOKEN="8739642193:AAGBB7upaVV-pC8HGkRvsU_DqwSgbbNQqPA"
GEMINI_API_KEY="AIzaSyCAjN3OaFgFValwapPcAsWON2ibwBxs1FI"

# Gemini-ni sozlash 
genai.configure(api_key=GEMINI_API_KEY)

# Model sozlamalari
generation_config={
  "temperature":0.9, 
  "top_p":1,
  "top_k":1,
  "max_output_tokens":2048,
}

model=genai.GenerativeModel(
  model_name="gemini-2.5-flash-lite",
  generation_config=generation_config,
  system_instruction="Sen Nurbekning aqlli va do'stona yordamchisisan. Guruhda kimdir 'Nurbek' deb yozsa, ularga qisqa, aqlli va biroz hazil aralash javob ber,agar savol berilsa to'g'ri javob ber. O'zbek tilida gaplash."
)

# Bot va Dispatcher
bot=Bot(token=TELEGRAM_TOKEN)
dp=Dispatcher()

logging.basicConfig(level=logging.INFO)



# XABARLARNI QAYTA ISHLASH 

@dp.message(F.text.lower().contains("nurbek"))
async def nurbek_handler(message: types.Message):
    try:
        await bot.send_chat_action(chat_id=message.chat.id,action="typing")
        
        # AI-dan javob olish
        response=model.generate_content(message.text)
        
        if response.text:
            await message.reply(response.text)
        else:
            await message.reply("AI hozircha jim...")

    except Exception as e:
        logging.error(f"Xato yuz berdi:{e}")
        # Agar bu yerda 404 chiqsa, hududiy cheklov
        await message.answer(f"Xatolik: {str(e)}")

async def main():
    print("Bot ishga tushdi (Stabil versiya)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")

