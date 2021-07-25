from uuid import UUID
import uuid
from services.db import DB
from routes.schema.news import NewsResponseSchema


async def select_news() -> NewsResponseSchema:
    query = """
        select id, topic, main_text, img_link, user_id
        from news
    """
    news = await DB.conn.fetch(query)

    return {'news': news}


async def post_news(main_text: str, topic: str, user_id: UUID, img_link: str) -> str:
    query = """
        insert into news (id, topic, main_text, img_link, user_id)
        values ($1, $2, $3, $4, $5)
    """
    try:
        await DB.conn.execute(query, uuid.uuid4(), topic, main_text, img_link, user_id)
        return 'The news was successfully added'
    except Exception as e:
        return f'Error: {e}'
