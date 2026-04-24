"""Optional judge helper for future hosted rubric evaluation."""

from pathlib import Path


def load_rubric(name="code_review.md"):
    rubric_path = Path(__file__).resolve().parents[1] / "rubrics" / name
    return rubric_path.read_text()


if __name__ == "__main__":
    print(
        "This demo keeps the active eval gate deterministic. "
        "Loaded rubric follows.\n"
    )
    print(load_rubric())
