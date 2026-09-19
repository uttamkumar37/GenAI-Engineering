from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    provider_name: str = "mock-llm"
    max_reply_tokens: int = 256
    default_temperature: float = 0.7


@lru_cache
def get_settings() -> Settings:
    return Settings(
        provider_name=os.environ.get("CHAT_API_PROVIDER_NAME", "mock-llm"),
        max_reply_tokens=int(os.environ.get("CHAT_API_MAX_REPLY_TOKENS", "256")),
        default_temperature=float(os.environ.get("CHAT_API_DEFAULT_TEMPERATURE", "0.7")),
    )
