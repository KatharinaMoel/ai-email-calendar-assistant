# AI Personal Assistant

An incremental cohort project for building an AI assistant that helps manage email and calendar work. Nylas provides one integration layer for supported email and calendar providers, while the application keeps receiving events, AI decisions, data access, and user-facing APIs separate.

## Week 1

Week 1 establishes the repository structure and the boundaries of the application. The files are intentionally lightweight placeholders that later weeks will implement.

```text
Email and calendar providers
        ↓
      Nylas
        ↓ webhooks / API
     FastAPI
        ↓
  Assistant workflows
   ↙           ↘
PostgreSQL     OpenAI
```

## Project structure

```text
app/
├── main.py                    # Application entry point
├── config.py                  # Environment-based settings
├── api/routes/
│   ├── health.py              # Health endpoint
│   └── webhooks.py            # Receive Nylas webhook events
├── integrations/nylas/
│   ├── client.py              # Nylas API client
│   └── auth.py                # Hosted authentication flow
├── agents/
│   └── assistant.py           # AI decision-making logic
├── services/
│   ├── email.py               # Email workflow coordination
│   └── calendar.py            # Calendar workflow coordination
├── database/
│   ├── connection.py          # PostgreSQL connection
│   ├── models.py              # Database tables
│   └── repository.py          # Database reads and writes
└── schemas/
    ├── email.py               # Canonical email data
    ├── calendar.py            # Canonical calendar data
    └── webhook.py             # Incoming event data
```

## Getting started

1. Install Python 3.12 or newer and `uv`.
2. Copy `.env.example` to `.env`.
3. Create a Nylas developer account and fill in the Nylas values.
4. Run `uv sync`.
5. Start the placeholder application with `uv run python -m app.main`.

Never commit `.env` or real account credentials.
