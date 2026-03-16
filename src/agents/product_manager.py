from __future__ import annotations

import os
from textwrap import dedent

from src.agents.prompts import PRODUCT_MANAGER_JSON_PROMPT, PRODUCT_MANAGER_PROMPT
from src.core.llm import DeepSeekClient


class ProductManagerAgent:
    def __init__(self, llm: DeepSeekClient) -> None:
        self.llm = llm
        self.model = os.getenv("MODEL_PRODUCT", "deepseek-chat")

    def build_prd(self, idea: dict, project_name: str) -> str:
        user_prompt = dedent(f"""
        项目名：{project_name}
        结构化 idea：{idea}

        请输出高级产品经理级别 PRD，必须包含以下章节：
        - Product Vision
        - User Scenarios
        - Functional Requirements
        - Non-functional Requirements
        - System Boundaries
        - Open Questions（每个问题必须包含唯一 [QUESTION_ID: PMQ-xxx]）
        - Implementation Suggestions
        - Prototype Description（Page Structure / UI Modules / Interaction Flow）

        要求：
        1. 使用清晰 Markdown，给架构与工程 agent 直接消费。
        2. 不要把未知项写成已确定事实。
        3. 必须输出至少 3 条 open questions。
        """)
        return self.llm.chat(model=self.model, system_prompt=PRODUCT_MANAGER_PROMPT, user_prompt=user_prompt)

    def build_prd_json(self, idea: dict, project_name: str) -> dict:
        user_prompt = dedent(f"""
        请把下面需求转成“完整 PRD 结构化 JSON”，不是仅保留 idea 摘要。

        项目名：{project_name}
        idea：{idea}

        json schema:
        {{
          "project_name": "string",
          "idea": {{
            "title": "string",
            "summary": "string",
            "details": "string",
            "requirements": ["string"],
            "unknowns": ["string"]
          }},
          "product_vision": "string",
          "user_scenarios": [
            {{
              "id": "US-001",
              "role": "string",
              "scenario": "string",
              "success_criteria": ["string"]
            }}
          ],
          "functional_requirements": [
            {{
              "id": "FR-001",
              "title": "string",
              "description": "string",
              "priority": "P0|P1|P2",
              "acceptance_criteria": ["string"]
            }}
          ],
          "non_functional_requirements": [
            {{
              "id": "NFR-001",
              "category": "performance|security|usability|reliability|maintainability|other",
              "description": "string",
              "metric": "string"
            }}
          ],
          "system_boundaries": {{
            "in_scope": ["string"],
            "out_of_scope": ["string"],
            "external_dependencies": ["string"]
          }},
          "open_questions": [
            {{
              "question_id": "PMQ-001",
              "question": "string",
              "impact": "string",
              "blocking": true
            }}
          ],
          "implementation_suggestions": [
            {{
              "area": "string",
              "suggestion": "string",
              "rationale": "string"
            }}
          ],
          "prototype_description": {{
            "page_structure": [
              {{"page": "string", "purpose": "string"}}
            ],
            "ui_modules": [
              {{"module": "string", "responsibility": "string"}}
            ],
            "interaction_flow": [
              {{"name": "string", "steps": ["string"]}}
            ]
          }},
          "risks": ["string"],
          "assumptions": ["string"]
        }}

        输出要求：
        1) 只输出合法 JSON，不要 Markdown。
        2) 所有数组字段必须存在（无内容时用空数组）。
        3) open_questions 必须保留 question_id，格式 PMQ-xxx。
        """)
        return self.llm.chat_json(model=self.model, system_prompt=PRODUCT_MANAGER_JSON_PROMPT, user_prompt=user_prompt)

    def answer_question_update_prd(self, prd_text: str, question_id: str, answer: str) -> str:
        user_prompt = dedent(f"""
        你会收到已有 PRD、一个 question_id 以及 CEO 的回答。
        请把回答合并进 PRD 并更新相关章节，保留所有 QUESTION_ID。

        question_id: {question_id}
        answer: {answer}

        原始 PRD:
        {prd_text}
        """)
        return self.llm.chat(model=self.model, system_prompt=PRODUCT_MANAGER_PROMPT, user_prompt=user_prompt)
