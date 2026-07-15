import asyncio
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "profiles.json"
MAX_HISTORY_MESSAGES = 20

_lock = asyncio.Lock()


@dataclass
class UserProfile:
    language: str = "en"
    nickname: str | None = None
    ai_role: str = "You are Eron, a helpful personal assistant."
    history: list[dict[str, str]] = field(default_factory=list)


def _read_all() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_all(data: dict[str, Any]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def get_profile(user_id: int) -> UserProfile:
    async with _lock:
        data = _read_all()
        raw = data.get(str(user_id))
        return UserProfile(**raw) if raw else UserProfile()


async def save_profile(user_id: int, profile: UserProfile) -> None:
    async with _lock:
        data = _read_all()
        data[str(user_id)] = asdict(profile)
        _write_all(data)


async def append_history(user_id: int, role: str, content: str) -> UserProfile:
    async with _lock:
        data = _read_all()
        raw = data.get(str(user_id))
        profile = UserProfile(**raw) if raw else UserProfile()
        profile.history.append({"role": role, "content": content})
        profile.history = profile.history[-MAX_HISTORY_MESSAGES:]
        data[str(user_id)] = asdict(profile)
        _write_all(data)
        return profile


async def clear_history(user_id: int) -> None:
    async with _lock:
        data = _read_all()
        raw = data.get(str(user_id))
        if raw:
            raw["history"] = []
            data[str(user_id)] = raw
            _write_all(data)
