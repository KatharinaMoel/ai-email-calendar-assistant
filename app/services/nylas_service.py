"""Small wrapper around the Nylas operations used by the assistant."""

from __future__ import annotations

import os

from nylas import Client

from app.schemas.nylas_email_schema import EmailObject


class NylasService:
    def __init__(self) -> None:
        self.client = Client(
            api_key=os.environ.get("NYLAS_API_KEY", ""),
            api_uri=os.environ.get("NYLAS_API_URI", ""),
        )

    def download_first_attachment(self, email: EmailObject) -> dict[str, bytes | str]:
        if not email.attachments:
            raise ValueError("The email has no attachments")
        attachment = email.attachments[0]
        content = self.client.attachments.download_bytes(
            identifier=attachment.grant_id,
            attachment_id=attachment.id,
            query_params={"message_id": email.id},
        )
        return {"content": content, "content_type": attachment.content_type, "filename": attachment.filename}

    def send_email(self, grant_id: str, to: list[str], subject: str, body: str):
        request_body = {
            "to": [{"email": address} for address in to],
            "subject": subject,
            "body": body,
        }
        return self.client.messages.send(grant_id, request_body=request_body)

    def delete_email(self, email: EmailObject):
        return self.client.messages.destroy(identifier=email.grant_id, message_id=email.id)
