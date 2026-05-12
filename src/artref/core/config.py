from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    scryfall_url: str = "https://api.scryfall.com"
    unsplash_url: str = "https://api.unsplash.com"
    wallhaven_url: str = "https://wallhaven.cc/api/v1"

    cache_dir: Path = Path.home() / ".cache" / "artref"
    cache_expire: int = 7 * 24 * 60 * 60

    server_addr: str = "127.0.0.1"
    server_port: int = 8000

    count_default: int = 3
    count_min: int = 1
    count_max: int = 10

    unsplash_key: Optional[str] = Field(default=None, validation_alias="UNSPLASH_KEY")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    def get_unsplash_key(self) -> str:
        if not self.unsplash_key:
            raise RuntimeError("Missing UNSPLASH_KEY")
        return self.unsplash_key


settings = Settings()
