from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = CURRENT_DIR / ".." / ".." / "outputs"

def write_output(*, output: str):
    OUTPUTS_DIR.mkdir(exist_ok=False)

    with open (OUTPUTS_DIR / "output.md", "w", encoding="utf-8") as f:
        f.write(output)
