# main.py

import asyncio
import json
import re
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties  # 💡 новый импорт

# === Настройки ===
BOT_TOKEN = "8292751440:AAG89FGJxkcVQ3tHWBPlTbDyBSRnr-IXpcc"
TRIGGERS_FILE = "triggers.json"

# === Инициализация бота с новым способом задания parse_mode ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # 💡 вот так теперь
)
dp = Dispatcher()

# === Загрузка триггеров ===
def load_triggers():
    try:
        with open(TRIGGERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# === Обработчик всех сообщений ===
@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return

    text = message.text.lower()
    triggers = load_triggers()

    for keyword, responses in triggers.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            await message.reply(f"Филипп Киркорян: {responses[0]}")
            break

# === Точка входа ===
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())