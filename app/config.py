"""
Application Configuration
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Astrology & Numerology API"
    VERSION: str = "1.0.0"

    # API Keys
    OPENAI_API_KEY: str
    HEYGEN_API_KEY: str

    # App Config
    BASE_URL: str = "http://72.61.158.79"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()