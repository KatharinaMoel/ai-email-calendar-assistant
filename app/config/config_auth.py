"""Local Nylas hosted-auth helper for the Week 1 setup exercise."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from nylas import Client
from nylas.models.auth import CodeExchangeRequest, URLForAuthenticationConfig

load_dotenv()

PORT = 5010
app = FastAPI(title="Nylas setup")
sessions: dict[str, dict[str, str]] = {}
nylas = Client(
    api_key=os.environ.get("NYLAS_API_KEY", ""),
    api_uri=os.environ.get("NYLAS_API_URI", ""),
)


@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = os.urandom(16).hex()
        sessions[session_id] = {}
    request.state.session = sessions[session_id]
    response = await call_next(request)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=14 * 24 * 60 * 60,
        samesite="lax",
    )
    return response


async def get_grant_id(request: Request) -> str:
    grant_id = os.environ.get("NYLAS_GRANT_ID") or request.state.session.get("grant_id")
    if not grant_id:
        raise HTTPException(status_code=401, detail="Authenticate with Nylas first")
    return grant_id


@app.get("/oauth/exchange")
async def exchange_code(code: str, request: Request):
    exchange = nylas.auth.exchange_code_for_token(
        CodeExchangeRequest(
            redirect_uri=f"http://localhost:{PORT}/oauth/exchange",
            code=code,
            client_id=os.environ.get("NYLAS_CLIENT_ID", ""),
        )
    )
    request.state.session["grant_id"] = exchange.grant_id
    return RedirectResponse(url="/nylas/auth")


@app.get("/nylas/auth")
async def authenticate(request: Request):
    grant_id = os.environ.get("NYLAS_GRANT_ID") or request.state.session.get("grant_id")
    if grant_id:
        return {"grant_id": grant_id}
    url = nylas.auth.url_for_oauth2(
        URLForAuthenticationConfig(
            client_id=os.environ.get("NYLAS_CLIENT_ID", ""),
            redirect_uri=f"http://localhost:{PORT}/oauth/exchange",
        )
    )
    return RedirectResponse(url=url)


@app.get("/nylas/recent-emails")
async def recent_emails(grant_id: str = Depends(get_grant_id)):
    messages, _, _ = nylas.messages.list(grant_id)
    return [message.to_dict() for message in messages]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.config.config_auth:app", host="127.0.0.1", port=PORT, reload=True)
