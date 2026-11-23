import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from software_factory.models import get_model_choice
from software_factory.outputs import write_output
from software_factory.prompts import get_prompt

TOOL_MODES = {
    "plan": ["Read", "Grep", "Glob"],
    "review": ["Read", "Grep", "Glob"],
    "execute": ["Read", "Grep", "Glob", "Write", "Bash(npm test)", "Bash(npm t)", "Bash(npm run lint)", "Bash(npm run *)"]
}

async def main(*, mode: str, repo_dir: Path) -> None:
    task = sys.stdin.read()
    prompt = get_prompt(mode=mode)

    model_choice = get_model_choice(task=task)

    print(f"Model choice {model_choice.model_name} ({model_choice.effort}) for {mode} mode")

    options = ClaudeAgentOptions(
        cwd=repo_dir,
        extra_args={"restricted": None},
        tools=TOOL_MODES[mode],
        model=model_choice.model_name,
        effort=model_choice.effort,
        system_prompt={"type": "preset", "preset": "claude_code", "append": prompt},
        permission_mode="acceptEdits"
    )

    async for message in query(prompt=task, options=options):
        if isinstance(message, ResultMessage):
            if message.is_error:
                raise SystemExit(message.result or message.subtype)

            write_output(output=message.result or "")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["plan", "execute", "review"], required=True)
    parser.add_argument("--repo-dir", type=Path, default=Path.cwd(), help="Repository for Claude to work in")
    args = parser.parse_args()
    repo_dir = args.repo_dir.resolve()
    if not repo_dir.is_dir():
        parser.error(f"repository directory does not exist: {repo_dir}")

    asyncio.run(main(
        mode=args.mode,
        repo_dir=repo_dir,
    ))
