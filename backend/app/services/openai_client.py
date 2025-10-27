from __future__ import annotations

from typing import Any, Dict

import httpx
from fastapi import HTTPException, status

from ..config import get_settings


class OpenAIClient:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_endpoint or not settings.openai_api_key:
            raise RuntimeError("Azure OpenAI configuration is missing.")

        self.endpoint = settings.openai_endpoint.rstrip("/")
        self.api_key = settings.openai_api_key
        self.deployment = settings.openai_deployment or "gpt-4o-mini"
        self.api_version = settings.openai_api_version
        self._headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json",
        }

    async def run_chat_completion(self, messages: list[dict[str, str]], temperature: float = 0.2) -> Dict[str, Any]:
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        payload = {
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=self._headers, json=payload)

        if response.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Azure OpenAI error: {response.text}",
            )

        return response.json()

