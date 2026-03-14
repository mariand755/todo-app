from __future__ import annotations

from pathlib import Path
import re

TEST_FILES = sorted(Path("frontend/src/test").rglob("*.test.*"))

BROKEN_IT = re.compile(r'^(\s*)it\(("|\")(.*?)(\2),\s*$')


def main() -> None:
    fixed = 0
    for path in TEST_FILES:
        lines = path.read_text().splitlines()
        output: list[str] = []
        changed = False

        for line in lines:
            match = BROKEN_IT.match(line)
            if not match:
                output.append(line)
                continue

            indent, quote, desc, _ = match.groups()
            output.append(f"{indent}it({quote}{desc}{quote}, async () => {{")
            changed = True

        if changed:
            path.write_text("\n".join(output) + "\n")
            fixed += 1

    print(f"Repaired callback signatures in {fixed} frontend test files")


if __name__ == "__main__":
    main()
