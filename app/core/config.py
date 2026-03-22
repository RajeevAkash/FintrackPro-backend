from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    MONGO_URI: str = Field(..., env="MONGO_URI")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRY_MINUTES: int = Field(default=1440, env="JWT_EXPIRY_MINUTES")
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    DATABASE_NAME: str = "fintrackpro"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
