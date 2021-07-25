import datetime
import ujson
from asyncpg import Record
from services.db import DB


async def get_password(username: str) -> Record:
    query = f"""
        select user_password
        from users
        where username = '{username}'
    """
    return await DB.conn.fetchval(query)


async def register_user(user_id: str, username: str, user_password: dict) -> None:
    query = """
        insert into users (id, username, user_password, created_at)
        values ($1, $2, $3, $4)
    """
    await DB.conn.execute(query, user_id, username,
                          ujson.dumps(user_password), datetime.datetime.now())


async def user_from_login(username: str) -> str:
    query = """
        select id
        from users
        where username = $1
    """
    user_id = await DB.conn.fetchval(query, username)
    return user_id.hex


async def user_exist(username: str) -> str:
    query = """
        select exists (
            select
            from users
            where username = $1
        )
    """
    return await DB.conn.fetchval(query, username)
