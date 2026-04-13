import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Telegram Userbot
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
    if not TELEGRAM_CHAT_ID: missing.append("TELEGRAM_CHAT_ID")
    if not OPENAI_API_KEY: missing.append("OPENAI_API_KEY")

    if missing:
        raise ValueError(f"Отсутствуют необходимые переменные окружения: {', '.join(missing)}")
    return True
