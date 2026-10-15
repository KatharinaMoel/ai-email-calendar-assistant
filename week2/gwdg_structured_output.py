import json
import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

"""
This script is structured_output.py pointed at GWDG Chat AI (Academic Cloud)
instead of OpenAI. See gwdg-quickstart.py for the setup.
"""

load_dotenv()

api_key = os.getenv("ACADEMIC_CLOUD_API_KEY")
if not api_key:
    raise SystemExit("ACADEMIC_CLOUD_API_KEY is not set (shell or .env).")

model = os.getenv("GWDG_MODEL", "qwen3-30b-a3b-instruct-2507")

client = OpenAI(
    api_key=api_key,
    base_url="https://chat-ai.academiccloud.de/v1",
    timeout=120,
)

# --------------------------------------------------------------
# Using a JSON Schema
# --------------------------------------------------------------

response = client.responses.create(
    model=model,
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "date": {"type": "string"},
                    "participants": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "date", "participants"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
)

event = json.loads(response.output_text)
print(event)

# --------------------------------------------------------------
# Using a Pydantic model (and simple response format)
# --------------------------------------------------------------


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]


response = client.responses.parse(
    model=model,
    input="Alice and Bob are going to a science fair on Friday",
    instructions="Extract the event information",
    text_format=CalendarEvent,
)

response_model = response.output_parsed

print(type(response_model))
print(response_model.model_dump_json(indent=2))
