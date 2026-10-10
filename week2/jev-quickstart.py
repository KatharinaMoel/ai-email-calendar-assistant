from typesafe_sdk import Choice, Noul, Score, TypeSafeClient
from dotenv import load_dotenv

"""
This script demonstrates how to get typed decisions using Jev, TypeSafe's
System One model.

Unlike the OpenAI Responses API, Jev does not write a chat reply. You send
state plus typed questions, and Jev returns decisions and probabilities.

- State: The content you want the model to evaluate.
- Question: A named judgment defined with a primitive (Choice, Score, or Noul).
- Instructions: What you want the model to decide for that question.
- Criteria: The options or rubric that define the possible answers.

Based on: https://github.com/daveebbelaar/ai-cookbook/tree/main/models/jev
"""

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()

# --------------------------------------------------------------
# Initialize Jev client (reads TYPESAFE_API_KEY from the environment)
# --------------------------------------------------------------

client = TypeSafeClient(model="jev-1.13.0")

ticket = "I was charged twice for order A-104. This is frustrating. Please refund the duplicate."

# --------------------------------------------------------------
# 1. Choice: pick one option from a set you define
# --------------------------------------------------------------

response = client.system_one(
    state=ticket,
    questions={
        "team": Choice(
            instructions="Which team should handle this support ticket?",
            criteria={
                "billing": "Payments, charges, or refunds.",
                "technical": "Errors, bugs, or login failures.",
                "other": "Anything else.",
            },
        ),
    },
)

answer = response.choices["team"]
print("Team:", answer.choice)
print("Probabilities:", answer.probabilities)
print("Confidence:", answer.confidence)

# --------------------------------------------------------------
# 2. Score: place the input on an ordered rubric
# --------------------------------------------------------------

response = client.system_one(
    state=ticket,
    questions={
        "frustration": Score(
            instructions="How frustrated is the customer in this support ticket?",
            criteria=[
                "Calm or neutral.",
                "Frustrated but civil.",
                "Very angry or abusive.",
            ],
        ),
    },
)

answer = response.scores["frustration"]
# Levels are numbered from zero; the score can fall between levels.
print("Frustration score:", answer.score)
print("Legend:", answer.legend)
print("Confidence:", answer.confidence)

# --------------------------------------------------------------
# 3. Noul: probability (0 to 1) that a yes-or-no question is yes
# --------------------------------------------------------------

response = client.system_one(
    state=ticket,
    questions={
        "refund_requested": Noul(
            instructions="Does the customer explicitly ask for money to be returned?",
        ),
    },
)

probability = response.nouls["refund_requested"].noul
# 0.5 means uncertainty, not medium severity.
print("Probability of a refund request:", probability)
