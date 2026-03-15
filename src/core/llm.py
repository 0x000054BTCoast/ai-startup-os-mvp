from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI


class DeepSeekClient:
    def __init__(self) -> None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        if not api_key:
            raise RuntimeError("Missing DEEPSEEK_API_KEY in .env")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, *, model: str, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        return content or ""

    def chat_json(self, *, model: str, system_prompt: str, user_prompt: str, temperature: float = 0.0) -> dict[str, Any]:
        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or "{}"
        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Model did not return valid JSON: {content}") from exc
