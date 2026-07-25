"""
Central place for environment/config values so nothing else in the
codebase touches os.environ directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_URL: str = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_URL: str = "https://api.groq.com/openai/v1/chat/completions"

    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "5000"))
    DEBUG: bool = os.getenv("FLASK_ENV", "production") == "development"

    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "medsafer")

    @classmethod
    def has_ai_key(cls) -> bool:
        return bool(cls.GROQ_API_KEY)


config = Config()