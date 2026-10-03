"""Register the Week 1 message-created webhook with Nylas."""

import os

from dotenv import load_dotenv
from nylas import Client
from nylas.models.webhooks import CreateWebhookRequest, WebhookTriggers


def create_webhook():
    load_dotenv()
    server_url = os.environ.get("SERVER_URL", "").rstrip("/")
    email = os.environ.get("EMAIL", "")
    if not server_url.startswith("https://"):
        raise ValueError("SERVER_URL must be a public HTTPS URL")
    if not email:
        raise ValueError("EMAIL must be set")

    client = Client(
        api_key=os.environ.get("NYLAS_API_KEY", ""),
        api_uri=os.environ.get("NYLAS_API_URI", ""),
    )
    webhook, _, _ = client.webhooks.create(
        request_body=CreateWebhookRequest(
            trigger_types=[WebhookTriggers.MESSAGE_CREATED],
            webhook_url=f"{server_url}/events",
            description="AI Personal Assistant message webhook",
            notification_email_addresses=[email],
        )
    )
    return webhook


if __name__ == "__main__":
    created = create_webhook()
    print(created)
    print("Copy the returned webhook secret into NYLAS_WEBHOOK_SECRET in .env")
