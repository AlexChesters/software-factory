import argparse
import asyncio
import sys

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from software_factory.models import get_model_choice
from software_factory.outputs import write_output
from software_factory.prompts import get_prompt

TOOL_MODES = {
    "plan": ["Read", "Grep", "Glob"],
    "review": ["Read", "Grep", "Glob"],
    "execute": ["Read", "Grep", "Glob", "Write", "Bash(npm test)", "Bash(npm t)", "Bash(npm run lint)", "Bash(npm run *)"]
}

async def main(*, mode: str) -> None:
    task = sys.stdin.read()
    prompt = get_prompt(mode=mode)

    model_choice = get_model_choice(task=task)

    print(f"Model choice {model_choice.model_name} ({model_choice.effort}) for {mode} mode")

    options = ClaudeAgentOptions(
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
    args = parser.parse_args()

    asyncio.run(main(
        mode=args.mode
    ))
