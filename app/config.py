import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class ConfigError(RuntimeError):
    pass


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Environment variable {name} is not set. Check your .env file.")
    return value


def _optional(name: str) -> str | None:
    return os.getenv(name) or None


def _search_roots() -> list[str]:
    raw = os.getenv("SEARCH_ROOTS")
    if not raw:
        return [str(Path.home())]
    return [item.strip() for item in raw.split(",") if item.strip()]


@dataclass(frozen=True)
class Config:
    bot_token: str
    owner_id: int
    groq_token: str | None
    openai_token: str | None
    claude_token: str | None
    search_roots: list[str]

    @classmethod
    def load(cls) -> "Config":
        return cls(
            bot_token=_require("BOT_TOKEN"),
            owner_id=int(_require("USER_ID")),
            groq_token=_optional("GROQ_TOKEN"),
            openai_token=_optional("OPEN_AI_TOKEN"),
            claude_token=_optional("CLAUDE_TOKEN"),
            search_roots=_search_roots(),
        )


config = Config.load()
