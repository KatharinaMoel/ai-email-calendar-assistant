import json
import os
import sys
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from nylas import Client
from openai import OpenAI
from pydantic import BaseModel, Field

sys.path.append(str(Path(__file__).resolve().parent.parent))  # allow importing schemas

from schemas.nylas_email_schema import EmailObject
from schemas.nylas_webhook_schema import WebhookEvent

load_dotenv()

EVENTS_DIR = Path(__file__).resolve().parent.parent.parent / "requests" / "events"

PROMPT = "Classify the email as spam or not_spam."


class EmailCategory(str, Enum):
    SPAM = "spam"
    NOT_SPAM = "not_spam"


class Classification(BaseModel):
    category: EmailCategory
    confidence: float = Field(ge=0, le=1, description="Confidence score for the category")


# --------------------------------------------------------------
# Step 1: Load a saved event
# --------------------------------------------------------------


def load_email(event_id: str) -> EmailObject:
    with open(EVENTS_DIR / f"{event_id}.json") as f:
        event = WebhookEvent(**json.load(f))
    return EmailObject(**event.data["object"])


# --------------------------------------------------------------
# Step 2: Only process emails sent from your own address
# --------------------------------------------------------------


def is_from_me(email: EmailObject) -> bool:
    return email.from_[0].email == os.getenv("EMAIL")


# --------------------------------------------------------------
# Step 3: Classify with an LLM
# --------------------------------------------------------------


def classify(email: EmailObject) -> Classification:
    response = OpenAI().responses.parse(
        model="gpt-4o-mini",
        instructions=PROMPT,
        input=f"From: {email.from_[0].email}\nSubject: {email.subject}\n\n{email.body}",
        text_format=Classification,
    )
    return response.output_parsed


# --------------------------------------------------------------
# Step 4: Delete spam after confirmation
# --------------------------------------------------------------


def delete_email(email: EmailObject) -> None:
    nylas = Client(
        api_key=os.environ.get("NYLAS_API_KEY", ""),
        api_uri=os.environ.get("NYLAS_API_URI", ""),
    )
    nylas.messages.destroy(identifier=email.grant_id, message_id=email.id)


def run(event_id: str) -> None:
    email = load_email(event_id)

    if not is_from_me(email):
        print(f"Skipping email from {email.from_[0].email}")
        return

    result = classify(email)
    print(f"Subject: {email.subject}")
    print(f"Category: {result.category.value} (confidence {result.confidence:.2f})")

    if result.category != EmailCategory.SPAM:
        return

    if input("Delete this email? [y/N] ").strip().lower() == "y":
        delete_email(email)
        print("Deleted.")
    else:
        print("Kept.")


if __name__ == "__main__":
    run(sys.argv[1])  # event id: a file name in requests/events/ without .json
