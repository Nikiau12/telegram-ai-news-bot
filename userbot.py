import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, AI_BOT_INBOX_ID, POLL_INTERVAL_SECONDS, TELEGRAM_SESSION_STRING

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Используем сессию из строки (для деплоя) или файл (локально)
if TELEGRAM_SESSION_STRING:
    app = Client("my_account", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, session_string=TELEGRAM_SESSION_STRING)
else:
    app = Client("my_account", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

async def handle_marketanalyst_news(client, message):
    """Обработка сообщений из канала MarketAnalyst AI и пересылка в инбокс."""
    # Мы следим за всеми сообщениями в этом чате/канале
    text = message.text or message.caption
    if not text:
        return

    logger.info("Найдена новая новость в MarketAnalyst AI, проверяю...")
    
    # Защита от петли: если в сообщении уже есть наш хэштег, значит это работа AI бота
    if "#Bitcoin" in text:
        logger.info("Это уже обработанная новость (найден #Bitcoin), пропускаю.")
        return

    try:
        # Пересылаем текст в инбокс нашего AI бота
        await client.send_message(chat_id=int(AI_BOT_INBOX_ID), text=text)
        logger.info("Raw news переслана успешно!")
    except Exception as e:
        logger.error(f"Ошибка при пересылке в инбокс: {e}")

async def main():
    async with app:
        logger.info("Юзербот-Fetcher запущен! Слежу за каналом MarketAnalystAI...")
        # Добавляем хендлер для входящих сообщений из канала MarketAnalystAI
        app.add_handler(MessageHandler(handle_marketanalyst_news, filters.chat("MarketAnalystAI")))
        
        # Держим клиент запущенным
        await asyncio.Event().wait()

if __name__ == "__main__":
    import os
    if not os.path.exists("my_account.session"):
        logger.info("Первый запуск: тебе нужно будет ввести номер телефона и код подтверждения в терминале.")
    
    app.run(main())
