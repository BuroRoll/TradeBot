from pydantic import BaseSettings


class Settings(BaseSettings):
    BINANCE_API_KEY = ''
    BINANCE_SECRET_KEY = ''
    TELEGRAM_API_TOKEN = ''
    TELEGRAM_CHAT_ID = ''


settings = Settings()

# settings = Settings(
#     _env_file='./env',
#     _env_file_encoding='utf-8'
# )
