import uuid
from datetime import datetime
from uuid import UUID

from aiologger import Logger
from asyncpg.exceptions import UniqueViolationError
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel, EmailStr
from starlette import status

import container
from apps.api.main_app import exceptions
from db import PG


class UserDto(BaseModel):
    id: UUID
    email: EmailStr
    password: str


class UserExists(Exception):
    message = "Пользователь с указанным email существует"
    status_code = status.HTTP_409_CONFLICT


@container.register
class UserService:
    def __init__(self, logger: Logger, db: PG):
        self._logger = logger
        self._db = db

    async def create_user(self, email: str, plain_password: str):

        hash_password = pbkdf2_sha256.hash(plain_password)
        user_id = uuid.uuid4()
        stmt = """
            insert into users (user_id, email, hash_pass, created_at)
            values ($1, $2, $3, $4)
        """
        values = (user_id, email, hash_password, datetime.now())
        try:
            await self._db.fetchrow(stmt, *values)
        except UniqueViolationError as e:
            raise UserExists from e

        return user_id

    async def __find_by_param(self, param: str, param_name: str) -> UserDto:
        stmt = f"""
            SELECT user_id as id, email, hash_pass as password
            FROM users
            WHERE {param_name} = '{param}'
        """
        row = await self._db.fetchrow(stmt)
        if row:
            return UserDto(**row)
        raise exceptions.UserNotFound()

    async def find_by_email(self, email: str) -> UserDto:
        return await self.__find_by_param(param=email, param_name="email")

    async def find_by_id(self, user_id: UUID) -> UserDto:
        return await self.__find_by_param(param=user_id.hex, param_name="id")

    @staticmethod
    def password_verify(*, hashed: str, plain: str) -> bool:
        is_verify: bool = pbkdf2_sha256.verify(plain, hashed)
        return is_verify
