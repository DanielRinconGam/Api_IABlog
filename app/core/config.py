import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = 60

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GITHUB_PAGES_ORIGIN = os.getenv("GITHUB_PAGES_ORIGIN", "*")
    
    DATABASE_URL: str

settings = Settings()
