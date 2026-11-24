"""Static self-check of a feature's contract folder (contract-builder step 11).

Usage: python3 -I check_contract.py docs/features/<slug>/contracts
Exit 0 when there are no findings, 1 otherwise. Standard library only.

Checks: the report starts with a valid Verdict; every refusal code in the contract is in the
feature's closed list (an ADR line "Codes: ...") or named in the report's Deferrals; exit codes are
unique and include 0; every field-origin row has an origin; no person-data word appears outside a
negation; a "# stale" mark only with a FAIL verdict.
"""

import re
import sys
from pathlib import Path

VERDICTS = ("PASS (with deferrals)", "PASS", "FAIL")
PERSON_WORDS = re.compile(
    r"\b(assignees?|authors?|reporters?|e-?mails?|user_?ids?|usernames?|logins?)\b", re.I
)
NEGATION = re.compile(r"\b(drop|dropped|never|no|not|nothing|refus\w*)\b", re.I)
CODE = re.compile(r"`([a-z]+(?:_[a-z]+)+)`")


def report_path(contracts: Path) -> Path | None:
    for name in ("contract-report.md", "api-sync-report.md"):
        if (contracts / name).is_file():
            return contracts / name
    return None


def adr_dir(contracts: Path) -> Path:
    """The nearest adr/ above the contracts folder (an --out-dir run sits one level deeper)."""
    for parent in contracts.resolve().parents:
        if (parent / "adr").is_dir():
            return parent / "adr"
    return contracts.parent / "adr"


def closed_list(adrs: Path) -> set[str]:
    codes: set[str] = set()
    for adr in sorted(adrs.glob("*.md")):
        text = adr.read_text(encoding="utf-8")
        for match in re.finditer(r"Codes:(.*?)(?:\n\n|\Z)", text, re.S):
            codes.update(CODE.findall(match.group(1)))
    return codes


def section(text: str, title: str) -> str:
    match = re.search(rf"^#+ [^\n]*{re.escape(title)}[^\n]*\n(.*?)(?=^#+ |\Z)", text, re.S | re.M)
    return match.group(1) if match else ""


def contract_codes(text: str) -> set[str]:
    codes = set(re.findall(r"Refused: ([a-z_]+):", text))
    checks = re.findall(r"^#+ Checks, in order[^\n]*\n(.*?)(?=^#+ |\Z)", text, re.S | re.M)
    for line in "\n".join(checks).splitlines():
        if re.match(r"\|\s*\d+\s*\|", line):
            codes.update(CODE.findall(line.split("|")[3]))
    return codes


def check(contracts: Path) -> list[str]:
    findings: list[str] = []
    report = report_path(contracts)
    if report is None:
        return [f"{contracts}: no contract-report.md or api-sync-report.md"]
    report_text = report.read_text(encoding="utf-8")
    verdict_line = next(
        (ln for ln in report_text.splitlines() if ln.startswith("**Verdict:**")), ""
    )
    verdict = verdict_line.removeprefix("**Verdict:**").strip()
    if verdict not in VERDICTS:
        findings.append(
            f"{report.name}: first Verdict line is {verdict!r}, expected one of {VERDICTS}"
        )

    deferrals = section(report_text, "Deferrals")
    allowed = closed_list(adr_dir(contracts))
    contract_files = [
        p for p in sorted(contracts.iterdir()) if p.suffix in (".md", ".yaml") and p != report
    ]
    for path in contract_files:
        text = path.read_text(encoding="utf-8")
        for code in sorted(contract_codes(text) - allowed):
            if code not in deferrals:
                findings.append(
                    f"{path.name}: refusal code {code!r} is not in the ADR closed list or Deferrals"
                )
        exits = [int(m) for m in re.findall(r"^\|\s*(\d)\s*\|", section(text, "Exit codes"), re.M)]
        if exits and (0 not in exits or len(exits) != len(set(exits))):
            findings.append(f"{path.name}: exit codes {exits} must be unique and include 0")
        for number, line in enumerate(text.splitlines(), 1):
            if PERSON_WORDS.search(line) and not NEGATION.search(line):
                findings.append(
                    f"{path.name}:{number}: person-data word outside a negation: "
                    f"{line.strip()[:80]}"
                )
            if "# stale" in line and verdict != "FAIL":
                findings.append(
                    f"{path.name}:{number}: '# stale' field with verdict {verdict!r}; expected FAIL"
                )

    for line in section(report_text, "Field origins").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        is_row = line.startswith("|") and len(cells) >= 2 and not set(cells[0]) <= set("-: ")
        if is_row and cells[0] not in ("schema_path", "path") and cells[1] in ("", "?", "-"):
            findings.append(f"{report.name}: field {cells[0]!r} has no origin")
    return findings


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    findings = check(Path(argv[1]))
    for finding in findings:
        print(finding)
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
