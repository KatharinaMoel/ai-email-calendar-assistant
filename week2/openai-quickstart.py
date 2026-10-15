from openai import OpenAI
from dotenv import load_dotenv
import os

"""
This script demonstrates how to generate a response using the OpenAI API.
"""

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()

# --------------------------------------------------------------
# Initialize OpenAI client
# --------------------------------------------------------------

# TODO: does only work if OPENAI_API_KEY is set in .env or shell
api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY is not set (shell or .env).")

client = OpenAI(api_key=api_key)

# --------------------------------------------------------------
# Introducing instructions
# --------------------------------------------------------------

"""
Inputs can now be a single string or a list of messages.

The list of roles can now be:
- system
- developer
- user
- assistant
"""

response = client.responses.create(
    model="gpt-4o",
    instructions="Talk like a pirate.",
    input="Are semicolons optional in JavaScript?",
)

print(response.output_text)


# --------------------------------------------------------------
# Which would be similar to:
# --------------------------------------------------------------

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "developer", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.output_text)