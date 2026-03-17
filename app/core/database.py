from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Prepify AI"
    DATABASE_URL: str = "postgresql://user:pass@localhost/prepify"
    REDIS_URL: str = "redis://localhost:6379/0"
    VECTOR_DB_PATH: str = "./data/chroma"
    MODEL_NAME: str = "mistralai/Mistral-7B-Instruct-v0.2" # Or local model path
    
    class Config:
        env_file = ".env"

settings = Settings()
