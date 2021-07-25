from typing import Optional, Union
from services.db import DB


async def select_user(user_id) -> Union[str, dict]:
    try:
        query = """
            select username, phone, city, first_name
            from users
            where id = $1
        """
        return await DB.conn.fetchrow(query, user_id)
    except Exception as e:
        return f'Error: {e}'


async def update_user_info(user_id: str, username: Optional[str],
                           first_name: Optional[str], city: Optional[str],
                           phone: Optional[str]) -> str:
    try:
        print(first_name)
        query = """
            update users
            set
            username = coalesce($1, username),
            first_name = coalesce($2, first_name),
            city = coalesce($3, city),
            phone = coalesce($4, phone)
            where id = $5
        """
        await DB.conn.execute(query, username, first_name, city, phone, user_id)
        return 'The information was successfully updated'
    except Exception as e:
        return f'Error: {e}'
