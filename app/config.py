import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_url: str = "mongodb+srv://hassanrizvi139:bpYhZXlFuB3cwBEz@padelug.4rot0yj.mongodb.net/?retryWrites=true&w=majority&appName=PadelUG"
    database_name: str = "padelug_db"
    
    # API Configuration
    api_host: str = "localhost"
    api_port: int = 8000
    debug: bool = True
    
    # Application Configuration
    app_name: str = "PadelUG API"
    app_version: str = "1.0.0"
    app_description: str = "A FastAPI-based REST API for PadelUG with MongoDB integration"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings() 