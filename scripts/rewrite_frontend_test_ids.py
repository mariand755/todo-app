from __future__ import annotations

from pathlib import Path
import re

ROOT = Path("frontend/src/test")
UNIT_FILES = sorted((ROOT / "unit").rglob("*.test.*"))
INTEGRATION_FILES = sorted((ROOT / "integration").rglob("*.test.*"))

IT_PATTERN = re.compile(r'^(\s*)(it(?:\.\w+)?)\(("|\")(.*?)(\3)(.*)$')
TITLE_PREFIX_PATTERN = re.compile(
    r"^@?(UT\d+|INT\d+|FUT\d+|FINT\d+|BUT\d+|BINT\d+)\s*\|\s*"
)
GENERATED_SUMMARY_COMMENT = re.compile(r"^\s*//\s*Checks that .*\.$")
GENERATED_ID_COMMENT = re.compile(
    r"^\s*//\s*@(?:UT\d+|INT\d+|FUT\d+|FINT\d+|BUT\d+|BINT\d+)\s*$"
)


def rewrite_files(files: list[Path], prefix: str) -> int:
    counter = 1
    for path in files:
        lines = path.read_text().splitlines()
        output: list[str] = []

        for line in lines:
            if GENERATED_SUMMARY_COMMENT.match(line) or GENERATED_ID_COMMENT.match(
                line
            ):
                continue

            match = IT_PATTERN.match(line)
            if not match:
                output.append(line)
                continue

            indent, it_call, quote, desc, _, suffix = match.groups()
            clean_desc = TITLE_PREFIX_PATTERN.sub("", desc).strip() or "test behavior"
            output.append(
                f"{indent}{it_call}({quote}@{prefix}{counter:02d} | {clean_desc}{quote}{suffix}"
            )
            counter += 1

        path.write_text("\n".join(output) + "\n")

    return counter - 1


def main() -> None:
    unit_count = rewrite_files(UNIT_FILES, "FUT")
    int_count = rewrite_files(INTEGRATION_FILES, "FINT")
    print(f"Updated {unit_count} frontend unit tests with FUT title IDs")
    print(f"Updated {int_count} frontend integration tests with FINT title IDs")


if __name__ == "__main__":
    main()
