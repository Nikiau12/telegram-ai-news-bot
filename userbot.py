import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHAT_ID, POLL_INTERVAL_SECONDS
from processor import process_news_item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Имя сессии для сохранения входа
app = Client("my_account", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)

# Хранилище для последних обработанных новостей (чтобы не дублировать)
processed_titles = set()

async def handle_cryptopanic_news(client, message):
    """Обработка сообщений от CryptoPanic ботa."""
    # Проверяем, что сообщение от нужного бота
    if message.from_user and message.from_user.username == "CryptoPanicBot":
        text = message.text or message.caption
        if not text:
            return

        logger.info("Получено сообщение от CryptoPanicBot")
        
        # Разделяем на строки, обычно бот присылает список новостей
        lines = text.split('\n')
        for line in lines:
            if not line.strip() or "http" not in line:
                continue
            
            # Простейший парсинг: заголовок и ссылка
            # Ожидается формат: "Title http://link"
            if line in processed_titles:
                continue
                
            logger.info(f"Обработка новости: {line[:50]}...")
            
            # Отправляем в ИИ
            tweet_text = await process_news_item(line)
            
            if tweet_text:
                try:
                    # Отправляем результат в целевой чат
                    await client.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=tweet_text)
                    logger.info("Саммари успешно отправлено!")
                except Exception as e:
                    logger.error(f"Ошибка при отправке в чат: {e}")
            
            processed_titles.add(line)
            # Ограничиваем размер кэша
            if len(processed_titles) > 100:
                processed_titles.pop()

async def poll_news_command():
    """Периодическая отправка команды /news боту CryptoPanic."""
    while True:
        try:
            logger.info("Отправка /news боту @CryptoPanicBot...")
            await app.send_message("CryptoPanicBot", "/news")
        except Exception as e:
            logger.error(f"Ошибка при отправке команды боту: {e}")
        
        await asyncio.sleep(POLL_INTERVAL_SECONDS)

async def main():
    async with app:
        logger.info("Юзербот запущен!")
        # Добавляем хендлер для входящих сообщений
        app.add_handler(MessageHandler(handle_cryptopanic_news, filters.chat("CryptoPanicBot")))
        
        # Запускаем фоновую задачу опроса
        asyncio.create_task(poll_news_command())
        
        # Держим клиент запущенным
        await asyncio.Event().wait()

if __name__ == "__main__":
    import os
    if not os.path.exists("my_account.session"):
        logger.info("Первый запуск: тебе нужно будет ввести номер телефона и код подтверждения в терминале.")
    
    app.run(main())
