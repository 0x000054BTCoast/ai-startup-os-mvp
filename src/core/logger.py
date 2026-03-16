from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


@dataclass
class LogRecord:
    timestamp: str
    request: Any
    response: Any
    error: str | None = None


class CoreLogger:
    """Minimal structured logger for core flow operations."""

    def __init__(self, log_dir: str | Path = "logs", retention_days: int = 7) -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = retention_days
        self.log_file = self.log_dir / "core_flow.jsonl"
        self._cleanup_old_logs()

    def _cleanup_old_logs(self) -> None:
        threshold = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
        for file in self.log_dir.glob("*.json*"):
            modified = datetime.fromtimestamp(file.stat().st_mtime, tz=timezone.utc)
            if modified < threshold:
                file.unlink(missing_ok=True)

    def log(self, *, request: Any, response: Any = None, error: str | None = None) -> None:
        record = LogRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            request=request,
            response=response,
            error=error,
        )
        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.__dict__, ensure_ascii=False) + "\n")
