from __future__ import annotations

from pathlib import Path
import re

ROOT = Path("backend/tests")
UNIT_FILES = sorted((ROOT / "unit").glob("test_*.py"))
INTEGRATION_FILES = sorted((ROOT / "integration").glob("test_*.py"))


def ensure_import_pytest(lines: list[str]) -> list[str]:
    if any(re.match(r"^\s*import\s+pytest\b", line) for line in lines):
        return lines

    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("from __future__ import"):
            insert_idx = i + 1

    i = insert_idx
    while i < len(lines):
        line = lines[i]
        if line.startswith("import ") or line.startswith("from ") or line.strip() == "":
            if line.startswith("import ") or line.startswith("from "):
                insert_idx = i + 1
            i += 1
            continue
        break

    lines.insert(insert_idx, "import pytest")
    return lines


def rewrite_files(files: list[Path], prefix: str) -> int:
    test_def = re.compile(
        r"^(\s*)def\s+test_(?:UT\d+_|INT\d+_|BUT\d+_|BINT\d+_)?([A-Za-z0-9_]+)(\s*\()"
    )
    test_mark = re.compile(r"^\s*@pytest\.mark\.(UT\d+|INT\d+|BUT\d+|BINT\d+)\s*$")

    counter = 1
    for path in files:
        lines = ensure_import_pytest(path.read_text().splitlines())
        output: list[str] = []

        i = 0
        while i < len(lines):
            line = lines[i]

            # Always drop existing ID markers and rebuild them from scratch.
            if test_mark.match(line):
                i += 1
                continue

            if line.strip().startswith("@pytest.fixture"):
                output.append(line)
                i += 1
                continue

            match = test_def.match(line)
            if match:
                # Do not tag fixture functions even if they start with test_.
                prev_non_empty = ""
                for prev_line in reversed(output):
                    if prev_line.strip():
                        prev_non_empty = prev_line.strip()
                        break
                if prev_non_empty.startswith("@pytest.fixture"):
                    line = test_def.sub(r"\1def test_\2\3", line)
                    output.append(line)
                    i += 1
                    continue

                marker = f"@pytest.mark.{prefix}{counter:02d}"
                output.append(marker)

                line = test_def.sub(r"\1def test_\2\3", line)
                output.append(line)
                counter += 1
                i += 1
                continue

            output.append(line)
            i += 1

        path.write_text("\n".join(output) + "\n")

    return counter - 1


def main() -> None:
    unit_count = rewrite_files(UNIT_FILES, "BUT")
    int_count = rewrite_files(INTEGRATION_FILES, "BINT")
    print(f"Updated {unit_count} backend unit tests with BUT markers")
    print(f"Updated {int_count} backend integration tests with BINT markers")


if __name__ == "__main__":
    main()
