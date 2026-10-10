from ollama import chat

"""
This script demonstrates how to generate a response with an open source model
running locally through Ollama. No API key is needed.

Setup:
1. Install Ollama: https://ollama.com/download
2. Pull a small model: ollama pull qwen2.5:3b-instruct
"""

model = "qwen2.5:3b-instruct"

# --------------------------------------------------------------
# Send messages to a local model
# --------------------------------------------------------------

"""
The message format is the same as the OpenAI example:
- system
- user
- assistant
"""

response = chat(
    model=model,
    messages=[
        {"role": "system", "content": "Talk like a pirate."},
        {"role": "user", "content": "Are semicolons optional in JavaScript?"},
    ],
)

print(response.message.content)
