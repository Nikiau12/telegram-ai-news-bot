from openai import AsyncOpenAI
from config import OPENAI_API_KEY

if OPENAI_API_KEY and OPENAI_API_KEY != "твой_ключ_openai":
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

SYSTEM_PROMPT = """
Ты — профессиональный крипто-аналитик и автор в Twitter с огромной аудиторией.
Тебе на вход дается заголовок новости про Биткоин. 
Твоя задача — решить, является ли эта новость ВАЖНОЙ для аудитории, которая следит за курсом BTC. 
Если новость — мусор (реклама, старые новости, незначительные колебания, мелкие скандалы), ответь ровно одним словом: SKIP.
Если новость действительно важная (институциональные покупки, макроэкономика США, законы, ETF, технические прорывы), напиши ОДИН красивый, короткий и вовлекающий твит на русском языке. 
Используй 1-2 эмодзи. Добавь хэштег #Bitcoin. Не пиши больше никаких вводных слов, только сам текст твита!
"""

async def process_news_item(news_title):
    """
    Передает заголовок новости в OpenAI. Возвращает готовый твит или None.
    """
    if not client:
        return None

    try:
        completion = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Новость: {news_title}"}
            ],
            temperature=0.7
        )
        
        result = completion.choices[0].message.content.strip()
        
        # Если ИИ решил, что новость мусорная
        if result.upper().startswith("SKIP"):
            return None
            
        return result
    except Exception as e:
        print(f"Ошибка при работе с OpenAI: {e}")
        return None
