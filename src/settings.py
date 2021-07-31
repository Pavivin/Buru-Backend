import os

AUDIENCE: str = 'Hackathon-club'
APP_ID: str = 'Backend-FastAPI'
VERSION: str = '0.1'

APP_HOST: str = os.getenv('APP_HOST', '0.0.0.0')
APP_PORT: int = int(os.getenv('APP_PORT', 8000))

MINUTE: int = 60
DAY: int = 86400

REFRESH_TOKEN_TTL_SECONDS: int = 30 * DAY
ACCESS_TOKEN_TTL_SECONDS: int = 150 * MINUTE

DATABASE_URL: str = os.getenv('DATABASE_URL')

SECRET_KEY: str = os.getenv('SECRET_KEY', '1234')
ALGORITHMS_JWT: str = os.getenv('ALGORITHMS_JWT')

HASH_NAME: str = os.getenv('HASH_NAME')


origins = [
    '*'
]
