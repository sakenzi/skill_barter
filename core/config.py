import os 
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_USER: str

    def reload_env(self):
        load_dotenv(override=True)

    @property
    def DATABASE_URL_asyncpg(self):
        self.reload_env()
        return f"postgresql+asyncpg://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1

    DATETIME_FORMAT: str = '%d-%m-%Y %H:%M:%S'

settings = Settings()