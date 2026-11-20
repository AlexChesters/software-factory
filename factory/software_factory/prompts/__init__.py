from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

def get_prompt(*, mode: str) -> str:
    with open(CURRENT_DIR / f"{mode}.md", "r", encoding="utf-8") as f:
        return f.read()
