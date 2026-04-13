import aiohttp
import asyncio
from config import CRYPTOPANIC_API_KEY

async def fetch_latest_bitcoin_news():
    """
    Получает последние важные новости про биткоин через CryptoPanic API.
    """
    if not CRYPTOPANIC_API_KEY or CRYPTOPANIC_API_KEY == "твой_ключ_cryptopanic":
        print("CryptoPanic API key не настроен!")
        return []

    # 'filter=important' помогает отсеять часть шума сразу на стороне API
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_API_KEY}&currencies=BTC&filter=important"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("results", [])
                else:
                    print(f"Ошибка при запросе к CryptoPanic: {response.status}")
                    return []
    except Exception as e:
        print(f"Исключение при получении новостей: {e}")
        return []
