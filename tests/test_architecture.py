"""The dependency rule from ARCHITECTURE.md and docs/adr/0002-modular-monolith.md, on every import.

A context imports only `shared`, `platform` and itself; `shared` and `platform` import no context
and no entry point. Inside a context, imports point inward only: handler -> service -> repo, and
infra -> app -> domain. Computation's `domain` imports only the standard library and `shared`, so
its formulas stay pure. Standard library `ast`, no dependency; `make lint` runs this file.
"""

import ast
import sys
from pathlib import Path

import pytest

PACKAGE = "evidence_meter"
SRC = Path(__file__).resolve().parent.parent / "src" / PACKAGE
CONTEXTS = ("collection", "definitions", "computation", "evidence_guard", "reporting")
KERNEL = ("shared", "platform")
# Outer to inner: a layer may import itself and the layers after it.
LAYERS = {
    "collection": ("handler", "service", "repo"),
    "definitions": ("handler", "service", "repo"),
    "computation": ("infra", "app", "domain"),
    "evidence_guard": ("handler", "service", "repo"),
    "reporting": ("handler", "service", "repo"),
}


def imported_modules(module: str, source: str) -> list[str]:
    """Absolute names of the modules `source` imports, with relative imports resolved."""
    package = module.split(".")
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = package[: len(package) - node.level] if node.level else []
            target = ".".join([*base, node.module] if node.module else base)
            found.append(target)
            found += [f"{target}.{alias.name}" for alias in node.names]
    return found


def violations(module: str, source: str) -> list[str]:
    """Each import of `module` that breaks the dependency rule, as `module -> imported`."""
    parts = module.split(".")
    top = parts[1] if len(parts) > 1 else ""
    layer = parts[2] if len(parts) > 2 else ""
    broken = []
    for name in imported_modules(module, source):
        target = name.split(".")
        if target[0] != PACKAGE:
            third_party = target[0] not in sys.stdlib_module_names
            if top == "computation" and layer == "domain" and third_party:
                broken.append(f"{module} -> {name}")
            continue
        other = target[1] if len(target) > 1 else ""
        other_layer = target[2] if len(target) > 2 else ""
        if top in CONTEXTS:
            allowed = other in (top, *KERNEL)
            if top == "computation" and layer == "domain":
                allowed = other in (top, "shared")
            if other == top and layer in LAYERS[top] and other_layer in LAYERS[top]:
                order = LAYERS[top]
                allowed = order.index(other_layer) >= order.index(layer)
        elif top in KERNEL:
            allowed = other in (top, *KERNEL) or other == ""
        else:
            allowed = True
        if not allowed:
            broken.append(f"{module} -> {name}")
    return sorted(set(broken))


def module_name(path: Path) -> str:
    # A package keeps its `__init__` part so relative imports resolve against the package itself.
    return ".".join(path.relative_to(SRC.parent).with_suffix("").parts)


@pytest.mark.parametrize(
    ("module", "source"),
    [
        ("evidence_meter.reporting.service", "from evidence_meter.computation import domain"),
        ("evidence_meter.collection.repo", "import evidence_meter.entrypoints.cli"),
        ("evidence_meter.shared", "from evidence_meter import definitions"),
        ("evidence_meter.platform.migrate", "from evidence_meter.reporting import repo"),
        ("evidence_meter.computation.domain", "import fastapi"),
        ("evidence_meter.computation.domain", "from evidence_meter.platform import migrate"),
        ("evidence_meter.computation.domain.formulas", "from ..infra import store"),
        ("evidence_meter.computation.app", "from evidence_meter.computation.infra import store"),
        ("evidence_meter.evidence_guard.repo.store", "from ..service import rules"),
        ("evidence_meter.definitions.service", "from evidence_meter.definitions.handler import x"),
    ],
)
def test_checker_reports_a_forbidden_import(module: str, source: str) -> None:
    assert violations(module, source), f"{module}: '{source}' should break the rule"


@pytest.mark.parametrize(
    ("module", "source"),
    [
        ("evidence_meter.reporting.handler", "from evidence_meter.reporting.service import pages"),
        ("evidence_meter.collection.service", "from evidence_meter.shared import Team"),
        ("evidence_meter.collection.repo", "from evidence_meter.platform import db"),
        ("evidence_meter.computation.infra.store", "from ..domain import formulas"),
        (
            "evidence_meter.computation.domain",
            "import statistics\nfrom evidence_meter.shared import Period",
        ),
        ("evidence_meter.entrypoints.cli", "from evidence_meter.reporting import handler"),
        ("evidence_meter.evidence_guard.service", "import fastapi"),
    ],
)
def test_checker_accepts_an_allowed_import(module: str, source: str) -> None:
    assert violations(module, source) == []


@pytest.mark.parametrize("context", CONTEXTS)
def test_every_context_has_its_package_layers_and_readme(context: str) -> None:
    folder = SRC / context
    missing = [
        str(path.relative_to(SRC))
        for path in [
            folder / "__init__.py",
            folder / "README.md",
            *(folder / layer / "__init__.py" for layer in LAYERS[context]),
        ]
        if not path.is_file()
    ]
    assert missing == []


@pytest.mark.parametrize("path", sorted(SRC.rglob("*.py")), ids=lambda p: str(p.relative_to(SRC)))
def test_source_follows_the_dependency_rule(path: Path) -> None:
    assert violations(module_name(path), path.read_text()) == []
