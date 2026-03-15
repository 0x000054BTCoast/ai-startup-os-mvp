from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.agents.architect import ArchitectAgent
from src.agents.engineer import EngineerAgent
from src.agents.product_manager import ProductManagerAgent
from src.core.llm import DeepSeekClient
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

    def kickoff(self, *, goal: str, project_name: str, base_dir: str = "projects") -> RunResult:
        project_dir = ensure_dir(Path(base_dir) / project_name)
        prd_dir = ensure_dir(project_dir / "prd")
        arch_dir = ensure_dir(project_dir / "architecture")
        reports_dir = ensure_dir(project_dir / "reports")

        prd_md = self.pm.build_prd(goal=goal, project_name=project_name)
        prd_json = self.pm.build_prd_json(goal=goal, project_name=project_name)
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

        return RunResult(
            project_dir=project_dir,
            prd_path=prd_path,
            prd_json_path=prd_json_path,
            architecture_path=architecture_path,
            dev_plan_path=dev_plan_path,
        )
