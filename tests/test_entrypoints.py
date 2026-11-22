"""Smoke tests: the CLI and the API start. No business behaviour exists yet."""

import pytest
from fastapi.testclient import TestClient

from evidence_meter.entrypoints import cli
from evidence_meter.entrypoints.api import app


def test_cli_help_exits_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as stopped:
        cli.main(["--help"])
    assert stopped.value.code == 0
    assert "evidence-meter" in capsys.readouterr().out


def test_cli_without_a_command_prints_help_and_succeeds(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main([]) == 0
    assert "usage" in capsys.readouterr().out


def test_api_health_answers_ok() -> None:
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_unknown_route_uses_the_error_envelope() -> None:
    response = TestClient(app).get("/no-such-route")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Not Found"}}
