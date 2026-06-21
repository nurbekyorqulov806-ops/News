
import requests
from bs4 import BeautifulSoup
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re

TOKEN = "8965922679:AAG8ClUfuy85HHF2gtQ8UIjpxlSWGFD87Bk"

BTN_LATEST = "🕐 So'nggi yangiliklar"
BTN_WORLD = "🌍 Jahon yangiliklari"
BTN_UZ = "🇺🇿 O'zbekiston yangiliklari"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

DATE_PATTERN = re.compile(
    r"(Bugun|Kecha|\d{1,2}:\d{2}\s*/\s*\d{2}\.\d{2}\.\d{4})", re.IGNORECASE
)


def fetch_page_news(url: str):
    """Bitta sahifadan (sarlavha, link) juftliklarini qaytaradi."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    items = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_text = link.get_text(separator=" ", strip=True)

        if "/20" not in href:
            continue
        if not DATE_PATTERN.search(full_text):
            continue

        title = DATE_PATTERN.split(full_text)[0].strip()
        if len(title) < 10:
            continue

        full_url = href if href.startswith("http") else f"https://daryo.uz{href}"
        items.append((title, full_url))

    return items


def get_latest_mixed(limit: int = 10):
    """So'nggi yangiliklar: aralash (o'z + jahon), vaqt tartibida, sahifalashsiz."""
    items = fetch_page_news("https://daryo.uz/news/list")

    seen = set()
    result = []
    for title, url in items:
        if url not in seen:
            seen.add(url)
            result.append((title, url))
        if len(result) >= limit:
            break
    return result


def get_top_news(base_url: str, pages: int = 3, limit: int = 10):
    """Bir nechta sahifadan yig'ib, sarlavha uzunligi bo'yicha 'muhim' 10 tani tanlaydi."""
    all_items = []
    seen = set()

    for page in range(1, pages + 1):
        url = base_url if page == 1 else f"{base_url}?page={page}"
        page_items = fetch_page_news(url)

        for title, link in page_items:
            if link not in seen:
                seen.add(link)
                all_items.append((title, link))

    # Sarlavha uzunligi bo'yicha kamayish tartibida saralash (uzunroq = ko'pincha muhimroq/batafsilroq)
    all_items.sort(key=lambda x: len(x[0]), reverse=True)

    return all_items[:limit]


def format_news(news_list):
    if not news_list:
        return ["Hozircha yangilik topilmadi. Sayt strukturasi o'zgargan bo'lishi mumkin."]
    return [f"📰 {title}\n{url}" for title, url in news_list]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [BTN_LATEST],
        [BTN_WORLD, BTN_UZ],
    ]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Salom! Qaysi yangiliklarni ko'rmoqchisiz?",
        reply_markup=markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text not in (BTN_LATEST, BTN_WORLD, BTN_UZ):
        await update.message.reply_text("Iltimos, pastdagi tugmalardan birini tanlang 👇")
        return

    await update.message.reply_text("Yuklanmoqda... ⏳")

    if text == BTN_LATEST:
        news_items = get_latest_mixed(limit=10)
    elif text == BTN_WORLD:
        news_items = get_top_news("https://daryo.uz/category/dunyo", pages=3, limit=10)
    else:  # BTN_UZ
        news_items = get_top_news("https://daryo.uz/category/uzbekistan", pages=3, limit=10)

    for item in format_news(news_items):
        await update.message.reply_text(item, disable_web_page_preview=False)


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")
app.run_polling()