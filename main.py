import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, POLL_INTERVAL_SECONDS, check_config
from fetcher import fetch_latest_bitcoin_news
from processor import process_news_item

logging.basicConfig(level=logging.INFO)

if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "твой_телеграм_бот_токен":
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
else:
    bot = None

dp = Dispatcher()
seen_news_ids = set()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет! Я Бот для поиска важных новостей о Биткоине.\n"
        f"Твой chat_id: {message.chat.id}\n"
        f"Скопируй этот chat_id и вставь его в файл .env в переменную TELEGRAM_CHAT_ID, если еще не сделал этого!"
    )

async def news_polling():
    """Фоновая задача для периодической проверки новостей."""
    logging.info("Начинаю фоновый мониторинг новостей...")
    while True:
        try:
            news_items = await fetch_latest_bitcoin_news()
            
            # Проходим по новостям (сначала старые в полученном списке)
            for item in reversed(news_items):
                news_id = item.get("id")
                if news_id in seen_news_ids:
                    continue
                    
                title = item.get("title", "")
                url = item.get("url", "")
                
                logging.info(f"Найдена новая новость: {title}")
                
                # Обработка через ИИ
                tweet_text = await process_news_item(title)
                
                if tweet_text:
                    message_text = f"{tweet_text}\n\nИсточник: {url}"
                    try:
                        if TELEGRAM_CHAT_ID and TELEGRAM_CHAT_ID != "твой_айди_чата_для_получения_новостей":
                            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_text)
                            logging.info("Сообщение успешно отправлено в Telegram!")
                        else:
                            logging.warning("TELEGRAM_CHAT_ID не настроен, сообщение не отправлено.")
                    except Exception as e:
                        logging.error(f"Ошибка при отправке в телеграм: {e}")

                seen_news_ids.add(news_id)
                await asyncio.sleep(2) # Избегаем спама API OpenAI
                
        except Exception as e:
            logging.error(f"Глобальная ошибка в фоне: {e}")
            
        await asyncio.sleep(POLL_INTERVAL_SECONDS)

async def main():
    try:
        check_config()
    except ValueError as e:
        logging.error(e)
        logging.info("Пожалуйста, заполни файл .env реальными ключами.")
        return

    if not bot:
        logging.error("Не инициализирован Telegram Bot (выполни настройку ключей).")
        return

    # Запускаем поллинг новостей в фоне
    asyncio.create_task(news_polling())
    logging.info("Telegram бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
