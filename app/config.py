from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://enfdb:123@db:5432/library"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()