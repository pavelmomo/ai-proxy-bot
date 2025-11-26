from typing import TypedDict

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CallbackKeys(TypedDict):
    secret_key: str
    confirmation_code: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    URL_SCHEMA: str = "http"
    DOMAIN: str = "localhost"
    CALLBACK_PATH: str = "/callback"

    PUTER_USERNAME: str = "user"
    PUTER_PASSWORD: str = "password"

    VK_TOKEN: str = "token"

    # Will be received in runtime
    VK_SECRET_KEY: str = "secret_key"
    VK_CONFIRMATION_CODE: str = "code"

    @computed_field
    @property
    def CALLBACK_URL(self) -> str:
        return f"{self.URL_SCHEMA}://{self.DOMAIN}{self.CALLBACK_PATH}"


settings = Settings()
