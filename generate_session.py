import asyncio
from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

async def generate():
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    
    if not api_id or not api_hash:
        print("Ошибка: Сначала заполни TELEGRAM_API_ID и TELEGRAM_API_HASH в .env")
        return

    async with Client(":memory:", api_id=api_id, api_hash=api_hash) as app:
        session_string = await app.export_session_string()
        print("\n" + "="*50)
        print("ТВОЯ СЕССИЯ (СКОПИРУЙ ЭТО):")
        print("="*50)
        print(session_string)
        print("="*50)
        print("\nВставь эту длинную строку в .env в переменную TELEGRAM_SESSION_STRING")

if __name__ == "__main__":
    asyncio.run(generate())
