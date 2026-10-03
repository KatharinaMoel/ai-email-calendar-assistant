"""Models for the Nylas message fields used by the Week 1 application."""

from pydantic import BaseModel, Field


class Sender(BaseModel):
    email: str
    name: str | None = None


class Attachment(BaseModel):
    content_disposition: str | None = None
    content_id: str | None = None
    content_type: str
    filename: str
    grant_id: str
    id: str
    is_inline: bool = False
    size: int


class EmailObject(BaseModel):
    attachments: list[Attachment] = Field(default_factory=list)
    bcc: list[Sender] = Field(default_factory=list)
    body: str = ""
    cc: list[Sender] = Field(default_factory=list)
    date: int
    folders: list[str] = Field(default_factory=list)
    from_: list[Sender] = Field(default_factory=list, alias="from")
    grant_id: str
    id: str
    object: str
    reply_to: list[Sender] = Field(default_factory=list)
    snippet: str = ""
    starred: bool = False
    subject: str = ""
    thread_id: str
    to: list[Sender] = Field(default_factory=list)
    unread: bool = False
