import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    elasticsearch_host: str = os.getenv("ELASTICSEARCH_HOST", "localhost:9200")
    elasticsearch_user: str = os.getenv("ELASTICSEARCH_USER", "elastic")
    elasticsearch_password: str = os.getenv("ELASTICSEARCH_PASSWORD", "changeme")
    
    class Config:
        env_file = ".env"

settings = Settings()
