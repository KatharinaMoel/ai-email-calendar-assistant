from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

"""
This script is like openai-quickstart.py, just pointed at GWDG Chat AI (Academic Cloud)
instead of OpenAI. GWDG offers an OpenAI-compatible API, so only the client
setup and the model name change.

Setup:
1. Get an API key for GWDG Chat AI. API docs and model names:
   https://docs.hpc.gwdg.de/services/ai-services/saia/index.html
2. Set ACADEMIC_CLOUD_API_KEY in your shell or in .env.
3. Optional: set GWDG_MODEL to another model name. To list the available
   models, run `uv run week2/gwdg-quickstart.py --models`.
"""

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()

api_key = os.getenv("ACADEMIC_CLOUD_API_KEY")
if not api_key:
    raise SystemExit("ACADEMIC_CLOUD_API_KEY is not set (shell or .env).")

model = os.getenv("GWDG_MODEL", "qwen3-30b-a3b-instruct-2507")

# --------------------------------------------------------------
# Initialize the client with the GWDG base URL
# --------------------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://chat-ai.academiccloud.de/v1",
    timeout=60,
)

if "--models" in sys.argv:
    for m in sorted(m.id for m in client.models.list().data):
        print(m)
    raise SystemExit

# --------------------------------------------------------------
# Introducing instructions
# --------------------------------------------------------------

"""
Inputs can be a single string or a list of messages.

The list of roles can be:
- system
- developer
- user
- assistant
"""

response = client.responses.create(
    model=model,
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)


# --------------------------------------------------------------
# Which would be similar to:
# --------------------------------------------------------------

response = client.responses.create(
    model=model,
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)
