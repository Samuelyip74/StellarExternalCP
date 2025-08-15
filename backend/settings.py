from pydantic_settings import BaseSettings
from pydantic import AnyUrl, Field

class Settings(BaseSettings):
    # General
    ENV: str = "dev"

    # Default AP Login URL (can be overridden by query param `loginurl` if AP supports it)
    AP_LOGIN_URL: AnyUrl | str = "https://cportal.al-enterprise.com/login"

    # Default landing URLs
    DEFAULT_SUCCESS_URL: str = "https://example.com/success"
    DEFAULT_ERROR_URL: str = "https://example.com/error"

    # CORS / Frontend
    FRONTEND_ORIGIN: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()