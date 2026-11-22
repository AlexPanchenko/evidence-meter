"""The backend API. Health only until a feature serves data; binds to 127.0.0.1 (docs/adr/0004)."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from evidence_meter import __version__

app = FastAPI(title="Evidence Meter", version=__version__)


@app.exception_handler(HTTPException)
async def error_envelope(_: Request, exc: HTTPException) -> JSONResponse:
    """Every error leaves the API as {"error": {"code", "message"}}."""
    code = {404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
    body = {"error": {"code": code, "message": str(exc.detail)}}
    return JSONResponse(status_code=exc.status_code, content=body)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
