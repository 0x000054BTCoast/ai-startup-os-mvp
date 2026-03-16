from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.router import StartupOSRouter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Startup OS MVP")
    parser.add_argument("--goal", required=True, help="CEO instruction, e.g. 为 PRD2Prototype 写 PRD 和技术方案")
    parser.add_argument("--project", default=None, help="project folder name")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    project_name = args.project or os.getenv("DEFAULT_PROJECT_NAME", "demo-project")

    router = StartupOSRouter()
    result = router.kickoff(goal=args.goal, project_name=project_name)

    print("\n=== Done ===")
    print(f"Project: {result.project_dir}")
    print(f"PRD: {result.prd_path}")
    print(f"PRD JSON: {result.prd_json_path}")
    print(f"Architecture: {result.architecture_path}")
    print(f"Dev Guide: {result.dev_plan_path}")


if __name__ == "__main__":
    main()
