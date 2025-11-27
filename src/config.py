from logging import config
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
    SERVER_NAME: str = "vk_bot"
    LOG_LEVEL: str = "INFO"

    PUTER_USERNAME: str = "user"
    PUTER_PASSWORD: str = "password"
    PUTER_MODEL: str = "gpt-4.1"

    VK_TOKEN: str = "token"

    # Will be received in runtime
    VK_SECRET_KEY: str = "secret_key"
    VK_CONFIRMATION_CODE: str = "code"

    @computed_field
    @property
    def CALLBACK_URL(self) -> str:
        return f"{self.URL_SCHEMA}://{self.DOMAIN}{self.CALLBACK_PATH}"


settings = Settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": {
            "format": "%(asctime)s: %(levelname)s: [%(filename)s] %(message)s",
            "datefmt": "%d-%m-%y %I:%M:%S",
        },
        "access": {
            "format": "%(asctime)s: %(levelname)s: %(message)s",
            "datefmt": "%d-%m-%y %I:%M:%S",
        },
    },
    "handlers": {
        "default_handler": {
            "class": "logging.StreamHandler",
            "formatter": "default_formatter",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["default_handler"],
            "level": settings.LOG_LEVEL,
        },
        "uvicorn": {
            "handlers": ["default_handler"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        },
        "vkbottle": {
            "handlers": ["default_handler"],
            "level": settings.LOG_LEVEL,
        },
    },
}

config.dictConfig(LOGGING_CONFIG)
