from dataclasses import dataclass, field
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Хранит настройки подключения к модели эмбеддингов.

    Attributes:
        base_url: Базовый URL OpenAI-совместимого API.
        api_key: Ключ для запросов к API.
        embedding_model: Идентификатор модели эмбеддингов.
    """

    base_url: str
    api_key: str = field(repr=False)
    embedding_model: str


def load_settings() -> Settings:
    """Читает настройки модели из переменных окружения.

    Returns:
        Настройки подключения к LM Studio.

    Raises:
        ValueError: Одна или несколько обязательных переменных пусты.
    """
    load_dotenv(override=False)
    names = ("LLM_BASE_URL", "LLM_API_KEY", "EMBEDDING_MODEL")
    values = {name: getenv(name, "").strip() for name in names}
    missing = [name for name in names if not values[name]]
    if missing:
        raise ValueError(f"Заполни переменные окружения: {', '.join(missing)}")

    return Settings(
        base_url=values["LLM_BASE_URL"],
        api_key=values["LLM_API_KEY"],
        embedding_model=values["EMBEDDING_MODEL"],
    )
