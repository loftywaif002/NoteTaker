from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str = Field(default="sqlite:///./notes.db")
    # For SQLite only: need this to avoid 'check_same_thread' error
    SQLALCHEMY_CONNECT_ARGS: dict = {"check_same_thread": False}
    # MCP server base URL (e.g., http://localhost:8001)
    MCP_BASE_URL: Optional[str] = Field(default="http://localhost:8001")
    # Auto-summarization toggles
    AUTOSUMMARIZE_ON_CREATE: bool = True
    AUTOSUMMARIZE_ON_UPDATE: bool = True
    # CORS (set your Next.js URL here)
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost:3000"]
    class Config:
        env_file = ".env"
        extra = "ignore"
settings = Settings()

