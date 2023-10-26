from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'sqlite+aiosqlite:///./charity_fund.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
