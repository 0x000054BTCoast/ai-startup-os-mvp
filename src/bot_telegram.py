from __future__ import annotations

import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Support `python src/bot_telegram.py` by ensuring repo root is importable.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.router import StartupOSRouter
from src.integrations.telegram.command_parser import parse_command
from src.integrations.telegram.state import TelegramStateStore

API_BASE = "https://api.telegram.org/bot{token}/{method}"


def tg_call(token: str, method: str, payload: dict | None = None) -> dict:
    url = API_BASE.format(token=token, method=method)
    resp = requests.post(url, json=payload or {}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def send_message(token: str, chat_id: str, text: str) -> None:
    tg_call(token, "sendMessage", {"chat_id": chat_id, "text": text})


def _parse_generate_prompt_args(args: list[str]) -> tuple[str | None, str | None, str | None]:
    project = args[0] if args else None
    module = None
    doc = None
    for i, arg in enumerate(args):
        if arg == "--module" and i + 1 < len(args):
            module = args[i + 1]
        if arg == "--doc" and i + 1 < len(args):
            doc = args[i + 1]
    return project, module, doc


def main() -> None:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")

    router = StartupOSRouter()
    state_store = TelegramStateStore()

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

            chat_state = state_store.get_chat_state(msg_chat_id)
            current_project = chat_state.get("current_project") or os.getenv("DEFAULT_PROJECT_NAME", "demo-project")
            pending_qid = chat_state.get("pending_question_id")

            if text.startswith("/start"):
                send_message(token, chat_id, "已启动。可用命令：/createProject /jumpIntoProject /brainstormWithProductManager /answerOpenQuestion /generateCodexPrompt")
                continue

            cmd = parse_command(text)

            try:
                if pending_qid and (not cmd or cmd.name != "answerOpenQuestion"):
                    prd_path = router.answer_open_question(project_name=current_project, question_id=pending_qid, answer=text)
                    chat_state["pending_question_id"] = None
                    state_store.set_chat_state(msg_chat_id, chat_state)
                    send_message(token, chat_id, f"已记录问题 {pending_qid} 的回答，并更新 PRD：{prd_path}")
                    continue

                if cmd and cmd.name == "createProject":
                    if not cmd.args:
                        send_message(token, chat_id, "用法: /createProject {projectName}")
                        continue
                    project_dir = router.create_project(cmd.args[0])
                    send_message(token, chat_id, f"项目已创建：{project_dir}")
                    continue

                if cmd and cmd.name == "jumpIntoProject":
                    if not cmd.args:
                        send_message(token, chat_id, "用法: /jumpIntoProject {projectName}")
                        continue
                    project_dir = router.jump_into_project(cmd.args[0])
                    chat_state["current_project"] = cmd.args[0]
                    state_store.set_chat_state(msg_chat_id, chat_state)
                    send_message(token, chat_id, f"已切换项目上下文：{project_dir}")
                    continue

                if cmd and cmd.name.startswith("brainstormWith"):
                    agent = cmd.name.replace("brainstormWith", "")
                    prompt = " ".join(cmd.args).strip()
                    if not prompt:
                        send_message(token, chat_id, "用法: /brainstormWithProductManager 你的问题")
                        continue
                    answer = router.brainstorm_with(agent=agent, message=prompt, project_name=current_project)
                    send_message(token, chat_id, answer[:3500])
                    continue

                if cmd and cmd.name == "answerOpenQuestion":
                    if not cmd.args:
                        send_message(token, chat_id, "用法: /answerOpenQuestion {questionId} [你的回答]")
                        continue
                    qid = cmd.args[0]
                    inline_answer = " ".join(cmd.args[1:]).strip()
                    if inline_answer:
                        prd_path = router.answer_open_question(project_name=current_project, question_id=qid, answer=inline_answer)
                        send_message(token, chat_id, f"已更新问题 {qid}：{prd_path}")
                    else:
                        chat_state["pending_question_id"] = qid
                        state_store.set_chat_state(msg_chat_id, chat_state)
                        send_message(token, chat_id, f"请直接发送 {qid} 的回答内容。")
                    continue

                if cmd and cmd.name == "generateCodexPrompt":
                    project, module, doc = _parse_generate_prompt_args(cmd.args)
                    project = project or current_project
                    result = router.generate_codex_prompt(project_name=project, module=module, doc=doc)
                    send_message(token, chat_id, result[:3500])
                    continue

                # Non-command text: treat as idea and run full pipeline in current context.
                send_message(token, chat_id, f"收到，基于项目 {current_project} 开始生成 PRD / 技术方案 / 开发指南……")
                result = router.kickoff(goal=text, project_name=current_project)
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
