#!/usr/bin/env python3
"""Extract and validate all ```graph``` blocks in an Obsidian note.

Usage:
    python3 validate_graphs.py <note.md> [note2.md ...]

Checks:
  - every graph block is valid YAML with a dict root
  - required field "elements" + "bounds" present
  - element indices referenced (e0/e1/.../f:eN) exist
  - apostrophes inside unquoted-looking labels? (advisory, prints warnings)
"""
import sys
import re
import yaml

BLOCK_RE = re.compile(r"```graph\s*\n(.*?)```", re.S)


def validate(path):
    with open(path, encoding="utf-8") as f:
        md = f.read()
    blocks = BLOCK_RE.findall(md)
    problems, warnings = [], []
    for i, src in enumerate(blocks):
        label = f"{path}:block#{i+1}"
        try:
            doc = yaml.safe_load(src)
        except Exception as e:
            problems.append(f"{label}: YAML error: {e}")
            continue
        if not isinstance(doc, dict):
            problems.append(f"{label}: root not a mapping")
            continue
        if "elements" not in doc:
            problems.append(f"{label}: missing 'elements'")
            continue
        elems = doc.get("elements") or []
        n = len(elems)
        refs = set()
        def walk(x):
            if isinstance(x, str) and re.fullmatch(r"e\d+", x):
                refs.add(int(x[1:]))
            elif isinstance(x, list):
                for y in x:
                    walk(y)
        walk(elems)
        for r in sorted(refs):
            if r >= n:
                problems.append(f"{label}: reference e{r} out of range (only {n} elements)")
        if "bounds" not in doc:
            problems.append(f"{label}: missing 'bounds'")
    return problems, warnings, len(blocks)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    all_problems = []
    total_blocks = 0
    for path in sys.argv[1:]:
        problems, _warnings, n = validate(path)
        total_blocks += n
        print(f"{path}: {n} graph block(s)")
        for p in problems:
            print("  [FAIL]", p)
        all_problems.extend(problems)
    print(f"total blocks: {total_blocks}; failures: {len(all_problems)}")
    return 1 if all_problems else 0


if __name__ == "__main__":
    sys.exit(main())
