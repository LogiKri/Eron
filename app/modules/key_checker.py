import asyncio
import json
import logging
from enum import Enum
from typing import Any, Optional

import aiohttp

logger = logging.getLogger(__name__)


class APIProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    COHERE = "cohere"
    MISTRAL = "mistral"
    PERPLEXITY = "perplexity"
    DEEPSEEK = "deepseek"


PROVIDERS_CONFIG: dict[APIProvider, dict[str, Any]] = {
    APIProvider.OPENAI: {
        "base_url": "https://api.openai.com/v1",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
    APIProvider.GROQ: {
        "base_url": "https://api.groq.com/openai/v1",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
    APIProvider.ANTHROPIC: {
        "base_url": "https://api.anthropic.com/v1",
        "test_endpoint": "/messages",
        "auth_header": "x-api-key",
        "auth_prefix": "",
        "method": "POST",
        "test_payload": {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "Hi"}],
        },
    },
    APIProvider.GOOGLE: {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "test_endpoint": "/models",
        "auth_header": "x-goog-api-key",
        "auth_prefix": "",
        "method": "GET",
    },
    APIProvider.COHERE: {
        "base_url": "https://api.cohere.ai/v1",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
    APIProvider.MISTRAL: {
        "base_url": "https://api.mistral.ai/v1",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
    APIProvider.PERPLEXITY: {
        "base_url": "https://api.perplexity.ai",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
    APIProvider.DEEPSEEK: {
        "base_url": "https://api.deepseek.com/v1",
        "test_endpoint": "/models",
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "method": "GET",
    },
}


class UniversalAPIKeyChecker:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "UniversalAPIKeyChecker":
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.session:
            await self.session.close()

    async def check_key(self, api_key: str, provider: APIProvider) -> tuple[bool, str]:
        config = PROVIDERS_CONFIG[provider]
        url = config["base_url"] + config["test_endpoint"]

        try:
            if config["method"] == "GET":
                return await self._check_get(url, api_key, config["auth_header"], config["auth_prefix"])
            return await self._check_post(
                url, api_key, config["auth_header"], config["auth_prefix"], config.get("test_payload", {})
            )
        except Exception as exc:
            logger.error("Error checking API key for %s: %s", provider, exc)
            return False, f"❌ Error: {exc}"

    async def _check_get(self, url: str, api_key: str, auth_header: str, auth_prefix: str) -> tuple[bool, str]:
        headers = {auth_header: f"{auth_prefix}{api_key}", "Content-Type": "application/json"}
        try:
            async with self.session.get(url, headers=headers, timeout=self.timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    return True, f"✅ Valid API key. {self._models_summary(data)}"
                error_text = await response.text()
                return False, f"❌ {self._error_message(error_text, response.status)}"
        except aiohttp.ClientError as exc:
            return False, f"❌ Connection error: {exc}"
        except asyncio.TimeoutError:
            return False, "❌ Timeout error"

    async def _check_post(
        self, url: str, api_key: str, auth_header: str, auth_prefix: str, payload: dict
    ) -> tuple[bool, str]:
        headers = {auth_header: f"{auth_prefix}{api_key}", "Content-Type": "application/json"}
        if auth_header == "x-api-key":
            headers["anthropic-version"] = "2023-06-01"

        async with self.session.post(url, json=payload, headers=headers, timeout=self.timeout) as response:
            if response.status in (200, 201):
                return True, "✅ Valid API key"
            error_text = await response.text()
            return False, f"❌ {self._error_message(error_text, response.status)}"

    @staticmethod
    def _models_summary(data: dict) -> str:
        models = data.get("data", [])
        if not models:
            return "Models available"
        names = [m.get("id", "") for m in models[:3] if m.get("id")]
        suffix = "..." if len(models) > 3 else ""
        return f"Available models: {', '.join(names)}{suffix}" if names else "Models available"

    @staticmethod
    def _error_message(error_text: str, status: int) -> str:
        try:
            error_data = json.loads(error_text)
        except json.JSONDecodeError:
            if "401" in error_text or "Unauthorized" in error_text:
                return "Invalid API key"
            if "403" in error_text or "Forbidden" in error_text:
                return "Access forbidden"
            if "429" in error_text:
                return "Rate limited"
            return f"API error {status}"

        error = error_data.get("error")
        if isinstance(error, dict):
            return error.get("message", f"API error {status}")
        if isinstance(error, str):
            return error
        return error_data.get("message") or error_data.get("detail") or f"API error {status}"


async def quick_check_api_key(api_key: str, provider: APIProvider) -> tuple[bool, str]:
    async with UniversalAPIKeyChecker() as checker:
        return await checker.check_key(api_key, provider)


async def check_configured_keys(keys: dict[APIProvider, str | None]) -> dict[APIProvider, tuple[bool, str]]:
    configured = {provider: key for provider, key in keys.items() if key}
    if not configured:
        return {}

    async with UniversalAPIKeyChecker() as checker:
        results = await asyncio.gather(*(checker.check_key(key, provider) for provider, key in configured.items()))

    return dict(zip(configured.keys(), results))
