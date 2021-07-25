import hashlib
import os
import ujson


def check_password_hash(user_password: str, password_hash: dict) -> bool:
    password_hash = ujson.loads(password_hash)
    salt, key = password_hash['salt'], password_hash['key']
    new_key = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'),
                                  salt.encode('utf-8'), 100000).hex()
    return key == new_key


def create_password_hash(user_password: str) -> dict:
    salt = os.urandom(32).hex()
    key = hashlib.pbkdf2_hmac('sha256', user_password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    return {
        'salt': salt,
        'key': key
    }
