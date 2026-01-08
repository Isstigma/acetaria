from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding='utf-8')

    db_url: str = "postgresql://username:password@localhost:5432/acetariaa"
    cors_origins: str = "http://localhost:5173"
    api_prefix: str = "/api/v1"
    acetaria_auto_seed: int = 0

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
