from services.db import DB


async def all_users():
    try:
        query = """
            select id, username, phone,
                city, first_name
            from users
        """
        return await DB.conn.fetch(query)
    except Exception as e:
        return f'Error: {e}'
