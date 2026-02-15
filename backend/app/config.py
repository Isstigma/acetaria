from pathlib import Path
from typing import List, Union
from urllib.parse import quote_plus

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    ENV: str = Field("dev", alias="ENV")

    api_prefix: str = Field("/api/v1", alias="API_PREFIX")
    acetaria_auto_seed: int = Field(0, alias="ACETARIA_AUTO_SEED") # TODO: maybe it's worth making it bool

    cors_origins: Union[str, List[str]] = Field(
        "http://localhost:5173",
        alias="CORS_ORIGINS",
    )

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field("localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    # redis_host: str = Field("localhost", alias="REDIS_HOST")
    # redis_port: int = Field(6379, alias="REDIS_PORT")
    # redis_db: int = Field(..., alias="REDIS_DB")
    # redis_password: SecretStr = Field(..., alias="REDIS_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_prod(self) -> bool: #TODO: maybe it's worth making it private 
        return self.ENV.lower() == "prod"

    @property
    def auto_seed(self) -> bool:
        return bool(self.acetaria_auto_seed)

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def cors_methods(self) -> List[str]:
        return ["GET", "POST", "PUT", "DELETE"] if self.is_prod else ["*"]

    @property
    def cors_headers(self) -> List[str]:
        return ["Authorization", "Content-Type"] if self.is_prod else ["*"]  

    @property
    def postgres_url(self) -> str:
        url = URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=quote_plus(self.postgres_password.get_secret_value()),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )
        return url.render_as_string(hide_password=False)  

    # @property
    # def redis_url(self) -> str:
    #     password = quote_plus(self.redis_password.get_secret_value())
    #     return f"redis://:{password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


settings = Settings() # TODO: in theory, if we're making a microservice application, we'll need to initialize settings differently