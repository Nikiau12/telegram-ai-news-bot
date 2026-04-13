import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, AI_BOT_INBOX_ID, check_config
from processor import process_news_item

logging.basicConfig(level=logging.INFO)

if TELEGRAM_BOT_TOKEN:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
else:
    bot = None

dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет! Я Бот-Процессор.\n"
        f"ID этого чата: `{message.chat.id}`\n"
        f"Вставь этот ID в `AI_BOT_INBOX_ID` в .env, чтобы я слушал новости здесь."
    )

@dp.message()
async def handle_raw_news(message: types.Message):
    """Обработка входящего текста новости от Юзербота."""
    # Проверяем, что сообщение пришло из нужного инбокса
    if str(message.chat.id) != str(AI_BOT_INBOX_ID):
        return

    text = message.text or message.caption
    if not text:
        return

    logging.info("Получена порция сырых новостей от Юзербота...")
    
    # Разделяем порцию на отдельные новости
    lines = text.split('\n')
    for line in lines:
        if not line.strip() or "http" not in line:
            continue

        logging.info(f"Анализирую: {line[:50]}...")
        
        # ИИ Обработка
        tweet_text = await process_news_item(line)
        
        if tweet_text:
            try:
                # Отправляем в финальный канал
                await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=tweet_text)
                logging.info("Готовое саммари отправлено в канал!")
            except Exception as e:
                logging.error(f"Ошибка при отправке в канал: {e}")
        
        await asyncio.sleep(1) # Небольшая пауза между запросами к ИИ

async def main():
    try:
        check_config()
    except ValueError as e:
        logging.error(e)
        logging.info("Пожалуйста, заполни файл .env.")
        return

    if not bot:
        logging.error("Не настроен TELEGRAM_BOT_TOKEN.")
        return

    logging.info("AI Бот-Процессор запущен и ждет новостей в инбоксе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
