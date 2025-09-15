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
from aiogram.filters import Command

# === Обработчик команды /add ===
@dp.message(Command("add"))
async def add_trigger(message: Message):
    args = message.text.split(maxsplit=2)
    
    if len(args) < 3:
        await message.reply("❌ Используй формат:\n/add триггер ответ")
        return

    keyword = args[1].lower()
    response = args[2]

    try:
        with open(TRIGGERS_FILE, "r+", encoding="utf-8") as f:
            data = json.load(f)
            if keyword in data:
                data[keyword].append(response)
            else:
                data[keyword] = [response]

            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.truncate()

        await message.reply(f"✅ Добавлено:\nКлюч: <b>{keyword}</b>\nОтвет: <i>{response}</i>")

    except Exception as e:
        await message.reply(f"❌ Ошибка при сохранении: {e}")
# === Обработчик всех сообщений ===
@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return

    text = message.text.lower()
    triggers = load_triggers()

    for keyword, responses in triggers.items():
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            await message.reply(f"Филипп Киркоряныч: {responses[0]}")
            break

# === Точка входа ===
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())