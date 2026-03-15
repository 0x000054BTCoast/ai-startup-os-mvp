from __future__ import annotations

import os
from textwrap import dedent

from src.agents.prompts import PRODUCT_MANAGER_JSON_PROMPT, PRODUCT_MANAGER_PROMPT
from src.core.llm import DeepSeekClient


class ProductManagerAgent:
    def __init__(self, llm: DeepSeekClient) -> None:
        self.llm = llm
        self.model = os.getenv("MODEL_PRODUCT", "deepseek-chat")

    def build_prd(self, goal: str, project_name: str) -> str:
        user_prompt = dedent(f"""
        项目名：{project_name}
        CEO 指令：{goal}

        请输出一份 implementation-ready PRD，必须包含以下章节：
        - Executive Summary
        - Background
        - Problem Statement
        - Goal
        - Non-goals
        - User Roles
        - Core Flows
        - Functional Requirements
        - Edge Cases
        - Acceptance Criteria
        - Dependencies
        - Open Questions

        要求：
        1. 使用清晰的 Markdown。
        2. 不要写技术实现细节。
        3. 明确未知项，不要假装已经确定。
        4. 写给 AI 架构师和 AI 工程师看。
        """)
        return self.llm.chat(model=self.model, system_prompt=PRODUCT_MANAGER_PROMPT, user_prompt=user_prompt)

    def build_prd_json(self, goal: str, project_name: str) -> dict:
        user_prompt = dedent(f"""
        请把下面需求转成严格 json。

        项目名：{project_name}
        CEO 指令：{goal}

        json schema:
        {{
          "project_name": "string",
          "background": "string",
          "problem_statement": "string",
          "goals": ["string"],
          "non_goals": ["string"],
          "user_roles": [{{"name": "string", "description": "string"}}],
          "core_flows": [{{"name": "string", "steps": ["string"]}}],
          "functional_requirements": [{{"id": "FR-1", "title": "string", "detail": "string"}}],
          "edge_cases": ["string"],
          "acceptance_criteria": ["string"],
          "dependencies": ["string"],
          "open_questions": ["string"]
        }}
        """)
        return self.llm.chat_json(model=self.model, system_prompt=PRODUCT_MANAGER_JSON_PROMPT, user_prompt=user_prompt)
