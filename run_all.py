import asyncio
import logging
from main import main as run_processor
from userbot import main as run_fetcher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Runner")

async def start_all():
    logger.info("Запуск всей системы (Сборщик + Аналитик)...")
    # Запускаем обоих ботов параллельно
    await asyncio.gather(
        run_processor(),
        run_fetcher()
    )

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        logger.info("Система остановлена пользователем.")
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске: {e}")
