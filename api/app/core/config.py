from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    ALLOWED_ORIGINS: str
    DEBUG: bool
    API_PREFIX: str

    GOOGLE_API_KEY: str

    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_HOST: str
    DEEPGRAM_API_KEY: str
    CARTESIA_API_KEY: str

    @property
    def allowed_origins_list(self) -> List[str]:
        if self.ALLOWED_ORIGINS:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
        return []
    
settings = Settings()