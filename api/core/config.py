from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    ALLOWED_ORIGINS: str = ""
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    @property
    def allowed_origins_list(self) -> List[str]:
        if self.ALLOWED_ORIGINS:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
        return []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()