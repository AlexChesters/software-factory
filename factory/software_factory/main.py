import argparse
import asyncio
import sys
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from software_factory.models import DEFAULT_EFFORT, ModelChoice, get_model_choice
from software_factory.outputs import write_output
from software_factory.prompts import get_prompt

READ_TOOLS = ["Read", "Grep", "Glob"]
WRITE_TOOLS = ["Read", "Grep", "Glob", "Write", "Bash(npm test)", "Bash(npm t)", "Bash(npm run lint)", "Bash(npm run *)"]

TOOL_MODES = {
    "plan": READ_TOOLS,
    "review": READ_TOOLS,
    "execute": WRITE_TOOLS,
    "revise": WRITE_TOOLS
}

async def main(
    *, mode: str, repo_dir: Path, model: str | None = None, effort: str | None = None
) -> None:
    task = sys.stdin.read()
    prompt = get_prompt(mode=mode)

    if model:
        model_choice = ModelChoice(model_name=model, effort=effort or DEFAULT_EFFORT)
    else:
        model_choice = get_model_choice(task=task)

    print(f"Model choice {model_choice.model_name} ({model_choice.effort}) for {mode} mode")

    options = ClaudeAgentOptions(
        cwd=repo_dir,
        extra_args={"restricted": None},
        tools=TOOL_MODES[mode],
        model=model_choice.model_name,
        effort=model_choice.effort,
        system_prompt={"type": "preset", "preset": "claude_code", "append": prompt},
        permission_mode="acceptEdits",
        max_budget_usd=1
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
    parser.add_argument("--model", help="Claude model to use instead of TypeSafe model selection")
    parser.add_argument("--effort", help=f"Effort level for an explicit model (default: {DEFAULT_EFFORT})")
    args = parser.parse_args()
    if args.effort and not args.model:
        parser.error("--effort cannot be specified without --model")

    repo_dir = args.repo_dir.resolve()
    if not repo_dir.is_dir():
        parser.error(f"repository directory does not exist: {repo_dir}")

    asyncio.run(main(
        mode=args.mode,
        repo_dir=repo_dir,
        model=args.model or None,
        effort=args.effort or None,
    ))
