"""Top-level model for Nylas webhook events."""

from typing import Any

from pydantic import BaseModel


class WebhookEvent(BaseModel):
    specversion: str
    type: str
    source: str
    id: str
    time: int
    webhook_delivery_attempt: int
    data: dict[str, Any]
