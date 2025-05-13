
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()


class Settings(BaseModel):
    DATABASE_URI: str = Field(..., env="DATABASE_URI")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except ValidationError as e:
    print("Error loading settings:", e)
    settings = None
