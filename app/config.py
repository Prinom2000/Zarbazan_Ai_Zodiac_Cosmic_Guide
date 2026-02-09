"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Astrology & Numerology API"
    VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    BASE_URL: str = os.getenv("BASE_URL", "http://72.61.158.79")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()