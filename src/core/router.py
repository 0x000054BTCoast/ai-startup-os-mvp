from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.agents.architect import ArchitectAgent
from src.agents.engineer import EngineerAgent
from src.agents.product_manager import ProductManagerAgent
from src.core.idea_parser import IdeaParser
from src.core.llm import DeepSeekClient
from src.core.logger import CoreLogger
from src.utils.files import ensure_dir, write_json, write_text


@dataclass
class RunResult:
    project_dir: Path
    prd_path: Path
    prd_json_path: Path
    architecture_path: Path
    dev_plan_path: Path


class StartupOSRouter:
    def __init__(self) -> None:
        self.llm = DeepSeekClient()
        self.pm = ProductManagerAgent(self.llm)
        self.architect = ArchitectAgent(self.llm)
        self.engineer = EngineerAgent(self.llm)
        self.logger = CoreLogger()
        self.current_project: str | None = None

    def create_project(self, project_name: str, base_dir: str = "projects") -> Path:
        project_dir = ensure_dir(Path(base_dir) / project_name)
        for d in ["prd", "architecture", "reports", "notes"]:
            ensure_dir(project_dir / d)
        self.logger.log(request={"action": "create_project", "project_name": project_name}, response={"project_dir": str(project_dir)})
        return project_dir

    def jump_into_project(self, project_name: str, base_dir: str = "projects") -> Path:
        project_dir = ensure_dir(Path(base_dir) / project_name)
        self.current_project = project_name
        self.logger.log(request={"action": "jump_into_project", "project_name": project_name}, response={"project_dir": str(project_dir)})
        return project_dir

    def kickoff(self, *, goal: str, project_name: str, base_dir: str = "projects") -> RunResult:
        request = {"action": "kickoff", "goal": goal, "project_name": project_name}
        try:
            project_dir = self.create_project(project_name, base_dir)
            prd_dir = ensure_dir(project_dir / "prd")
            arch_dir = ensure_dir(project_dir / "architecture")
            reports_dir = ensure_dir(project_dir / "reports")

            idea = IdeaParser.parse_input(goal)
            prd_md = self.pm.build_prd(idea=idea, project_name=project_name)
            prd_json = self.pm.build_prd_json(idea=idea, project_name=project_name)
            architecture_md = self.architect.build_architecture(prd_markdown=prd_md, prd_json=prd_json, project_name=project_name)
            dev_plan_md = self.engineer.build_dev_plan(prd_markdown=prd_md, architecture_markdown=architecture_md, project_name=project_name)

            prd_path = prd_dir / "prd_full.md"
            prd_json_path = prd_dir / "prd_structured.json"
            architecture_path = arch_dir / "technical_design.md"
            dev_plan_path = reports_dir / "dev_execution_guide.md"

            write_text(prd_path, prd_md)
            write_json(prd_json_path, prd_json)
            write_text(architecture_path, architecture_md)
            write_text(dev_plan_path, dev_plan_md)
            result = RunResult(project_dir, prd_path, prd_json_path, architecture_path, dev_plan_path)
            self.logger.log(request=request, response={"project_dir": str(project_dir), "prd": str(prd_path)})
            return result
        except Exception as exc:
            self.logger.log(request=request, error=str(exc))
            raise

    def brainstorm_with(self, *, agent: str, message: str, project_name: str) -> str:
        prompt = f"项目名: {project_name}\n用户问题: {message}\n仅做讨论，不写文件。"
        request = {"action": "brainstorm", "agent": agent, "project_name": project_name, "message": message}
        try:
            key = agent.lower()
            if "product" in key or key == "pm":
                answer = self.pm.llm.chat(model=self.pm.model, system_prompt="你是资深产品经理，进行头脑风暴。", user_prompt=prompt)
            elif "architect" in key:
                answer = self.architect.llm.chat(model=self.architect.model, system_prompt="你是资深架构师，进行头脑风暴。", user_prompt=prompt)
            elif "engineer" in key:
                answer = self.engineer.llm.chat(model=self.engineer.model, system_prompt="你是资深工程师，进行头脑风暴。", user_prompt=prompt)
            else:
                raise ValueError(f"Unsupported agent: {agent}")
            self.logger.log(request=request, response=answer[:500])
            return answer
        except Exception as exc:
            self.logger.log(request=request, error=str(exc))
            raise

    def answer_open_question(self, *, project_name: str, question_id: str, answer: str, base_dir: str = "projects") -> Path:
        request = {"action": "answer_open_question", "project": project_name, "question_id": question_id, "answer": answer}
        try:
            prd_path = Path(base_dir) / project_name / "prd" / "prd_full.md"
            if not prd_path.exists():
                raise FileNotFoundError(f"PRD not found: {prd_path}")
            prd_text = prd_path.read_text(encoding="utf-8")
            if question_id not in prd_text:
                raise ValueError(f"Question ID not found: {question_id}")

            updated = self.pm.answer_question_update_prd(prd_text=prd_text, question_id=question_id, answer=answer)
            append_text = f"\n\n[CEO_ANSWER:{question_id}]\n{answer}\n"
            if append_text not in updated:
                updated += append_text
            write_text(prd_path, updated)
            self.logger.log(request=request, response={"prd_path": str(prd_path)})
            return prd_path
        except Exception as exc:
            self.logger.log(request=request, error=str(exc))
            raise

    def generate_codex_prompt(self, *, project_name: str, module: str | None = None, doc: str | None = None) -> str:
        request = {"action": "generate_codex_prompt", "project": project_name, "module": module, "doc": doc}
        try:
            output = self.engineer.generate_codex_prompt(project_name=project_name, module=module, doc=doc)
            self.logger.log(request=request, response=output[:500])
            return output
        except Exception as exc:
            self.logger.log(request=request, error=str(exc))
            raise
