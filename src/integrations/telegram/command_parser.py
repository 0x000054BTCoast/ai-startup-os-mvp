from __future__ import annotations

import shlex
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    name: str
    args: list[str]


def parse_command(text: str) -> ParsedCommand | None:
    if not text.startswith("/"):
        return None
    parts = shlex.split(text)
    if not parts:
        return None

    head = parts[0]
    for known in [
        "createProject",
        "jumpIntoProject",
        "brainstormWithProductManager",
        "brainstormWithArchitect",
        "brainstormWithEngineer",
        "answerOpenQuestion",
        "generateCodexPrompt",
    ]:
        if head.startswith(f"/{known}"):
            inline_tail = head[len(known) + 1 :]
            args = []
            if inline_tail:
                args.append(inline_tail)
            args.extend(parts[1:])
            return ParsedCommand(name=known, args=args)
    return ParsedCommand(name=head.lstrip("/"), args=parts[1:])
