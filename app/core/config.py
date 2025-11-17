import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Auth
    JWT_SECRET = os.getenv("JWT_SECRET", "super-secret")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE", 1440))

    # IA
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # CORS
    GITHUB_PAGES_ORIGIN = os.getenv("GITHUB_PAGES_ORIGIN", "*")

    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
