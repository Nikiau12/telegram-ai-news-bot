import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Telegram Userbot (Fetcher)
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_SESSION_STRING = os.getenv("TELEGRAM_SESSION_STRING")

# Telegram AI Bot (Processor)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") # Final destination channel
AI_BOT_INBOX_ID = os.getenv("AI_BOT_INBOX_ID") # Chat for raw news

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Настройки поиска и бота
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", 300))
SEARCH_KEYWORDS = ["Bitcoin", "BTC", "биткоин"]

def check_config():
    """Проверяет наличие всех необходимых ключей."""
    missing = []
    if not TELEGRAM_API_ID: missing.append("TELEGRAM_API_ID")
    if not TELEGRAM_API_HASH: missing.append("TELEGRAM_API_HASH")
    if not TELEGRAM_BOT_TOKEN: missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID: missing.append("TELEGRAM_CHAT_ID")
    if not AI_BOT_INBOX_ID: missing.append("AI_BOT_INBOX_ID")
    if not OPENAI_API_KEY: missing.append("OPENAI_API_KEY")

    if missing:
        raise ValueError(f"Отсутствуют необходимые переменные окружения: {', '.join(missing)}")
    return True
