from __future__ import annotations

import os
from textwrap import dedent

from src.agents.prompts import ARCHITECT_PROMPT
from src.core.llm import DeepSeekClient


class ArchitectAgent:
    def __init__(self, llm: DeepSeekClient) -> None:
        self.llm = llm
        self.model = os.getenv("MODEL_ARCHITECT", "deepseek-reasoner")

    def build_architecture(self, prd_markdown: str, prd_json: dict, project_name: str) -> str:
        user_prompt = dedent(f"""
        项目名：{project_name}

        下面是 PRD Markdown：
        {prd_markdown}

        下面是 PRD JSON：
        {prd_json}

        请输出一份技术方案，必须包含：
        - Architecture Overview
        - MVP Scope
        - Module Boundaries
        - Data Flow
        - Suggested Repository Structure
        - API / Module Contracts
        - Tech Choices
        - Risks and Fallbacks
        - Phase 1 / Phase 2 Implementation Plan

        约束：
        1. 优先本地优先、少后端、易跑通。
        2. 假设操作者是 0 coding 经验产品经理。
        3. 不要过度设计。
        """)
        return self.llm.chat(model=self.model, system_prompt=ARCHITECT_PROMPT, user_prompt=user_prompt)
