from __future__ import annotations

import json
from pathlib import Path


class TelegramStateStore:
    def __init__(self, path: str | Path = ".telegram_state.json") -> None:
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, state: dict) -> None:
        self.path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_chat_state(self, chat_id: str) -> dict:
        state = self.load()
        return state.get(chat_id, {})

    def set_chat_state(self, chat_id: str, chat_state: dict) -> None:
        state = self.load()
        state[chat_id] = chat_state
        self.save(state)
