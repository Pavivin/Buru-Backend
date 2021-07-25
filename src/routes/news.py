from fastapi import APIRouter, Request
from fastapi.params import Depends
from queries.news import post_news, select_news
from utils.auth_bearer import JWTBearer
from utils.user_id import id_from_token

from routes.schema.news import NewsRequestSchema, NewsResponseSchema

news_router = APIRouter()


@news_router.get('/feed', response_model=NewsResponseSchema, description='NewsSchema')
async def get_news() -> dict:
    return await select_news()


@news_router.post('/feed', dependencies=[Depends(JWTBearer())], description='NewsSchema')
async def add_news(request: Request, schema: NewsRequestSchema) -> str:
    resp: dict = await request.json()
    user_id = id_from_token(request)
    main_text = resp.get('main_text')
    topic = resp.get('topic')
    img_link = resp.get('img_link')
    return await post_news(main_text, topic, user_id, img_link)
