from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    CHROMA_DB_DIR: str = Field(default="./chroma")
    class Config:
        env_file = ".env"
settings = Settings()