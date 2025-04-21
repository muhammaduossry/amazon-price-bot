import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRODUCT_URL = os.getenv("PRODUCT_URL")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

last_price = None
bot = Bot(token=TELEGRAM_TOKEN)

def get_price():
    res = requests.get(PRODUCT_URL, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")
    price_span = soup.select_one("span.a-price > span.a-offscreen")
    if not price_span:
        return None
    return float(price_span.text.replace("ج.م", "").replace(",", "").strip())

async def monitor_price():
    global last_price
    while True:
        try:
            price = get_price()
            if price is None:
                print("مش لاقي السعر")
            elif price != last_price:
                await bot.send_message(chat_id=CHAT_ID, text=f"📢 السعر اتغير!\nالسعر الجديد: {price} ج.م\n{PRODUCT_URL}")
                last_price = price
            else:
                print(f"السعر ثابت: {price}")
        except Exception as e:
            print("مشكلة:", e)
        await asyncio.sleep(1800)

if __name__ == "__main__":
    asyncio.run(monitor_price())