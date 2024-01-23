from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/"
    product_info_lifetime: int = 60 * 60 * 3  # 3 hours

    class Config:
        env_file = ".env"


settings = Settings()
