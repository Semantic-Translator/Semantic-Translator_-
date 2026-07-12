"""Generic OpenAI-compatible HTTP provider.

The provider is optional and disabled by default.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from backend.llm.base import GenerationResult, LLMProvider


class HttpLLMProvider(LLMProvider):
    name = "http"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: int = 60,
    ) -> None:
        self.base_url = base_url or os.getenv("SEMANTIC_LLM_BASE_URL", "")
        self.api_key = api_key or os.getenv("SEMANTIC_LLM_API_KEY", "")
        self.model = model or os.getenv("SEMANTIC_LLM_MODEL", "")
        self.timeout_seconds = timeout_seconds

    def _endpoint(self) -> str:
        return self.base_url.rstrip("/") + "/chat/completions"

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> GenerationResult:
        if not self.base_url or not self.model:
            raise RuntimeError("HTTP LLM provider is not configured.")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        request = urllib.request.Request(
            self._endpoint(),
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as error:
            raise RuntimeError(f"HTTP LLM request failed: {error}") from error

        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError("HTTP LLM response contains no choices.")

        text = choices[0].get("message", {}).get("content", "")

        return GenerationResult(
            text=text,
            provider=self.name,
            model=self.model,
            metadata={
                "usage": data.get("usage", {}),
                "request_id": data.get("id"),
            },
        )

    def health(self) -> dict:
        return {
            "provider": self.name,
            "model": self.model,
            "available": bool(self.base_url and self.model),
            "configured": bool(self.base_url and self.model),
        }
