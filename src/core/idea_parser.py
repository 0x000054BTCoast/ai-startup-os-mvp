from __future__ import annotations

from pathlib import Path


class IdeaParser:
    """Parse short text or markdown files into a normalized idea JSON."""

    @staticmethod
    def parse_input(idea_input: str) -> dict:
        path = Path(idea_input)
        if path.exists() and path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8")
        else:
            text = idea_input
        return IdeaParser.parse_markdown(text)

    @staticmethod
    def parse_markdown(content: str) -> dict:
        lines = [line.rstrip() for line in content.splitlines()]
        title = ""
        details_lines: list[str] = []
        reqs: list[str] = []
        unknowns: list[str] = []
        current = "details"

        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#") and not title:
                title = line.lstrip("# ").strip()
                continue
            low = line.lower()
            if "requirement" in low or "需求" in line:
                current = "requirements"
                continue
            if "unknown" in low or "open question" in low or "待确认" in line:
                current = "unknowns"
                continue
            if line.startswith(("- ", "* ")):
                item = line[2:].strip()
                if current == "requirements":
                    reqs.append(item)
                elif current == "unknowns":
                    unknowns.append(item)
                else:
                    details_lines.append(item)
                continue

            details_lines.append(line)

        details = "\n".join(details_lines).strip()
        if not title:
            first = details_lines[0] if details_lines else "Untitled Idea"
            title = first[:80]

        summary = details_lines[0] if details_lines else title
        return {
            "title": title,
            "summary": summary,
            "details": details,
            "requirements": reqs,
            "unknowns": unknowns,
        }
