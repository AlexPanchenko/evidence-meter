"""Structural lint for the Mermaid blocks of a SAD (C4 and sequence diagrams).

Usage: python3 -I lint_mermaid.py <file.md> [more.md ...]

Checks what breaks rendering silently or misleads a reader, without a browser: unmatched
fences, C4 element ids used before they are declared, boundary typos, unbalanced braces,
template placeholders, undeclared sequence participants and alt/end balance. A reply to the
actor after an `end` is a warning, not a failure: it is fine when it holds for every branch,
and only a reader can judge that (diagram honesty).
Exit 0 when every block passes (warnings allowed), 1 otherwise. Standard library only.
"""

import re
import sys

C4_DECL = re.compile(
    r"\b(Person|Person_Ext|System|System_Ext|SystemDb|Container|ContainerDb|ContainerQueue"
    r"|Container_Boundary|System_Boundary|Enterprise_Boundary)\((\w+)"
)
C4_REL = re.compile(r"\bRel\w*\((\w+),\s*(\w+)")
SEQ_DECL = re.compile(r"^\s*(?:participant|actor)\s+(\w+)", re.M)
SEQ_MSG = re.compile(r"^\s*(\w+)\s*-{1,2}>>?\+?-?\s*(\w+)\s*:", re.M)
PLACEHOLDER = re.compile(r'"<[^">]+>"|\(<[^)>]+>\)|:\s*<[^>]+>\s*$', re.M)


def lint_c4(block: str) -> list[str]:
    problems = []
    declared: set[str] = set()
    for line in block.splitlines():
        for _, ident in C4_DECL.findall(line):
            declared.add(ident)
        for src, dst in C4_REL.findall(line):
            for ident in (src, dst):
                if ident not in declared:
                    problems.append(f"Rel uses '{ident}' before it is declared")
    if re.search(r"Container_Bondary|ContainerBoundary|SystemBoundary\(", block):
        problems.append("boundary typo (needs Container_Boundary / System_Boundary)")
    if block.count("{") != block.count("}"):
        problems.append("unbalanced braces")
    return problems


def lint_sequence(block: str) -> tuple[list[str], list[str]]:
    problems: list[str] = []
    warnings: list[str] = []
    declared = set(SEQ_DECL.findall(block))
    for src, dst in SEQ_MSG.findall(block):
        for ident in (src, dst):
            if ident not in declared:
                problems.append(f"participant '{ident}' is not declared")
    opens = len(re.findall(r"^\s*(?:alt|opt|loop|par|critical|break)\b", block, re.M))
    ends = len(re.findall(r"^\s*end\b", block, re.M))
    if opens != ends:
        problems.append(f"{opens} blocks opened, {ends} closed")
    actors = set(re.findall(r"^\s*actor\s+(\w+)", block, re.M))
    lines = block.splitlines()
    last_end = max((i for i, ln in enumerate(lines) if re.match(r"^\s*end\b", ln)), default=None)
    if last_end is not None:
        for ln in lines[last_end + 1 :]:
            m = SEQ_MSG.match(ln)
            if m and m.group(2) in actors:
                warnings.append(
                    f"reply to actor '{m.group(2)}' after the last 'end': check it holds for every"
                    " branch, or move it inside each branch"
                )
                break
    return problems, warnings


def lint_file(path: str) -> int:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    failures = 0
    if text.count("```") % 2:
        print(f"{path}: unmatched code fence")
        failures += 1
    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    for n, block in enumerate(blocks, 1):
        kind = block.split(None, 1)[0] if block.strip() else "empty"
        warnings: list[str] = []
        if kind.startswith("C4"):
            problems = lint_c4(block)
        elif kind == "sequenceDiagram":
            problems, warnings = lint_sequence(block)
        else:
            problems = []
        if PLACEHOLDER.search(block):
            problems.append("template placeholder left in the block")
        status = "ok" if not problems else "FAIL"
        print(f"{path}: block {n} ({kind}): {status}")
        for p in problems:
            print(f"  - {p}")
        for w in warnings:
            print(f"  ! warning: {w}")
        failures += bool(problems)
    if not blocks:
        print(f"{path}: no mermaid blocks")
    return failures


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    return 1 if sum(lint_file(p) for p in argv) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
