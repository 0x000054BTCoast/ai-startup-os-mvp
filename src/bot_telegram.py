from __future__ import annotations

import os
import time
import requests
from dotenv import load_dotenv

from src.core.router import StartupOSRouter

API_BASE = "https://api.telegram.org/bot{token}/{method}"


def tg_call(token: str, method: str, payload: dict | None = None) -> dict:
    url = API_BASE.format(token=token, method=method)
    resp = requests.post(url, json=payload or {}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def send_message(token: str, chat_id: str, text: str) -> None:
    tg_call(token, "sendMessage", {"chat_id": chat_id, "text": text})


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")

    router = StartupOSRouter()
    offset = 0
    print("Telegram bot polling started...")
    while True:
        updates = tg_call(token, "getUpdates", {"timeout": 30, "offset": offset})
        for item in updates.get("result", []):
            offset = item["update_id"] + 1
            message = item.get("message", {})
            text = (message.get("text") or "").strip()
            msg_chat_id = str(message.get("chat", {}).get("id", ""))
            if msg_chat_id != str(chat_id):
                continue
            if not text:
                continue
            if text.startswith("/start"):
                send_message(token, chat_id, "已启动。直接发一句需求给我，例如：为 PRD2Prototype 写 PRD 和技术方案")
                continue
            project_name = os.getenv("DEFAULT_PROJECT_NAME", "demo-project")
            send_message(token, chat_id, "收到，开始生成 PRD / 技术方案 / 开发指南……")
            try:
                result = router.kickoff(goal=text, project_name=project_name)
                reply = (
                    f"已完成。\n\n"
                    f"项目目录：{result.project_dir}\n"
                    f"PRD：{result.prd_path}\n"
                    f"结构化 JSON：{result.prd_json_path}\n"
                    f"技术方案：{result.architecture_path}\n"
                    f"开发指南：{result.dev_plan_path}"
                )
            except Exception as exc:
                reply = f"执行失败：{exc}"
            send_message(token, chat_id, reply)
        time.sleep(2)


if __name__ == "__main__":
    main()
