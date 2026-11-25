from pathlib import Path

SKILLS_ROOT = (
    Path(__file__).resolve().parents[3] / "plugins" / "software-factory" / "skills"
)


def get_prompt(*, mode: str) -> str:
    return (SKILLS_ROOT / mode / "references" / "prompt.md").read_text(encoding="utf-8")
