import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig(BaseModel):
    dsn: str = os.environ.get('DB_URL')


class Config(BaseSettings):
    api_version: str = 'v0.0.1'
    application_name: str = 'Traffic Devils Test Task'
    application_description: str = 'Traffic Devils Test Task Description'
    debug: bool = os.environ.get('DEBUG')
    database: DatabaseConfig = DatabaseConfig()
    timezone: str = 'Europe/Kiev'
    jwt_secret: str = os.environ.get('JWT_SECRET')
    jwt_lifetime: int = 60 * 60 * 24  # 1 day


config = Config()
