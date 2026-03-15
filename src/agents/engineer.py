from __future__ import annotations

import os
from textwrap import dedent

from src.agents.prompts import ENGINEER_PROMPT
from src.core.llm import DeepSeekClient


class EngineerAgent:
    def __init__(self, llm: DeepSeekClient) -> None:
        self.llm = llm
        self.model = os.getenv("MODEL_ENGINEER", "deepseek-reasoner")

    def build_dev_plan(self, prd_markdown: str, architecture_markdown: str, project_name: str) -> str:
        user_prompt = dedent(f"""
        项目名：{project_name}

        下面是 PRD：
        {prd_markdown}

        下面是技术方案：
        {architecture_markdown}

        请输出开发执行指南，必须包含：
        - Step-by-step implementation order
        - File-by-file plan
        - Commands to run locally
        - Validation checklist
        - Common errors and fixes
        - Next 3 small deliverables

        要求：
        1. 站在 0 coding 经验产品经理的角度写。
        2. 每一步尽量具体到命令、文件、预期结果。
        3. 不要假设用户懂 Python 或前端框架。
        """)
        return self.llm.chat(model=self.model, system_prompt=ENGINEER_PROMPT, user_prompt=user_prompt)
