"""FastAPI application for receiving and inspecting Nylas webhooks."""

from __future__ import annotations

import hashlib
import hmac
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

from app.schemas.nylas_email_schema import EmailObject
from app.schemas.nylas_webhook_schema import WebhookEvent

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

app = FastAPI(title="AI Personal Assistant")
templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")
webhooks: list[EmailObject] = []


def verify_signature(message: bytes, key: bytes, signature: str | None) -> bool:
    """Verify the HMAC-SHA256 signature attached to a Nylas webhook."""
    if not key or not signature:
        return False
    digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def store_event_json(event: WebhookEvent) -> Path:
    """Persist a raw event locally so learners can inspect its shape."""
    events_dir = PROJECT_ROOT / "requests" / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    path = events_dir / f"{uuid.uuid4()}.json"
    path.write_text(event.model_dump_json(indent=2), encoding="utf-8")
    return path


@app.api_route("/events", methods=["GET", "POST"])
async def webhook(request: Request, x_nylas_signature: str | None = Header(default=None)):
    """Answer Nylas challenges and receive signed message events."""
    if request.method == "GET":
        challenge = request.query_params.get("challenge")
        if challenge:
            return PlainTextResponse(challenge)
        return PlainTextResponse("No challenge", status_code=status.HTTP_400_BAD_REQUEST)

    body = await request.body()
    secret = os.environ.get("NYLAS_WEBHOOK_SECRET") or os.environ.get("WEBHOOK_SECRET", "")
    if not verify_signature(body, secret.encode("utf-8"), x_nylas_signature):
        return PlainTextResponse("Signature verification failed", status_code=401)

    try:
        event = WebhookEvent.model_validate_json(body)
        email = EmailObject.model_validate(event.data["object"])
    except (KeyError, ValueError) as exc:
        return PlainTextResponse(f"Invalid event data: {exc}", status_code=400)

    store_event_json(event)
    webhooks.append(email)
    return PlainTextResponse("Webhook received", status_code=200)


@app.get("/")
def index(request: Request):
    """Show email events received during the current local session."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"webhooks": webhooks},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
